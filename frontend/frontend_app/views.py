from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
import urllib.request
import urllib.parse
import json
from .forms import CreateListing, CreateManufacturer, CreateUser, Login, Profile, ForgotPassword, ResetPassword
# from .forms import ListingForm
from django.urls import reverse
import re


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


def user_profile(request, id):
    if (request.method == 'POST'):
        if form.is_valid():
            cleanform = form.cleaned_data
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request(
                'http://services:8000/api/v1/users/' + str(id), data=data)
            return JsonResponse(resp)
            return render(request, 'user_profile.html', resp)
    else:
        form = Profile()
        req = urllib.request.Request(
            'http://services:8000/api/v1/users/' + str(id))
        resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    # return JsonResponse(resp)
    return render(request, 'user_profile.html', resp)


def edit_user(request):
    if (request.method == 'POST'):
        if form.is_valid():
            cleanform = form.cleaned_data
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request(
                'http://services:8000/api/v1/users/' + str(id), data=data)
            return JsonResponse({'eatass': 'ducks'})
            # return render(request, 'user_profile.html', resp)
            return HttpResponseRedirect('/users/' + str(id))
    else:
        form = Profile()
        req = urllib.request.Request(
            'http://services:8000/api/v1/users/' + str(id))
        resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    # return JsonResponse(resp)
    profile = Profile()
    return render(request, 'edit_user.html', {'profile': profile, 'resp': resp})


def create_listing(request):
    auth = request.get_signed_cookie('auth')
    is_man = request.get_signed_cookie('is_man')
    if not auth or not is_man:
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        form = CreateListing(request.POST)
        if form.is_valid():
            cleanform = form.cleaned_data
            # Next few lines are used to for testing to see what has been added to the db
            # req = urllib.request.Request('http://services:8000/api/v1/newly-added/')
            # new_json = urllib.request.urlopen(req).read().decode('utf-8')
            # new_dict = json.loads(new_json)
            cleanform.update({"man_id": request.get_signed_cookie('man_id')})
            # return JsonResponse(cleanform)
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request(
                'http://services:8000/api/v1/create-new-listing', data=data)
            new_json = urllib.request.urlopen(req).read().decode('utf-8')
            new_dict = json.loads(new_json)
            # return JsonResponse(new_dict)
            # product_details(request ,new_dict['product_id'])
            return HttpResponseRedirect('product-details/'+str(new_dict['product_id']))
    else:
        form = CreateListing()
    return render(request, 'create_listing.html', {'form': form})


def create_man(request):
    if request.method == 'POST':
        form = CreateManufacturer(request.POST)
        if form.is_valid():
            cleanform = form.cleaned_data
            cleanform.update({'is_man': "true"})
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request(
                'http://services:8000/api/v1/create-account', data=data)
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
            cleanform.update({'is_man': "false"})
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request(
                'http://services:8000/api/v1/create-account', data=data)
            new_json = urllib.request.urlopen(req).read().decode('utf-8')
            new_dict = json.loads(new_json)
            return HttpResponseRedirect('/home')
    else:
        form = CreateUser()
    return render(request, 'create_user.html', {'form': form})


def forgot_password(request):
    # req_resp = {'emailTo': "jp3dh@virginia.edu"}
    # regex_test = r'(?!^).(?=[^@]+@)'
    # email_asterisk = re.sub(regex_test, '*', req_resp['emailTo'])
    # # if length before @ is less than or equal to 3
    # return render(request, 'password_reset_done.html', {'emailTo': email_asterisk})
    if request.method == 'POST':
        form = ForgotPassword(request.POST)
        if form.is_valid():
            cleanform = form.cleaned_data
            # return JsonResponse(cleanform)
            get_reset_info = cleanform['reset_info']
            if '@' in cleanform['reset_info']:
                cleanform['email'] = get_reset_info
            elif cleanform['is_man']:
                cleanform['man_name'] = get_reset_info
            else:
                cleanform['username'] = get_reset_info
            # reverse the link with password arguments to be replaced in the service layer : __uid64__ and __token__
            cleanform['url_pattern'] = request.scheme + "://" + request.META['HTTP_HOST'] + \
                reverse('password_reset_confirm', args=[
                        '__uid64__', '__token__', str(cleanform['is_man']).lower()])
            req_resp = convert_and_call(
                cleanform, 'http://services:8000/api/v1/reset-password/')
            # check error and redirect to some done and check email template
            if 'error' in req_resp:
                error_string = "There seems to be a problem with this email/username. Please double check spelling."
                return render(request, 'forgot_password.html', {'form': form, 'error': error_string})
            # lets users know that email was sent succesfully
            regex_asterisk = r'(?!^).(?=[^@]+@)'
            email_asterisk = re.sub(regex_asterisk, '*', req_resp['emailTo'])
            return render(request, 'password_reset_done.html', {'emailTo': email_asterisk})
        # else:
        #     return JsonResponse({'errors': form.errors})
    else:
        form = ForgotPassword()
    return render(request, 'forgot_password.html', {'form': form})


