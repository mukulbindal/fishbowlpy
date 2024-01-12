from .drivertype import DriverType
from .browserdriver import BrowserDriver
from .config import CONFIG
import time
import json
import os


class FishBowlClient:
    __session_key = None
    __session_expiry = None
    __driver = None

    def __init__(self, session_key=None, session_expiry=None):
        if session_key:
            self.__session_key = session_key
        if session_expiry:
            self.__session_expiry = session_expiry

        self.load_session()

    def login(self, driver_type=DriverType.CHROME_DRIVER):
        if self.load_session():
            return

        if not self.__driver:
            self.__driver = BrowserDriver(driver_type=driver_type).get_driver()
        self.__driver.get(url=CONFIG.FISHBOWLAPP_LOGIN_URL)

        while True:
            print("Attempting to fetch cookie...")
            cookie = self.__driver.get_cookie(CONFIG.SESSION_KEY_COOKIE_NAME)

            if cookie:
                print("Fetching cookie...", cookie)
                self.__session_key = cookie.get(
                    CONFIG.SESSION_KEY_COOKIE_VALUE)
                self.__session_expiry = cookie.get(
                    CONFIG.SESSION_KEY_COOKIE_EXPIRY)
                self.save_session_data()
                break
            time.sleep(CONFIG.LOGIN_SLEEP_DURATION)
        print("Logged in successfully", self.__session_key)
        self.__driver.quit()

    def __str__(self) -> str:
        return f"""FishBowlClient(session_key: {self.__session_key}, session_expiry: {self.__session_expiry})"""

    def save_session_data(self):
        data = {CONFIG.SESSION_KEY_COOKIE_VALUE: self.__session_key,
                CONFIG.SESSION_KEY_COOKIE_EXPIRY: self.__session_expiry}
        os.makedirs(os.path.dirname(CONFIG.SESSION_FILE), exist_ok=True)
        with open(CONFIG.SESSION_FILE, 'w', encoding='utf-8') as session_file:
            json.dump(data, session_file)

    def load_session(self, file=CONFIG.SESSION_FILE) -> bool:
        session_data = None
        try:
            with open(file, "r", encoding='utf-8') as session_file:
                session_data = json.load(session_file)
        except FileNotFoundError as e:
            print('File not found', e)

        if not session_data:
            return False

        if session_data[CONFIG.SESSION_KEY_COOKIE_EXPIRY] < time.time():
            print("Session has Expired")
            return False

        self.__session_key = session_data[CONFIG.SESSION_KEY_COOKIE_VALUE]
        self.__session_expiry = session_data[CONFIG.SESSION_KEY_COOKIE_EXPIRY]

        return True
