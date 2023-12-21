from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def  allcategories(request):
    c=Category.objects.all()

    return render(request,'category.html',{'c':c})


def allproducts(request,p):
    c=Category.objects.get(name=p)
    p=Product.objects.filter(category=c)
    return render(request,'products.html',{'c':c,'p':p})

def details(request,p):
    p=Product.objects.get(name=p)
    return render(request,'details.html',{'p':p})

def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        pas=request.POST['p']
        cpas=request.POST['cp']
        e=request.POST['e']
        if(pas==cpas):
            b=User.objects.create_user(username=u,password=pas,email=e)
            b.save()
            return allcategories(request)
        else:
            return HttpResponse("password not matching")
    return render(request,'register.html')
def log(request):
    if(request.method=="POST"):
        uname=request.POST['u']
        pa=request.POST['p']
        user=authenticate(username=uname,password=pa)
        if user:
            login(request,user)
            return allcategories(request)
        else:
            messages.error(request,"invalid credential")
    return render(request,'login.html')
@login_required()
def logoutt(request):
    logout(request)
    return log(request)
    return render(request,'login.html')
