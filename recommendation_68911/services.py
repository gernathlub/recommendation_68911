import json
import time
import requests
from .exceptions import RecommendationException

from .settings import get_config

class RecommendationService():
    def __init__(self) -> None:
        self.SQS_URL = get_config("RECOMMENDER")["RECOMMENDATION_SQS_URL"]
        if not self.SQS_URL:
            return RecommendationException("Missing RECOMMENDATION_SQS_URL setting")
    
    def update_car_vector(self, object_pk, object_vector, object_dict):
        data = json.dumps({
            "Type": "UPDATE_VECTOR",
            "Object": {
                "attributes": object_dict,
                "vector": object_vector,
                "postgres_id": object_pk
            }
        })
        try:
            requests.get(self.SQS_URL, params={"Action": "SendMessage", "MessageBody": data})
        except Exception:
            return RecommendationException("Sending request feiled")
        
    def create_interaction(self, object_dict, object_vector, object_type, session, actor):
        data = json.dumps({
            "Type": "INTERACTION",
            "Session_id": session,
            "User_id": actor.pk if actor else None,
            "Interaction": {
                "object": object_dict,
                "vector": object_vector,
                "int_type": object_type,
                "timestamp": time.time()
            }
        })
        try:
            requests.get(self.SQS_URL, params={"Action": "SendMessage", "MessageBody": data})
        except Exception:
            return RecommendationException("Sending request feiled")