from django.http import HttpResponse
import urllib.request
import urllib.parse
import json


def index(request):
    req = urllib.request.Request('http://services:8000/api/v1/test/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return HttpResponse(resp['man_name'])
