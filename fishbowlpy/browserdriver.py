from selenium import webdriver
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from .drivertype import DriverType
from .config import CONFIG


class BrowserDriver:
    __driver = None
    __service = None

    def __init__(self, driver_type=DriverType.CHROME_DRIVER) -> None:
        if driver_type == DriverType.CHROME_DRIVER:
            self.__service = webdriver.ChromeService(
                executable_path=CONFIG.CHROME_DRIVER_PATH)
            self.__driver = webdriver.Chrome(service=self.__service)
        elif driver_type == DriverType.EDGE_DRIVER:
            self.__service = webdriver.EdgeService(
                executable_path=CONFIG.EDGE_DRIVER_PATH)
            self.__driver = webdriver.Edge(service=self.__service)

    def get_driver(self) -> ChromiumDriver:
        return self.__driver
