from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateListing, CreateManufacturer, CreateUser, Login, Profile, ForgotPassword, ResetPassword
from django import forms
import urllib.request
import urllib.parse
import json
import re
import base64

def home(request):
    if request.get_signed_cookie('auth', -1) == -1:
        return HttpResponseRedirect('/')
    top_dict = fetch('http://services:8000/api/v1/top/')
    new_dict = fetch('http://services:8000/api/v1/newly-added/')
    top_dict['newlyAddedGrouped'] = group(new_dict['newlyAddedSorted'], 4)
    if request.get_signed_cookie('is_man', 'False') == 'True':
        top_dict['is_man'] = True
    return render(request, 'home.html', top_dict)


@csrf_exempt
def search(request):
    form_data = request.POST.dict()
    resp = post(form_data, 'http://services:8000/api/v1/search/')
    if request.get_signed_cookie('is_man', 'False') == 'True':
        resp['is_man'] = True
    return render(request, 'search.html', resp)


def product_details(request, id):
    if request.get_signed_cookie('auth', -1) == -1:
        return HttpResponseRedirect('/')
    post_data = {}
    get_user_id = request.get_signed_cookie('user_id', False)
    if get_user_id:
        post_data = {'user_id': get_user_id}
    product_dict = post(post_data, 'http://services:8000/api/v1/product-details/' + str(id))
    if request.get_signed_cookie('is_man', 'False') == 'True':
        product_dict['is_man'] = True
    product_dict['rec_groups'] = group(product_dict['rec_prods'], 4)
    # return JsonResponse(product_dict)
    return render(request, 'frontend_app/product_details.html', product_dict)


def user_profile(request):
    user_id = request.get_signed_cookie('user_id', -1)
    if user_id == -1:
        return HttpResponseRedirect('/')
    resp = fetch('http://services:8000/api/v1/users/' + str(user_id))
    return render(request, 'user_profile.html', resp)


def edit_user(request):
    user_id = request.get_signed_cookie('user_id', -1)

    if user_id == -1:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = Profile(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect('/users/edit')
        form_data = form.cleaned_data
        post(form_data, 'http://services:8000/api/v1/users/' + str(user_id))
        return HttpResponseRedirect('/users')
    else:
        profile = Profile()
        return render(request, 'edit_user.html', {'profile': profile})


def create_listing(request):
    resp = None
    try:
        if request.method == 'POST':
            form = CreateListing(request.POST, request.FILES)
            if form.is_valid():
                form_data = form.cleaned_data
                # TO DO: check for 2.5MB size and then throw form error if it is
                get_product_img = request.FILES['product_img'].file.getvalue()
                # return JsonResponse({"no error": str(get_product_img), 'valid': form.is_valid()})
                form_data['man_id'] = request.get_signed_cookie('man_id')
                form_data['product_img'] = base64.b64encode(get_product_img)
                resp = post(
                    form_data, 'http://services:8000/api/v1/create-new-listing')
                if 'error' in resp:
                    # return JsonResponse(resp)
                    # error checking for Will to implement
                    form.add_error(None, forms.ValidationError(
                        "Failed to submit listing. Please try again."))
                    return render(request, 'create_listing.html', {'form': form})
                else:
                    return HttpResponseRedirect('/product-details/' + str(resp['product_id']))
            else:
                return render(request, 'create_listing.html', {'form': form})
        else:
            if request.get_signed_cookie('is_man', 'False') == 'False':
                return HttpResponseRedirect('/')
            form = CreateListing()
            return render(request, 'create_listing.html', {'form': form})
    except Exception as e:
        return JsonResponse({
            'error': "error in create Listing " + str(e),
            'errorJSON': resp
        })


def create_man(request):
    if request.method == 'POST':
        form = CreateManufacturer(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect('/create-manufacturer')
        form_data = form.cleaned_data
        form_data['is_man'] = 'true'
        post(form_data, 'http://services:8000/api/v1/create-account')
        return HttpResponseRedirect('/')
    else:
        form = CreateManufacturer()
    return render(request, 'create_man.html', {'form': form})


def create_user(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect('/create-user')
        form_data = form.cleaned_data
        form_data['is_man'] = 'false'
        post(form_data, 'http://services:8000/api/v1/create-account')
        return HttpResponseRedirect('/')
    else:
        form = CreateUser()
    return render(request, 'create_user.html', {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPassword(request.POST)
        if form.is_valid():
            cleanform = form.cleaned_data
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
            req_resp = post(
                cleanform, 'http://services:8000/api/v1/reset-password/')
            # check error and redirect to some done and check email template
            if 'error' in req_resp:
                error_string = "There seems to be a problem with this email/username. Please double check spelling."
                return render(request, 'forgot_password.html', {'form': form, 'error': error_string})
            else:
                # lets users know that email was sent succesfully
                regex_asterisk = r'(?!^).(?=[^@]+@)'
                email_asterisk = re.sub(
                    regex_asterisk, '*', req_resp['emailTo'])
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
            req_resp = post(
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
        req_resp = post(
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

        if not form.is_valid():
            return HttpResponseRedirect('/')

        login_data = form.cleaned_data

        if login_data['is_man']:
            login_data['man_name'] = login_data.pop('username')

        try:
            resp = post(login_data, 'http://services:8000/api/v1/login')
            if not resp['code'] == 'success':
                return render(request, 'login.html', {'form': form, 'failed': 'true'})
        except:
            return render(request, 'login.html', {'form': form, 'error': 'true'})

        response = HttpResponseRedirect('/home')
        response.set_signed_cookie('auth', resp['auth'])
        response.set_signed_cookie('is_man', login_data['is_man'])

        if login_data['is_man']:
            response.set_signed_cookie('man_id', resp['auth_id'])
        else:
            response.set_signed_cookie('user_id', resp["auth_id"])

        return response
    else:
        # fix = fetch('http://services:8000/index-fixtures/')
        form = Login()
        return render(request, 'login.html', {'form': form})


def logout(request):
    response = HttpResponseRedirect('/')
    auth = request.get_signed_cookie('auth', -1)
    is_man = request.get_signed_cookie('is_man', 'False') == 'True'

    if auth == -1:
        return response

    logout_data = {
        'auth': auth,
        'is_man': is_man
    }

    post(logout_data, 'http://services:8000/api/v1/logout')

    response.delete_cookie('man_id')
    response.delete_cookie('user_id')
    response.delete_cookie('user_id')
    response.delete_cookie('auth')
    response.delete_cookie('is_man')
    return response


def group(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def fetch(url):
    try:
        req = urllib.request.Request(url)
        return json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    except Exception as e:
        return {
            'error': 'Failed to fetch from ' + url,
            'errReason':  'Message: ' + str(e)
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
