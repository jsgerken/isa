from .models import Manufacturer, Product, User, Authenticator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
import os
import hmac
from django.conf import settings
from django.core.files.base import ContentFile
import base64

def selenium(request):
    man = Manufacturer.objects.get(man_name='selenium_man')
    man.delete()
    user = User.objects.get(username='selenium')
    user.delete()
    prod = Product.objects.get(name='selenium')
    prod.delete()
    return JsonResponse({'status': 'cleared selenium test data'})

def get_all_manufacturers(request):
    if request.method == 'GET':
        manufacturers_list = Manufacturer.objects.all()
        response = []
        for manufacturer in manufacturers_list:
            man_object = {
                'man_id': manufacturer.man_id,
                'man_name': manufacturer.man_name,
                'web_url': manufacturer.web_url,
                'phone_number': manufacturer.phone_number,
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
        for product in products_list.values():
            response.append(product)
        return JsonResponse({"allProducts": response})
    else:
        error_object = {
            'error': 'HTTP method error: get all products endpoint expects a GET request'
        }
        return JsonResponse(error_object)


def get_or_update_manufacturer(request, id):
    if request.method == 'GET':
        try:
            manufacturer = Manufacturer.objects.get(man_id=id)
            man_object = {}
            man_object['man_id'] = manufacturer.man_id
            man_object['man_name'] = manufacturer.man_name
            man_object['web_url'] = manufacturer.web_url
            man_object['phone_number'] = manufacturer.phone_number
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
            manufacturer.phone_number = request.POST.__getitem__(
                'phone_number')
            manufacturer.save()
            updated_man = {
                'man_name': manufacturer.man_name,
                'web_url': manufacturer.web_url,
                'phone_number': manufacturer.phone_number,
            }
            return JsonResponse(updated_man)
        except ObjectDoesNotExist:
            error_object = {
                'error': 'Update failed: manufacturer with man_id ' + str(id) + ' does not exist'
            }
            return JsonResponse(error_object)
        except MultiValueDictKeyError:
            error_object = {
                'error': 'Update failed: you must provide man_name, web_url, and phone_number in your POST body to update a manufacturer'
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
            product = Product.objects.filter(product_id=id)
            return JsonResponse(product.values()[0])
        except ObjectDoesNotExist:
            error_object = {
                'error': 'Get failed: product with product_id ' + str(id) + ' does not exist'
            }
            return JsonResponse(error_object)
        except Exception as e:  # for development purpose. can remove exception as e in production
            return JsonResponse({
                'error': 'Double check param data for accepted fields and uniqueness. API currently accepts: email, username, password, phone_numberber, first_name, last_name',
                'errMessage': 'DEV_MODE_MESSAGE: ' + str(e)
            })
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
                'phone_number': manufacturer.phone_number,
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
    try:
        if request.method == 'POST':
            new_values = request.POST.dict()
            man = Manufacturer(**new_values)
            man.password = make_password(
                new_values['password'], salt='f1nd1ngn3m0', hasher='default')
            man.save()
            new_values[man._meta.pk.name] = man.pk
            return JsonResponse(new_values)
        else:
            error_object = {
                'error': 'HTTP method error: create manufacturer endpoint expects a POST request'
            }
            return JsonResponse(error_object)
    except MultiValueDictKeyError:
        error_object = {
            'error': 'Create failed: you must provide man_name, web_url, and phone_number in your POST body to create a manufacturer'
        }
        return JsonResponse(error_object)
    except Exception as e:  # for development purpose. can remove exception as e in production
        return JsonResponse({
            'error': 'Double check param data for accepted fields and uniqueness. API currently accepts: man_name, web_url, phone_numberber, password, is_man',
            'errMessage': 'DEV_MODE_MESSAGE: ' + str(e)
        })


def create_product(request):
    try:
        if request.method == 'POST':
            new_values = request.POST.dict()
            # decode bytes from uploaded img
            convert_bytes_to_file = ContentFile(
                base64.b64decode(new_values.pop('product_img')))
            product = Product(**new_values)
            product.save()
            # create image name
            file_name = new_values['name'] + " " + \
                new_values['type'] + " " + str(product.pk) + '.png'
            # save the file to s3
            product.product_img.save(file_name, convert_bytes_to_file)
            # grab the url now so we dont have to open the file later
            product.img_url = product.product_img.url
            product.save()
            new_values[product._meta.pk.name] = product.pk
            new_values['product_img'] = product.product_img.name
            new_values['img_url'] = product.product_img.url
            return JsonResponse(new_values)
        else:
            return JsonResponse({
                'error':  'HTTP method error: create product endpoint expects a POST request'
            })
    except MultiValueDictKeyError:
        error_object = {
            'error': 'Create failed: you must provide type, man_id, name, description, price, warranty, and product_img in your POST body to create a product'
        }
        return JsonResponse(error_object)
    except Exception as e:
        return JsonResponse({
            'error': 'Double check param data for accepted fields and uniqueness. API currently accepts: type, man_id, name, description, price, warranty, and product_img',
            'errReason':  'In Create Product – DEV_MODE_MESSAGE: ' + str(e)
        }
        )


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


@csrf_exempt
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
            'error': 'Double check param data for accepted fields and uniqueness. API currently accepts: email, username, password, phone_numberber, first_name, last_name',
            'errMessage': 'DEV_MODE_MESSAGE: ' + str(e)
        })


