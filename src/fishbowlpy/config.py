import os

FISHBOWLAPP_URL = "https://fishbowlapp.com"
FISHBOWLAPP_LOGIN_URL = "https://fishbowlapp.com/login"

LOGIN_SLEEP_DURATION = 5

SESSION_KEY_COOKIE_NAME = 'session_key'
SESSION_KEY_COOKIE_VALUE = 'value'
SESSION_KEY_COOKIE_EXPIRY = 'expiry'
SESSION_KEY_COOKIE_DOMAIN = 'domain'
SESSION_KEY_COOKIE_DOMAIN_FISHBOWL = '.fishbowlapp.com'

SESSION_FILE = os.path.join(os.path.dirname(__file__), "tmp", "session", "session_data.json")

GET_BOWLS_URL = FISHBOWLAPP_URL + "/bowls"
GET_POSTS_URL = "https://api.fishbowlapp.com/v4/feed/60f19b15fc523b002f774065/posts?sort=byDate&skipSystemMessages=true&start=0&count=20"

CA_CERT_LOCATION = "https://raw.githubusercontent.com/mukulbindal/fishbowlpy/main/resources/certs/Zscaler%20Root%20CA.crt"
CA_CERT_FILEPATH = os.path.join(os.path.dirname(__file__), 'tmp', 'certs','Zscaler Root CA.crt')

LOGS_PATH = os.path.join(os.path.dirname(__file__),'tmp','logs')
LOGS_FILE = os.path.join(LOGS_PATH, 'fishbowlpy.log')
LOGS_FORMAT = "[%(asctime)s] [%(levelname)s] [%(process)d] [%(module)s.%(funcName)s] [%(lineno)d]: %(message)s"
