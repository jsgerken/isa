from .models import Manufacturer, Product, User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError


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
        return JsonResponse({'allManufacturers': response})
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
                'views': product.views,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'warranty': product.warranty,
                "img_url": product.img_url
            }
            response.append(prod_object)
        return JsonResponse({'allProducts': response})
    else:
        error_object = {
            'error': 'HTTP method error: get all products endpoint expects a GET request'
        }


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
            manufacturer.phone_num = request.POST.__getitem__('phone_num')
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
            product.type = request.POST.__getitem__('type')
            product.man_id = request.POST.__getitem__('man_id')
            product.name = request.POST.__getitem__('name')
            product.description = request.POST.__getitem__('description')
            product.price = request.POST.__getitem__('price')
            product.warranty = request.POST.__getitem__('warranty')
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
                'man_name': manufacturer.man_name,
                'web_url': manufacturer.web_url,
                'phone_num': manufacturer.phone_num,
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
            product.type = request.POST.__getitem__('type')
            product.man_id = request.POST.__getitem__('man_id')
            product.name = request.POST.__getitem__('name')
            product.description = request.POST.__getitem__('description')
            product.price = request.POST.__getitem__('price')
            product.warranty = request.POST.__getitem__('warranty')
            product.save()
            created_prod = {
                'product_id': product.product_id,
                'type': product.type,
                'man_id': product.man_id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'warranty': product.warranty,
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


def get_all_users(request):
    try:
        if request.method == 'GET':
            user_list = User.objects.all()
            response = []
            for users in user_list.values():
                response.append(users)
            return JsonResponse({'allUsers': response})
        else:
            return JsonResponse({
                'error': 'HTTP method error: get all users endpoint expects a GET request'
            })
    except Exception as e:  # for development purpose. can remove exception as e in production
        return JsonResponse({
            'error': 'Error while getting all Users from DB. Check errMessage for more info',
            'errMessage': 'DEV_MODE_MESSAGE: ' + str(e)
        })


def get_or_update_user(request, id):
    try:
        if request.method == 'GET':
            # using the filter lets me leverage queryset methods
            user_list = User.objects.filter(user_id=id)
            # like this one that turns objects into dict
            return JsonResponse(user_list.values()[0])
        elif request.method == 'POST':
            user_list = User.objects.filter(user_id=id)
            new_values = request.POST.dict()
            user_list.update(**new_values)
            return JsonResponse(user_list.values()[0])
        else:
            return JsonResponse({
                'error': 'HTTP method error: User endpoint expects a GET or POST request'
            })
    except IndexError:  # this is what filter throws if it does not find user with given id.
        return JsonResponse({
            'error': 'Get failed: user with user_id ' + str(id) + ' does not exist',
        })
    except Exception as e:  # for development purpose. can remove exception as e in production
        return JsonResponse({
            'error': 'Double check param data for accepted fields and uniqueness. API currently accepts: email, username, password, phone_number, first_name, last_name',
            'errMessage': 'DEV_MODE_MESSAGE: ' + str(e)
        })


def create_user(request):
    try:
        if request.method == 'POST':
            new_values = request.POST.dict()
            user = User(**new_values)
            user.save()
            return JsonResponse(new_values)
        else:
            return JsonResponse({
                'error': 'HTTP method error: User endpoint expects a GET or POST request'
            })
    except Exception as e:
        return JsonResponse({
            'error': 'Double check param data for accepted fields and uniqueness. API currently accepts: email, username, password, phone_number, first_name, last_name',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        }
        )


def delete_user(request, id):
    try:
        if request.method == 'DELETE':
            user = User.objects.filter(user_id=id)
            deleted_user = user.values()[0]
            user.delete()
            return JsonResponse(deleted_user)
        else:
            return JsonResponse({
                'error': 'HTTP method error: User endpoint expects a GET or POST request'
            })
    except IndexError:
        return JsonResponse({
            'error': 'Delete failed: user with user_id ' + str(id) + ' does not exist',
        })
    except Exception as e:
        return JsonResponse({
            'error': 'Double check param data for accepted fields and uniqueness. API currently accepts: email, username, password, phone_number, first_name, last_name',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        })