def create_user(request):
    try:
        if request.method == 'POST':
            new_values = request.POST.dict()
            user = User(**new_values)
            user.password = make_password(
                new_values['password'], salt='f1nd1ngn3m0', hasher='default')
            user.save()
            new_values[user._meta.pk.name] = user.pk
            return JsonResponse(new_values)
        else:
            return JsonResponse({
                'error': 'HTTP method error: User endpoint expects a POST request'
            })
    except Exception as e:
        return JsonResponse({
            'error': 'Double check param data for accepted fields and uniqueness. API currently accepts: email, username, password, phone_numberber, first_name, last_name',
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
            'error': 'Double check param data for accepted fields and uniqueness. API currently accepts: email, username, password, phone_numberber, first_name, last_name',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        })


def login(request):
    try:
        if request.method == 'POST':
            req_data = request.POST.dict()
            get_man = req_data.pop("is_man")
            is_man = get_man.lower() == 'true'
            authee_name = (req_data.get('username'),
                           req_data.get('man_name'))[is_man]
            password = req_data['password']
            # have to use lambda because python evaluates both then picks instead of only the one to pick , lame!
            authee = (lambda: User.objects.get(username=authee_name), lambda: Manufacturer.objects.get(
                man_name=authee_name))[is_man]()
            authee_id = authee.pk
            get_auth_model = ('User', 'Manufacturer')[is_man]
            if check_password(password, authee.password):
                auth = Authenticator.objects.filter(
                    auth_id=authee_id, auth_model=get_auth_model)
                if not auth:
                    authenticator = hmac.new(
                        key=settings.SECRET_KEY.encode('utf-8'),
                        msg=os.urandom(32),
                        digestmod='sha256',
                    ).hexdigest()
                    new_auth = Authenticator(
                        authenticator=authenticator, auth_id=authee_id, auth_model=get_auth_model)
                    new_auth.save()
                    return JsonResponse({'code': 'success', 'auth': authenticator, 'auth_id': authee_id})
                else:
                    return JsonResponse({'code': 'success', 'auth': auth[0].authenticator, 'auth_id': authee_id})
            else:
                return JsonResponse({'code': 'failure', 'errMessage': 'Incorrect Password'})
        else:
            return JsonResponse({
                'error': 'HTTP method error: Login endpoint expects a POST request'
            })
    except Exception as e:
        return JsonResponse({
            'error': 'Error',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        })


# fix logout to also query for auth_model
def logout(request):
    try:
        if request.method == 'POST':
            req_data = request.POST.dict()
            get_man = req_data.pop('is_man')
            is_man = get_man.lower() == 'true'
            get_auth_model = ('User', 'Manufacturer')[is_man]
            authenticator = Authenticator.objects.get(
                authenticator=req_data['auth'], auth_model=get_auth_model)
            authenticator.delete()
            return JsonResponse({
                'code': 'success',
                'deleted_auth': req_data['auth']
            })
        else:
            return JsonResponse({
                'error': 'HTTP method error: Login endpoint expects a POST request'
            })
    except Exception as e:
        return JsonResponse({
            'error': 'Error',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        })


def get_user_id(request):
    # will retrieve with either email or username
    try:
        if request.method == 'POST':
            user_info = request.POST.dict()
            user_email = user_info.get('email')
            user_username = user_info.get('username')
            if user_email:
                user_object = User.objects.get(email=user_email)
                return JsonResponse({"user_id": user_object.pk, 'email': user_object.email})
            elif user_username:
                user_object = User.objects.get(username=user_username)
                return JsonResponse({"user_id": user_object.pk, 'email': user_object.email})
            else:
                return JsonResponse({"error": 'No email or username was provided to get_user_id'})
        else:
            return JsonResponse({
                'error': 'HTTP method error: get_user_id endpoint expects a POST request'
            })
    except Exception as e:
        return JsonResponse({
            'error': 'Error in get_user_id in models',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        })


