from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .form import CustomUserForm,CustomUserUpdateForm
from django.contrib.auth import logout
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
import random
# Create your views here.

def index(request):
    products=Products.objects.filter(status=0,trending=1)
    return render(request,'index.html',{'products':products})



def update(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/login')  
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'update.html', {'form': form})



def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

def login_page(request):
    if request.method == "POST":
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        email = request.POST.get('email')
        user = authenticate(request, username=name, password=pwd, email=email)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login')
    return render(request, 'login.html')
def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request,"Registration completed")
            return redirect('/')
    return render(request,'register.html',{'form':form})

def collections(request):
    categories = Category.objects.filter(status=0)
    return render(request, 'collections.html', {'categories': categories})

def collectionsview(request, name):
    if Category.objects.filter(status=0, name=name).exists():
        category = Category.objects.get(status=0, name=name)
        products = Products.objects.filter(category=category)
        return render(request, 'product.html', {'products': products,'title':category.name})
    else:
        messages.warning(request, "No such category")
        return redirect('collections')
def productview(request, name):
    if Products.objects.filter(status=0, name=name).exists():
        product = Products.objects.get(status=0, name=name)
        return render(request, 'product_view.html', {'product': product})
    else:
        messages.warning(request, "No such category")
        return redirect('collections')
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_qty = data.get('product_qty')
                product_id = data.get('pid')
                
                if not product_id:
                    return JsonResponse({'status': 'Invalid Product ID'}, status=400)
                
                product_id = int(product_id)  # Ensure product_id is an integer
                product_status = Products.objects.get(id=product_id)
                
                if product_status:
                    if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                        return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                    else:
                        if product_status.quantity >= product_qty:
                            Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                            return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                        else:
                            return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON'}, status=400)
            except Products.DoesNotExist:
                return JsonResponse({'status': 'Product Not Found'}, status=404)
            except ValueError:
                return JsonResponse({'status': 'Invalid Product ID'}, status=400)
            except Exception as e:
                return JsonResponse({'status': str(e)}, status=500)
        else:
           
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)
     

def cart(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"cart.html",{'cart':cart})
    else:
        return redirect("/")
def removecart(request,id):
    cartitem=Cart.objects.get(id=id)
    cartitem.delete()
    return redirect("/cart")


def checkout(request):
   
    
            cartitems=Cart.objects.filter(user=request.user)
            total_price=0
            for item in cartitems:
                total_price=total_price+item.product.selling_price*item.product_qty

            userprofile=Profile.objects.filter(user=request.user).first()
    
            context={'cartitems':cartitems,'total_price':total_price,'userprofile':userprofile}


            return render(request,'checkout.html',context)
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, OrderItem, Cart,Profile
import random

