from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def Products(request):
    html = "<html><body>It is now %s.</body></html>"
    return HttpResponse(html)