from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class food(models.Model):
    food_id = models.AutoField(primary_key=True)
    by_restaurant = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    parent_id = models.IntegerField(default=0)
    name = models.CharField(max_length=300)
    category = models.CharField(max_length=200)
    sub_category = models.CharField(max_length=200)
    description = models.TextField()
    preparation_time_in_minutes = models.IntegerField(default=15)
    price = models.IntegerField(default=50)
    image = models.ImageField(upload_to='foods/images', null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    feedback = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} by {self.by_restaurant}'



class r_attribute(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    restaurant_user_id = models.IntegerField(default=0)
    tag_line = models.CharField(max_length=200, blank=True, null=True)
    about = models.TextField(default='', blank=False)
    image = models.ImageField(upload_to='restaurants/images', null=True, blank=True)
    date_of_registration = models.DateField(auto_now_add=True, null=True)
    opening_time_hours = models.IntegerField(default=9)
    closing_time_hours = models.IntegerField(default=20)
    address = models.CharField(max_length=500, null=False, blank=False)
    location = models.CharField(max_length=500, null=False, blank=False)
    City =  models.CharField(max_length=500, null=False, blank=False)
    State = models.CharField(max_length=500, null= False, blank=False)
    pin_code = models.IntegerField(validators=[
            MaxValueValidator(999999),
            MinValueValidator(100000)
        ], null= False, blank=False)
    guardian_phone_number = models.CharField(max_length=11, null= False, blank=False)



class staff_attribute(models.Model):
    staff_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    security_key = models.IntegerField(default=24681357, validators=[
            MaxValueValidator(99999999),
            MinValueValidator(10000000)
        ])



class c_attribute(models.Model):
    customer_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, null= False, blank=False)
    gender = models.CharField(max_length=20, null= False, blank=False)
    address = models.CharField(max_length=500, null=False, blank=False)
    City =  models.CharField(max_length=500, null=False, blank=False)
    State = models.CharField(max_length=500, null= False, blank=False)
    pin_code = models.IntegerField(validators=[
            MaxValueValidator(999999),
            MinValueValidator(100000)
        ], null= False, blank=False)


class Otp_Confirmation(models.Model):
    otp_confirmation_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation_status = models.BooleanField(default=False)




class order(models.Model):
    dynamic_order_id = models.AutoField(primary_key=True)
    ordered_by = models.ForeignKey(User, on_delete=models.PROTECT)
    order_date = models.DateField(auto_now_add=True)
    total_restaurants_associated = models.IntegerField(default=1)
    name_of_those_restaurants = models.TextField()
    net_delivery_status =  models.BooleanField(default=False)

    def __str__(self):
        return f'order {self.dynamic_order_id} by {self.ordered_by.username}'

   
class sub_order(models.Model):
    sub_order_id = models.AutoField(primary_key=True)
    parent_order = models.ForeignKey(order, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False) 
    paid_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True) 
    ordered_ids = models.CharField(max_length=3000)
    cost = models.IntegerField()
    total_preparation_time_in_minutes = models.IntegerField()
    preparation_status = models.BooleanField(default=False)
    delivery_status =  models.BooleanField(default=False)

    def __str__(self):
        return f'sub_order of order number - {self.parent_order.dynamic_order_id}, {self.parent_order.ordered_by.username}'

        