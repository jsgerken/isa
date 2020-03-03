from django.http import JsonResponse
import urllib.request
import urllib.parse
import json


def test(request):
    req = urllib.request.Request('http://models:8000/api/v1/manufacturers/1')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)
def prod_test(request):
    req = urllib.request.Request('http://models:8000/api/v1/products/1')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)