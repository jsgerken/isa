from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
import urllib.request
import urllib.parse
import json
from .forms import CreateListing, CreateManufacturer, CreateUser, Login


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


def create_listing(request):
    auth = request.COOKIES.get('auth')
    if not auth:
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        form = CreateListing(request.POST)
        if form.is_valid():
            cleanform = form.cleaned_data
            cleanform.update( {'man_id' : 3} )
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request('http://services:8000/api/v1/create-new-listing', data=data)
            new_json = urllib.request.urlopen(req).read().decode('utf-8')
            new_dict = json.loads(new_json)
            return HttpResponseRedirect('/home')
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
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request('http://services:8000/api/v1/login', data=data)
            new_json = urllib.request.urlopen(req).read().decode('utf-8')
            new_dict = json.loads(new_json)
            return JsonResponse(new_dict)
            try:
                if not new_dict["code"] == 'success':
                    return HttpResponseRedirect('/')
            except Exception as e:
                return HttpResponseRedirect('/')
            authenticator = new_dict["auth"] 
            response = HttpResponseRedirect('/home')
            response.set_cookie("auth", authenticator)
            return response
    else:
        form = Login()
    return render(request, 'login.html', {'form': form})
