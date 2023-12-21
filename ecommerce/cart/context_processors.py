from cart.models import Cart

def product_count(request):
    item_count=0
    u=request.user
    try:
        cart=Cart.objects.filter(user=u)
        for i in  cart:
            item_count=item_count+i.quantity
    except:
        item_count=0
    return {'count':item_count}


