from . import views
from django.urls import path, register_converter
    
from . import converters


register_converter(converters.FullTicker, "full_ticker")


urlpatterns = [
    path('history/<full_ticker:ticker>', views.check_history)
]
