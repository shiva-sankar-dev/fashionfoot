from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Login(AbstractUser):  
    userType=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50,null=True)
    def str(self):
        return self.username
    

class user_reg(models.Model):
    user=models.OneToOneField(Login,on_delete=models.CASCADE,null=True)
    user_full_name=models.CharField(max_length=100,null=True)
    img1=models.ImageField(upload_to='profile-image/',null=True)
    user_email=models.EmailField(null=True)
    user_mob_number=models.CharField(max_length=100,null=True)
    user_password=models.TextField(null=True)
    user_cpassword=models.TextField(null=True)

class feedback(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    user_feedback=models.TextField(max_length=500)
    feedback_date=models.DateField()
    


class contact(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    fullname=models.CharField(max_length=100,null=True)
    mail=models.EmailField(max_length=100,null=True)
    message=models.TextField(max_length=400,null=True)
    date=models.DateField(null=True)
    

class products(models.Model):
    # id=models.IntegerField(primary_key=True)
    product_name=models.TextField(max_length=100,null=True)
    product_desc=models.TextField(max_length=300,null=True)
    product_category=models.TextField(max_length=300,null=True)
    product_price=models.IntegerField(null=True)
    product_image=models.ImageField(null=True)
    product_size=models.IntegerField(null=True)
    product_gender=models.TextField(max_length=100,null=True)
    product_brand=models.TextField(max_length=100,null=True)
    product_color=models.TextField(max_length=100,null=True)
    product_date=models.DateField(null=True)
    priority=models.IntegerField(default=5)
    number_of_items=models.IntegerField(null=True)
    offer_price=models.IntegerField(null=True)





class cart(models.Model):

    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE,null=True)
    product_id=models.ForeignKey(products,on_delete=models.CASCADE,null=True)
    cart_amount=models.IntegerField(null=True)
    order_qty=models.IntegerField(null=True)
    # subtotal=models.IntegerField(null=True)


class orders(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    product_id=models.ForeignKey(products,on_delete=models.CASCADE)
    order_amount=models.IntegerField()
    ordered_date=models.DateField()
    order_qty=models.IntegerField(null=True)


class checkout(models.Model):
    ORDER_CONFIRMED="confirm"
    ORDER_PROCESSED="processed"
    ORDER_DELIVERED="delivered"
    ORDER_REJECTED='rejected'
    status_choice=((ORDER_CONFIRMED,'confirm'),
                   (ORDER_PROCESSED,'processed'),
                   (ORDER_DELIVERED,'delivered'),
                   (ORDER_REJECTED,'rejected'),
                   )
    order_status=models.TextField(choices=status_choice,default=ORDER_CONFIRMED)
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE,null=True)
    product_id=models.ForeignKey(products,on_delete=models.CASCADE,null=True)
    f_name=models.TextField(max_length=100,null=True)
    l_name=models.TextField(max_length=100,null=True)
    d_address=models.TextField(max_length=300,null=True)
    h_address=models.TextField(max_length=300,null=True)
    city=models.TextField(max_length=100,null=True)
    state=models.TextField(max_length=100,null=True)
    country=models.TextField(max_length=100,null=True)
    zip_code=models.IntegerField(null=True)
    e_mail=models.EmailField(null=True)
    mobile=models.CharField(max_length=15, null=True)
    cdate=models.DateField(null=True)
    amts=models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    
class savedaddress(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE,null=True)
    f_name=models.TextField(max_length=100,null=True)
    l_name=models.TextField(max_length=100,null=True)
    d_address=models.TextField(max_length=300,null=True)
    h_address=models.TextField(max_length=300,null=True)
    city=models.TextField(max_length=100,null=True)
    state=models.TextField(max_length=100,null=True)
    country=models.TextField(max_length=100,null=True)
    zip_code=models.IntegerField(null=True)
    e_mail=models.EmailField(null=True)
    mobile=models.CharField(max_length=15, null=True)
    
    
    
class edit(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE,null=True) 
    img=models.ImageField(upload_to='profile-image/',default="../static/assets/images/01.png",null=True)
    location=models.TextField(max_length=100,null=True)
    
    
class rating(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE,null=True) 
    product_id=models.ForeignKey(products,on_delete=models.CASCADE,null=True)
    review=models.TextField(max_length=300,null=True)
    taken_image=models.ImageField(null=True)
    date=models.DateField(null=True)
    star_rating = models.PositiveIntegerField(default=0)

    
class wishlist(models.Model):
    
    product_id=models.ForeignKey(products,on_delete=models.CASCADE,null=True)
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE,null=True)
    



class payment(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE) 
    amount=models.IntegerField()
    payment_date=models.DateField()
    

# models of admin.
    
class category(models.Model):

    category_name=models.CharField(max_length=50,null=True)
    category_description=models.CharField(max_length=250,null=True)
    category_price=models.CharField(max_length=50,null=True)
    category_image=models.ImageField(null=True)         