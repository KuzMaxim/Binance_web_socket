from . import views
from django.urls import path, include

urlpatterns = [
    path('history', views.check_history)
]
