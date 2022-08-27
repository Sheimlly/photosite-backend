from django.db import models

class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    email = models.EmailField(max_length = 254)
    message = models.CharField(max_length=200)
    date = models.DateTimeField()

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    active = models.BooleanField()

class Photo(models.Model):
    phoro_id = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to='resources/photos/')
    portfolio = models.BooleanField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)


class Offers(models.Model):
    offer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    short_description = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField()
    photo = models.ImageField(upload_to='resources/photos/offers/')
    frontpage = models.BooleanField(default=False)