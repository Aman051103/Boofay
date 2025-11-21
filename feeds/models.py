from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Contact(models.Model):
    query_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    query = models.TextField(default='')
    dated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Query by {self.name}'
