from fishbowlpy.fishbowlclient import DriverType
from fishbowlpy.fishbowlclient import FishBowlClient

client = FishBowlClient()
client.login(driver_type=DriverType.EDGE_DRIVER)
print(client)
