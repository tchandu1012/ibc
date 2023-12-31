# settings.py
from pydantic import BaseSettings
import yaml

class Settings(BaseSettings):
    # Define your settings here
    loggers: dict
    handlers: dict
    formatters: dict

    class Config:
        # Set the name of your logging.yaml file here
        env_file = "logging.yaml"
