from datetime import date
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres import *
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist




# Create your views here.
def registration(request):
    if request.POST:
        name=request.POST["uname"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        password=request.POST["pass"]
        repassword=request.POST["cpass"]
        log=Login.objects.create_user(username=email,password=password,userType='Customer',viewpassword=password)
        log.save()
        obj=user_reg.objects.create(user=log,user_full_name=name,user_email=email,user_mob_number=phone,user_password=password,user_cpassword=repassword)
        obj.save()
    return render(request,'registration.html')

def customerslogin(request):
    if request.POST:
        email=request.POST['email']
        password=request.POST['password']
        customer=authenticate(username=email,password=password)
        if customer:
            login(request,customer)
            request.session["userID"]=customer.id
            return redirect('customers-home-content')
        else:
            success_message="wrong username or password"
            messages.error(request,success_message)
            
    return render(request,'customers-login.html')

def customerslogout(request):
    logout(request)
    return redirect("customers-home-content")

# def dashboard(request):
#     return render(request,'dashboard.html')

def customerssearch(request):
    q=""
    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        q = wishlist.objects.filter(user_id=user).values_list('product_id', flat=True)  # List of product IDs in wishlist
        
        
    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)

        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            context={
                "data":result,
                "wishlist_ids": q,
            }
            return render(request,"customerssearch.html",context)
        return render(request,"customerssearch.html")   

    return render(request,'customerssearch.html')

def addproduct(request):
    if request.POST:
        productimages=request.FILES['img']
        productname=request.POST['title']
        productbrand=request.POST['brand']
        productcategory=request.POST['category']
        productdescription=request.POST['description']
        productdate=request.POST['date']
        productprice=request.POST['price']
        productgender=request.POST['gender']
        productcolor=request.POST['color']
        productsize=request.POST['size']
        productquantity=request.POST['quantity']
        productoffer=request.POST['productoffer']
        obj=products.objects.create(product_image=productimages,product_name=productname,product_brand=productbrand,product_category=productcategory,product_desc=productdescription,product_date=productdate,product_price=productprice,product_gender=productgender,product_color=productcolor,product_size=productsize,number_of_items=productquantity,offer_price=productoffer)
        obj.save()
    return render(request,'admin-add-product.html')

def product(request):
    data=products.objects.all()
    return render(request,'products.html',{"data":data})

def customershome(request):

    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)

            

    return render(request,'customers-home.html')




def customersproducts(request):   
    q="" 
    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        q=wishlist.objects.filter(user_id=user).values_list('product_id', flat=True)
    
    data=products.objects.all()

    page=1
    if request.GET:
        page=request.GET.get('page',1)
    data=products.objects.all()
    product_paginator=Paginator(data,8)
    data=product_paginator.get_page(page)   

    context={
        "data":data, 
        "wishlist_ids":q,
    }
    return render(request,'customers-products.html',context)

def customershomecontent(request):
    data=products.objects.all().order_by('-id')[:4]
    featuredproduct=products.objects.order_by("priority")[:4]
    q=""

    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        q=wishlist.objects.filter(user_id=user).values_list('product_id', flat=True)
    
    if 'viewmen' in request.POST:
        result=products.objects.filter(product_gender__contains="male")
        context={
                "view":result,
                "wishlist_ids":q,
            }
        return render(request,"customers-products.html",context)
    
    if 'viewwomen' in request.POST:
        result=products.objects.filter(product_gender__contains="female")
        context={
                "view":result,
                "wishlist_ids":q,
            }
        return render(request,"customers-products.html",context)
    if 'brand-adidas' in request.POST:
        result=products.objects.filter(product_brand__contains="adidas")
        context={
                "view":result,
                "wishlist_ids":q,
            }
        return render(request,"customers-products.html",context)
    
    context={
        "data":data,
        "featuredproduct":featuredproduct,
        "wishlist_ids":q,
    }

    return render(request,'index.html',context)


# views.py
import requests

def contacts(request):
    if "userID" in request.session:
        u_id = request.session["userID"]
        user = user_reg.objects.get(user__id=u_id)

    if "sendmessage" in request.POST:
        fullname = request.POST['fullname']
        email = request.POST['email']
        message = request.POST['message']
        currentdate = date.today()
        
        # Save message in the contact model
        obj = contact.objects.create(
            user_id=user, fullname=fullname, mail=email,
            message=message, date=currentdate
        )
        obj.save()

        # Send data to Web3Forms
        data = {
            "access_key": "0fe05a4e-e52d-4253-ac6e-34e6034c1b7d", 
            "name": fullname,
            "email": email,
            "message": message,
        }

        response = requests.post("https://api.web3forms.com/submit", json=data)
        result = response.json()

        # Handle success or failure response from Web3Forms
        if result.get("success"):
            messages.success(request, "Message sent successfully!")
        else:
            messages.error(request, "Message failed to send.")

        return redirect("contact")

    return render(request, 'contact.html')


