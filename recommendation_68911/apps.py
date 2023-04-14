from django.apps import AppConfig

class DefaultAppConfig(AppConfig):
    name = "recommendation_68911"
    
    def ready(self):
        from django.conf import settings
        if not hasattr(settings , "RECOMMENDATION_SQS_URL") or settings.RECOMMENDATION_SQS_URL is None:
            raise Exception('recommendation_68911 extension requires RECOMMENDATION_SQS_URL setting')
        if 'postgresql' not in settings.DATABASES['default']['ENGINE']:
            raise Exception('recommendation_68911 extension works only with postgresql database')