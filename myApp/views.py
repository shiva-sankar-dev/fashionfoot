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
    customername=""
    count=""
    wishlistscount=""
    user=""
    profile_picure=""
    q=""

    

    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        count=cart.objects.filter(user_id__id=user.id).count()
        wishlistscount=wishlist.objects.filter(user_id_id=user).count()
        customername=user.user_full_name
        dp=user
        profile_picure=user
        q=wishlist.objects.filter(user_id=user)
        
        
        

    
    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            q=wishlist.objects.filter(user_id=user)

            context={
                "result":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                "q":q,
            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html")    

    data=products.objects.all()




    page=1
    if request.GET:
        page=request.GET.get('page',1)
    data=products.objects.all()
    product_paginator=Paginator(data,8)
    data=product_paginator.get_page(page)   
    # dp=""

    context={
        "count":count,
        "data":data,
        "customername":customername,   
        "wishlistscount":wishlistscount,
        "q":q,
        # "dp":dp,
        "dp":profile_picure,
        


             
        
    }
    return render(request,'customers-products.html',context)

def customershomecontent(request):
    customername=""
    count=""
    wishlistscount=""
    profile_picure=""
    data=products.objects.all().order_by('-id')[:4]
    featuredproduct=products.objects.order_by("priority")[:4]

    if "userID" in request.session:

        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        wishlistscount=wishlist.objects.filter(user_id_id=user).count()
        customername=user.user_full_name
        q=wishlist.objects.filter(user_id=user)
        profile_picure=user
        count=cart.objects.filter(user_id__id=user.id).count()
        

        
    
    
    if 'viewmen' in request.POST:
        
        result=products.objects.filter(product_gender__contains="male")

        context={
                "view":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                # "q":q

            }
        return render(request,"customers-products.html",context)
    if 'viewwomen' in request.POST:
        
        result=products.objects.filter(product_gender__contains="female")

        context={
                "view":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                # "q":q

            }
        return render(request,"customers-products.html",context)
    if 'brand-adidas' in request.POST:
        
        result=products.objects.filter(product_brand__contains="adidas")

        context={
                "view":result,
                "count":count,

            }
        return render(request,"customers-products.html",context)
    
    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)

        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            context={
                "result":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                # "q":q,

            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html")   

 

    context={
        "count":count,
        "data":data,
        "customername":customername,
        "featuredproduct":featuredproduct,
        "wishlistscount":wishlistscount,
        "dp":profile_picure,



    }

    return render(request,'index.html',context)

def contacts(request):
    user=""
    wishlistscount=""
    customername=""
    count=""
    q=""
    dp=""
    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        count=cart.objects.filter(user_id__id=user.id).count()
        wishlistscount=wishlist.objects.filter(user_id_id=user).count
        customername=user.user_full_name
        q=wishlist.objects.filter(user_id=user)
        dp=user


    
    if "sendmessage" in request.POST:
        fullname=request.POST['fullname']
        email=request.POST['email']
        message=request.POST['message']
        currentdate=date.today()
        obj=contact.objects.create(user_id=user,fullname=fullname,mail=email,message=message,date=currentdate)
        obj.save()
        messages.success(request,"Message send success")
        return redirect("contact")
    
    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            context={
                "result":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                "q":q
                
            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html")    

    context={
        "count":count,
        "customername":customername,
        "wishlistscount":wishlistscount,
        "dp":dp,


        
    }
    return render(request,'contact.html',context)

def about(request):
    user=""
    wishlistscount=""
    customername=""
    count=""
    q=""
    dp=""
    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        count=cart.objects.filter(user_id__id=user.id).count()
        wishlistscount=wishlist.objects.filter(user_id_id=user).count
        q=wishlist.objects.filter(user_id=user)
        dp=user
        customername=user.user_full_name
    
    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        
        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            context={
                "result":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                "q":q
                
            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html")    

    context={
        "count":count,
        "customername":customername,
        "wishlistscount":wishlistscount,
        "dp":dp,
        
        

        
    }
    return render(request,'about.html',context)

def store(request):
    count=""
    wishlistscount=""
    user=""
    dp=""
    q=""
    customername=""
    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        count=cart.objects.filter(user_id__id=user.id).count()
        wishlistscount=wishlist.objects.filter(user_id_id=user).count()
        q=wishlist.objects.filter(user_id=user)
        dp=user
        customername=user.user_full_name
    
    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            context={
                "result":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                "q":q,
                
            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html")    
    
    context={
        "count":count,
        "customername":customername,
        "wishlistscount":wishlistscount,
        "dp":dp,

        
    }
    return render(request,'customers-stores.html',context)
@login_required(login_url="user-login")
def wishlists(request):
    u_id=request.session['userID']
    user=user_reg.objects.get(user__id=u_id)
    customername=user.user_full_name
    wishlists=wishlist.objects.filter(user_id_id=user)
    wishlistscount=wishlist.objects.filter(user_id_id=user).count()
    count=cart.objects.filter(user_id_id=user).count()
    q=wishlist.objects.filter(user_id=user)
    dp=user


    
    
    
    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        
        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            context={
                "result":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                "q":q,
            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html") 
    
    context={
        "customername":customername,
        "wishlists":wishlists,
        "count":count,
        "wishlistscount":wishlistscount,
        "dp":dp,
        

    }
    
    return render(request,"wishlist.html",context)

@login_required(login_url="user-login")
def addwishlists(request,id):
    u_id=request.session['userID']
    user=user_reg.objects.get(user__id=u_id)
    check=wishlist.objects.filter(user_id=user,product_id_id=id).first()
    if not check:
        wishlist.objects.create(user_id=user,product_id_id=id)

    return redirect("customers-products")  
 
@login_required(login_url="user-login")   
def deletewishlists(request,id):
    u_id=request.session['userID']
    user=user_reg.objects.get(user__id=u_id)
    wishlist.objects.filter(user_id=user,product_id=id).delete()
    return redirect("customers-products")
    
   

def customerswishlistremove(request,id):
    remove=wishlist.objects.get(id=id)
    remove.delete()
    return redirect("wishlist")

def productdetails(request,id):
    data=products.objects.get(id=id)
    amt=data.product_price
    offer=data.offer_price
    wishlistscount=""
    count=""
    customername=""
    profile_picure=""
    dp=""
    q=""
    wish=""
    
    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        wishlistscount=wishlist.objects.filter(user_id_id=user).count()
        count=cart.objects.filter(user_id__id=user.id).count()
        profile_picure=user
        customername=user.user_full_name
        dp=edit.objects.filter(user_id_id=user)
        q=wishlist.objects.filter(user_id=user)   
        wish=wishlist.objects.filter(user_id_id=user,product_id=id)
            
        
        
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
    
    # if 'whishlist' in request.POST:
    #     prod=wishlist.objects.create(product_id_id=data.id,user_id=user)
    #     prod.save()
    #     return redirect('product-details',id=id)



    context={
        "bar_one":bar_one,
        "bar_two":bar_two,
        "bar_three":bar_three,
        "bar_four":bar_four,
        "bar_five":bar_five,
        "data":data,
        "review":leavreview,
        "count":count,
        "dp":dp,
        "customername":customername,
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
        "wishlistscount":wishlistscount,
        "wish":wish,
        "userss":userss,
        "dp":profile_picure,



            
        

        }
    if 'cart-btn' in request.POST:
        quantity=request.POST['qty']
        
        amt=int(quantity)*int(offer_prince)
        count=cart.objects.count()
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        obj=cart.objects.create(product_id=data,user_id=user,cart_amount=amt,order_qty=quantity)
        obj.save()
        return redirect('customers-products')
    if 'checkout-btn' in request.POST:
        data1=products.objects.get(id=id)
        name=data1.product_name
        img=data1.product_image
        quantity=request.POST['qty']
        amt=int(quantity)*int(offer_prince)
        current_date=date.today()
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        customername=user.user_full_name
        obj=orders.objects.create(product_id=data,user_id=user,order_amount=amt,order_qty=quantity,ordered_date=current_date)
        obj.save()
        
    


        context_data={
        "data":data,
        "quantity":quantity,
        "amt":amt,
        "count":count,
        "data1":data1,
        "img":img,
        "name":name ,
        "customername":customername,
        }
        query_params = '&'.join([f'{key}={value}' for key, value in context_data.items()])
        redirect_url = f'{reverse("customerssinglecheckout", kwargs={"id": id})}?{query_params}'
        return redirect(redirect_url)
    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            context={
                "result":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                "q":q,
            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html") 

        
        
        
    return render(request,'customers-product-details.html',context)

def customerscheckout(request):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    data=cart.objects.filter(user_id__id=user.id)
    count=cart.objects.filter(user_id__id=user.id).count()
    wishlistscount=wishlist.objects.filter(user_id_id=user).count()
    q=wishlist.objects.filter(user_id=user)
    profile_picure=user

    

    customername=user.user_full_name
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
        "count":count,
        "total":total,
        "free":free,
        "customername":customername,
        "wishlistscount":wishlistscount,
        "saved":saved,
        "dp":profile_picure,


        
    }
    
    if 'paybtn' in request.POST:

        for i in data:
            product=i.product_id
            amts=i.cart_amount
            qty=i.order_qty
            no_of_item=i.product_id.number_of_items
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
    
        
    

    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            context={
                "result":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                "q":q,
            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html")  
    


    return render(request,'customers-checkout.html',context)

def customerssinglecheckout(request,id):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    customername=user.user_full_name
    count=cart.objects.filter(user_id__id=user.id).count
    wishlistscount=wishlist.objects.filter(user_id_id=user).count()
    q=wishlist.objects.filter(user_id=user)
    profile_picure=user


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
        "count":count,
        "customername":customername,
        "totals":to,
        "wishlistscount":wishlistscount,
        "saved":saved,
        "dp":profile_picure,

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

        


    
    
    
    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            context={
                "result":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                "q":q
            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html")   


        
    context={
        "count":count,
        "customername":customername,
        "totals":to,
        "wishlistscount":wishlistscount,
        "saved":saved,
        "dp":profile_picure,

    }

   
    return render(request,'customers-single-checkout.html',{**context_data, **context})

def customersprofile(request):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    users=user_reg.objects.filter(user__id=u_id)
    count=cart.objects.filter(user_id__id=user.id).count()
    wishlistscount=wishlist.objects.filter(user_id_id=user).count()
    ordercount=checkout.objects.filter(user_id_id=user).count()
    q=wishlist.objects.filter(user_id=user)
    profile_picure=user


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
        # Check if a new photo is uploaded, otherwise keep the old one
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            user.img1 = photo
        else:
            photo = user.img1  # Retain the old image if no new image is provided
    
        # Fetch the previous edit object (if exists)
        previous_edit = edit.objects.filter(user_id=user).first()
    
        # Check if a new location is provided, otherwise retain the old location
        location = request.POST.get('location', None)
        if not location and previous_edit:
            location = previous_edit.location  # Retain the old location if no new location is provided
    
        # Delete the previous edit entry (optional, depending on your logic)
        edit.objects.filter(user_id=user).delete()
    
        # Save the user with the updated data (only if a new image provided)
        user.save()
    
        # Create a new edit record with the new or retained location
        edit.objects.create(user_id=user, img=photo, location=location)
    
        return redirect("customers-profile")


    
    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        if searchinput:
            result=products.objects.filter(product_name     =searchinput)
            context={
                "result":result,
                "wishlistscount":wishlistscount,
                "customername":customername,
                "count":count,
                "q":q
            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html")  
    context={
        "count":count,
        "customername":customername,
        "users":users,
        "profile":profile,
        "pro":pro,
        "statuses":statuses,
        "wishlistscount":wishlistscount,
        "ordercount":ordercount,
        "dp":profile_picure,


        
    }  


    
    return render(request,'customers-profile.html',context)



@login_required(login_url='user-login')
def customerscart(request):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    carts=cart.objects.filter(user_id__id=user.id)
    count=cart.objects.filter(user_id__id=user.id).count()
    wishlistscount=wishlist.objects.filter(user_id_id=user).count()
    q=wishlist.objects.filter(user_id=user)
    profile_picure=user


    customername=user.user_full_name

    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            context={
                "result":result,
                "wishlistscount":wishlistscount,
                "count":count,
                "q":q
            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html")    

 
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
        "count":count,
        "free":free,
        "total":total,
        "customername":customername,
        "wishlistscount":wishlistscount,
        "dp":profile_picure,


        
        
    }
    
    return render(request,'cart.html',context)



def cartremove(request,id):
    remove=cart.objects.get(id=id)
    remove.delete()
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
    
    return redirect('customers-profile')


def customerswritereview(request,id):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    count=cart.objects.filter(user_id__id=user.id).count()
    customername=user.user_full_name
    product=products.objects.get(id=id)  
    wishlistscount=wishlist.objects.filter(user_id_id=user).count()
    q=wishlist.objects.filter(user_id=user)
    profile_picure=user


  
    

    
    if request.POST:
        review=request.POST['leave-review']
        image=request.FILES.get('imgupload',None)
        rating1=request.POST["rating"]
        
        today=date.today()
        obj=rating.objects.create(user_id=user,product_id=product,review=review,date=today,taken_image=image,star_rating=rating1)
        obj.save()
        return redirect("/product-details/"+id)
    
    if request.method == "POST":
        searchinput=request.POST.get('searchbox',None)
        if searchinput:
            result=products.objects.filter(product_name__contains=searchinput)
            context={
                "result":result,
                "count":count,
                "wishlistscount":wishlistscount,
                "q":q,

            }
            return render(request,"customers-products.html",context)
        return render(request,"customers-products.html")  
    context={

        "count":count,

        "customername":customername,
        "product":product,
        "wishlistscount":wishlistscount,
        "dp":profile_picure,


        
        
    }  

    return render(request,"write-review.html",context)