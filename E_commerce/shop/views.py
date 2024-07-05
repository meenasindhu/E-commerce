from django.http import  JsonResponse
from django.shortcuts import render,redirect
from shop.models import *
from django.contrib import messages
from shop.forms import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json


#from django.http import HttpResponse

# Create your views here.
def home(request):
    products=product.objects.filter(trending=1)
    return render(request,'shop/index.html',{"product":products})
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"logged out successfully")
    return redirect('home')
def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd =request.POST.get('password')
            user = authenticate(request,username=name,password=pwd)
            if user is not None:
                  login(request,user)
                  messages.success(request,"Logged in Successfully")
                  return redirect("home")
            else:
                messages.error(request,"Invalid User Name or Password")
                return redirect("login")
        return render(request,"shop/login.html")
def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registration success you can login now..!")
        return redirect('/login')
    return render(request,'shop/register.html',{"form":form})
        
def collections(request):
    category=catagory.objects.filter(status=0)#1 is hidden based on our model,0 is show
    return render(request,'shop/collections.html',{"category":category})
def collectionsview(request,name):
    if(catagory.objects.filter(name=name,status=0)):
        products=product.objects.filter(catagory__name=name)# product name =catagory name
        return render(request,'shop/products/index.html',{"products":products,"catagory_name":name})
    else:
        messages.warning(request,"No such catagory found")
        return redirect('collections')
def productdetails(request,cname,pname):
    if(catagory.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            products=product.objects.filter(name=pname,status=0).first()
            return render(request,'shop/products/productdetails.html',{"products":products})
        else:
             messages.error(request,"No such catagory found")
             return redirect('collections')

        
    else:
        messages.error(request,"No such catagory found")
        return redirect('collections')
def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status=product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'product added to cart success'}, status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'}, status=200)

        else:
            return JsonResponse({'status':'login to add cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect("home")
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')
def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status=product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Favourite'}, status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product Added to Favourite'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add Favourite'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
        
def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})
    else:
        return redirect("home")
def remove_fav(request,fid):
    item=Favourite.objects.get(id=fid)
    item.delete()
    return redirect("/favviewpage")
 