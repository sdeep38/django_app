from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib import messages
from customer.models import Contact, Profile, Notice
from customer.forms import NewUserForm, ProfileForm
from datetime import datetime
from django.http import Http404, JsonResponse
from django.core.files.storage import FileSystemStorage
import os
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.template.loader import get_template
import random
import csv

# Create your views here.

# @login_required(login_url='accounts/authenticate')
def home(request):
    return render(request,"home.html")

def register(request):
    if request.method == 'POST':

        # generate username & password ...
        user_name = 'user' + str(random.randint(1000,9999))
        user_key = User.objects.make_random_password(length=5)

        form = NewUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=user_name)
            user.first_name = form.cleaned_data['first_name'].capitalize()
            user.last_name = form.cleaned_data['last_name'].capitalize()
            user.email = form.cleaned_data['email']
            user.set_password(user_key)
            user.save()

            messages.success(request,'user id : {}'.format(user_name))
            messages.success(request,'password : {}'.format(user_key))
            return redirect('/app/register/register_success/')
        else:
            messages.error(request, 'Invalid Form Submission')
            return redirect('/app/register')

    form = NewUserForm()

    context = {
                'form':form,
            }
    return render(request,"register2.html", context)

def reg_success(request):
    return render(request,"signup_success.html")

def reg_user(request):          # Not real
    if request.method == 'POST':

        if id == 1:
            form = ProfileForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(username=user_name)
                user.first_name = form.cleaned_data['first_name'].capitalize()
                user.last_name = form.cleaned_data['last_name'].capitalize()
                user.email = form.cleaned_data['email']
                user.set_password(user_key)
                user.save()

            messages.success(request,'user id : {}'.format(user_name))
            messages.success(request,'password : {}'.format(user_key))
            return redirect('/app/register/register_success/')
        else:
            messages.error(request, 'Invalid Form Submission')
            return redirect('/app/register')

    form = NewUserForm()

    context = {
                'form':form,
            }
    return render(request,"register_profile.html", context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/user/changepass/')
        messages.error(request, 'Invalid Form Submission')
    else:
        form = PasswordChangeForm(request.user)

    return render(request,"cpass.html",{'form':form})

# @login_required(login_url='/authenticate')
def upload(request):
    if request.method=="POST":
        upload_file = request.FILES['myfile']
        if upload_file:
            fs = FileSystemStorage()
            fs.save(upload_file.name,upload_file)
            messages.success(request, 'File successfully uploaded')
        else:
            messages.warning(request, 'File Not Chosen')
            
    return render(request,"upload2.html")

def dashboard(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(id=request.user.id)
        notices = Notice.objects.order_by('-created_at')
        context = {
            "user" : user,
            "profile" : profile,
            "notices" : notices,
        }

        for notice in notices:
            delta = datetime.now().date() - notice.created_at.date()
            if delta.days >= 7:
                notice.new_tag = False

        return render(request,"dashboard.html",context)
    return redirect('app/login')

def classroom(request):
    return render(request,"classroom.html")

def get_item(request):
    return render(request,"search.html")

def get_users(request):
    users = Contact.objects.all()
    return render(request,"users.html",{'users':users})
    
def dologin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/user/dashboard')
        else:
            messages.error(request, 'Invalid UserID or Password')
            return redirect('/app/login')
            
    elif request.user.is_authenticated:
        return redirect('/user/dashboard')

    return render(request,"authenticate.html")

def edit(request,id):
    user = Contact.objects.get(id=id)
    return render(request,'edit.html',{'user':user})
    
def contact(request):
    if request.method=="POST":
        email = request.POST['email']
        name = request.POST['name']
        phn = request.POST['phone']
        desc = request.POST['desc']
        if email != "" or desc != "" or phn != "" or name != "":
            contact = Contact(email=email,name=name,phn=phn,desc=desc,date=datetime.today())
            contact.save()
            messages.success(request, 'Your message has been submitted')
        else:
            messages.warning(request, 'All Fields are required')
    else:
        contact = Contact()
    return render(request,"contact-us.html")

def update(request,id):
    user = Contact.objects.get(id=id)
    if request.method == "POST":
        email = request.POST['email']
        name = request.POST['name']
        phn = request.POST['phone']
        desc = request.POST['desc']
        contact = Contact(id=id,email=email,name=name,phn=phn,desc=desc,date=datetime.today())
        contact.save()
        return redirect("/")
    return render(request,'edit.html',{'user':user})

def error_404(request,exception):
    raise Http404

def fpass(request):
    return render(request,"forgot.html")

def checkout(request):
    return render(request,"checkout.html")

def profile(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(id=request.user.id)
        context = {
            "user" : user,
            "profile" : profile
        }
        return render(request,"profile.html",context)
    return redirect('app/login')

def dologout(request):
    logout(request)
    return redirect('/app/login')

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def getfees(request):
    return render(request, "fee.html")

def payfees(request):
    return HttpResponse("<h2>Fee Payment Gateway is under maintainance</h2>")

def drive(request):
    return HttpResponse("<h2>Unlimited storage for your files</h2>")

def addmail(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        email = request.POST['email']
        user.email = email
        user.save()
        messages.success(request, 'Your Email has been successfully updated')
        return redirect("/user/dashboard")
    return HttpResponse("<h2>Method Not Allowed</h2>")

def addcall(request):
    user_profile = Profile.objects.get(id=request.user.id)
    if request.method == 'POST':
        mobile = request.POST['phone']
        user_profile.mobile = mobile
        user_profile.save()
        messages.success(request, 'Your Mobile Number has been successfully updated')
        return redirect("/user/dashboard")
    return HttpResponse("<h2>Method Not Allowed</h2>")

def archives(request):
    return render(request, "assignment.html")

def courses(request):
    users = User.objects.all()
    return render(request, "courses.html",context={'users':users})

def exam(request):
    return HttpResponse('You are at /user/user/page/exam')

@csrf_exempt
def myform(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_data = {
            'myemail' : email,
            'mypwd' : password,
        }

        return JsonResponse(user_data)
    else:
        return render(request, 'myform.html')

def getText(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=details.csv'
    head = ['User Id','Username','Email']

    writer = csv.writer(response)
    users = User.objects.all()

    writer.writerow(head)

    for user in users:
        writer.writerow([user.id, user.username, user.email])

    return response



