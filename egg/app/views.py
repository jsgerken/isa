from app.models import Manufacturer, Product
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError

# Manufacturer methods
def get_all_manufacturers(request):
    if request.method == 'GET':
        manufacturers_list = Manufacturer.objects.all()
        response = []
        for manufacturer in manufacturers_list:
            man_object = {}
            man_object['man_id'] = manufacturer.man_id
            man_object['man_name'] = manufacturer.man_name
            man_object['web_url'] = manufacturer.web_url
            man_object['phone_num'] = manufacturer.phone_num
            response.append(man_object)
        return JsonResponse(response, safe=False)
    else:
        return HttpResponse(status=405)

def get_or_update_manufacturer(request, id):
    if request.method == 'GET':
        try:
            manufacturer = Manufacturer.objects.get(man_id=id)
            man_object = {}
            man_object['man_id'] = manufacturer.man_id
            man_object['man_name'] = manufacturer.man_name
            man_object['web_url'] = manufacturer.web_url
            man_object['phone_num'] = manufacturer.phone_num
            return JsonResponse(man_object)
        except ObjectDoesNotExist:
            error_object = {
                'error': 'Get failed: manufacturer with man_id ' + str(id) + ' does not exist'
            }
            return JsonResponse(error_object)
    elif request.method == 'POST':
        try:
            manufacturer = Manufacturer.objects.get(man_id=id)
            updated_man = {}
            manufacturer.man_name = request.POST.__getitem__('man_name')
            manufacturer.web_url = request.POST.__getitem__('web_url')
            manufacturer.phone_num= request.POST.__getitem__('phone_num')
            manufacturer.save()
            updated_man = {
                'man_name': manufacturer.man_name,
                'web_url': manufacturer.web_url,
                'phone_num': manufacturer.phone_num,
            }
            return JsonResponse(updated_man)
        except ObjectDoesNotExist:
            error_object = {
                'error': 'Update failed: manufacturer with man_id ' + str(id) + ' does not exist'
            }
            return JsonResponse(error_object)   
        except MultiValueDictKeyError:
            error_object = {
                'error': 'Update failed: you must provide man_name, web_url, and phone_num in your POST body'
            }
            return JsonResponse(error_object) 
    else:
        return HttpResponse(status=405)

def delete_manufacturer(request, id):
    if request.method == 'POST':
        try:
            manufacturer= Manufacturer.objects.get(man_id=id)
            deleted_object = {}
            deleted_object['man_id'] = manufacturer.man_id
            deleted_object['man_name'] = manufacturer.man_name
            deleted_object['web_url'] = manufacturer.web_url
            deleted_object['phone_num'] = manufacturer.phone_num
            manufacturer.delete()
            return JsonResponse(deleted_object)
        except ObjectDoesNotExist:
            error_object = {
                'error': 'Delete failed: manufacturer with man_id ' + str(id) + ' does not exist'
            }
            return JsonResponse(error_object)
    else:
        return HttpResponse(status=405)

def create_manufacturer(request):
    if request.method == 'POST':
        try:
            manufacturer = Manufacturer()
            manufacturer.man_name = request.POST.__getitem__('man_name')
            manufacturer.web_url = request.POST.__getitem__('web_url')
            manufacturer.phone_num = request.POST.__getitem__('phone_num')
            manufacturer.save()
            new_man = {
                'man_id': manufacturer.man_id,
                'man_name' : manufacturer.man_name,
                'web_url' : manufacturer.web_url,
                'phone_num' : manufacturer.phone_num,
            }
            return JsonResponse(new_man)
        except MultiValueDictKeyError:
            error_object = {
                'error': 'Create failed: you must provide man_name, web_url, and phone_num in your POST body'
            }
            return JsonResponse(error_object)         
    else:
        return HttpResponse(status=405)

# Product methods
def get_all_products(request):
    if request.method == 'GET':
        products_list = Product.objects.all()
        response = []
        for product in products_list:
            prod_object = {}
            prod_object['prod_id'] = product.product_id
            prod_object['type'] = product.type
            man = get_object_or_404(Manufacturer, man_id = product.man_id)
            prod_object['man_name'] = man.man_name
            prod_object['name'] = product.name
            prod_object['price'] = product.price
            response.append(prod_object)
        return JsonResponse(response, safe=False)
    elif request.method == 'POST':
        return HttpResponse(status=405)
        
def get_or_update_product(request, id):
    if request.method == 'GET':
        products_list = Product.objects.filter(product_id=id)
        response = []
        for product in products_list:
            prod_object = {}
            prod_object['prod_id']=product.product_id
            prod_object['type']=product.type
            man = get_object_or_404(Manufacturer, man_id = product.man_id)
            prod_object['man_name'] = man.man_name
            prod_object['name']=product.name
            prod_object['price']=product.price
            response.append(prod_object)
        return JsonResponse(response, safe=False)
    elif request.method == 'POST':
        products_list = Product.objects.filter(product_id=id)
        updated_prod = {}
        for product in products_list:
            product.type= request.POST.get('type', 'Error')
            product.man_id= request.POST.get('man_id', 'Error')
            product.name= request.POST.get('name', 'Error')
            product.price = request.POST.get('price', 'Error')
            product.save()
            updated_prod = {
                'prod_id' : product.product_id,
                'type' : product.type,
                'man_id' : product.man_id,
                'name' : product.name,
                'price' : product.price
            }
        return JsonResponse(updated_prod)
    else:
        return HttpResponse(status=405)

def delete_product(request, id):
    if request.method == 'POST':
        product_list = Product.objects.filter(product_id=id)
        prod_object = {}
        for product in product_list:
            prod_object['prod_id'] = product.product_id
        Product.objects.filter(product_id=id).delete()
        return JsonResponse(prod_object)
    else:
        return HttpResponse(status=405)

def create_product(request):
    if request.method == 'POST':
        product = Product()
        product.type= request.POST.get('type', 'Error')
        product.man_id= request.POST.get('man_id', 'Error')
        product.name= request.POST.get('name', 'Error')
        product.price = request.POST.get('price', 'Error')
        product.save()
        created_prod = {
            'prod_id' : product.product_id,
            'type' : product.type,
            'man_id' : product.man_id,
            'name' : product.name,
            'price' : product.price
        }
        return JsonResponse(created_prod)
    else:
        return HttpResponse(status=405)
