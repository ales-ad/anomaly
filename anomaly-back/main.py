import asyncio
import importlib
import os
from contextlib import suppress
import traceback

from fastapi import FastAPI, Request, Response, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from tortoise.contrib.fastapi import register_tortoise
from starlette.concurrency import iterate_in_threadpool

from core.db import TORTOISE_CONFIG
from core.auth import auth_header_store
from core.exceptions import BaseAppException
from core.response import AppResponse, Error
from core.logger import log
from core.request import AppRequest


BEARER_JWT_KEY = HTTPBearer(scheme_name="JWT", auto_error=False)


async def _build_swagger_jwt(
        _: HTTPAuthorizationCredentials | None = Security(BEARER_JWT_KEY)
):
    # Функция нужна, чтобы сделать JWT-авторизацию в сваггере с текущей auth реализацией
    return


async def log_request(
        request: Request,
        response: Response
):
    _msg = f"Request: [{request.method}] -> {request.url} < {request.headers} << {request.path_params}"
    with suppress(Exception):
        text = await request.json()
        if len(text) > 20000:
            _msg += f" <<< {text[:1000]}... message too long"
        _msg += f" <<< {await request.json()}"

    log.info(_msg)

    try:
        yield
    except BaseAppException as e:
        resp_err = Error(name=str(e), extra_info=e.err_info())

        log.info(
            f"Response: [{request.method}] -> {request.url} >>> "
            f"BaseAppException {e.status_code=} {resp_err}"
        )

        raise
    except RequestValidationError as e:
        print("err1")
        log.info(
            f"({AppRequest.id}) ({request.url}) Validation error {e}. Info: {str(e.errors())}"
        )
        raise
    except Exception as e:
        print("err2")
        log.info( f"({AppRequest.id}) ({request.url}) InternalServerError {e}. Traceback: {"".join(traceback.format_exception(e)[-30:])}")
        raise


app = FastAPI(
    dependencies=[
        Depends(_build_swagger_jwt),
        Depends(log_request)
    ]
)


async def app_middleware(request: Request, call_next):
    AppRequest.gen_id()
    AppRequest.ip.set(getattr(getattr(request, 'client', None), 'host', '127.0.0.1'))
    AppRequest.api_name.set(request.scope.get('path'))

    log.configure_extra()

    auth_header_store.set_authorization_header(request.headers.get("Authorization"))

    try:
        response = await call_next(request)

        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))

        log.debug(
            f"Response: [{request.method}] -> {request.url} >>> "
            f"{response.status_code=} {(b''.join(response_body)).decode()}"
        )

        return response

    except BaseAppException as e:
        resp_err = Error(name=str(e), extra_info=e.err_info())

        return Response(
            status_code=e.status_code,
            content=AppResponse(error=resp_err, error_desc=e.error_desc).model_dump_json(),
            headers={"Content-Type": "application/json"}
        )
    except Exception:
        return Response(
            status_code=500,
            content=AppResponse(error=Error(name="InternalServerError")).model_dump_json(),
            headers={"Content-Type": "application/json"}
        )


app.middleware("http")(app_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=True,
)
# todo: сделать lifespan для редиса

for obj in os.scandir("apps"):
    if obj.is_dir():
        if os.path.isfile(f"apps/{obj.name}/router.py"):
            r = importlib.import_module(f"apps.{obj.name}.router")
            app.include_router(r.router)
