from django.shortcuts import redirect, render, HttpResponseRedirect
from django.core.mail import send_mail
from .models import Custom_User
from django.contrib.auth import authenticate, login
from django.conf import settings
import random
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def reg(request):
    if request.user.is_authenticated:
        messages.success(request, "You Are Already Logged In.")
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        image = request.FILES.get('image')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if all([username, first_name, last_name, email, password1, password2]):
            if password1 == password2:
                otp = random.randint(1000, 9999)
                user = Custom_User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    address=address,
                    city=city,
                    state=state,
                    country=country,
                    zip_code=zip_code,
                    image=image,
                    password=password1,
                    otp=otp
                )
                user.save()
                send_email(email, otp)
                return redirect('verify_otp')
    return render(request, 'auth/login.html')


def send_email(email, otp):
    subject = 'Welcome to our website'
    message = f'Thank you for registering with us your otp is {otp}.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def verify_otp(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)
        if otp:
            user = Custom_User.objects.filter(otp=otp).first()
            if user:
                user.is_verified = True
                user.save()
                return redirect('reg')
        else:
            return redirect('verify_otp')
    return render(request, 'auth/otp_submit.html')


def logout(request):
    auth_logout(request)
    return redirect('reg')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_verified:
                login(request, user)
                return redirect('home')
            else:
                return redirect('verify_otp')


def Forget_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Custom_User.objects.filter(email=email).first()
        if user:
            otp = random.randint(1000, 9999)
            user.otp = otp
            user.save()
            send_email(email, otp)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Email not found.")
    return render(request, 'auth/forget_page.html')


def verify_otp_forget(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        password1 = request.POST.get('pass')
        password2 = request.POST.get('pass1')
        if otp and password1 and password2:
            user = Custom_User.objects.filter(otp=otp).first()
            if user:
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    return redirect('reg')
                else:
                    messages.error(request, "Passwords do not match.")
            else:
                messages.error(request, "Invalid OTP.")

    return redirect('reg')


def user_deshboard(request):
    if not request.user.is_authenticated:
        return redirect('reg') 
    
    user = request.user
    user_data = Custom_User.objects.get(id=user.id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        if password1:
            user_data.first_name=first_name,
            user_data.last_name=last_name,
            user_data.email=email,
            user_data.password=password1
        user_data.set_password(password1)
        user_data.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   

    return render(request, 'auth/user-deshboard.html',{'user_data':user_data})

