from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
import urllib.request
import urllib.parse
import json




def index(request):
    req = urllib.request.Request('http://services:8000/api/v1/test/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return HttpResponse(resp['man_name'])

def detail(request):
    #question = get_object_or_404()
#     manu1 = {
#         "model": "models_app.manufacturer",
#         "pk": 1,
#         "fields": {
#             "man_name": "Intel",
#             "web_url": "https://www.intel.com/",
#             "phone_num": "1-626-854-9338"
#         }
# }
#     prod1 = {
#             "product_id": 1,
#             "type": "CPU",
#             "man_id": 1,
#             "name": "Intel Core i5-9600K",
#             "description": "So crisp",
#             "price": 300,
#             "warranty": "1 week"
#     }
    #return HttpResponse(template.render(request))
    req = urllib.request.Request('http://services:8000/api/v1/prod_test')

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    img = "https://c1.neweggimages.com/NeweggImage/ProductImageCompressAll1280/13-157-843-V07.jpg"

    return render(request, 'frontend/item-desc.html', {'product': resp, 'image': img})

