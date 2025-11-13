from django.shortcuts import render

def login(request):
    return render(request, 'usuarios/login.html')

def signin(request):
    return render(request, 'usuarios/signin.html')

def password_forget(request):
    return render(request, 'usuarios/password_forget.html')

def new_password(request):
    return render(request, 'usuarios/new_password.html')
