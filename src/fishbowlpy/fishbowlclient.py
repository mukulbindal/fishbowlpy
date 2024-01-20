from .fishbowlloginmanager import FishBowlLoginManager
from .fishbowlapi import FishBowlAPI
from .drivertype import DriverType
from .utils.logger import getLogger

LOGGER = getLogger(__name__)


class FishBowlClient:
    """This class is used to interact with the FishBowlApp. This class provides the interface with the ability to
    configure the required configuration like driver paths, session key etc.
    
    :param login_manager(FishBowlLoginManager): An instance of the FishBowlLoginManager class.
    :param fishbowl_api(FishBowlAPI): An instance of the FishBowlAPI class.
    :param driver_type(DriverType): An instance of the DriverType class.
    :param **kwargs: Any other keyword arguments.
    
    :return: None
    
    Basic Usage:
    >>> from fishbowlpy.fishbowlclient import FishBowlClient
    >>> client = FishBowlClient()
    >>> client.get_bowls_names() 
    >>> client.get_posts(bowl_name='fishbowl')
    
    :copyright: (c) 2024 MIT Licensed
    """
    def __init__(self, **kwargs) -> None:
        """This class is used to interact with the FishBowlApp. This class provides the interface with the ability to
        configure the required configuration like driver paths, session key etc.
        
        :param login_manager(FishBowlLoginManager): An instance of the FishBowlLoginManager class.
        :param fishbowl_api(FishBowlAPI): An instance of the FishBowlAPI class.
        :param driver_type(DriverType): An instance of the DriverType class.
        :param **kwargs: Any other keyword arguments.
        
        :return: None
        
        Basic Usage:
        >>> from fishbowlpy.fishbowlclient import FishBowlClient
        >>> client = FishBowlClient()
        >>> client.get_bowls_names() 
        >>> client.get_posts(bowl_name='fishbowl')
        
        :copyright: (c) 2024 MIT Licensed
        """
        
        self.__login_manager = kwargs['login_manager'] or FishBowlLoginManager(**kwargs)

        self.__fishbowl_api = kwargs['fishbowl_api'] or FishBowlAPI(session_key=self.__login_manager.get_session_key())
    
    def refresh_session(self):
        """This is a placeholder method that will be used to refresh the session"""
        pass
    def get_bowls_names(self):
        """This is a placeholder method that will be used to get the names of the subscribed bowls"""
        # Hard coded for now
        # It shoould use the bs4 to parse html and get the proper names
        return ['tech-india', 'job-referrals']
    
    def get_posts(self, bowl_name:str):
        """This method returns the posts in the `bowl_name` in json format.
        
        :param bowl_nameBowl name from where to get the posts.
        
        :return: Posts in json format.
        """
        return self.__fishbowl_api.get_posts(bowl_name=bowl_name)
    
        