def get_man_id(request):
    # will retrieve with either email or man_name
    try:
        if request.method == 'POST':
            man_info = request.POST.dict()
            man_email = man_info.get('email')
            man_name = man_info.get('man_name')
            if man_email:
                man_object = Manufacturer.objects.get(email=man_email)
                return JsonResponse({"man_id": man_object.pk, 'email': man_object.email})
            elif man_name:
                man_object = Manufacturer.objects.get(man_name=man_name)
                return JsonResponse({"man_id": man_object.pk, 'email': man_object.email})
            else:
                return JsonResponse({"error": 'No email or username was provided to get_man_id'})
        else:
            return JsonResponse({
                'error': 'HTTP method error: get_user_id endpoint expects a POST request'
            })
    except Exception as e:
        return JsonResponse({
            'error': 'Error in get_man_id in models',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        })


def get_or_create_token(request):
    sample = {
        'authee_id': 2,
        'create': "true",  # if create is passed and true, will create token if one is not found
        'is_man': 'true'
    }
    try:
        if request.method == 'POST':
            req_data = request.POST.dict()
            is_create = req_data.get('create')
            authee_id = req_data.pop('authee_id')
            get_man = req_data.pop('is_man')
            is_man = get_man.lower() == 'true'
            get_auth_model = ('User', 'Manufacturer')[is_man]
            auth = Authenticator.objects.filter(
                auth_id=authee_id, auth_model=get_auth_model)
            if auth:
                return JsonResponse({'code': 'success', 'auth': auth[0].authenticator, 'auth_id': authee_id})
            elif not auth and is_create and is_create.lower() == 'true':
                authenticator = hmac.new(
                    key=settings.SECRET_KEY.encode('utf-8'),
                    msg=os.urandom(32),
                    digestmod='sha256',
                ).hexdigest()
                new_auth = Authenticator(
                    authenticator=authenticator, auth_id=authee_id, auth_model=get_auth_model)
                new_auth.save()
                return JsonResponse({'code': 'success', 'auth': authenticator, 'auth_id': authee_id})
            else:
                return JsonResponse({'error': 'Authenticator not found and not created'})
        else:
            return JsonResponse({
                'error': 'HTTP method error: get_or_delete_token endpoint expects a POST request'
            })
    except Exception as e:
        return JsonResponse({
            'error': 'Error in get_or_create_token in models layer',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        })
    # return JsonResponse({"auth": "1233"})


# def change_user_password(request):
#     sample = {
#         "user_id": 3,  # the users id that we can use to filter objects by
#         "new_password": "newPassword!"
#     }
#     change_password_helper(User, request)
#     # get by PK
#     # call helper
#     # user.password = make_password(
#     #     new_values['password'], salt='f1nd1ngn3m0', hasher='default')
#     # user.save()


# def change_man_password(request):
#     sample = {
#         "man_id": 3,  # the users id that we can use to filter objects by
#         "new_password": "newPassword!"
#     }
#     change_password_helper(Manu, request)
#     # get man by pk
#     # call helper
#     # return


def change_password(request):
    sample = {
        "user_id/man_id": 3,  # the users id that we can use to filter objects by
        "new_password": "newPassword!"
    }
    try:
        if request.method == 'POST':
            req_data = request.POST.dict()
            get_user_id = req_data.get('user_id')
            get_man_id = req_data.get('man_id')
            new_password = req_data.pop('new_password')
            ret_string = 'changed password for '
            change_object = None
            if get_user_id:
                change_object = User.objects.get(user_id=get_user_id)
                ret_string += change_object.first_name + " " + change_object.last_name
            elif get_man_id:
                change_object = Manufacturer.objects.get(man_id=get_man_id)
                ret_string += change_object.man_name
            else:
                return JsonResponse({"error": "No user_id or man_id was found in change_password request"})
            change_object.password = make_password(
                new_password, salt='f1nd1ngn3m0', hasher='default')
            change_object.save()
            return JsonResponse({'code': "success", 'message': ret_string})
        else:
            return JsonResponse({
                'error': 'HTTP method error: get_user_id endpoint expects a POST request'
            })
    except Exception as e:
        return JsonResponse({
            'error': 'Error in get_user_id in models',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        })
