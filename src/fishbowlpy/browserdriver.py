from selenium import webdriver
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from .drivertype import DriverType
from .config import CONFIG


class BrowserDriver:
    __driver = None
    __service = None
    __driver_type = None
    __driver_path = None
    __default_driver_locations = {DriverType.CHROME_DRIVER: ChromeDriverManager().install(), 
                                  DriverType.EDGE_DRIVER: EdgeChromiumDriverManager().install()}

    def __init__(self, driver_type=DriverType.CHROME_DRIVER, driver_path:str=None) -> None:
        if driver_path:
            self.__driver_path = driver_path
        if driver_type:
            self.__driver_type = driver_type
        if not driver_path:
            self.__driver_path = self.__default_driver_locations[self.__driver_type]
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
