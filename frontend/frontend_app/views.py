from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
import urllib.request
import urllib.parse
import json
from .forms import ListingForm


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
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():

            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ListingForm()

    return render(request, 'create_listing.html', {'form': form})
