from django.db import models

class Crypto(models.Model):
    ticker = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=7)
    time_create = models.DateTimeField(auto_now_add=True)