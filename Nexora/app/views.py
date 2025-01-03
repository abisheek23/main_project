from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import  User
from django.contrib import messages
from .models import *
import os

# Create your views here.

def log(req):
    if 'admin' in req.session:
        return redirect(admin_home)
    if 'user' in req.session:
        return redirect (user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            login(req,data)
            if data.is_superuser:
              req.session['admin']=uname   #create session 
              return redirect(admin_home)
            else:
                req.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(req, " invalid user name or password")
            return redirect(login)
    else:
        return render(req,'login.html')
def AU_logout(req):
     logout(req)
     req.session.flush()
     return redirect(log)


    


def admin_home(req):
    if 'admin' in req.session:
       data=prodect.objects.all()
       return render(req,'admin/adminhome.html',{'products':data})
    else:
        return redirect(log)


def add_category(req):
    if 'admin' in req.session:
        if req.method == 'POST':
            name = req.POST['name']
            Category.objects.create(name=name.lower())
            categories = Category.objects.all()
            return render(req, 'admin/add_category.html', {'categories': categories})
        else:
            categories = Category.objects.all()
            return render(req, 'admin/add_category.html', {'categories': categories})
    else:
          return redirect(log)
    
def delete_category(req, id):
    if 'admin' in req.session:
        try:
            category = Category.objects.get(id=id)
            category.delete()
        except Category.DoesNotExist:
            pass  # You can add an error message here if needed
        return redirect(add_category)
    else:
        return redirect(log)

def add_products(req) :
    if 'admin' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            pname=req.POST['name']
            description=req.POST['description']
            pprice=req.POST['price']
            offer_price=req.POST['off_price']
            cate=req.POST['category']
            pstock=req.POST['stock']
            file=req.FILES['image']
            cat=Category.objects.get(pk=cate)
            data=prodect.objects.create(pid=pid,name=pname,dis=description,price=pprice,offer_price=offer_price,category=cat,stoct=pstock,img=file)
            data.save()
            return redirect(admin_home)
        else:
            cate=Category.objects.all()
            return render(req,'admin/add_prodects.html',{'cate':cate})
    else:
        return redirect(log)



def view_pro(req):
    cate_id = req.GET.get('category', None)
    cate = Category.objects.all()  # Fetch all categories
    
    if cate_id:  # If category filter is applied
        products = prodect.objects.filter(category__id=cate_id)  # Filter products based on the category ID
    else:  # If no category filter is provided
        products = prodect.objects.all()  # Fetch all products

    # Render the products and categories on the template
    return render(req, 'admin/view_product.html', {'product': products, 'cate': cate})



def edit_product(req,pid):
    if req.method=='POST':
        p_id=req.POST['pid']
        pname=req.POST['name']
        description=req.POST['description']
        pprice=req.POST['price']
        offer_price=req.POST['off_price']
        cate=req.POST['category']
        pstock=req.POST['stock']
        file=req.FILES.get('image')
        
        if file:
            prodect.objects.filter(pk=pid).update(pid=p_id,name=pname,dis=description,price=pprice,offer_price=offer_price,stoct=pstock)
            data=prodect.objects.get(pk=pid)
            data.img=file
            data.save()
        else:
            prodect.objects.filter(pk=pid).update(pid=pid,name=pname,dis=description,price=pprice,offer_price=offer_price,stoct=pstock)
        return redirect(admin_home)

    else:
         data=prodect.objects.get(pk=pid)
         return  render(req,'admin/edit_product.html',{'data':data})
    
def delet_product(req,pid):
    data=prodect.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(admin_home)



       

def reg(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        # print(email)
        # send_mail('account created', 'you created a account in e_com', settings.EMAIL_HOST_USER, [email])

        try:
          data=User.objects.create_user(first_name=uname, username=email,email=email,password=pswd)
          data.save()
          return redirect (req,login)
        except:
           messages.warning(req, " already used ")
           return redirect(reg)
    else:
        return render(req,'user/registration.html')
    
def user_home(req):
    products = prodect.objects.all() 
    
    cate=Category.objects.all()
   

    if 'user' in req.session:
        return render(req,'user/user_home.html', { 'product': products,'cate':cate})
    else:
        return redirect (login)
    
def shop(req):
    cate_id = req.GET.get('category', None)
    cate = Category.objects.all()  
    
    if cate_id:  # If category filter is applied
        products = prodect.objects.filter(category__id=cate_id)  
    else:  
        products = prodect.objects.all()[::-1]  
   

    if 'user' in req.session:
        return render(req,'user/shop.html', { 'product': products,'cate': cate})
    else:
        return redirect (login)
    
def viewpro(req,pid):
    products=prodect.objects.get(pk=pid)
    if 'user' in req.session:
       return render(req,'user/viewpro.html',{'product':products})
    
def add_to_cart(req,pid):
    product=prodect.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        data=Cart.objects.get(product=product,user=user)
        data.qty+=1
        data.save()
    except:
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)[::-1] 

    return render (req,'user/cart.html',{'cart':data})

def qty_in(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty+=1
    data.save()
    return redirect(view_cart)

def delete_cart_item(req, id):
    if 'user' in req.session:
        try:
            Cartitem = Cart.objects.get(id=id)
            Cartitem.delete()
            return redirect(view_cart)
        except Cart.DoesNotExist:
            pass  # You can add an error message here if needed
            return redirect(user_home)
    else:
        return redirect(view_cart)
    
def qty_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    print(data.qty)
    if data.qty==0:
        data.delete()
    return redirect(view_cart)
def qty_in(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty+=1
    data.save()
    return redirect(view_cart)


# def pro_buy(req,pid): # to buy product directly from product_dtls page
#     product=prodect.objects.get(pk=pid)
#     user=User.objects.get(username=req.session['user'])
#     qty=1
#     price=product.offer_price
#     buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
#     buy.save()
#     return redirect(bookings)

def bookings(req,pid,aid):
    product=prodect.objects.get(pk=pid )
    adress=Adress.objects.get(pk=aid)
    return render (req,'user/bookings.html',{'products':product,'adress':adress} )
def add_adress(req,pid):
    if 'user' in req.session:
        if req.method=='POST':
       
         phno=req.POST['ph_no']
         state=req.POST['state']
         district=req.POST['district']
         adress=req.POST['adress']
         user=User.objects.get(username=req.session['user'])
         data=Adress.objects.create(phno=phno,position=state,district=district,Adress=adress,user=user)
         data.save()
         return redirect('bookings',pid=pid )
        return render(req,'user/adress.html')
    else:
        return redirect(log)

 