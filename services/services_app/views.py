from django.http import JsonResponse, HttpResponseRedirect
import urllib.request
import urllib.parse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from kafka import KafkaProducer
from elasticsearch import Elasticsearch


def fetch(url):
    try:
        req = urllib.request.Request(url)
        return json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    except Exception as e:
        return {
            'error': 'Failed to fetch from ' + url,
            'errReason': 'Message: ' + str(e)
        }


def es_index_fixtures(request):
    # del_req = urllib.request.Request('http://es:9200/*', method='DELETE')
    try:
        es = Elasticsearch(['es'])
        es.indices.delete(index='listing_index')
        prods = fetch('http://models:8000/api/v1/products/')
        all_prods = prods['allProducts']
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        for product in all_prods:
            producer.send('new-listings-topic',
                          json.dumps(product).encode('utf-8'))
        producer.flush()
        producer.close()
        return JsonResponse({'status': 'good'})
    except:
        return JsonResponse({'status': 'bad'})
    # return JsonResponse(json.loads(urllib.request.urlopen(del_req).read().decode('utf-8')))


def get_all_es(request):
    es = Elasticsearch(['es'])
    es_results = es.search(index='listing_index', body={'query': {
        'match_all': {}
    },  'size': 1000})
    results = []
    resp = {
        'results': results
    }
    return JsonResponse(es_results)


@csrf_exempt
def search(request):
    es = Elasticsearch(['es'])
    data = request.POST.dict()
    query = data['query']
    type = data['type']
    if type == 'Most Popular':
        es_results = es.search(
            index='listing_index',
            body={
                'query': {
                    'function_score': {
                        'query': {
                            'query_string': {
                                'query': query + '*'
                            }
                        },
                        'field_value_factor': {
                            'field': 'views',
                            'modifier': 'log1p',
                            'missing': 0.1
                        }
                    }
                }
            }
        )
    else:
        es_results = es.search(index='listing_index', body={
            'query': {'query_string': {'query': query + '*'}}})
    es_results['hits']['hits'].sort(key=lambda x: x['_score'], reverse=True)
    results = []
    for result in es_results['hits']['hits']:
        results.append(result['_source'])
    resp = {
        'results': results
    }
    return JsonResponse(resp)


def get_top_viewed(request):
    es = Elasticsearch(['es'])
    es_results = es.search(index='listing_index', body={"size": 10, "query": {"function_score": {"query": {
                           "match_all": {}}, "field_value_factor": {"field": "views", "modifier": "log1p", "missing": 0.1}}}})
    products_only = []
    # used to remove extra metadata that es returns
    for product in es_results['hits']['hits']:
        products_only.append(product['_source'])
    return JsonResponse({'products': products_only})


def test(request):
    req = urllib.request.Request('http://models:8000/api/v1/manufacturers/1')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)


