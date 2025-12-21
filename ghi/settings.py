import logging
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Log(BaseSettings):
    log_level: int = logging.INFO
    log_format: str = r"%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s"


class Settings(BaseModel):
    log: Log = Log()


settings = Settings()
