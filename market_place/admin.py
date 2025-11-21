from django.contrib import admin
from .models import food, r_attribute, c_attribute, order, sub_order, staff_attribute, Otp_Confirmation

# Register your models here.
admin.site.register(food)
admin.site.register(staff_attribute)
admin.site.register(r_attribute)
admin.site.register(c_attribute)
admin.site.register(Otp_Confirmation)
admin.site.register(order)
admin.site.register(sub_order)