def about(request):

    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)

    return render(request,'about.html')

def store(request):
    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
    
    return render(request,'customers-stores.html')

@login_required(login_url="user-login")
def wishlists(request):
    u_id=request.session['userID']
    user=user_reg.objects.get(user__id=u_id)
    wishlists=wishlist.objects.filter(user_id_id=user)
    
    context={
        "wishlists":wishlists,
    }
    
    return render(request,"wishlist.html",context)

@login_required(login_url="user-login")
def addwishlists(request,id):
    u_id=request.session['userID']
    user=user_reg.objects.get(user__id=u_id)
    check=wishlist.objects.filter(user_id=user,product_id_id=id).first()
    if not check:
        wishlist.objects.create(user_id=user,product_id_id=id)

    return redirect(request.META.get('HTTP_REFERER', 'customers-products'))  
 
@login_required(login_url="user-login")   
def deletewishlists(request,id):
    u_id=request.session['userID']
    user=user_reg.objects.get(user__id=u_id)
    wishlist.objects.filter(user_id=user,product_id=id).delete()
    return redirect(request.META.get('HTTP_REFERER', 'customers-products')) 
    
   
   
   
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required(login_url="user-login")
@require_POST
def toggle_wishlist(request):
    print("Toggle wishlist view called")  # Debugging line
    product_id = request.POST.get('product_id')
    u_id = request.session.get('userID')
    user = user_reg.objects.get(user__id=u_id)
    
    wishlist_item = wishlist.objects.filter(user_id=user, product_id_id=product_id).first()
    
    if wishlist_item:
        wishlist_item.delete()
        print("Item removed from wishlist",product_id)
        return JsonResponse({'added': False})
    else:
        wishlist.objects.create(user_id=user, product_id_id=product_id)
        print("Item added to wishlist",product_id)
        return JsonResponse({'added': True})

   
   

def customerswishlistremove(request,id):
    remove=wishlist.objects.get(id=id)
    remove.delete()
    if remove:
        messages.success(request,"Item removed successfully")
    else:
        messages.error(request,"Failed to remove item")
    return redirect("wishlist")

def productdetails(request,id):
    data=products.objects.get(id=id)
    amt=data.product_price
    offer=data.offer_price
    wish=""
    
    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        wish=wishlist.objects.filter(user_id=user).values_list('product_id', flat=True)
            
        
        
    userss=user_reg.objects.filter()
    no_of_item=data.number_of_items
    leavreview=rating.objects.filter(product_id=id)

    rate1=rating.objects.filter(product_id=id,star_rating=1).count()
    rate2=rating.objects.filter(product_id=id,star_rating=2).count()
    rate3=rating.objects.filter(product_id=id,star_rating=3).count()
    rate4=rating.objects.filter(product_id=id,star_rating=4).count()
    rate5=rating.objects.filter(product_id=id,star_rating=5).count()
    bar_one=(rate1/5)*100
    bar_two=(rate2/5)*100
    bar_three=(rate3/5)*100
    bar_four=(rate4/5)*100
    bar_five=(rate5/5)*100
    total=rate5+rate4+rate3+rate2+rate1
    totalrate=total/5
    offer_prince=int(amt*(1-(offer/100)))
    
    context={
        "bar_one":bar_one,
        "bar_two":bar_two,
        "bar_three":bar_three,
        "bar_four":bar_four,
        "bar_five":bar_five,
        "data":data,
        "review":leavreview,
        "no_of_item":no_of_item,
        "rate1":rate1,
        "rate2":rate2,
        "rate3":rate3,
        "rate4":rate4,
        "rate5":rate5,
        "totalrate":totalrate,
        "total":total,
        "offer_prince":offer_prince,
        "offer":offer,
        "wishlist_ids":wish,
        "userss":userss,
        }
    if 'cart-btn' in request.POST:
        quantity=request.POST['qty']
 
        amt=int(quantity)*int(offer_prince)
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        obj=cart.objects.create(product_id=data,user_id=user,cart_amount=amt,order_qty=quantity)
        obj.save()
        return redirect(request.META.get('HTTP_REFERER', 'cart'))
    if 'checkout-btn' in request.POST:
        data1=products.objects.get(id=id)
        name=data1.product_name
        img=data1.product_image
        quantity=request.POST['qty']
        amt=int(quantity)*int(offer_prince)
        current_date=date.today()
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        obj=orders.objects.create(product_id=data,user_id=user,order_amount=amt,order_qty=quantity,ordered_date=current_date)
        obj.save()

        context_data={
            "data":data,
            "quantity":quantity,
            "amt":amt,
            "data1":data1,
            "img":img,
            "name":name ,
        }
        query_params = '&'.join([f'{key}={value}' for key, value in context_data.items()])
        redirect_url = f'{reverse("customerssinglecheckout", kwargs={"id": id})}?{query_params}'
        return redirect(redirect_url)

    return render(request,'customers-product-details.html',context)

