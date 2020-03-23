from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from .forms import Login, CreateUser, CreateManufacturer

import urllib.request
import urllib.parse
import json
from .forms import ListingForm

#data = parse.urlencode(<your data dict>).encode()
#req = request.Request(<your url>, data=data) # this will make the method "POST"
#resp = request.urlopen(req)


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


def login(request):
    # If we received a GET request instead of a POST request
    # if request.method == 'GET':
    #     form = Login(request.GET)
    #     if form.is_valid():
    #         return HttpResponseRedirect('/login')
    # else:
    #     form = CreateUser()
    form = Login(request.GET)
    if request.method == 'GET':
        # display the login form page
        next = request.GET.get('')
        return render(request,'login.html',{'form':form})

    # Creates a new instance of our login_form and gives it our POST data
    f = Login(request.POST)

    # Check if the form instance is invalid
    if not f.is_valid():
      # Form was bad -- send them back to login page and show them an error
      return render(request,'login.html',{'form':form})

    # Sanitize username and password fields
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']
    next = f.cleaned_data.get('next')
    # Send validated information to our experience layer
    #Curr unwritten
    #resp = login_exp_api(username, password)
    #if not resp:
    #   return render('login.html', ...)
    # authenticator = resp['resp']['authenticator']

    # response = HttpResponseRedirect(next)
    # response.set_cookie("auth", authenticator)

    # return response
    return render (request, 'login.html', {'form':form})
    
def create_user(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/login')
    else:
        form = CreateUser()
    
    return render (request, 'create_user.html', {'form':form})

def create_manufacturer(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/login')
    else:
        form = CreateManufacturer()
    return render (request, 'create_manufacturer.html', {'form':form})

def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():

            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ListingForm()

    return render(request, 'create_listing.html', {'form': form})
