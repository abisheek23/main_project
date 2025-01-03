from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name=models.TextField()


class prodect(models.Model):
    pid=models.TextField()
    name=models.TextField()
    dis=models.TextField() 
    price=models.IntegerField()
    offer_price=models.IntegerField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    stoct=models.IntegerField()
    img=models.FileField()

class Cart(models.Model):
    product=models.ForeignKey(prodect,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()

class Adress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    State = [
        ('1', 'Andhra Pradesh'),
        ('2', 'Telangana'),
        ('3', 'kerala'),
        ('4', 'Tamil Nadu'),
        ('5', 'Karnataka'),
    ]
    phno= models.IntegerField()
    position = models.CharField(max_length=1, choices=State)
    district=models.CharField(max_length=25)
    Adress=models.TextField()