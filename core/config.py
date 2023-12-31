import logging.config
import yaml
import os
from dotenv import load_dotenv

class Settings:
    PROJECT_NAME: str = "IBC Miro 🔥"
    PROJECT_VERSION: str = "1.0.0"


def configure_logging(env):
    print("Loading logging configuration from 'logging.yaml'")
    try:
        with open('logging.yaml', 'r') as f:
            logging_config = yaml.safe_load(f)
    except Exception as e:
        print(f"Failed to load logging configuration: {e}")
        return

    # Retrieve the loggers configuration
    loggers_config = logging_config.get('loggers', {})
    # Retrieve the loggers configuration
    loggers_handlers = logging_config.get('handlers', {})

#    print(f"loggers_config: {loggers_config}")
#    print(f"loggers_handlers: {loggers_handlers}")

    # Check if the specified environment exists in the loggers configuration
    if env in loggers_config:
#        print(f"Found configuration for '{env}' environment. loggers_config[env] = {loggers_config[env]}")
        # Get the handlers for the specified environment
        handlers_for_env = loggers_config[env].get('handlers', [])
        formatters_for_env = loggers_config[env].get('formatter', 'simple')
        loggers_formatters = logging_config.get('formatters', {})

        # Create a new config_for_env dict with the existing environment config
        config_for_env = {
            'version': logging_config.get('version', 1),
            'disable_existing_loggers': logging_config.get('disable_existing_loggers', False),
            'handlers': loggers_handlers,
            'formatters': loggers_formatters,
            'loggers': {
                env: {
                    **loggers_config[env],
                    'handlers': handlers_for_env,
                    'formatter': formatters_for_env
                }
            }
        }
#       print(f"config_for_env : {config_for_env}")
        logging.config.dictConfig(config_for_env)
    else:
        print(f"Environment '{env}' not found in the logging configuration.")

load_dotenv()
configure_logging(os.getenv("Environment"))
logger = logging.getLogger(os.getenv("Environment"))
settings = Settings()
