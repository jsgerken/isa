from django.http import JsonResponse, HttpResponseRedirect
import urllib.request
import urllib.parse
import json
from django.views.decorators.csrf import csrf_exempt


def get_top_viewed(request):
    req = urllib.request.Request('http://models:8000/api/v1/products/')
    products_json = urllib.request.urlopen(req).read().decode('utf-8')
    products_dict = json.loads(products_json)
    products = products_dict['allProducts']
    products.sort(key=lambda x: x['views'], reverse=True)
    return JsonResponse({'products': products})


def test(request):
    req = urllib.request.Request('http://models:8000/api/v1/manufacturers/1')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)


def newly_added(request):
    req = urllib.request.Request('http://models:8000/api/v1/products/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp_array = json.loads(resp_json)['allProducts']
    resp_sorted = sorted(resp_array, key=lambda i: i['datetime_created'])
    return JsonResponse({"newlyAddedSorted": resp_sorted})


def product_details(request, id):
    req_product = urllib.request.Request(
        'http://models:8000/api/v1/products/' + str(id))
    resp_product = json.loads(urllib.request.urlopen(
        req_product).read().decode('utf-8'))
    if 'error' in resp_product:
        return JsonResponse(resp_product);
    req_man = urllib.request.Request(
        'http://models:8000/api/v1/manufacturers/' + str(resp_product["man_id"]))
    resp_man = json.loads(urllib.request.urlopen(
        req_man).read().decode('utf-8'))
    resp_product['description'] = resp_product['description'].split('|')
    return JsonResponse({"resp_product": resp_product, "resp_man": resp_man})


def sort_products(request, attribute):
    req = urllib.request.Request('http://models:8000/api/v1/products/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp_array = json.loads(resp_json)['allProducts']
    resp_sorted = sorted(resp_array, key=lambda i: i[attribute], reverse=True)
    return JsonResponse({"sorted": resp_sorted})


def get_man_from_product(request, product_id):
    req_product = urllib.request.Request(
        'http://models:8000/api/v1/products/' + str(product_id))
    resp_product = json.loads(urllib.request.urlopen(
        req_product).read().decode('utf-8'))
    req_man = urllib.request.Request(
        'http://models:8000/api/v1/manufacturers/' + str(resp_product["man_id"]))
    resp_man = json.loads(urllib.request.urlopen(
        req_man).read().decode('utf-8'))
    return JsonResponse(resp_man)

@csrf_exempt
def create_account(request): 
# I wanted to do some redirection with the POST so that there was less code duplication
# but HTTP does not like redirection of POST so I just grab data, encoded, and send
    try:
        if request.method == 'POST':
            req_data = request.POST.dict()
            data = urllib.parse.urlencode(req_data).encode()
            req =  urllib.request.Request("http://models:8000/api/v1/users/create/", data=data)
            resp_json = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
            return JsonResponse(resp_json)
        else:
            return JsonResponse({
                'error': 'HTTP method error: User endpoint expects a POST request'
            })
    except Exception as e:
        return JsonResponse({
            'error': 'Double check param data for accepted fields and uniqueness. API currently accepts: email, username, password, phone_number, first_name, last_name',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        })

def logout(requst): 
    return; 

def login(request): 
    return; 

def create_new_listing(request): 
    return; 