def customerscheckout(request):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    data=cart.objects.filter(user_id__id=user.id)

    try:
        saved=savedaddress.objects.get(user_id_id=user)
    except ObjectDoesNotExist:
        saved=None
        
    free=0
    total=0
    for i in data:
        total+=i.cart_amount
        if total > 50:
            free=total
        else:
            free=total+50
        
    context={
        "data":data,
        "total":total,
        "free":free,
        "saved":saved,
    }
    
    if 'paybtn' in request.POST:

        for i in data:
            product=i.product_id
            amts=i.cart_amount
            qty=i.order_qty
            # no_of_item=i.product_id.number_of_items
            first_name = request.POST['fname'] 
            last_name=request.POST.get("lname", "")
            Delivery_Address=request.POST["Delivery_Address"]
            Address=request.POST["Address"]
            City=request.POST["City"]
            State=request.POST["State"]
            Country=request.POST["Country"]
            Zip_code=request.POST["Zip_code"]
            Email_Address=request.POST["Email_Address"]
            Mobile_No=request.POST["Mobile_No"]
            Cdate=date.today()
            check=checkout.objects.create(user_id=user,product_id=product,f_name=first_name,l_name=last_name,d_address=Delivery_Address,h_address=Address,city=City,state=State,country=Country,zip_code=Zip_code,e_mail=Email_Address,mobile=Mobile_No,cdate=Cdate,amts=amts)
            check.save()
            data.delete()

            d=i.product_id.number_of_items-qty
            if d > 0: 
                i.product_id.number_of_items=d
                i.product_id.save()
            else:
                i.product_id.number_of_items=0
                i.product_id.save()
                

        return redirect('customers-profile')
    
    if 'saveaddress' in request.POST:
        first_name = request.POST['fname']
        last_name=request.POST.get("lname", "")
        Delivery_Address=request.POST["Delivery_Address"]
        Address=request.POST["Address"]
        City=request.POST["City"]
        State=request.POST["State"]
        Country=request.POST["Country"]
        Zip_code=request.POST["Zip_code"]      
        Email_Address=request.POST["Email_Address"]
        Mobile_No=request.POST["Mobile_No"]
        savedaddress.objects.filter(user_id_id=user).delete()
        save=savedaddress.objects.create(user_id=user,f_name=first_name,l_name=last_name,d_address=Delivery_Address,h_address=Address,city=City,state=State,country=Country,zip_code=Zip_code,e_mail=Email_Address,mobile=Mobile_No)
        save.save()        
        return redirect("customers-checkout")
    
    return render(request,'customers-checkout.html',context)

def customerssinglecheckout(request,id):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)

    try:
        saved=savedaddress.objects.get(user_id_id=user)
    except ObjectDoesNotExist:
        saved=None

    context_data = {}
    # Parse query parameters to extract context data
    for key, value in request.GET.items():
        context_data[key] = value
    amts = context_data.get('amt', None)
    quantity = context_data.get('quantity', None)
    
    product = products.objects.get(id=id)
    to=0
    l=int(amts)
    if l > 50:
        to=l
    else:
        to=l+50  
    
        
    if 'saveaddresss' in request.POST:
        
        first_name = request.POST['fname']
        last_name=request.POST.get("lname", "")
        Delivery_Address=request.POST["Delivery_Address"]
        Address=request.POST["Address"]
        City=request.POST["City"]
        State=request.POST["State"]
        Country=request.POST["Country"]
        Zip_code=request.POST["Zip_code"]      
        Email_Address=request.POST["Email_Address"]
        Mobile_No=request.POST["Mobile_No"]
        savedaddress.objects.filter(user_id_id=user).delete()
        save=savedaddress.objects.create(user_id=user,f_name=first_name,l_name=last_name,d_address=Delivery_Address,h_address=Address,city=City,state=State,country=Country,zip_code=Zip_code,e_mail=Email_Address,mobile=Mobile_No)
        save.save()    
        context={
            "totals":to,
            "saved":saved,
        }
        return render(request,'customers-single-checkout.html',{**context_data, **context})
        
    
    if 'paybtn' in request.POST:
        first_name = request.POST['fname']
        last_name=request.POST.get("lname", "")
        Delivery_Address=request.POST["Delivery_Address"]
        Address=request.POST["Address"]
        City=request.POST["City"]
        State=request.POST["State"]
        Country=request.POST["Country"]
        Zip_code=request.POST["Zip_code"]      
        Email_Address=request.POST["Email_Address"]
        Mobile_No=request.POST["Mobile_No"]
        Cdate=date.today()

        checks=checkout.objects.create(user_id=user,product_id=product,f_name=first_name,l_name=last_name,d_address=Delivery_Address,h_address=Address,city=City,state=State,country=Country,zip_code=Zip_code,e_mail=Email_Address,mobile=Mobile_No,cdate=Cdate,amts=amts)
        checks.save()
        d=product.number_of_items-int(quantity)
        if d > 0:
            product.number_of_items=d
            product.save()
        else:
            product.number_of_items=0
            product.save()

        return redirect("customers-profile")
    
    context={
        "totals":to,
        "saved":saved,
    }
    return render(request,'customers-single-checkout.html',{**context_data, **context})

