import json
import os
import time
from fishbowlpy.browserdriver import BrowserDriver
from fishbowlpy.config import CONFIG
from fishbowlpy.drivertype import DriverType
from .utils.logger import getLogger

LOGGER = getLogger(__name__)

class FishBowlLoginManager:
    __session_key = None
    __session_expiry = None
    __driver = None

    def __init__(
        self,
        session_key: str = None,
        session_expiry: float = None,
        login_popup: bool = False,
        driver_type: str = DriverType.CHROME_DRIVER,
        driver_path: str = None
    ):
        """Initialize a FishBowlLoginManager object with a session key and session expiry.
        If session_key is not provided, tries to retreive the session from previously
        logged in session. If login_popup is True, attempts to login manually.

        Args:
            session_key (str, optional): session key from cookie. Defaults to None.
            session_expiry (float, optional): session expiry in epoch seconds. Defaults to None.
            login_popup (bool, optional): Indicates whether login popup should be opened. Defaults to False.
            driver_type (str, optional): Driver type if login popup is True. Defaults to DriverType.CHROME_DRIVER
        """
        print("Creating the login manager...")
        if session_key:
            self.__session_key = session_key
        if session_expiry:
            self.__session_expiry = session_expiry
        print("Attempting to load session...")
        logged_in = self.load_session()
        if not logged_in and login_popup:
            if driver_type:
                self.login(driver_type, driver_path=driver_path)
            else:
                self.login()

    def login(self, driver_type: str = DriverType.CHROME_DRIVER, driver_path: str = None):
        """Fishbowl client logs in by either reading previous session or by manually
        loggin in.

        Args:
            driver_type (str, optional): Provide the driver type. Defaults to DriverType.CHROME_DRIVER.
        """
        if self.load_session():
            return

        if not self.__driver:
            self.__driver = BrowserDriver(driver_type=driver_type, 
                                          driver_path=driver_path).get_driver()
        self.__driver.get(url=CONFIG.FISHBOWLAPP_LOGIN_URL)

        while True:
            LOGGER.debug("Attempting to fetch cookie...")
            cookie = self.__driver.get_cookie(CONFIG.SESSION_KEY_COOKIE_NAME)

            if cookie:
                LOGGER.debug("Fetching cookie..."+ cookie)
                self.__session_key = cookie.get(CONFIG.SESSION_KEY_COOKIE_VALUE)
                self.__session_expiry = cookie.get(CONFIG.SESSION_KEY_COOKIE_EXPIRY)
                self.save_session_data()
                break
            time.sleep(CONFIG.LOGIN_SLEEP_DURATION)
        LOGGER.debug("Logged in successfully"+ self.__session_key)
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
            CONFIG.SESSION_KEY_COOKIE_VALUE: self.__session_key,
            CONFIG.SESSION_KEY_COOKIE_EXPIRY: self.__session_expiry,
        }
        os.makedirs(os.path.dirname(CONFIG.SESSION_FILE), exist_ok=True)
        with open(CONFIG.SESSION_FILE, "w", encoding="utf-8") as session_file:
            json.dump(data, session_file)

    def load_session(self, file=CONFIG.SESSION_FILE) -> bool:
        print("Loading session from file:" , file)
        session_data = None
        try:
            with open(file, "r", encoding="utf-8") as session_file:
                session_data = json.load(session_file)
        except FileNotFoundError as e:
            LOGGER.error("File not found"+ e)
        if not session_data:
            return False
        if session_data[CONFIG.SESSION_KEY_COOKIE_EXPIRY] < time.time():
            LOGGER.error("Session has Expired")
            return False
        self.__session_key = session_data[CONFIG.SESSION_KEY_COOKIE_VALUE]
        self.__session_expiry = session_data[CONFIG.SESSION_KEY_COOKIE_EXPIRY]

        return True

    def set_session_key(self, session_key=None, session_expiry=None):
        if session_expiry:
            self.__session_expiry = session_expiry
        if session_key:
            self.__session_key = session_key
    
    def get_session_key(self):
        return self.__session_key