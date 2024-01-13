import sys
sys.path.append('../src')

from fishbowlpy.fishbowlapi import FishBowlAPI

api = FishBowlAPI("c0a616e2-078c-4563-bddc-36f19d032513")
#api.get_bowl_details('tech-india')
api.get_posts('tech-india')