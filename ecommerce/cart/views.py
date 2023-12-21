from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart,Account,Order
# Create your views here.
@login_required()
def cartview(request):
    sum=0
    u=request.user
    try:
        cart=Cart.objects.filter(user=u)
        for i in cart:
            sum+=i.quantity*i.product.price
    except:
        pass

    return render(request,'cart.html',{'c':cart,'total':sum})



@login_required()
def add_to_cart(request,p):
    product=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=product)
        if(cart.quantity<cart.product.stock):
            cart.quantity+=1
        cart.save()
    except:
        cart=Cart.objects.create(product=product,user=u,quantity=1)
        cart.save()

    return redirect('cart:cartview')


@login_required()
def minus_cart(request,p):
    product=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=product)
        if cart.quantity>1:
            cart.quantity-=1
            cart.save()
    except:
        pass
    return redirect('cart:cartview')


@login_required()
def delete_cart(request,p):
    product=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=product)
        cart.delete()
    except:
        pass
    return redirect('cart:cartview')


def orderform(request):
    if(request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['an']
        u=request.user
        cart=Cart.objects.filter(user=u)
        ac=Account.objects.get(accnum=n)
        sum=0
        for i in cart:
            sum+=i.quantity*i.product.price
        if(ac.amount>=sum):
            ac.amount=ac.amount-sum
            ac.save()
            for i in cart:
                o=Order.objects.create(user=u,product=i.product,address=a,phone=p,noitemss=i.quantity,order_status="paid")
                o.save()
                i.product.stock=i.product.stock-i.quantity
                i.product.save()
            cart.delete()
            msg="Order Placed Successfully"
            return render(request,'orderdetail.html',{'m':msg})

        else:
            msg="Insufficient Amount in user Account, You cannot place Order"
            return render(request,'orderdetail.html',{'m':msg})


    return render(request,'orderform.html')


def order_view(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'or':o})
