import requests

from .urlmanager import FishbowlURLManager

class FishBowlAPI:
    __session_key = None
    __url_manager = None
    def __init__(self, session_key: str):
        self.__session_key = session_key
        self.__url_manager = FishbowlURLManager()

    def get_posts(self, bowl_name:str=None, sort:str=None, start:int=None, count:int=None):
        """_summary_

        Args:
            bowl_name (str): _description_

        1. Get the bowl details using the bowl name
        2. Fetch the bowl id and call posts api to get the posts
        """
        kwargs = {k:v for k,v in locals().items() if v is not None and k not in ['self', 'bowl_name']}
        bowl_details = self.get_bowl_details(bowl_name)
        bowl_id = bowl_details['_id']
        print(bowl_id)
        posts = self.get_posts_by_bowl_id(bowl_id, **kwargs)
        return posts


    def get_bowl_details(self, bowl_name):
        _url = self.__url_manager.get_bowl_details_url(bowl_name)
        _headers = self.__url_manager.get_headers(self.__session_key)
        #_cert = self.__url_manager.get_cert_path()
        data = requests.get(url=_url, headers=_headers, verify=True, timeout=60)
        return dict(data.json())

    def get_posts_by_bowl_id(self, bowl_id, sort:str=None, start:int=None, count:int=None):
        kwargs = {k:v for k,v in locals().items() if v is not None and k not in ['self', 'bowl_id']}
        _url = self.__url_manager.get_posts_url(bowl_id, **kwargs)
        _headers = self.__url_manager.get_headers(self.__session_key)
        #_cert = self.__url_manager.get_cert_path()
        print(_url)
        data = requests.get(url=_url, headers=_headers, verify=True, timeout=60)
        print(len(dict(data.json())))
        return dict(data.json())

    def get_comments(self):
        pass