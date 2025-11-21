from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class order_data(models.Model):
    data_id = models.AutoField(primary_key=True)
    parent_restaurant = models.ForeignKey(User, on_delete=models.CASCADE)
    timeStamp = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'payment data - {self.by_restaurant}, dated - {self.timeStamp}'