from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import urllib.request
import urllib.parse
import json


def index(request):
    req = urllib.request.Request('http://services:8000/api/v1/type/all/')
    product_json = urllib.request.urlopen(req).read().decode('utf-8')
    product_dict = json.loads(product_json)
    return render(request, 'frontend_app/products.html', product_dict)
    #req = urllib.request.Request('http://services:8000/api/v1/test/')
    #resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    #resp = json.loads(resp_json)
    #return HttpResponse(resp['man_name'])


def home(request):
    req = urllib.request.Request('http://exp:8000/api/v1/newly-added/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    args = {}
    args['newlyAddedGrouped'] = group(resp['newlyAddedSorted'], 4)
    # return JsonResponse({"test": str(args)})
    return render(request, 'home.html', args)

    # url = "http://models:8000/static/models_app/ProductImages/RAM.jpg"
    # # req = urllib.request.Request(url)
    # img = Image.open(urllib.urlopen(url))
    # return JsonResponse({"hi": str(img)})


def group(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]
