# importing all models instead so we dont have to list them individually
from app.models import *
from django.http import JsonResponse, HttpResponse


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


# Endpoints for Users belows
def get_all_users(request):
    if request.method == 'GET':
        users_list = User.objects.all()
        return build_json_user(users_list)
    else:
        return HttpResponse(status=405)


def get_or_update_user(request, id):
    if request.method == 'GET':
        user_list = User.objects.filter(user_id=id)
        return build_json_user(user_list)
    elif request.method == 'POST':
        user_list = User.objects.filter(user_id=id)
        if not user_list:
            return HttpResponse(status=404)  # find correct response
        # only problem is some checks should be done first to make sure new values shouldn't be able to modify anything
        # also what to return should be adjusted
        new_values = request.POST.dict()
        user_list.update(**new_values)
        # updated_user = user_list.values()[0]
        # updated_user.update(new_values)
        return JsonResponse(user_list.values()[0])
    else:
        return HttpResponse(status=405)


# helper method for Jsonresponse builder for Users
def build_json_user(users_list):
    response = []
    for user in users_list:
        user_object = {}
        user_object["user_id"] = user.user_id
        user_object["email"] = user.email
        user_object["username"] = user.username
        user_object["phone_number"] = user.phone_number
        user_object["first_name"] = user.first_name
        user_object["last_name"] = user.last_name
        user_object["is_deleted"] = user.is_deleted
        response.append(user_object)
    return JsonResponse(response, safe=False)


def create_user(request):
    if request.method == 'POST':
        new_values = request.POST.dict()
        user = User(**new_values)

        # manufacturer.man_name = request.POST.get('man_name', 'Error')
        # manufacturer.web_url = request.POST.get('web_url', 'Error')
        # manufacturer.phone_num = request.POST.get('phone_num', 'Error')
        # manufacturer.save()
        # created_man = {
        #     'man_name': manufacturer.man_name,
        #     'web_url': manufacturer.web_url,
        #     'phone_num': manufacturer.phone_num,
        # }
        return JsonResponse(new_values)
    else:
        return HttpResponse(status=405)
