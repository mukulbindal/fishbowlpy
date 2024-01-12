from .fishbowlloginmanager import FishBowlLoginManager
from .drivertype import DriverType

class FishBowlClient:
    __login_manager:FishBowlLoginManager = None

    def __init__(self, login_manager:FishBowlLoginManager=None,
                 session_key: str = None,
                 session_expiry: float = None,
                 login_popup: bool = False,
                 driver_type: str = DriverType.CHROME_DRIVER) -> None:
        if login_manager:
            self.__login_manager = login_manager
        else:
            self.__login_manager = FishBowlLoginManager(session_expiry=session_expiry, 
                                                        session_key=session_key, 
                                                        login_popup=login_popup, 
                                                        driver_type=driver_type)
    
    def refresh_session(self):
        pass
    def get_bowls_names(self):
        # Hard coded for now
        # It shoould use the bs4 to parse html and get the proper names
        return ['tech-india', 'job-referrals']
    
    def get_posts(self, bowl_name, )
    
        