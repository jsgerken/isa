from app.models import Manufacturer
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
