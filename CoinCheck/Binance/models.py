from django.db import models
from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError

class Crypto(models.Model):
    ticker = models.CharField(max_length=10)
    price = models.IntegerField()
    time_create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.ticker
    
    @staticmethod
    def post(ticker, price):
        instance = Crypto(ticker=ticker, price=price)
        instance.full_clean() # Валидация перед сохранением
        instance.save() 
    
    @staticmethod
    @sync_to_async
    def get(ticker):
        try:
            crypto = Crypto.objects.filter(ticker=ticker).latest('time_create')
            return crypto.price
        except Crypto.DoesNotExist:
            return None