def customersprofile(request):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    users=user_reg.objects.filter(user__id=u_id)
    ordercount=checkout.objects.filter(user_id_id=user).count()

    customername=user.user_full_name
    profile=checkout.objects.filter(user_id__id=user.id)
    filtered_objects = checkout.objects.filter(id__gt=0,user_id__id=user.id)
    filtered_ids = filtered_objects.values_list('id', flat=True)
    statuses = []
    for id_value in filtered_ids:

        checkout_obj = checkout.objects.get(id=id_value)
        status=checkout_obj.order_status
        statuses.append(status)

    pro=edit.objects.filter(user_id__id=user.id)
    


    
    if 'edit-btn' in request.POST:        
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            user.img1 = photo
        else:
            photo = user.img1  
    
        previous_edit = edit.objects.filter(user_id=user).first()
    
        location = request.POST.get('location', None)
        if not location and previous_edit:
            location = previous_edit.location  
            
        edit.objects.filter(user_id=user).delete()
        user.save()
    
        edit.objects.create(user_id=user, img=photo, location=location)
    
        return redirect("customers-profile")

    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        if searchinput:
            result=products.objects.filter(product_name     =searchinput)
            context={
                "result":result,
            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html")  
    context={
        "customername":customername,
        "users":users,
        "profile":profile,
        "pro":pro,
        "statuses":statuses,
        "ordercount":ordercount,
    }  
    return render(request,'customers-profile.html',context)



@login_required(login_url='user-login')
def customerscart(request):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    carts=cart.objects.filter(user_id__id=user.id)
  
    free=0
    total=0
    for i in carts:
        free+=i.cart_amount
        if free> 50:
            total=free
        else:
            total=free+50


    context={
        "data":carts,
        "free":free,
        "total":total,  
    }
    
    return render(request,'cart.html',context)


def cartremove(request,id):
    remove=cart.objects.get(id=id)
    remove.delete()
    if remove:
        messages.success(request,"Cart item removed successfully")
    else:
        messages.error(request,"Failed to remove item from cart")
    return redirect('customers-cart')
    

def forgetpassword(request):
    return render(request,"Forget-Password.html")

def cartincrement(request,id):
    incr=cart.objects.get(id=id)
    incr.order_qty += 1
    price=incr.product_id.product_price
    offer=incr.product_id.offer_price
    result=int(price*(1-offer/100)) 
    incr.cart_amount=result*incr.order_qty
    incr.save()
    return redirect('customers-cart')


    
def cartdecrement(request,id):
    incr=cart.objects.get(id=id)
    incr.order_qty -= 1
    price=incr.product_id.product_price
    offer=incr.product_id.offer_price
    result=int(price*(1-offer/100)) 
    incr.cart_amount=result*incr.order_qty
    if incr.order_qty <1:
        incr.delete()
    else:
        incr.save()
    return redirect('customers-cart')


def customersprofileorderremove(request,id):
    remove=checkout.objects.get(id=id)
    remove.delete()
    if remove:
        messages.success(request,"Your order cancel succeffully")
    else:
        messages.error(request,"Failed to cancel your order")
    return redirect('customers-profile')


def customerswritereview(request,id):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    customername=user.user_full_name
    product=products.objects.get(id=id)  
    profile_picure=user

    if request.POST:
        review=request.POST['leave-review']
        image=request.FILES.get('imgupload',None)
        rating1=request.POST["rating"]
        
        today=date.today()
        obj=rating.objects.create(user_id=user,product_id=product,review=review,date=today,taken_image=image,star_rating=rating1)
        obj.save()
        return redirect("/product-details/"+id)
    context={
        "customername":customername,
        "product":product,
        "dp":profile_picure,
    }  

    return render(request,"write-review.html",context)