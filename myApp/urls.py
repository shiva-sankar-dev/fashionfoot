from django.contrib import admin
from django.urls import include, path
from myApp import views

urlpatterns = [

    path('registration/',views.registration,name='user-registration'),
    path('login/',views.customerslogin,name='user-login'),
    # path('dash/',views.dashboard),
    path('product/',views.product,name='products'),
    path('add-product/',views.addproduct,name='add-product'),
    path('customer-home/',views.customershome,name='customers-home'),
    path('customers-products/',views.customersproducts,name='customers-products'),
    path('',views.customershomecontent,name='customers-home-content'),
    path('contact/',views.contacts,name='contact'),
    path('about/',views.about,name='about'),
    path('store/',views.store,name='store'),
    path('wishlist/',views.wishlists,name='wishlist'),
    path('add-wishlist/<id>',views.addwishlists,name='add-wishlist'),
    path('delete-wishlist/<id>',views.deletewishlists,name='delete-wishlist'),
    path('customers-wishlist-remove/<id>',views.customerswishlistremove,name='customers-wishlist-remove'),
    path('product-details/<id>',views.productdetails,name='product-details'),
    path('customers-checkout/',views.customerscheckout,name='customers-checkout'),
    path('customers-single-checkout/<id>',views.customerssinglecheckout,name='customerssinglecheckout'),
    path('customer-profile/',views.customersprofile,name='customers-profile'),
    path('customer-cart/',views.customerscart,name='customers-cart'),
    path('customer-cart-remove/<int:id>',views.cartremove,name='customers-cart-remove'),
    path('customer-logout/',views.customerslogout,name='customers-logout'),
    path('customer-forget-password/',views.forgetpassword,name='customer-forget-password'),
    path('cart-increment/<int:id>',views.cartincrement,name='cart-increment'),
    path('cart-decrement/<int:id>',views.cartdecrement,name='cart-decrement'),
    path('customers-profile-order-remove/<id>',views.customersprofileorderremove,name='customers-profile-order-remove'),
    path('customers-write-review/<id>',views.customerswritereview,name='customers-write-review'),

           
    


]