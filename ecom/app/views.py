from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer,OrderPlaced,Cart,Products,User
from django.contrib.auth.models import User
from .forms import CustomerRegiForm,CustomerProfileForms
from django.db.models import Q

from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator




# def home(request):
#  return render(request, 'app/home.html')

# @method_decorator(login_required,name='dispatch')
class HomeView(View):
    def get(self,request):
        topwear=Products.objects.filter(category="TW")
        bottomwear=Products.objects.filter(category="BW")
        mobile=Products.objects.filter(category="M")
        # laptop=Products.objects.filter(category="L")
        
        total_item=0 
        if request.user.is_authenticated:
            total_item=len(Cart.objects.filter(user=request.user))
        
        return render(request,"app/home.html",{"topwear":topwear,"bottomwear":bottomwear,"mobile":mobile,"total_item":total_item})
        

# @method_decorator(login_required,name='dispatch')
class product_detail(View):
   def get(self,request,pk):
        product=Products.objects.get(pk=pk)
        
        item_already_in_cart=False 
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            
        total_item=0 
        if request.user.is_authenticated:
            total_item=len(Cart.objects.filter(user=request.user))
            
        return render(request,"app/productdetail.html",{"p":product,"item_already_in_cart":item_already_in_cart,"total_item":total_item})
