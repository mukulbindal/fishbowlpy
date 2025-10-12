from .fishbowlloginmanager import FishBowlLoginManager
from .fishbowlapi import FishBowlAPI
from .drivertype import DriverType
from .utils.logger import getLogger
import threading
import time
from datetime import datetime, timedelta
import json
import os

LOGGER = getLogger(__name__)


class FishBowlClient:
    """This class is used to interact with the FishBowlApp. This class provides the interface with the ability to
    configure the required configuration like driver paths, session key etc.
    
    :param login_manager(FishBowlLoginManager): An instance of the FishBowlLoginManager class.
    :param fishbowl_api(FishBowlAPI): An instance of the FishBowlAPI class.
    :param driver_type(DriverType): An instance of the DriverType class.
    :param auto_refresh(bool): Enable automatic token refresh in background. Default: False.
    :param refresh_interval_hours(int): Hours between automatic token refreshes. Default: 12.
    :param **kwargs: Any other keyword arguments.
    
    :return: None
    
    Basic Usage:
    >>> from fishbowlpy.fishbowlclient import FishBowlClient
    >>> client = FishBowlClient()
    >>> client.get_bowls_names() 
    >>> client.get_posts(bowl_name='fishbowl')
    
    With auto-refresh enabled:
    >>> client = FishBowlClient(auto_refresh=True, refresh_interval_hours=12)
    
    :copyright: (c) 2024 MIT Licensed
    """
    def __init__(self, auto_refresh=False, refresh_interval_hours=12, **kwargs) -> None:
        """This class is used to interact with the FishBowlApp. This class provides the interface with the ability to
        configure the required configuration like driver paths, session key etc.
        
        :param login_manager(FishBowlLoginManager): An instance of the FishBowlLoginManager class.
        :param fishbowl_api(FishBowlAPI): An instance of the FishBowlAPI class.
        :param driver_type(DriverType): An instance of the DriverType class.
        :param driver_path(str): A path to the webdriver executable
        :param auto_refresh(bool): Enable automatic token refresh in background. Default: False.
        :param refresh_interval_hours(int): Hours between automatic token refreshes. Default: 12.
        :param **kwargs: Any other keyword arguments.
        
        :return: None
        
        Basic Usage:
        >>> from fishbowlpy.fishbowlclient import FishBowlClient
        >>> client = FishBowlClient()
        >>> client.get_bowls_names() 
        >>> client.get_posts(bowl_name='fishbowl')
        
        :copyright: (c) 2024 MIT Licensed
        """
        
        self.__login_manager = kwargs['login_manager'] if 'login_manager' in kwargs else FishBowlLoginManager(**kwargs)
        self.__fishbowl_api = kwargs['fishbowl_api'] if 'fishbowl_api' in kwargs else FishBowlAPI(session_key=self.__login_manager.get_session_key())
        
        # Initialize token refresh attributes
        self.__session_key = self.__login_manager.get_session_key()
        self.__session_expiry = None
        self.__refresh_running = False
        self.__refresh_thread = None
        
        # Try to load existing session
        self.load_session()
        
        # Start auto-refresh if enabled
        if auto_refresh:
            self.start_token_refresh_scheduler(refresh_interval_hours)
            LOGGER.info(f"Auto-refresh enabled with interval: {refresh_interval_hours} hours")
    
    def refresh_session(self):
        """Refresh the session to keep it alive. This method refreshes the authentication
        and updates the session key.
        
        :return: True if refresh was successful, False otherwise
        :rtype: bool
        
        Basic Usage:
        >>> client = FishBowlClient()
        >>> success = client.refresh_session()
        >>> if success:
        ...     print("Session refreshed successfully")
        """
        try:
            LOGGER.info("Attempting to refresh session...")
            
            # Re-authenticate using the login manager to get a fresh session
            if self.__login_manager:
                # Call the login manager's refresh method if available
                # Otherwise, we trigger a re-login
                self.__login_manager.refresh_session()
                
                # Get the new session key
                new_session_key = self.__login_manager.get_session_key()
                
                if new_session_key:
                    self.__session_key = new_session_key
                    self.__session_expiry = datetime.now() + timedelta(hours=24)
                    
                    # Update the API instance with new session key
                    self.__fishbowl_api = FishBowlAPI(session_key=self.__session_key)
                    
                    # Save the refreshed session
                    self.save_session()
                    
                    LOGGER.info(f"Session refreshed successfully at {datetime.now()}")
                    return True
                else:
                    LOGGER.error("Failed to obtain new session key during refresh")
                    return False
            else:
                LOGGER.error("Login manager not available for session refresh")
                return False
                
        except Exception as e:
            LOGGER.error(f"Error refreshing session: {str(e)}")
            return False
    
    def save_session(self):
        """Save the current session to a file for persistence.
        This allows the session to be restored without re-authentication.
        
        :return: True if save was successful, False otherwise
        :rtype: bool
        
        Basic Usage:
        >>> client = FishBowlClient()
        >>> client.save_session()
        """
        try:
            session_data = {
                'session_key': self.__session_key,
                'session_expiry': self.__session_expiry.isoformat() if self.__session_expiry else None,
                'last_refresh': datetime.now().isoformat()
            }
            
            # Create .fishbowlpy directory in user's home if it doesn't exist
            config_dir = os.path.expanduser('~/.fishbowlpy')
            os.makedirs(config_dir, exist_ok=True)
            
            session_file = os.path.join(config_dir, 'session.json')
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            LOGGER.info(f"Session saved successfully to {session_file}")
            return True
            
        except Exception as e:
            LOGGER.error(f"Error saving session: {str(e)}")
            return False
    
    def load_session(self):
        """Load a previously saved session from file.
        
        :return: True if session was loaded successfully, False otherwise
        :rtype: bool
        
        Basic Usage:
        >>> client = FishBowlClient()
        >>> if client.load_session():
        ...     print("Session loaded successfully")
        ... else:
        ...     print("No saved session or session expired")
        """
        try:
            config_dir = os.path.expanduser('~/.fishbowlpy')
            session_file = os.path.join(config_dir, 'session.json')
            
            if not os.path.exists(session_file):
                LOGGER.debug("No saved session found")
                return False
            
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            self.__session_key = session_data.get('session_key')
            
            # Parse session expiry
            if session_data.get('session_expiry'):
                self.__session_expiry = datetime.fromisoformat(session_data['session_expiry'])
            
            # Check if session is expired or about to expire (within 5 minutes)
            if self.__session_expiry and datetime.now() >= self.__session_expiry - timedelta(minutes=5):
                LOGGER.info("Session expired or expiring soon, refreshing session...")
                return self.refresh_session()
            
            # Update the API instance with loaded session key
            if self.__session_key:
                self.__fishbowl_api = FishBowlAPI(session_key=self.__session_key)
                LOGGER.info("Session loaded successfully")
                return True
            
            return False
            
        except Exception as e:
            LOGGER.error(f"Error loading session: {str(e)}")
            return False
    
    def start_token_refresh_scheduler(self, interval_hours=12):
        """Start a background thread that periodically refreshes the session.
        This keeps the session alive for non-interactive use cases.
        
        :param interval_hours: How often to refresh the session (in hours). Default: 12
        :type interval_hours: int
        
        Basic Usage:
        >>> client = FishBowlClient()
        >>> client.start_token_refresh_scheduler(interval_hours=6)
        """
        def refresh_task():
            while self.__refresh_running:
                # Sleep for the specified interval
                time.sleep(interval_hours * 3600)
                
                if self.__refresh_running:
                    LOGGER.info(f"[{datetime.now()}] Running scheduled session refresh...")
                    success = self.refresh_session()
                    
                    if not success:
                        LOGGER.warning("Scheduled session refresh failed")
        
        # Set refresh flag and start thread
        if not self.__refresh_running:
            self.__refresh_running = True
            
            # Start the refresh thread as daemon so it doesn't block program exit
            self.__refresh_thread = threading.Thread(target=refresh_task, daemon=True)
            self.__refresh_thread.start()
            
            LOGGER.info(f"Session refresh scheduler started (interval: {interval_hours} hours)")
    
    def stop_token_refresh_scheduler(self):
        """Stop the background session refresh scheduler.
        
        Basic Usage:
        >>> client = FishBowlClient(auto_refresh=True)
        >>> # ... do some work ...
        >>> client.stop_token_refresh_scheduler()
        """
        if self.__refresh_running:
            self.__refresh_running = False
            LOGGER.info("Session refresh scheduler stopped")
    
    def get_bowls_names(self):
        """This is a placeholder method that will be used to get the names of the subscribed bowls
        
        :return: List of bowl names
        :rtype: list
        """
        # Hard coded for now
        # It should use the bs4 to parse html and get the proper names
        return ['tech-india', 'job-referrals']
    
    def get_posts(self, bowl_name: str):
        """This method returns the posts in the `bowl_name` in json format.
        
        :param bowl_name: Bowl name from where to get the posts.
        
        :return: Posts in json format.
        :rtype: dict
        
        Basic Usage:
        >>> client = FishBowlClient()
        >>> posts = client.get_posts(bowl_name='tech-india')
        """
        return self.__fishbowl_api.get_posts(bowl_name=bowl_name)
    
    def __del__(self):
        """Cleanup method to ensure background threads are stopped properly"""
        self.stop_token_refresh_scheduler()
