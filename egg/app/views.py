from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from app.models import Product
# Create your views here.
def Products(request):
    if request.method == 'GET':
        listOfProducts = Product.objects.all()
        response = []
        for product in listOfProducts:
            prod_object = {}
            prod_object['prod_id']=product.prod_id
            prod_object['type']=product.product_type
            prod_object['man_id']=product.man_id
            prod_object['name']=product.name
            prod_object['price']=product.price
            response.append(prod_object)
        return JsonResponse(response, safe=False)
    elif request.method == 'POST':
        return HttpResponse([])