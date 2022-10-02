from django.db import models

class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.IntegerField(default=0, blank=True)
    email = models.EmailField(max_length = 254)
    message = models.CharField(max_length=200)
    date = models.DateTimeField()
    readed =  models.BooleanField(default=False)

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


# Offers models
class Offers(models.Model):
    offer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    active = models.BooleanField()
    photo = models.ImageField(upload_to='resources/photos/offers/', blank=True)
    frontpage = models.BooleanField(default=False)

class OfferDescription(models.Model):
    offer_description_id = models.AutoField(primary_key=True)
    offer = models.ForeignKey(Offers, default=None, on_delete=models.CASCADE, related_name='offer_description')
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description