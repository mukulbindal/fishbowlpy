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
        """
        LOGGER.debug("Creating the login manager...")
        self.__session_key = session_key or None
        self.__session_expiry = session_expiry or None
        self.__driver = None
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

    def load_session(self, file=config.SESSION_FILE) -> bool:
        LOGGER.debug(f"Loading session from file: {file}")
        session_data = None
        try:
            with open(file, "r", encoding="utf-8") as session_file:
                session_data = json.load(session_file)
        except FileNotFoundError as e:
            LOGGER.error(f"File not found {e}")
        if not session_data:
            return False
        
        if session_data[config.SESSION_KEY_COOKIE_EXPIRY] < time.time():
            LOGGER.error("Session has Expired")
            return False
        self.__session_key = session_data[config.SESSION_KEY_COOKIE_VALUE]
        self.__session_expiry = session_data[config.SESSION_KEY_COOKIE_EXPIRY]

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
        