# Recommendation_68911
Django PyPi package serving as the interface for the recommendation system, providing models, managers, and migrations required by the vector recommendation service. This package is meant only for Django version 3.2 (and above) and above using the PostgreSQL database version 9.5 (and above). The package is intended to be used with a specific recommendation engine developed as part of my master's thesis project (not yet published) and is not for general purposes.

## Installation guide
Install pip package:

```bash
pip install recommendation-68911
```

Add the package to the installed apps in the `settings.py` file (recommended before custom apps depending on this package).

```python
# settings.py

INSTALLED_APPS = [
    ...
    'recommendation_68911',
    'your_custom_app',
]
```

Add the `RECOMMENDATION_SQS_URL` variable to your settings, which will specify the URL of your recommendation microservice API endpoint.

```python
# settigs.py

RECOMMENDATION_SQS_URL = 'https://your.api.endpiont/...'
```

Run the pre-created migration to install the cube extension for your PostgreSQL (extension is compatible to be used also within AWS RDS).

```bash
python3 manage.py migrate recommendation_68911
```

Add RecomObjectQuerySet as a parent to your recommended object class QuerySet manager. If you don't have one, you will need to create one.

```python
# managers.py

from recommendation_68911.managers import RecomObjectQuerySet

class YourObjectQuerySet(..., RecomObjectQuerySet):
    ...
```

Specify `AbstractRecomObject` as the parent of the object class you want to recommend and `AbstractRecomActor` for the actor class in your app's `models.py`. Also specify objects attributable to `YourObjectClass` to use the `QuerySetManager` created in the previous step. Finally, it's strongly recommended to specify cases when you don't want to perform object vector updates in the `save()` method by setting the `self.update_vector` attribute. If updating the vector is wanted, it is required to provide the object's attributes in `self.dict_repr`.

```python
# models.py

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

To send your actor-object interactions to the microservice, you'll need to use the `create_interaction()` method of the provided `RecommendationService` class. It's recommended to perform this task within the `dispatch()` method of your view.

```python
# views.py

from recommendation_68911.services import RecommendationService

class YourDetailView(...):
    ...
    def dispatch(self, request, *args, **kwargs):
            super_result = super().dispatch(request, *args, **kwargs)
            ...
            if your_session and your_object.vector != None:
                RecommendationService().create_interaction(
                    object_dict={...},
                    object_vector=your_object.vector,
                    object_type="YOUR_TYPE",
                    your_session.session_key if your_session else None,
                    your_actor if your_actor.is_authenticated else None
                )
            return super_result
```

Your integration of the recommendation system is now finished. To apply a recommendation filter to a query set, add the `order_by_recommended()` method at the end of your query.

```python
# views.py

class YourListView(...):
    ...
    def get_queryset(...):
        qs = super().get_queryset(...)
        ...
        return qs.order_by_recommended(your_actor_object.vector)
```