from django.http import JsonResponse
import urllib.request
import urllib.parse
import json


def filterType(request, type):
    print(type)
    req = urllib.request.Request('http://models:8000/api/v1/products/')
    products_json = urllib.request.urlopen(req).read().decode('utf-8')
    products_dict = json.loads(products_json)
    products = products_dict['allProducts']
    products.sort(key=lambda x: x['views'], reverse=True)
    return JsonResponse({'products': products})