def placeorder(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            currentuser=User.objects.filter(id=request.user.id).first()

            if not currentuser.first_name:
                currentuser.first_name=request.POST.get('fname')
                currentuser.last_name= request.POST.get('lname')
                currentuser.save()
            if not Profile.objects.filter(user=request.user):
                userprofile=Profile()
                userprofile.user=request.user
                userprofile.phone = request.POST.get('phone')
                userprofile.address = request.POST.get('address')
                userprofile.city = request.POST.get('city')
                userprofile.state = request.POST.get('state')
                userprofile.country = request.POST.get('country')
                userprofile.save()


            neworder = Order()
            neworder.user = request.user
            neworder.fname = request.POST.get('fname')
            neworder.lname = request.POST.get('lname')
            neworder.email = request.POST.get('email')
            neworder.phone = request.POST.get('phone')
            neworder.address = request.POST.get('address')
            neworder.city = request.POST.get('city')
            neworder.state = request.POST.get('state')
            neworder.country = request.POST.get('country')
            neworder.pincode = request.POST.get('pincode')
            neworder.payment_mode = request.POST.get('payment_mode')
            neworder.payment_id = request.POST.get('payment_id')

            cart = Cart.objects.filter(user=request.user)
            cart_total_price = 0
            for item in cart:
                cart_total_price += item.product.selling_price * item.product_qty

            neworder.total_price = cart_total_price
            trackno = 'nithes' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=trackno).exists():
                trackno = 'nithes' + str(random.randint(1111111, 9999999))

            neworder.tracking_no = trackno
            neworder.save()

            neworderitems = Cart.objects.filter(user=request.user)
            for item in neworderitems:
                OrderItem.objects.create(
                    order=neworder,
                    product=item.product,
                    price=item.product.selling_price,
                    quantity=item.product_qty
                )

            # Clear the user's cart after placing the order
            Cart.objects.filter(user=request.user).delete()

            messages.success(request, "Your order has been placed successfully.")
            payMode=request.POST.get('payment_mode')
            if (payMode=="Paid by Razorpay"):
                return JsonResponse({'status':"Your order has been placed successfully"})
              # Redirect to a success page or homepage

        else:
            return JsonResponse({'status':"Order Not placed"})
              # Handle GET request properly, if needed

    else:
        return JsonResponse({'status':"Order Not placed"})
          # Redirect if user is not authenticated

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart  # Adjust this import based on your actual model structure

@login_required
def razorpaycheck(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_price = 0
        
        for item in cart:
            total_price += item.product.selling_price * item.product_qty
        
        return JsonResponse({
            'total_price': total_price
        })
    else:
        return JsonResponse({
            'error': 'User is not authenticated'
        }, status=401)  # Return Unauthorized status if user is not authenticated

def myorders(request):
    orders=Order.objects.filter(user=request.user)
    context={'orders':orders}

    return render(request,'my-orders.html',context)
def vieworder(request,trackno):
    order=Order.objects.filter(tracking_no=trackno).filter(user=request.user).first()
    orderitems=OrderItem.objects.filter(order=order)
    context={'order':order,'orderitems':orderitems}
    return render(request,'vieworder.html',context)

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def generate_pdf(request, order_id):
    # Fetch order details from the database
    order = get_object_or_404(Order, id=order_id)
    orderitems = OrderItem.objects.filter(order=order)

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill-{order.id}.pdf"'

    p = canvas.Canvas(response)
    
    # Company details
    p.drawString(100, 750, "Company Name: SNK")
    p.drawString(100, 735, "Address: 1568, Church Road Kashmere Gate,")
    p.drawString(100, 720, "New Delhi, Delhi, India - 110006.")

    # Order details
    y = 700
    p.drawString(100, y, f"First Name: {order.fname}")
    p.drawString(100, y-15, f"Last Name: {order.lname}")
    p.drawString(100, y-30, f"Email: {order.email}")
    p.drawString(100, y-45, f"Phone: {order.phone}")
    p.drawString(100, y-60, f"Address:")
    p.drawString(120, y-75, f"{order.address}")
    p.drawString(120, y-90, f"{order.city}, {order.state}")
    p.drawString(120, y-105, f"{order.country} - {order.pincode}")

    # Order items
    y -= 130
    for item in orderitems:
        p.drawString(100, y, f"Product: {item.product.name}")
        p.drawString(300, y, f"Quantity: {item.quantity}")
        p.drawString(400, y, f"Price: {item.price}")
        y -= 15

    # Grand total, payment mode, status, tracking number
    y -= 30
    p.drawString(100, y, f"Grand Total: {order.total_price}")
    y -= 15
    p.drawString(100, y, f"Payment Mode: {order.payment_mode}")
    y -= 15
    p.drawString(100, y, f"Order Status: {order.status}")
    y -= 15
    p.drawString(100, y, f"Tracking Number: {order.tracking_no}")

    p.showPage()
    p.save()

    return response


from django.shortcuts import render
from .models import Products

def product_list(request):
    products = Products.objects.all()
    return render(request, 'api_products.html', {'products': products})
