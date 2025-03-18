from django.db import models
from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from rest_framework import serializers#type: ignore




class Crypto(models.Model):
    ticker = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    time_create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.ticker
    
    @staticmethod
    @sync_to_async
    def post(ticker, price):
        instance = Crypto(ticker=ticker, price=price)
        instance.save() 
    
    @staticmethod
    @sync_to_async
    def get(full_ticker):
        try:
            crypto = Crypto.objects.filter(ticker=full_ticker).latest('time_create')
            return crypto.price
        except Crypto.DoesNotExist:
            return None
        
    @staticmethod
    @sync_to_async
    def get_history(ticker):
        try:
            cryptos = Crypto.objects.filter(ticker__startswith=ticker)
            serializer = CryptoSerializer(cryptos, many=True)
            return serializer.data
        except Exception as e:
            return {'error': str(e)}


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = ['ticker', 'price', 'time_create']