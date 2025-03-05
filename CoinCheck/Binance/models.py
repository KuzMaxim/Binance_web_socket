from django.db import models
from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from rest_framework import serializers#type: ignore




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
        
    @staticmethod
    @sync_to_async
    def get_history(ticker):
        try:
            cryptos = Crypto.objects.filter(ticker=ticker)
            serializer = CryptoSerializer(cryptos, many=True)
            return serializer.data
        except Exception as e:
            return {'error': str(e)}


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = ['ticker', 'price', 'time_create']