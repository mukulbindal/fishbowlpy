import os

from .config import CONFIG
from .filedownloader import download_file
class FishbowlURLManager:
    __headers = None

    def get_cert_path(self):
        print(CONFIG.CA_CERT_FILEPATH)
        if os.path.exists(CONFIG.CA_CERT_FILEPATH):
            return CONFIG.CA_CERT_FILEPATH
        download_file(CONFIG.CA_CERT_LOCATION, CONFIG.CA_CERT_FILEPATH)
        print(CONFIG.CA_CERT_FILEPATH)
        return CONFIG.CA_CERT_FILEPATH
    
    def get_headers(self, session_key):
        if not self.__headers:
            self.__headers = {'Accept': '*/*',
                   'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                   'session-key': session_key
                   }
        return self.__headers
    
    def get_bowl_details_url(self, bowl_name):
        return f"https://api.fishbowlapp.com/v4/feed/{bowl_name}?v=2&addNetworkingImages=true"
    
    def get_posts_url(self, bowl_id, sort:str='byDate', start:int=0, count:int=20):
        return f"https://api.fishbowlapp.com/v4/feed/{bowl_id}/posts?sort={sort}&skipSystemMessages=true&start={start}&count={count}"