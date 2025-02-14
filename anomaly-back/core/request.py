import uuid
from contextvars import ContextVar


class AppRequest:
    _id: ContextVar[str] = ContextVar("request_id", default="--INTERNAL--")
    ip: ContextVar[str] = ContextVar("request_ip", default="--INTERNAL--")
    api_name: ContextVar[str] = ContextVar("api_name", default="--INTERNAL--")

    @classmethod
    def gen_id(cls) -> None:
        cls._id.set(str(uuid.uuid4()))

    @classmethod
    @property
    def id(cls) -> str:
        return cls._id.get()
