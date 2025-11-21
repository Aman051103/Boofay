from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Contact
from django.core.mail import send_mail


# Create your views here.

def home(request):
    return redirect('/feeds/about-us')

def about(request):
    return render(request, 'feeds/about.html')

def contact(request):
    return render(request, 'feeds/contact.html')


def send_contact(request):
    if request.method == 'POST':
        name=request.POST.get('name', '')
        email=request.POST.get('e-mail', '')
        phone=request.POST.get('phone', '')
        query=request.POST.get('query', '')

        try:
            if request.user.is_authenticated:
                message = Contact(parent=request.user, name=name, phone=phone, email=request.user.email, query=query)
                message.save()
                
                send_mail(f"Username {request.user.username}'s query, from Boofey. User_id: {request.user.id}", f'USER INFO -\nE-mail Address: {request.user.email}\n\nPhone Number: {phone}\n\nQuery: "{query}"', 'mr.raojiad19092003@gmail.com', ["aby85365@gmail.com"], fail_silently=False)

            else:
                message = Contact(name=name, phone=phone, email=email, query=query)
                message.save()

                send_mail(f"A visitor - {name}'s query, from Boofey", f'USER INFO -\nE-mail Address: {email}\n\nPhone Number: {phone}\n\nQuery: "{query}"', 'mr.raojiad19092003@gmail.com', ["aby85365@gmail.com"], fail_silently=False)

            messages.success(request, 'Query sent!')

        except:
            messages.error(request, 'We are unable to send your query right now. Please try again later...')

        return redirect('/feeds')

