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
