import os
class FishbowlURLManager:
    __headers = None

    def get_cert_path(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'certs', 'Zscaler Root CA.crt')
        print(filename)
        with open(filename, "r") as file:
            print(file)
        return filename
    
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