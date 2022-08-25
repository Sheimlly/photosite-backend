from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    email = models.CharField(max_length=50)
    message = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')

class Categories(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField()

class Photo(models.Model):
    photo = models.ImageField(upload_to='resources/photos')
    portfolio = models.BooleanField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)


class Offer(models.Model):
    offerName = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    active = models.BooleanField()
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)