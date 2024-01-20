import requests
from .utils.logger import getLogger
from .urlmanager import FishbowlURLManager

LOGGER = getLogger(__name__)

class FishBowlAPI:
    
    def __init__(self, session_key: str):
        LOGGER.debug("Creating fishbowlapi object")
        self.__session_key = session_key or None 
        self.__url_manager = FishbowlURLManager()

    def get_posts(self, bowl_name:str, sort:str=None, start:int=None, count:int=None):
        kwargs = {k:v for k,v in locals().items() if v is not None and k not in ['self', 'bowl_name']}
        bowl_details = self.get_bowl_details(bowl_name)
        bowl_id = bowl_details['_id']
        LOGGER.debug(bowl_id)
        posts = self.get_posts_by_bowl_id(bowl_id, **kwargs)
        return posts


    def get_bowl_details(self, bowl_name):
        url = self.__url_manager.get_bowl_details_url(bowl_name)
        headers = self.__url_manager.get_headers(self.__session_key)
        data = requests.get(url = url, headers = headers, verify = True, timeout = 60)
        return dict(data.json())

    def get_posts_by_bowl_id(self, bowl_id, sort:str=None, start:int=None, count:int=None):
        kwargs = {k:v for k,v in locals().items() if v is not None and k not in ['self', 'bowl_id']}
        url = self.__url_manager.get_posts_url(bowl_id, **kwargs)
        headers = self.__url_manager.get_headers(self.__session_key)
        LOGGER.debug(url)
        data = requests.get(url = url, headers = headers, verify = True, timeout = 60)
        LOGGER.debug(len(dict(data.json())))
        return dict(data.json())

    def get_comments(self):
        pass