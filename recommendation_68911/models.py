from django.db import models
from django.contrib.postgres.fields import ArrayField
from .services import RecommendationService

class AbstractVectorizedModel(models.Model):
    vector = ArrayField(ArrayField(models.FloatField(), null=True, blank=True), null=True, blank=True)
    
    class Meta:
        abstract = True

class AbstractRecomObject(AbstractVectorizedModel):
    class Meta:
        abstract = True
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_vector = True
        self.dict_repr = None
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pk and self.update_vector:
            RecommendationService().update_car_vector(self.pk, self.vector, self.dict_repr)
        

class AbstractRecomActor(AbstractVectorizedModel):
    class Meta:
        abstract = True