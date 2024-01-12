import os


class CONFIG:
    CHROME_DRIVER_PATH = "D:\\My Open Source Contributions\\FishbowlApp\\drivers\\chromedriver.exe"
    EDGE_DRIVER_PATH = "D:\\My Open Source Contributions\\FishbowlApp\\drivers\\msedgedriver.exe"

    FISHBOWLAPP_URL = "https://fishbowlapp.com"
    FISHBOWLAPP_LOGIN_URL = "https://fishbowlapp.com/login"

    LOGIN_SLEEP_DURATION = 5

    SESSION_KEY_COOKIE_NAME = 'session_key'
    SESSION_KEY_COOKIE_VALUE = 'value'
    SESSION_KEY_COOKIE_EXPIRY = 'expiry'

    SESSION_FILE = os.path.join("session", "session_data.json")