def password_reset_confirm(request, uidb64, token, is_man):
    check_link_data = {"uid64": uidb64, "token": token, "is_man": is_man}
    if request.method == 'POST':
        form = ResetPassword(request.POST)
        if form.is_valid():
            cleanform = form.cleaned_data
            check_link_data['new_password'] = cleanform['new_password']
            req_resp = convert_and_call(
                check_link_data, 'http://services:8000/api/v1/change-password/')
            # check error and redirect to logged in view or log them in yourself
            if 'error' in req_resp:
                # comment swap these two lines below to display error reason
                # error_string = "Error occured while changing password: " + \
                #     req_resp['error'] + " due to: " + \
                #     req_resp['errReason'] + ' Please try again'
                error_string = "It appears an error occured while trying to change the password. Please try again."
                return render(request, 'reset_password.html', {'form': form, 'error': error_string, **check_link_data})
            # let user know that password was change succesfully
            return render(request, 'password_reset_complete.html')
            # return redirect('login')
        else:
            return render(request, 'reset_password.html', {'form': form, **check_link_data})
    else:
        # check the link and stuff here
        # check_link_data = {"uid64": uidb64, "token": token, "is_man": is_man}
        req_resp = convert_and_call(
            check_link_data, 'http://services:8000/api/v1/reset-password-confirm/')
        if 'error' in req_resp:
            form = ForgotPassword()
            error_string = "It looks like your password reset link expired or is invalid, please re-enter your email or username to receive another one."
            return render(request, 'forgot_password.html', {'form': form, "error": error_string})
        form = ResetPassword()
        return render(request, 'reset_password.html', {'form': form, **check_link_data})


def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            cleanform = form.cleaned_data
            if cleanform["is_man"]:
                cleanform.update({"man_name": cleanform.pop("username")})
            data = urllib.parse.urlencode(cleanform).encode()
            req = urllib.request.Request(
                'http://services:8000/api/v1/login', data=data)
            new_json = urllib.request.urlopen(req).read().decode('utf-8')
            new_dict = json.loads(new_json)
            try:
                if not new_dict["code"] == 'success':
                    return HttpResponseRedirect('/')
            except Exception as e:
                return HttpResponseRedirect('/')
            authenticator = new_dict["auth"]
            response = HttpResponseRedirect('/home')
            # return JsonResponse(new_dict)
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


# def password_reset(request):
#     # url_link = reverse('password_reset_confirm', args=[45, 21234])
#     # reverse the link with password arguments to be replaced in the service layer : __uid64__ and __token__
#     dataa = {"urlLink": request.scheme + "://" + request.META['HTTP_HOST'] + reverse(
#         'password_reset_confirm', args=['__uid64__', '__token__', '__addIsManHere__'])}
#     # data = urllib.parse.urlencode(dataa).encode()
#     # req = urllib.request.Request(
#     #     "http://services:8000/api/v1/send-email", data=data)
#     # resp_json = json.loads(
#     #     urllib.request.urlopen(req).read().decode('utf-8'))
#     # # return JsonResponse({"path": request.path, "pathInfo": request.path_info, "schema": request.scheme, "post": request.META['HTTP_HOST']})
#     # return JsonResponse(resp_json)
#     return JsonResponse({"hi": "wip"})


# def password_reset_confirm(request, uidb64, token):
#     return


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
