import sys
sys.path.append("../src")

from fishbowlpy import FishBowlClient

client = FishBowlClient()

client.get_posts(bowl_name='tech-india')