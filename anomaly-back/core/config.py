import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import tomllib


class AuthConfig(BaseModel):
    max_sessions: int
    max_login_failed_attempts: int
    max_login_sessions: int
    time_between_attempts_seconds: int
    ban_time_after_failed_minutes: int
    access_token_life_time_seconds: int
    refresh_token_life_time_days: int
    jwt_secret: str
    system_api_secret: str




class DBConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db_name: str
    sslmode: str

class LoggerConfig(BaseModel):
    file_level: Optional[str]
    stdout_level: Optional[str]
    tortoise_level: str


class TGConfig(BaseModel):
    token: str
    chat_id: int



class Config(BaseModel):
    Auth: AuthConfig
    DB: DBConfig
    TG: TGConfig
    Logger: LoggerConfig


def _merge_configs(a: dict, b: dict, path=[]):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge_configs(a[key], b[key], path + [str(key)])
        else:
            a[key] = b[key]
    return a


def load_config() -> Config:
    load_dotenv(".env")
    env_config = {
        "DB": {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "db_name": os.getenv("DB_NAME"),
            "sslmode": os.getenv("DB_SSLMODE")
        },
        "Auth": {
            "jwt_secret": os.getenv("JWT_SECRET"),
            "system_api_secret": os.getenv("SYSTEM_API_SECRET"),
        },
        "TG": {
            "token": os.getenv("TG_TOKEN"),
            "chat_id": os.getenv("TG_CHAT_ID"),
        },
       
    }

    with open("config.toml", "rb") as f:
        toml_config = tomllib.load(f)

    config_dict = _merge_configs(env_config, toml_config)

    return Config(**config_dict)