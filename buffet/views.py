from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from market_place.models import r_attribute, Otp_Confirmation, c_attribute
import datetime
from django.core.mail import send_mail
import random


def home(request):
    user = request.user
    if user.is_authenticated:
        check = ''
        for i in user.email:
            if i=='@':
                break
            else:
                check+=i

        parent=r_attribute.objects.filter(parent=user)

        if check==user.username and len(parent)==0:
            existance_check=c_attribute.objects.filter(parent=request.user)

            if not len(existance_check)==0:
                if datetime.datetime.now().hour>20 or datetime.datetime.now().hour<9:
                    return render (request , 'night.html')
                return redirect(f'/market-place/user/{user.username}')
            else:
                return render(request, 'market/pending_profile.html')

        else:
            existance_check=r_attribute.objects.filter(parent=request.user)
            if not len(existance_check)==0:
                if not request.user.is_staff:
                    return redirect(f'/collab/restaurant/admin/{user.username}')
            else:
                return render(request, 'collabs/pending_profile.html')
    return render(request, 'index.html')



def Login(request):
    return render(request, 'login.html')
    

def otp_confirmation(request):
    if request.method=='POST':
        otp=request.POST.get('otp')
        entered_otp=request.POST.get('enter_otp')
        otp = int(otp)
        entered_otp=int(entered_otp)

        if otp==entered_otp:
            messages.success(request, 'Authentication successfull. Kindly proceed.')

            user = request.user
            if user.is_authenticated:
                add_confirm=Otp_Confirmation(parent=request.user, confirmation_status=True)
                add_confirm.save()

                confirm=Otp_Confirmation.objects.filter(parent=request.user)

                if not len(confirm)==0:
                    if confirm[0].confirmation_status:
                        check = ''
                        for i in user.email:
                            if i=='@':
                                break
                            else:
                                check+=i

                        parent=r_attribute.objects.filter(parent=user)

                        if check==user.username and len(parent)==0:
                            return redirect(f'/market-place/user/{user.username}/profile')

                        else:
                            if not request.user.is_staff:
                                return redirect(f'/collab/restaurant/admin/{user.username}/profile')
        else:
            messages.warning(request, 'Wrong OTP entered. Kindly check your email or re-send the OTP to try again!')
            return redirect('/send-otp')


def sent_otp(request):
    if request.method=='POST':
        email=request.POST.get('email', '')

        otp=random.randint(100000, 999999) 

        try:
            send_mail(f"OTP/ from Buffey.in", f'Your Buffey SignUp authentication OTP is: {otp}', 'mr.raojiad19092003@gmail.com', [email], fail_silently=False)

            return render(request, 'otp_confirmation.html', {'otp': otp})

        except:
            messages.error(request, 'Sorry! We could not sent an E-mail regarding your otp confirmation on your entered email. Check if it is correct.')
            return redirect('/')


def send_otp(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'send_otp.html', {'user_email': user.email})


def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Successfully Logged out!")
        return redirect('/login-page')
    else:
        messages.info(request, "No user has logged in yet")
        return redirect('/login-page')


def restaurant_signup(request):
    return render(request, 'restaurant_signup.html')

def customer_signup(request):
    return render(request, 'customer_signup.html')


def send_otp_pwd(request):
    return render(request, 'change_pwd_auth.html')


def sent_otp_pwd(request):
    if request.method=='POST':
        email=request.POST.get('email', '')

        otp=random.randint(100000, 999999) 

        try:
            send_mail(f"OTP/ from Buffey.in", f'Your Buffey SignUp authentication OTP is: {otp}', 'mr.raojiad19092003@gmail.com', [email], fail_silently=False)
            return render(request, 'pwd_otp_confirmation.html', {'otp': otp})

        except:
            messages.error(request, 'Sorry! We could not sent an E-mail regarding your otp confirmation on your entered email. Check if it is correct.')
            return redirect('send-otp-pwd')



def otp_confirmation_pwd(request):
    if request.method=='POST':
        username=request.POST.get('username')
        otp=request.POST.get('otp')
        entered_otp=request.POST.get('enter_otp')
        otp = int(otp)
        entered_otp=int(entered_otp)

        if otp==entered_otp:
            user=User.objects.filter(username=username)[0]

            login(request, user)

            messages.success(request, 'Authentication successfull. Kindly proceed.')
            return redirect('/change-pwd')

        else:
            messages.warning(request, 'Wrong OTP entered. Kindly check your email or re-send the OTP to try again!')
            return redirect('/send-otp-pwd')


def change_pwd(request):
    if request.method=="POST":
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

        if pass1!=pass2:
            messages.warning(request, "Your entered passwords did not match each other. Please try again...")
            return render(request, 'change_pwd.html')

        try:
            user = User.objects.get(username__exact=request.user.username)
            user.set_password(pass1)
            user.save()
            
            messages.success(request, f'Your password has been changed successfully. You can now login!')

            return redirect('/login-page')


        except Exception as e:
            messages.error(request, 'Could not change your password. Please try again later or contact us on Boofey/feeds/contact-us')
            return render(request, 'change_pwd.html')

    else:
        if request.user.is_authenticated:
            return render(request,'change_pwd.html')

