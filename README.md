# Recommendation_68911
Django PyPi package serving as recommendation system interface, providing models, managers and migrations required by vector recommendation service. This package is ment only for Django version 3.2 and above, using PostgreSQL database. Package is ment to be used with specific recommendation engine (not published yet) and its not for general purpouse.

## Instalation guide
Install pip package:

```bash
pip install recommendation-68911
```

Add package to installed apps in settings.py file (recommended before custom apps depending on this package).


```python
INSTALLED_APPS = [
    ...
    'recommendation_68911',
    'your_custom_app',
]
```

Add RECOMMENDATION_SQS_URL variable to your setings, which will specity URL of your recommendation microservice API endpoint.

```python
RECOMMENDATION_SQS_URL = 'https://your.api.endpiont/...'
```

Run pre-created migration to install cube extension for your PostgreSQL (extension is compatible to be used also within AWS RDS).

```bash
python3 manage.py migrate recommendation_68911
```

Add RecomObjectQuerySet as parent to your recommended object class QuerySet manager. If you dont use one, you will neet to create it.

```python
from recommendation_68911.managers import RecomObjectQuerySet

class YourObjectQuerySet(..., RecomObjectQuerySet):
    ...
```

Specify AbstractRecomObject as parent of object class you want to recommend and AbstractRecomActor for actor class in your apps models.py. Also specify objects attrbute of YourObjectClass to use QuerySet manager created in previous step. Finally, its strongly recommended to specify cases when you dont want to perform pbjects vector update in save() method by setting self.update_vector attribute. If updating vector is wanted, its required to provide objects attributes in self.dict_repr. 

```python
from recommendation_68911.models import AbstractRecomObject, AbstractRecomActor

class YourObjectModel(..., AbstractRecomObject):
    ...
    objects = YourObjectManager.from_queryset(YourObjectQuerySet)
    ...
    def save(self, *args, **kwargs):
        if not your_condition:
            self.update_vector = False
        else:
            self.dict_repr = {
                ...
            }
        super().save(*args, **kwargs)    

class YourActorModel(..., AbstractRecomActor):
    ...
```

After this step, you are ready to create and execute the migration to apply changes.

```bash
python3 manage.py makemigrations <your_app>
python3 manage.py migrate <your_app>
```

Your integration of recommendation system is now finished. To apply recommendation filter on queryset, add order_by_recommended() method at the end of your query.

```python

class YourView(...):
    ...
    def get_queryset(...):
        qs = super().get_queryset(...)
        ...
        return qs.order_by_recommended(your_actor_object.vector)
```