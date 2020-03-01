# importing all models instead so we dont have to list them individually
from app.models import *
from django.http import JsonResponse, HttpResponse
# from django.core.exceptions import DoesNotExist


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
        manufacturers_list = Manufacturer.objects.filter(man_id=id)
        response = []
        for manufacturer in manufacturers_list:
            man_object = {}
            man_object['man_id'] = manufacturer.man_id
            man_object['man_name'] = manufacturer.man_name
            man_object['web_url'] = manufacturer.web_url
            man_object['phone_num'] = manufacturer.phone_num
            response.append(man_object)
        return JsonResponse(response, safe=False)
    elif request.method == 'POST':
        manufacturers_list = Manufacturer.objects.filter(man_id=id)
        updated_man = {}
        for manufacturer in manufacturers_list:
            manufacturer.man_name = request.POST.get('man_name', 'Error')
            manufacturer.web_url = request.POST.get('web_url', 'Error')
            manufacturer.phone_num = request.POST.get('phone_num', 'Error')
            manufacturer.save()
            updated_man = {
                'man_name': manufacturer.man_name,
                'web_url': manufacturer.web_url,
                'phone_num': manufacturer.phone_num,
            }
        return JsonResponse(updated_man)
    else:
        return HttpResponse(status=405)


def delete_manufacturer(request, id):
    if request.method == 'GET':
        manufacturers_list = Manufacturer.objects.filter(man_id=id)
        man_object = {}
        for manufacturer in manufacturers_list:
            man_object['man_id'] = manufacturer.man_id
            man_object['man_name'] = manufacturer.man_name
            man_object['web_url'] = manufacturer.web_url
            man_object['phone_num'] = manufacturer.phone_num
        Manufacturer.objects.filter(man_id=id).delete()
        return JsonResponse(man_object)
    else:
        return HttpResponse(status=405)


def create_manufacturer(request):
    if request.method == 'POST':
        manufacturer = Manufacturer()
        manufacturer.man_name = request.POST.get('man_name', 'Error')
        manufacturer.web_url = request.POST.get('web_url', 'Error')
        manufacturer.phone_num = request.POST.get('phone_num', 'Error')
        manufacturer.save()
        created_man = {
            'man_name': manufacturer.man_name,
            'web_url': manufacturer.web_url,
            'phone_num': manufacturer.phone_num,
        }
        return JsonResponse(created_man)
    else:
        return HttpResponse(status=405)


# ---- ENDPOINTS FOR USER MODEL BELOW --------
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
        }
        )

# ----stopped using but can be helpful later-----
# helper method for Jsonresponse builder for Users
# def build_json_user(users_list):
#     response = []
#     for user in users_list:
#         user_object = {}
#         user_object["user_id"] = user.user_id
#         user_object["email"] = user.email
#         user_object["username"] = user.username
#         user_object["phone_number"] = user.phone_number
#         user_object["first_name"] = user.first_name
#         user_object["last_name"] = user.last_name
#         user_object["is_deleted"] = user.is_deleted
#         response.append(user_object)
#     return JsonResponse(response, safe=False)

# need to catch saving errors for not correct parameters
