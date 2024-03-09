from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.core.os_manager import ChromeType

from .drivertype import DriverType
from .utils.logger import getLogger


LOGGER = getLogger(__name__)


class BrowserDriver:

    def __init__(self, driver_type=DriverType.CHROME_DRIVER, driver_path: str = None) -> None:
        self.__driver = None
        self.__service = None
        self.__driver_type = driver_type or DriverType.CHROME_DRIVER
        self.__driver_path = driver_path or self.get_default_driver(self.__driver_type)

        if driver_type == DriverType.CHROME_DRIVER:
            self.__service = webdriver.ChromeService(
                    executable_path=self.__driver_path)
            self.__driver = webdriver.Chrome(service=self.__service)

        elif driver_type == DriverType.EDGE_DRIVER:
            self.__service = webdriver.EdgeService(
                    executable_path=self.__driver_path)
            self.__driver = webdriver.Edge(service=self.__service)

        elif driver_type == DriverType.FIREFOX_DRIVER:
            self.__service = webdriver.FirefoxService(
                    executable_path=self.__driver_path)
            self.__driver = webdriver.Firefox(service=self.__service)

        elif driver_type == DriverType.IE_DRIVER:
            self.__service = webdriver.IeService(
                    executable_path=self.__driver_path)
            self.__driver = webdriver.Ie(service=self.__service)

        elif driver_type == DriverType.OPERA_DRIVER:
            self.__service = service.Service(
                    executable_path=self.__driver_path)
            self.__driver = webdriver.Opera()


    def get_driver(self) -> ChromiumDriver:
        return self.__driver

    def get_default_driver(self, driver_type: int) -> ChromiumDriver:
        try:
            match driver_type:
                case DriverType.CHROME_DRIVER:
                    return ChromeDriverManager().install()

                case DriverType.EDGE_DRIVER:
                    return EdgeChromiumDriverManager().install()

                case DriverType.FIREFOX_DRIVER:
                    return GeckoDriverManager().install()

                case DriverType.IE_DRIVER:
                    return IEDriverManager().install()

                case DriverType.OPERA_DRIVER:
                    return OperaDriverManager().install()


        except Exception as e:
            LOGGER.error(f"Error getting default driver {e}")


if __name__ == '__main__':
    b = BrowserDriver(driver_type=DriverType.OPERA_DRIVER)