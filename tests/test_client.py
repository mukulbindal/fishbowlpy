import sys
sys.path.append("../src")

from fishbowlpy.fishbowlclient import FishBowlClient
from fishbowlpy.drivertype import DriverType

client = FishBowlClient(driver_type=DriverType.EDGE_DRIVER)

posts = client.get_posts('tech-india')

print(posts)