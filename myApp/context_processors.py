from .views import *


def customersheaderandfooter(request):
    customername=""
    count=""
    wishlistscount=""
    dp=""
    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        count=cart.objects.filter(user_id__id=user.id).count()
        wishlistscount=wishlist.objects.filter(user_id_id=user).count
        dp=user
        customername=user.user_full_name
        
    return{
                "count":count,
                "wishlistscount":wishlistscount,
                "customername":customername,
                "dp":dp,
            
        }

