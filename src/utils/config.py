"""Module with config for whole project."""
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Pydantic BaseSettings class to use as config with declared Environment Variables.

    Attributes:
        LOG_LEVEL: Logging level for logger (DEBUG, INFO, WARNING, ERROR), default is DEBUG.
    """

    LOG_LEVEL: str = "DEBUG"


config = Config()
