from django.http import JsonResponse
from . import models

async def check_history(request):
    if request.method == 'GET':
        ticker = request.headers.get('Ticker')
        if ticker:
            history = await models.Crypto.get_history(ticker)
            return JsonResponse(history, safe=False)
        else:
            return JsonResponse({'error': 'Ticker header is required'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
