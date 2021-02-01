
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages

from .decorators import practitioner_required, regular_user_required
from .models import Profile,  User
from .forms import SignupForm, ProfileForm
# # Create your views here.


def allProfilesCount():
    return Profile.objects.all().count()

def returnSingleAilmentNamesAndCount():
    return Profile.objects.values('disease').annotate(Count('id')).order_by().filter(id__count__gte=1)

def index(request):
    return TemplateResponse(request, 'index.html')


@login_required(login_url='/auth/login')
@regular_user_required
def profile(request):
    if request.method == 'POST': 
        try:
            Profile.objects.get(user__email=request.user.email)
            messages.error(request, '!!! Your profile already exists')
            return redirect('ehealth:index')
        except:
            form = ProfileForm(request.POST) 
            if form.is_valid():
                userProfile = form.save(commit = False)
                userProfile.user = User.objects.get(email=request.user.email)
                userProfile.save()
                messages.success(request, '!!! Welcome')
                return redirect('ehealth:index')
            else:
                messages.error(request, "Something went wrong. Please try again.")
                return redirect('ehealth:profile')
    else: 
        return TemplateResponse(request, 'registration/profile.html')
    
@login_required(login_url='/auth/login')
@practitioner_required
def dashboard(request):
    profiles = Profile.objects.all()
    ailments = returnSingleAilmentNamesAndCount()
    return TemplateResponse(request, 'dashboard.html', {'profiles': profiles, 'ailments':ailments})

@login_required(login_url='/auth/login')
def stats(request):
    if not request.user.is_practitioner:
        try:
            Profile.objects.get(user__email=request.user.email)
        except:
            messages.error(request, '!!! Kindly fill the profile form before proceeding.')
            return redirect('ehealth:profile')
    try:
        dups = returnSingleAilmentNamesAndCount()
        count = allProfilesCount()
        ratio = 100/allProfilesCount()  #simple ratio
        ratiopx = (100/allProfilesCount()) * 3    #ratio with respect to template chart pix(300px bar heigh)
        return TemplateResponse(request, 'stats.html', {'dups': dups, 'ratio': ratio, 'ratiopx':ratiopx, 'count':count})
    except:
        return TemplateResponse(request, 'stats.html')
    

def sign_up(request):
    if request.user.is_authenticated:
        messages.error(request, "You are currently signed in")
        return redirect('ehealth:index')
    if request.method == 'POST': 
        if request.POST.get('password') != request.POST.get('passwd2'):
            messages.error(request, "Password mismatch")
            return redirect('ehealth:signup')
        email = request.POST.get('email')
        try:
            User.objects.get(email=email)
            messages.error(request, "This account already exists. Please login")
            return redirect('ehealth:signup')
        except:
            form = SignupForm(request.POST)
            if form.is_valid():
                newUser = form.save(commit = False)
                passwd = request.POST.get('password')
                newUser.set_password(passwd)
                newUser.username = email
                newUser.save()
                a = authenticate(email=email, password=passwd)
                auth_login(request, newUser)
                messages.success(request, '!!! Kindly fill the profile form before proceeding.')
                return redirect('ehealth:profile')
            else:
                messages.error(request, "Something went wrong. Please try again.")
                return redirect('ehealth:signup')
            
        
    else: 
        return TemplateResponse(request, 'registration/signup.html')
         
def medic_signup(request): 
    if request.user.is_authenticated:
        messages.error(request, "You are currently signed in")
        return redirect('ehealth:index')
    if request.method == 'POST': 
        if request.POST.get('password') != request.POST.get('passwd2'):
            messages.error(request, "Password mismatch")
            return redirect('ehealth:medic_signup')
        email = request.POST.get('email')
        try:
            User.objects.get(email=email)
            messages.error(request, "This account already exists. Please login")
            return redirect('ehealth:signup')
        except:
            form = SignupForm(request.POST) 
            if form.is_valid():
                newUser = form.save(commit = False)
                passwd = request.POST.get('password')
                newUser.set_password(passwd)
                newUser.is_practitioner = True
                newUser.username = email
                newUser.save()
                a = authenticate(email=email, password=passwd)
                auth_login(request, newUser)
                messages.success(request, '!!! Welcome')
                return redirect('ehealth:dashboard')
            else:
                messages.error(request, "Something went wrong. Please try again.")
                return redirect('ehealth:medic_signup')
        
    else: 
        return TemplateResponse(request, 'registration/practitioner_signup.html')








def log_in(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            messages.error(request, "You are currently signed in")
            return redirect('ehealth:index')
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                messages.error(request, '!!! Your account is disabled. Please contact the admin.')
                return redirect('ehealth:index')
            if check_password(password, user.password):
                a = authenticate(email=email, password=password)
                auth_login(request, user)
                if user.is_practitioner:
                    messages.success(request, '!!! Welcome')
                    return redirect("ehealth:dashboard")
                else:
                    try:
                        Profile.objects.get(user__email=email)
                        messages.success(request, '!!! Welcome')
                        return redirect("ehealth:index")
                    except:
                        messages.success(request, '!!! Kindly fill the profile form before proceeding')
                        return redirect("ehealth:profile")
            else:
                messages.error(request, '!!! Invalid credentials')
                return redirect('ehealth:login')

        except User.DoesNotExist:
            messages.error(request, '!!! Invalid credentials')
            return redirect('ehealth:index')

    return TemplateResponse(request, 'registration/login.html')


def logout_request(request):
    logout(request)
    messages.success(request, '!!! Logged out')
    return redirect('ehealth:index')

# def page_not_found(request):
#     return TemplateResponse(request, 'pnf.html')