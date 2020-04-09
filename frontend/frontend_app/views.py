from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
import urllib.request
import urllib.parse
import json
from .forms import CreateListing, CreateManufacturer, CreateUser, Login, Profile


def home(request):
    req = urllib.request.Request('http://services:8000/api/v1/top/')
    top_json = urllib.request.urlopen(req).read().decode('utf-8')
    top_dict = json.loads(top_json)
    req = urllib.request.Request('http://services:8000/api/v1/newly-added/')
    new_json = urllib.request.urlopen(req).read().decode('utf-8')
    new_dict = json.loads(new_json)
    top_dict['newlyAddedGrouped'] = group(new_dict['newlyAddedSorted'], 4)
    return render(request, 'home.html', top_dict)


def group(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def product_details(request, id):
    req = urllib.request.Request(
        'http://services:8000/api/v1/product-details/' + str(id))
    resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    return render(request, 'frontend_app/product_details.html', resp)


def user_profile(request):
    id = request.get_signed_cookie('user_id')
    if (request.method == 'POST'):
        if form.is_valid():
            cleanform = form.cleaned_data
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request('http://services:8000/api/v1/users/'+ str(id), data=data)
            return JsonResponse(resp)
            return render(request, 'user_profile.html', resp)
    else:
        form = Profile()
        req = urllib.request.Request(
            'http://services:8000/api/v1/users/' + str(id))
        resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    #return JsonResponse(resp)
    return render(request, 'user_profile.html', resp)

def edit_user(request):
    if (request.method == 'POST'):
        if form.is_valid():
            cleanform = form.cleaned_data
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request('http://services:8000/api/v1/users/'+ str(id), data=data)
            return JsonResponse({'eatass': 'ducks'})
            # return render(request, 'user_profile.html', resp)
            return HttpResponseRedirect('/users/'+ str(id))
    else:
        form = Profile()
        req = urllib.request.Request(
            'http://services:8000/api/v1/users/' + str(id))
        resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    #return JsonResponse(resp)
    profile = Profile()
    return render(request, 'edit_user.html', {'profile':profile, 'resp':resp})


def create_listing(request):
    auth = request.get_signed_cookie('auth')
    is_man = request.get_signed_cookie('is_man')
    if not auth or not is_man:
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        form = CreateListing(request.POST)
        if form.is_valid():
            cleanform = form.cleaned_data
            #Next few lines are used to for testing to see what has been added to the db
            # req = urllib.request.Request('http://services:8000/api/v1/newly-added/')
            # new_json = urllib.request.urlopen(req).read().decode('utf-8')
            # new_dict = json.loads(new_json)
            cleanform.update({"man_id": request.get_signed_cookie('man_id')})
            #return JsonResponse(cleanform)
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request('http://services:8000/api/v1/create-new-listing', data=data)
            new_json = urllib.request.urlopen(req).read().decode('utf-8')
            new_dict = json.loads(new_json)
            #return JsonResponse(new_dict)
            return HttpResponseRedirect('product-details/'+str(new_dict['product_id']))#product_details(request ,new_dict['product_id'])
    else:
        form = CreateListing()
    return render(request, 'create_listing.html', {'form': form})


def create_man(request):
    if request.method == 'POST':
        form = CreateManufacturer(request.POST)
        if form.is_valid():
            cleanform = form.cleaned_data
            cleanform.update( {'is_man' : "true"} )
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request('http://services:8000/api/v1/create-account', data=data)
            new_json = urllib.request.urlopen(req).read().decode('utf-8')
            new_dict = json.loads(new_json)
            return HttpResponseRedirect('/home')
    else:
        form = CreateManufacturer()
    return render(request, 'create_man.html', {'form': form})


def create_user(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            cleanform = form.cleaned_data
            cleanform.update( {'is_man' : "false"} )
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request('http://services:8000/api/v1/create-account', data=data)
            new_json = urllib.request.urlopen(req).read().decode('utf-8')
            new_dict = json.loads(new_json)
            return HttpResponseRedirect('/home')
    else:
        form = CreateUser()
    return render(request, 'create_user.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            cleanform = form.cleaned_data
            if cleanform["is_man"]:
                cleanform.update({"man_name": cleanform.pop("username")})
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request('http://services:8000/api/v1/login', data=data)
            new_json = urllib.request.urlopen(req).read().decode('utf-8')
            new_dict = json.loads(new_json)
            try:
                if not new_dict["code"] == 'success':
                    return HttpResponseRedirect('/')
            except Exception as e:
                return HttpResponseRedirect('/')
            authenticator = new_dict["auth"] 
            response = HttpResponseRedirect('/home')
            #return JsonResponse(new_dict)
            response.set_signed_cookie("auth", authenticator)
            response.set_signed_cookie("is_man", cleanform["is_man"])
            if (cleanform["is_man"]):
                response.set_signed_cookie("man_id", new_dict["auth_id"])
            return response
    else:
        form = Login()
    return render(request, 'login.html', {'form': form})

# def profile(request):
#     if request.method == 'GET':
#         req = urllib.request.Request(
#             'http://services:8000/api/v1/product-details/' + str(id))
#         resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
#         return render(request, 'frontend_app/product_details.html', resp)