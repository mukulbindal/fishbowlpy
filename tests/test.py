import sys
sys.path.append('../src')

from fishbowlpy.fishbowlloginmanager import DriverType
from fishbowlpy.fishbowlloginmanager import FishBowlLoginManager

client = FishBowlLoginManager()
client.login(driver_type=DriverType.EDGE_DRIVER)
print(client)
