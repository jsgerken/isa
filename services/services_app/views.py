from django.http import JsonResponse
import urllib.request
import urllib.parse
import json


def filterType(request, type):
    req = urllib.request.Request('http://models:8000/api/v1/products/')
    products_json = urllib.request.urlopen(req).read().decode('utf-8')
    products_dict = json.loads(products_json)
    products = products_dict['allProducts']
    products.sort(key=lambda x: x['views'], reverse=True)
    return JsonResponse({'products': products})

def test(request):
    req = urllib.request.Request('http://models:8000/api/v1/manufacturers/1')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)


def newly_added(request):
    req = urllib.request.Request('http://models:8000/api/v1/products/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp_array = json.loads(resp_json)['allProducts']
    resp_sorted = sorted(resp_array, key=lambda i: i['datetime_created'])
    return JsonResponse({"newlyAddedSorted": resp_sorted})