#  return render(request, 'app/productdetail.html')

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get("prod_id")
    product=Products.objects.get(id=product_id)
    # print(product)
    # print(user)
    
    
    Cart(user=user,product=product).save()
    return redirect('/show-cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user 
        cart=Cart.objects.filter(user=user)
        
        total_item=0 
        if request.user.is_authenticated:
            total_item=len(Cart.objects.filter(user=request.user)) 
        
        amount=0.0
        shipping_charge=70 
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for  c in cart_product:
                temp=(c.quantity*c.product.discounted_price)
                amount+=temp
                total_amount=amount+shipping_charge  
            
           
                
            return render(request, 'app/addtocart.html',{"cart":cart,"amount":amount,"total":total_amount,"total_item":total_item})
        
        else:
            return render(request, 'app/emptycart.html',{"total_item":total_item})

@login_required
def plus_cart(request):
    if request.method == "GET":
        prod_id=request.GET["prod_id"]
        print(prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # user=request.user
        c.quantity+=1
        c.save()
        msg="Your Cart is Empty"
        amount=0.0
        shipping_charge=70 
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        
        for  p in cart_product:
                temp=(p.quantity*p.product.discounted_price)
                amount+=temp
                # total_amount=amount+shipping_charge 
        data={
                    "quantity":c.quantity,
                    "amount":amount,
                    "total":amount+shipping_charge,
                    # "msg":msg 
                }     
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == "GET":
        prod_id=request.GET["prod_id"]
        print(prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # user=request.user
        c.quantity-=1
        c.save()
        
        amount=0.0
        shipping_charge=70 
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        
        for  p in cart_product:
                temp=(p.quantity*p.product.discounted_price)
                amount+=temp
                # total_amount=amount+shipping_charge 
        data={
                    "quantity":c.quantity,
                    "amount":amount,
                    "total":amount+shipping_charge 
                }     
        return JsonResponse(data)    

@login_required
def remove_item(request):
    if request.method == "GET":
        prod_id=request.GET["prod_id"]
        print(prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.delete()
        
        amount=0.0
        shipping_charge=70 
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        
        for  p in cart_product:
                temp=(p.quantity*p.product.discounted_price)
                amount+=temp
                # total_amount=amount+shipping_charge 
        data={
                    "amount":amount,
                    "total":amount+shipping_charge 
                }     
        return JsonResponse(data) 

@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForms()
        return render(request,'app/profile.html',{"form":form,"active":"btn-primary"})
    
    def post(self,request):
        form=CustomerProfileForms(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data["name"]
            locality=form.cleaned_data["locality"]
            city=form.cleaned_data["city"]
            state=form.cleaned_data["state"]
            zipcode=form.cleaned_data["zipcode"]
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            
            reg.save()
            messages.success(request,"Congratulations !! Profile Updated Successfully")
            
        total_item=0 
        if request.user.is_authenticated:
            total_item=len(Cart.objects.filter(user=request.user))
            return render(request, 'app/profile.html',{"form":form,"active":"btn-primary","total_item":total_item})

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user) #This is to get the current user,it solve the problem like to store user in login as a session.
    
    total_item=0 
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user)) 
        
    return render(request, 'app/address.html',{"add":add,"active":"btn-primary","total_item":total_item})
    
@login_required
def orders(request):
    user=request.user 
    order=OrderPlaced.objects.filter(user=user)
    
    total_item=0 
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/orders.html',{"order":order,"total_item":total_item})

@login_required
def cancle_orders(request):
    user=request.user 
    order=OrderPlaced.objects.filter(user=user)
    order.delete()
    
    total_item=0 
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/orders.html',{"total_item":total_item})
    

# def change_password(request):
#  return render(request, 'app/changepassword.html')


def mobile(request,data=None):
    if data == None:
        mobile=Products.objects.filter(category="M")
        
    elif data=="Redmi" or data=="Iphone" or data=="Vivo":
        mobile=Products.objects.filter(category="M").filter(brand=data)
        
    elif data=="below":
        mobile=Products.objects.filter(category="M").filter(discounted_price__lt=10000)
        
    elif data=="above":
        mobile=Products.objects.filter(category="M").filter(discounted_price__gt=10000)
        
    total_item=0 
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/mobile.html',{"mobile":mobile,"total_item":total_item})



def laptop(request,data=None):
    if data == None:
        laptop=Products.objects.filter(category="L")
        
    elif data=="Asus" or data=="Dell" or data=="Hp":
        laptop=Products.objects.filter(category="L").filter(brand=data)
        
    elif data=="below":
        laptop=Products.objects.filter(category="L").filter(discounted_price__lt=10000)
        
    elif data=="above":
        laptop=Products.objects.filter(category="L").filter(discounted_price__gt=10000)
        
    total_item=0 
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/laptop.html',{"laptop":laptop,"total_item":total_item})


def topwear(request,data=None):
    if data == None:
        topwear=Products.objects.filter(category="TW")
        
    elif data=="Zara" or data=="zudio" or data=="Levis" or data=="Raymond" or data=="Polo":
        topwear=Products.objects.filter(category="TW").filter(brand=data)
        
    # elif data=="below":
    #     mobile=Products.objects.filter(category="M").filter(discounted_price__lt=10000)
        
    # elif data=="above":
    #     mobile=Products.objects.filter(category="M").filter(discounted_price__gt=10000)
        
    total_item=0 
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/topwear.html',{"topwear":topwear,"total_item":total_item})



def bottomwear(request,data=None):
    if data == None:
        bottomwear=Products.objects.filter(category="BW")
        
    elif data=="Zara" or data=="zudio" or data=="Levis" or data=="Raymond" or data=="Lee":
        bottomwear=Products.objects.filter(category="BW").filter(brand=data)
        
    # elif data=="below":
    #     mobile=Products.objects.filter(category="M").filter(discounted_price__lt=10000)
        
    # elif data=="above":
    #     mobile=Products.objects.filter(category="M").filter(discounted_price__gt=10000)
        
    total_item=0 
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/bottomwear.html',{"bottomwear":bottomwear,"total_item":total_item})


# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

# @method_decorator(login_required,name='dispatch'
# # )
class CustomerRegistrationForm(View):
    def get(self,request):
        form=CustomerRegiForm()
        
        return render(request,'app/customerregistration.html',{"form":form})
    
    def post(self,request):
        form=CustomerRegiForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request,'app/customerregistration.html',{"form":form})

@login_required
def checkout(request):
    user=request.user 
    add=Customer.objects.filter(user=user)
    cart_item=Cart.objects.filter(user=user)
    # product=Products.objects.filter(title="title")
    amount=0.0
    shipping_charge=70 
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for  p in cart_product:
                temp=(p.quantity*p.product.discounted_price)
                amount+=temp
                total=amount+shipping_charge 
    
    total_item=0 
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/checkout.html',{"add":add,"cart_item":cart_item,"total":total,"total_item":total_item})

@login_required
def payment_done(request):
    user=request.user 
    custid=request.GET.get("custid")
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    # product=Cart.objects.filter(product=product)
    for c in cart:
        # product=c.product
        OrderPlaced(user=user,customer=customer,Product=c.product,quantity=c.quantity).save()
        
        c.delete()
    
    total_item=0 
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
    
    return redirect("orders")