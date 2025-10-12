import json
import os
import time
from .browserdriver import BrowserDriver
from . import config
from .drivertype import DriverType
from .utils.logger import getLogger

LOGGER = getLogger(__name__)

class FishBowlLoginManager:

    def __init__(
        self,
        session_key: str = None,
        session_expiry: float = None,
        login_popup: bool = True,
        driver_type: str = DriverType.CHROME_DRIVER,
        driver_path: str = None
    ):
        """Initialize a FishBowlLoginManager object with a session key and session expiry.
        If session_key is not provided, tries to retreive the session from previously
        logged in session. If login_popup is True, attempts to login manually.

        Args:
            session_key (str, optional): session key from cookie. Defaults to None.
            session_expiry (float, optional): session expiry in epoch seconds. Defaults to None.
            login_popup (bool, optional): Indicates whether login popup should be opened. Defaults to True.
            driver_type (str, optional): Driver type if login popup is True. Defaults to DriverType.CHROME_DRIVER
            driver_path (str, optional): Path to the driver executable. Defaults to None.
        """
        LOGGER.debug("Creating the login manager...")
        self.__session_key = session_key or None
        self.__session_expiry = session_expiry or None
        self.__driver = None
        self.__driver_type = driver_type
        self.__driver_path = driver_path
        LOGGER.debug("Attempting to load session...")
        logged_in = self.load_session()
        if not logged_in and login_popup:
            if driver_type:
                self.login(driver_type, driver_path=driver_path)
            else:
                self.login()

    def login(self, driver_type: str = DriverType.CHROME_DRIVER, driver_path: str = None):
        """Fishbowl client logs in by either reading previous session or by manually
        logging in.

        Args:
            driver_type (str, optional): Provide the driver type. Defaults to DriverType.CHROME_DRIVER.
            driver_path (str, optional): Path to the driver executable. Defaults to None.
        """
        if self.load_session():
            return

        if not self.__driver:
            self.__driver = BrowserDriver(driver_type=driver_type, 
                                          driver_path=driver_path).get_driver()
        self.__driver.get(url=config.FISHBOWLAPP_LOGIN_URL)

        while True:
            LOGGER.debug("Attempting to fetch cookie...")
            cookie = self.__driver.get_cookie(config.SESSION_KEY_COOKIE_NAME)

            if cookie and cookie.get(config.SESSION_KEY_COOKIE_DOMAIN) == config.SESSION_KEY_COOKIE_DOMAIN_FISHBOWL:
                LOGGER.debug(f"Fetching cookie...{cookie}")
                self.__session_key = cookie.get(config.SESSION_KEY_COOKIE_VALUE)
                self.__session_expiry = cookie.get(config.SESSION_KEY_COOKIE_EXPIRY)
                self.save_session_data()
                break
            time.sleep(config.LOGIN_SLEEP_DURATION)
        LOGGER.debug(f"Logged in successfully - {self.__session_key}")
        self.__driver.quit()

    def refresh_session(self):
        """Refresh the current session by re-authenticating and getting a new session key.
        This method opens a browser to re-login and obtain fresh session credentials.
        
        Returns:
            bool: True if refresh was successful, False otherwise
        """
        try:
            LOGGER.info("Refreshing session...")
            
            # Check if we have driver configuration saved
            driver_type = self.__driver_type if self.__driver_type else DriverType.CHROME_DRIVER
            driver_path = self.__driver_path if self.__driver_path else None
            
            # Initialize browser driver if not already initialized
            if not self.__driver:
                self.__driver = BrowserDriver(driver_type=driver_type, 
                                              driver_path=driver_path).get_driver()
            
            # Navigate to login page
            self.__driver.get(url=config.FISHBOWLAPP_LOGIN_URL)
            
            # Wait for user to login and get fresh cookie
            refresh_timeout = 300  # 5 minutes timeout for manual login
            start_time = time.time()
            
            while True:
                # Check timeout
                if time.time() - start_time > refresh_timeout:
                    LOGGER.error("Session refresh timeout - manual login not completed")
                    self.__driver.quit()
                    self.__driver = None
                    return False
                
                LOGGER.debug("Attempting to fetch cookie during refresh...")
                cookie = self.__driver.get_cookie(config.SESSION_KEY_COOKIE_NAME)

                if cookie and cookie.get(config.SESSION_KEY_COOKIE_DOMAIN) == config.SESSION_KEY_COOKIE_DOMAIN_FISHBOWL:
                    LOGGER.debug(f"Fetching refreshed cookie...{cookie}")
                    self.__session_key = cookie.get(config.SESSION_KEY_COOKIE_VALUE)
                    self.__session_expiry = cookie.get(config.SESSION_KEY_COOKIE_EXPIRY)
                    
                    # Save the refreshed session
                    self.save_session_data()
                    
                    LOGGER.info(f"Session refreshed successfully - {self.__session_key}")
                    self.__driver.quit()
                    self.__driver = None
                    return True
                    
                time.sleep(config.LOGIN_SLEEP_DURATION)
                
        except Exception as e:
            LOGGER.error(f"Error refreshing session: {str(e)}")
            if self.__driver:
                try:
                    self.__driver.quit()
                    self.__driver = None
                except:
                    pass
            return False

    def __str__(self) -> str:
        """Representation of the FishBowlLoginManager instance.

        Returns:
            str: String representation of the FishBowlLoginManager
        """      
        return f"""FishBowlLoginManager(session_key: {self.__session_key}, session_expiry: {self.__session_expiry})"""

    def save_session_data(self):
        """Saves the session data into a json file for future login attempts"""
        data = {
            config.SESSION_KEY_COOKIE_VALUE: self.__session_key,
            config.SESSION_KEY_COOKIE_EXPIRY: self.__session_expiry,
        }
        os.makedirs(os.path.dirname(config.SESSION_FILE), exist_ok=True)
        with open(config.SESSION_FILE, "w", encoding="utf-8") as session_file:
            json.dump(data, session_file)
        LOGGER.debug("Session data saved successfully")

    def load_session(self, file=config.SESSION_FILE) -> bool:
        """Load session from file. If session is expired, attempt to refresh it.
        
        Args:
            file (str): Path to session file. Defaults to config.SESSION_FILE
            
        Returns:
            bool: True if session loaded successfully, False otherwise
        """
        LOGGER.debug(f"Loading session from file: {file}")
        session_data = None
        try:
            with open(file, "r", encoding="utf-8") as session_file:
                session_data = json.load(session_file)
        except FileNotFoundError as e:
            LOGGER.error(f"File not found {e}")
        
        if not session_data:
            return False
        
        # Check if session has expired
        if session_data[config.SESSION_KEY_COOKIE_EXPIRY] < time.time():
            LOGGER.warning("Session has expired")
            # Optionally attempt automatic refresh here
            # return self.refresh_session()
            return False
            
        self.__session_key = session_data[config.SESSION_KEY_COOKIE_VALUE]
        self.__session_expiry = session_data[config.SESSION_KEY_COOKIE_EXPIRY]
        LOGGER.debug("Session loaded successfully")
        return True

    def set_session_key(self, session_key=None, session_expiry=None):
        """Sets the session key and session expiry

        Args:
            session_key (str, optional): The session key from cookie. Defaults to None.
            session_expiry (int, optional): The epoch time when session expires. Defaults to None.
        """        
        if session_expiry:
            self.__session_expiry = session_expiry
        if session_key:
            self.__session_key = session_key
    
    def get_session_key(self) -> str:
        """Returns the session key

        Returns:
            str: Session key for current session
        """        
        return self.__session_key
    
    def get_session_expiry(self) -> float:
        """Returns the session expiry timestamp

        Returns:
            float: Session expiry in epoch seconds
        """
        return self.__session_expiry
    
    def is_session_valid(self) -> bool:
        """Check if current session is still valid (not expired)
        
        Returns:
            bool: True if session is valid, False otherwise
        """
        if not self.__session_key or not self.__session_expiry:
            return False
        return self.__session_expiry > time.time()