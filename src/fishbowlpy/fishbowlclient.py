from .fishbowlloginmanager import FishBowlLoginManager
from .fishbowlapi import FishBowlAPI
from .drivertype import DriverType
from .utils.logger import getLogger

LOGGER = getLogger(__name__)


class FishBowlClient:

    def __init__(self, login_manager:FishBowlLoginManager=None,
                 session_key: str = None,
                 session_expiry: float = None,
                 login_popup: bool = True,
                 driver_type: str = DriverType.CHROME_DRIVER,
                 fishbowl_api: FishBowlAPI = None
                 ) -> None:
        
        self.__login_manager = login_manager or FishBowlLoginManager(session_expiry=session_expiry, 
                                                        session_key=session_key, 
                                                        login_popup=login_popup, 
                                                        driver_type=driver_type)

        self.__fishbowl_api = fishbowl_api or FishBowlAPI(session_key=self.__login_manager.get_session_key())
    
    def refresh_session(self):
        pass
    def get_bowls_names(self):
        # Hard coded for now
        # It shoould use the bs4 to parse html and get the proper names
        return ['tech-india', 'job-referrals']
    
    def get_posts(self, bowl_name):
        return self.__fishbowl_api.get_posts(bowl_name=bowl_name)
    
        