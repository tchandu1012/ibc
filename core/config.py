#config.py
import logging.config

from settings import Settings

#class Settings:
 #   PROJECT_NAME:str = "IBC Miro 🔥"
#  PROJECT_VERSION: str = "1.0.0"
# How to configure logging
# add  logging for both console and file log and this should be able to use i   
# n all packages in the project
# How to configure settings for the project        
settings = Settings()
# Configure the logging module using the settings
logging.config.dictConfig(settings.dict())
