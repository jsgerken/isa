from django.http import JsonResponse, HttpResponseRedirect
import urllib.request
import urllib.parse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


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

# I wanted to do some redirection with the POST so that there was less code duplication
# but HTTP does not like redirection of POST so I just grab data, encoded, and send
# action can equal: "create", "login"
def authAndListingHelper(request, action):
    try:
        if request.method == 'POST':
            url = ""
            req_data = request.POST.dict()
            # data = urllib.parse.urlencode(req_data).encode()
            action = action.lower()
            if action == "create":        
                is_man = req_data.pop("is_man")
                # if is_man is in the data, use it to decide between man and users. else, default to false
                url = ("http://models:8000/api/v1/users/create/", "http://models:8000/api/v1/manufacturers/create/")[is_man.lower() == 'true']
            elif action == 'login':
                url = "http://models:8000/account/login"
            elif action == 'logout':
                url = "http://models:8000/account/logout"
            elif action == 'listing':
                url = "http://models:8000/api/v1/products/create/"
            # make sure that one of the above actions changed the url
            if url: 
                data = urllib.parse.urlencode(req_data).encode()
                req =  urllib.request.Request(url, data=data)
                resp_json = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
                JsonResponse(resp_json)
                return resp_json 
            else: 
                # return JsonResponse({"error": "Incorrect action. Action must be: create, login, logout, listing"})
                return {"error": "Incorrect action. Action must be: create, login, logout, listing"}
        else:
            return {'error': 'HTTP method error: endpoint expects a POST request'}

    except Exception as e:
        return {
            'error': 'In experience layer. Double check param data for accepted fields and uniqueness and is_man is in data',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        }

#when you create an account ; we also call log in to give them an authenticator 
@csrf_exempt
def create_account(request): 
    resp_json_create = authAndListingHelper(request, 'create')
    if ('error' in resp_json_create):
        return JsonResponse(resp_json_create)
    resp_json_login = authAndListingHelper(request, 'login')
    if('error' in resp_json_login):
        return JsonResponse(resp_json_login)
    return JsonResponse({**resp_json_create, **resp_json_login})
        

# account/login
@csrf_exempt
def login(request): 
    return JsonResponse(authAndListingHelper(request, 'login'))

# account/logout
@csrf_exempt
def logout(request): 
    return JsonResponse(authAndListingHelper(request, 'logout'))

# a new listing is just a new product 
@csrf_exempt
def create_new_listing(request): 
    return JsonResponse(authAndListingHelper(request, 'listing'))

def sendEmail(request):
    # try:
    #     send_mail("Im in there",
    #     "Our own smtp server for a class 😎. I'm cracked out of my mind.",
    #     "Oldn'tEgg@no-reply.com",
    #     ['dm8ca@virginia.edu', "aar2dk@virginia.edu"],
    #     fail_silently=False)
        return JsonResponse({"we": "in there"})
    # except Exception as e: 
    #     return JsonResponse({"not cracked": str(e)}) 
