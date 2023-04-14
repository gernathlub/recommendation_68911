from functools import lru_cache

from django.conf import settings

CONFIG_DEFAULTS = {
    "RECOMMENDATION_SQS_URL": None
}


@lru_cache
def get_config(settings_name=None):
    if settings_name is None:
        settings_name = "RECOMMENDER"

    return {**CONFIG_DEFAULTS, **getattr(settings, settings_name, {})}