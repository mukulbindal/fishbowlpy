from selenium import webdriver
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from .drivertype import DriverType

from .utils.logger import getLogger

LOGGER = getLogger(__name__)


class BrowserDriver:
    __driver = None
    __service = None
    __driver_type = None
    __driver_path = None
    
    def __init__(self, driver_type=DriverType.CHROME_DRIVER, driver_path:str=None) -> None:
        if driver_path:
            self.__driver_path = driver_path
        if driver_type:
            self.__driver_type = driver_type
        if not driver_path:
            self.__driver_path = self.get_default_driver(self.__driver_type)
        if driver_type == DriverType.CHROME_DRIVER:
            self.__service = webdriver.ChromeService(
                executable_path=self.__driver_path)
            self.__driver = webdriver.Chrome(service=self.__service)
        elif driver_type == DriverType.EDGE_DRIVER:
            self.__service = webdriver.EdgeService(
                executable_path=self.__driver_path)
            self.__driver = webdriver.Edge(service=self.__service)

    def get_driver(self) -> ChromiumDriver:
        return self.__driver

    def get_default_driver(self, driver_type) -> ChromiumDriver:
        try:
            if driver_type == DriverType.CHROME_DRIVER:
                return ChromeDriverManager().install()
            elif driver_type == DriverType.EDGE_DRIVER:
                return EdgeChromiumDriverManager().install()
        except Exception as e:
            LOGGER.error(f"Error getting default driver {e}")