from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,null=True,blank=True,default="Ordered")
    customer = models.ForeignKey(User,on_delete=models.CASCADE)

    def get_total_item_price(self):
        return self.quantity * self.item.CIEmailField()

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField() 