def newly_added(request):
    req = urllib.request.Request('http://models:8000/api/v1/products/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp_array = json.loads(resp_json)['allProducts']
    resp_sorted = sorted(
        resp_array, key=lambda i: i['datetime_created'], reverse=True)
    return JsonResponse({"newlyAddedSorted": resp_sorted})


@csrf_exempt
def product_details(request, id):
    req_product = urllib.request.Request(
        'http://models:8000/api/v1/products/' + str(id))
    resp_product = json.loads(urllib.request.urlopen(
        req_product).read().decode('utf-8'))
    if 'error' in resp_product:
        return JsonResponse(resp_product)
    req_man = urllib.request.Request(
        'http://models:8000/api/v1/manufacturers/' + str(resp_product["man_id"]))
    resp_man = json.loads(urllib.request.urlopen(
        req_man).read().decode('utf-8'))
    resp_product['description'] = resp_product['description'].split('|')
    # add that this product was clicked to Kafka Q if it was by a user and not manufacturer
    try:
        if request.method == 'POST':
            req_data = request.POST.dict()
            get_user_id = req_data.get('user_id', False)
            if not get_user_id:
                raise Exception(
                    "Cannot add because user_id was not found in post data")
                # if here there was a user_id in data to add to Q
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            message = {
                'user_id': int(get_user_id),
                'product_id': resp_product['product_id']
            }
            producer.send('new-logs-topic',
                          json.dumps(message).encode('utf-8'))
            producer.flush()
            producer.close()

    except Exception as e:
        print(
            'error: In experience layer. Could not add to view to Kafka Q \n' +
            'errReason:  DEV_MODE_MESSAGE: ' + str(e)
        )
    return JsonResponse({"resp_product": resp_product, "resp_man": resp_man})


@csrf_exempt
def user_profile(request, id):
    req_data = request.POST.dict()
    data = urllib.parse.urlencode(req_data).encode()
    req_user = urllib.request.Request(
        'http://models:8000/api/v1/users/' + str(id), data=data)
    resp_user = json.loads(urllib.request.urlopen(
        req_user).read().decode('utf-8'))
    if 'error' in resp_user:
        return JsonResponse(resp_user)
    return JsonResponse({"resp_user": resp_user})


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


def authAndListingHelper(request, action):
    try:
        if request.method == 'POST':
            url = ''
            req_data = request.POST.dict()
            action = action.lower()
            if action == "create":
                is_man = req_data.pop("is_man")
                url = ("http://models:8000/api/v1/users/create/",
                       "http://models:8000/api/v1/manufacturers/create/")[is_man.lower() == 'true']
            elif action == 'login':
                url = 'http://models:8000/account/login'
            elif action == 'logout':
                url = 'http://models:8000/account/logout'
            elif action == 'listing':
                url = 'http://models:8000/api/v1/products/create/'
                producer = KafkaProducer(bootstrap_servers='kafka:9092')
            if url:
                resp = post(req_data, url)
                if action == 'listing':
                    producer.send('new-listings-topic',
                                  json.dumps(resp).encode('utf-8'))
                    # producer.close(timeout=1000)
                    producer.flush()
                    producer.close()
                return resp
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

        # when you create an account ; we also call log in to give them an authenticator


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
# sample = {
#   'auth' : token,
#   'is_man':'true'
# }
@csrf_exempt
def logout(request):
    return JsonResponse(authAndListingHelper(request, 'logout'))

# a new listing is just a new product


@csrf_exempt
def create_new_listing(request):
    return JsonResponse(authAndListingHelper(request, 'listing'))


# def sendEmail(request):
#     # try:
#     #     send_mail("Im in there",
#     #     "Our own smtp server for a class 😎. I'm cracked out of my mind.",
#     #     "Oldn'tEgg@no-reply.com",
#     #     ['jacoboscholarships@gmail.com'],
#     #     fail_silently=False)
#     return JsonResponse({"we": "done"})
#     # except Exception as e:
#     #     return JsonResponse({"not cracked": str(e)})


@csrf_exempt
def reset_password(request):
    possible = {
        "is_man": "true",
        "username": "guy14",
        "email": "email@email.com",
        "man_name": "nvidia14",
        "url_pattern": "/password-reset-confirm/"
    }
    try:
        if request.method == 'POST':
            req_data = request.POST.dict()
            get_man = req_data.pop("is_man")
            is_man = get_man.lower() == 'true'
            req_query = {}
            req_resp = {}
            if is_man:
                # req_query['man_name'] = req_data.get('man_name')
                get_man_name = req_data.get('man_name')
                get_email = req_data.get('email')
                if get_man_name:
                    req_query['man_name'] = get_man_name
                elif get_email:
                    req_query['email'] = get_email
                else:
                    return JsonResponse({'error': 'In services layer – reset password – No man_name or email'})
                req_resp = convert_and_call(
                    req_query, 'http://models:8000/api/v1/manufacturers/get-man-id/')
            elif not req_data.get('username') and not req_data.get('email'):
                return JsonResponse({'error': "Service Layer Error. No username or email was provided"})
            else:
                get_username = req_data.get('username')
                if get_username:
                    req_query['username'] = get_username
                else:
                    req_query['email'] = req_data.get('email')
                req_resp = convert_and_call(
                    req_query, 'http://models:8000/api/v1/users/get-user-id/')
                if 'error' in req_resp:
                    return JsonResponse(req_resp)
            get_id = (req_resp.get('user_id'), req_resp.get('man_id'))[is_man]
            token_resp = convert_and_call(
                {'authee_id': get_id, "create": "true", 'is_man': is_man}, 'http://models:8000/account/get-create-token/')
            if 'error' in token_resp:
                return JsonResponse(token_resp)
            url_replace = req_data['url_pattern'].replace(
                "__uid64__", urlsafe_base64_encode(force_bytes(get_id)), 1)
            url_replace = url_replace.replace(
                "__token__", token_resp['auth'], 1)
            email_data = {'emailTo': req_resp['email'],
                          "emailURL": url_replace, }
            # return JsonResponse(email_data)
            return JsonResponse(send_email(request, email_data))

        else:
            return JsonResponse({'error': 'HTTP method error: endpoint expects a POST request'})
    except Exception as e:
        return JsonResponse({
            'error': 'In experience layer - reset-password. Double check param data for accepted fields and uniqueness and is_man is in data',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        })

        # def send_email(request, authee_id, token_resp, url_pattern):


def send_email(request, data):
    try:
        subject = "Oldn't Egg – Reset Password Link"
        html_message = render_to_string(
            'reset_password_mail_template.html', {'emailURL': data['emailURL']})
        plain_message = strip_tags(html_message)
        from_email = "Oldn'tEgg@no-reply.com"
        # to = 'jacoboscholarships@gmail.com'
        to = data['emailTo']
        send_mail(subject, plain_message, from_email,
                  [to], fail_silently=False, html_message=html_message)
        return {"code": "success", "message": "email sent successfully", 'emailTo': to}
    # return render(request, 'reset_password_mail_template.html', {"url_email_pattern": url_email_pattern})
    except Exception as e:
        return {
            'error': 'In experience layer. Double check param data for accepted fields and uniqueness and is_man is in data',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        }


@csrf_exempt
def reset_password_confirm(request):
    return JsonResponse(helperConfirmChangePassword(request, False))


@csrf_exempt
def change_password(request):
    return JsonResponse(helperConfirmChangePassword(request, True))


# will check password and return if valid or not
def helperConfirmChangePassword(request, is_change_password):
    sample = {
        'uid64': 'MTU=',  # 15
        'token': 33432,
        'is_man': 'true',
        'new_password': 'newPass!'  # if is_change_password is true
    }
    try:
        if request.method == 'POST':
            req_data = request.POST.dict()
            get_is_man = req_data.pop('is_man')
            get_uid64 = req_data.pop('uid64')
            get_token = req_data.pop('token')
            is_man = get_is_man.lower() == 'true'
            decoded_id = urlsafe_base64_decode(get_uid64)
            check_link_data = {'authee_id': decoded_id,
                               'is_man': is_man, 'create': 'false'}
            req_resp = convert_and_call(
                check_link_data, 'http://models:8000/account/get-create-token/')
            if 'error' in req_resp:
                return req_resp
            if get_token != req_resp['auth']:
                return {'error': 'invalid token'}
            if not is_change_password:
                return {'code': 'success', 'message': 'token was verified with id. All good!'}
            # if it got to this point, token is valid and change password was requested
            # lets delete the token first
            delete_token_data = {"auth": get_token, 'is_man': is_man}
            req_resp = convert_and_call(
                delete_token_data, "http://models:8000/account/logout")
            if 'error' in req_resp:
                return {"error": "failed to delete token in reset password : service layer", **req_resp}
            # now lets change the password
            get_new_password = req_data.pop('new_password')
            change_password_data = {}
            if is_man:
                change_password_data['man_id'] = decoded_id
            else:
                change_password_data['user_id'] = decoded_id
            change_password_data['new_password'] = get_new_password
            req_resp = convert_and_call(
                change_password_data, 'http://models:8000/account/change-password/')
            return req_resp

        else:
            return {'error': 'HTTP method error: endpoint expects a POST request'}
    except Exception as e:
        return {
            'error': 'In experience layer. Double check param data for accepted fields and uniqueness and is_man is in data',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        }


def convert_and_call(data, url):
    try:
        data = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(url, data=data)
        resp_json = json.loads(
            urllib.request.urlopen(req).read().decode('utf-8'))
        return resp_json
    except Exception as e:
        return {
            'error': 'In experience layer. Failed in convert_and_call',
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        }


def post(data, url):
    try:
        data = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(url, data=data)
        return json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    except Exception as e:
        return {
            'error': 'Failed to post to ' + url,
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        }
