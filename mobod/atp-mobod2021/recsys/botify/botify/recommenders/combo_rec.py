import random
from typing import List
from .random import Random
from .recommender import Recommender


class ComboRec(Recommender):
    def __init__(self,  tracks_redis, recommendations_redis, catalog):
        self.recommendations_redis = recommendations_redis
        self.fallback = Random(tracks_redis)
        self.catalog = catalog
        
    def recommend_next(self, user: int, prev_track: int, prev_track_time: float, last_tracks: dict) -> int:
        recommendations = self.recommendations_redis.get(user)
        top = list(self.catalog.top_tracks[:100])
        shuffled_top = random.shuffle(top)[0]
        

        if recommendations is not None:
            shuffled = list(self.catalog.from_bytes(recommendations))
            random.shuffle(shuffled)
            if recommendations not in last_tracks.get(user):
                last_tracks[user].appned(shuffled[0])
                return shuffled[0]
        elif shuffled_top not in last_tracks.get(user):
            last_tracks[user].appned(shuffled_top)
            return shuffled_top
            # return self.fallback.recommend_next(user, prev_track, prev_track_time)