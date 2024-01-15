import logging 
import os
import sys
from ..config import CONFIG

def getLogger(name):
    os.makedirs(CONFIG.LOGS_PATH, exist_ok=True)
    logging.basicConfig(level=logging.DEBUG, 
                        handlers=[logging.FileHandler(CONFIG.LOGS_FILE),
                                  logging.StreamHandler(sys.stdout)],
                        format=CONFIG.LOGS_FORMAT)
    logger = logging.getLogger(name)
    return logger
    