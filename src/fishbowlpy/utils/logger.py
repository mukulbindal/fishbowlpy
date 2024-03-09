import logging 
import os
import sys
from .. import config

def getLogger(name):
    os.makedirs(config.LOGS_PATH, exist_ok=True)
    logging.basicConfig(level=logging.DEBUG, 
                        handlers=[logging.FileHandler(config.LOGS_FILE),
                                  logging.StreamHandler(sys.stdout)],
                        format=config.LOGS_FORMAT)
    logger = logging.getLogger(name)
    return logger
    