from django.http import JsonResponse
from . import models

async def check_history(request, ticker):
    history = await models.Crypto.get_history(ticker)
    return JsonResponse(history, safe=False)

