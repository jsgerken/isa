from app.models import Manufacturer, Product
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError

# Get_All Methods
def get_all_manufacturers(request):
    if request.method == 'GET':
        manufacturers_list = Manufacturer.objects.all()
        response = []
        for manufacturer in manufacturers_list:
            man_object = {
                'man_id': manufacturer.man_id,
                'man_name': manufacturer.man_name,
                'web_url': manufacturer.web_url,
                'phone_num': manufacturer.phone_num,
            }
            response.append(man_object)
        return JsonResponse(response, safe=False)
    else:
        error_object = {
            'error': 'HTTP method error: get all manufacturers endpoint expects a GET request'
        }
        return JsonResponse(error_object)

def get_all_products(request):
    if request.method == 'GET':
        products_list = Product.objects.all()
        response = []
        for product in products_list:
            prod_object = {
                'product_id': product.product_id,
                'type': product.type,
                'man_id': product.man_id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'warranty': product.warranty,
            }
            response.append(prod_object)
        return JsonResponse(response, safe=False)
    else:
        error_object = {
            'error': 'HTTP method error: get all products endpoint expects a GET request'
        }

#--------------------------------------------------------------------------------------------------------------

# Get/Update Methods
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
                'error': 'Update failed: you must provide man_name, web_url, and phone_num in your POST body to update a manufacturer'
            }
            return JsonResponse(error_object) 
    else:
        error_object = {
            'error': 'HTTP method error: manufacturer endpoint expects a GET or POST request'
        }
        return JsonResponse(error_object)

def get_or_update_product(request, id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(product_id=id)
            prod_object = {
                'product_id': product.product_id,
                'type': product.type,
                'man_id': product.man_id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'warranty': product.warranty,
            }
            return JsonResponse(prod_object)
        except ObjectDoesNotExist:
            error_object = {
                'error': 'Get failed: product with product_id ' + str(id) + ' does not exist'
            }
            return JsonResponse(error_object)
    elif request.method == 'POST':
        try:
            product = Product.objects.get(product_id=id)
            product.type= request.POST.__getitem__('type')
            product.man_id= request.POST.__getitem__('man_id')
            product.name= request.POST.__getitem__('name')
            product.price = request.POST.__getitem__('price')
            product.save()
            updated_prod = {
                'product_id': product.product_id,
                'type': product.type,
                'man_id': product.man_id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'warranty': product.warranty,
            }
            return JsonResponse(updated_prod)
        except ObjectDoesNotExist:
            error_object = {
                'error': 'Update failed: product with product_id ' + str(id) + ' does not exist'
            }
            return JsonResponse(error_object)   
        except MultiValueDictKeyError:
            error_object = {
                'error': 'Update failed: you must provide type, man_id, name, description, price, and warranty in your POST body to update a product'
            }
            return JsonResponse(error_object) 
    else:
        error_object = {
            'error': 'HTTP method error: product endpoint expects a GET or POST request'
        }
        return JsonResponse(error_object)

#---------------------------------------------------------------------------------------------------------------

# Delete Methods
def delete_manufacturer(request, id):
    if request.method == 'DELETE':
        try:
            manufacturer = Manufacturer.objects.get(man_id=id)
            deleted_man = {
                'man_id': manufacturer.man_id,
                'man_name': manufacturer.man_name,
                'web_url': manufacturer.web_url,
                'phone_num': manufacturer.phone_num,
            }
            manufacturer.delete()
            return JsonResponse(deleted_man)
        except ObjectDoesNotExist:
            error_object = {
                'error': 'Delete failed: manufacturer with man_id ' + str(id) + ' does not exist'
            }
            return JsonResponse(error_object)
    else:
        error_object = {
            'error': 'HTTP method error: delete manufacturer endpoint expects a DELETE request'
        }
        return JsonResponse(error_object)

def delete_product(request, id):
    if request.method == 'DELETE':
        try:
            product = Product.objects.get(product_id=id)
            deleted_product = {
                'product_id': product.product_id,
                'type': product.type,
                'man_id': product.man_id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'warranty': product.warranty,
            }
            product.delete()
            return JsonResponse(deleted_product)
        except ObjectDoesNotExist:
            error_object = {
                'error': 'Delete failed: product with product_id ' + str(id) + ' does not exist'
            }
            return JsonResponse(error_object)
    else:
        error_object = {
            'error': 'HTTP method error: delete product endpoint expects a DELETE request'
        }
        return JsonResponse(error_object)

#--------------------------------------------------------------------------------------------------------------

# Create Methods
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
                'error': 'Create failed: you must provide man_name, web_url, and phone_num in your POST body to create a manufacturer'
            }
            return JsonResponse(error_object)         
    else:
        error_object = {
            'error': 'HTTP method error: create manufacturer endpoint expects a POST request'
        }
        return JsonResponse(error_object)

def create_product(request):
    if request.method == 'POST':
        try:
            product = Product()
            product.type= request.POST.__getitem__('type')
            product.man_id= request.POST.__getitem__('man_id')
            product.name= request.POST.__getitem__('name')
            product.description = request.POST.__getitem__('description')
            product.price = request.POST.__getitem__('price')
            product.warranty = request.POST.__getitem__('warranty')
            product.save()
            created_prod = {
                'product_id' : product.product_id,
                'type' : product.type,
                'man_id' : product.man_id,
                'name' : product.name,
                'description' : product.description,
                'price' : product.price,
                'warranty' : product.warranty,
            }
            return JsonResponse(created_prod)
        except MultiValueDictKeyError:
            error_object = {
                'error': 'Update failed: you must provide type, man_id, name, description, price, and warranty in your POST body to create a product'
            }
            return JsonResponse(error_object)
    else:
        error_object = {
            'error': 'HTTP method error: create product endpoint expects a POST request'
        }
        return JsonResponse(error_object)

#--------------------------------------------------------------------------------------------------------------