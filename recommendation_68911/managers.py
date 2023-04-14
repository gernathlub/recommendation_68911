from django.db import models

class RecomObjectQuerySet(models.QuerySet):
    def order_by_recommended(self, user_vector):
        return self.extra(select={"dist": "cube(%s) <-> cube(cars.vector)"}, select_params=user_vector, order_by=['dist'])
