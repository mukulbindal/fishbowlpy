import requests
import os

from .utils.logger import getLogger

LOGGER = getLogger(__name__)

def download_file(url, filepath):
    LOGGER.debug(f"Downloading file from {url} to path: {filepath}")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    response = requests.get(url, timeout=60, verify=False)
    
    if response.status_code == 200:
        with open(filepath, "wb") as file:
            file.write(response.content)
        LOGGER.debug(f"File downloaded successfully at {filepath}")
    else:
        LOGGER.error(f"Error downloading file: {response.status_code}")
    
    