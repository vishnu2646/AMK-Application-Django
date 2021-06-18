from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.db.models import Count,Sum
from django.db.models.aggregates import Sum
from django.contrib.auth import authenticate,logout,login as auth_login
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from _datetime import date
import datetime
import razorpay
# Create your views here.
@login_required(login_url="signin")
def index(request):
    if request.method == "GET":
        form = OrderForm()
        return render(request,'index.html',{'form':form})
    if request.method == 'POST':
        user =  request.user
        order = Order()
        order.customer = user
        order.name = request.POST['name']
        order.quantity = request.POST['quantity']
        order.status = request.POST['status']
        order.save()
        return redirect('orders')
    return render(request,'index.html')

@login_required(login_url="login")
@allowed_users(allowed_roles=['customer'])
def products(request):
    orders = Order.objects.filter(customer=request.user)
    result = Order.objects.filter(customer=request.user).values('name').annotate(total_amt=Sum('quantity'))
    context={
        'orders':orders,
        "result":result,
    }
    return render(request,'products.html',context)

@login_required(login_url="signin")
@admin_only
def delevery(request):
    items = Item.objects.all()
    orders = Order.objects.all()
    result = Order.objects.values('name').annotate(total_amt=Sum('quantity'))
    milk = Order.objects.filter(name='milk').aggregate(Sum('quantity'))
    curd = Order.objects.filter(name='curd').aggregate(Sum('quantity'))
    scurd = Item.objects.filter(name='Curd').aggregate(Sum('quantity'))
    smilk = Item.objects.filter(name='Milk').aggregate(Sum('quantity'))
    a = smilk['quantity__sum']
    b = milk['quantity__sum']
    c = curd['quantity__sum']
    d = scurd['quantity__sum']
    res = a-b
    result1 = d-c
    context={
        'orders':orders,
        'result':result,
        'items':items,
        'res':res,
        'result1':result1
    }
    return render(request,'deliveryboy.html',context)

@login_required(login_url="signin")
@allowed_users(allowed_roles=['customer'])
def pricelist(request):
    return render(request,'pricelist.html')

def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			auth_login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')
	context = {}
	return render(request, 'login.html', context) 

def adminlogin(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			auth_login(request, user)
			return redirect('delivery')
		else:
			messages.info(request, 'Username OR password is incorrect')
	context = {}
	return render(request, 'admin-login.html', context) 


def logoutUser(request):
    logout(request)
    return redirect('signin')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request,'An Account was Creates for '+ username)
            return redirect("signin")
    context = {
        'form':form
    }
    return render(request,'register.html',context)

def deliveryupdate(request,pk):
    if request.method == 'GET':
        order = get_object_or_404(Order,pk=pk)
        form = OrderForm(initial={
            'status':order.status,
            'name':order.name,
            'quantity':order.quantity
        })
        return render(request,'index.html',{'form':form})

    if request.method == 'POST':
        order = get_object_or_404(Order,pk=pk)
        order.status = request.POST.get('status')
        order.save()
        return redirect('delivery')

@login_required(login_url="signin")
@allowed_users(allowed_roles=['customer'])
def caluclation(request):
    filters = Order.objects.filter(date__gte=date(2020,10,1),date__lte=date(2021,6,12))
    con = {
        "filteres":filters
    }
    if request.method == 'POST':
        maxi = request.POST.get('date_max').split('-')
        mini = request.POST.get('date_min').split('-')
        #orderfilter = Order.objects.filter(date__gte=datetime.date(int(mini[0]),int(mini[1]),int(mini[2])),date__lte=datetime.date(int(maxi[0]),int(maxi[1]),int(maxi[2]))).aggregate(Sum('quantity'))
        orderfilter = Order.objects.filter(date__gte=datetime.date(int(mini[0]),int(mini[1]),int(mini[2])),date__lte=datetime.date(int(maxi[0]),int(maxi[1]),int(maxi[2])))
        con = {
            'orderfilters':orderfilter,
        }
    return render(request,'calc.html',con)

def payment(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))*100
        client = razorpay.Client(auth=('rzp_test_5xu39CbqhRl6vA','sbHd8Laqb7WbCoSkT3tOLcz4'))
        response_payment = client.order.create(dict(amount=amount,currency='INR'))
        order_id = response_payment['id']
        order_status = response_payment['status']
        if order_status == 'created':
            payment = Payment(
                amount = amount,
                order_id = order_id
            )
            payment.save()
            response_payment['amount'] = amount
            form = PaymentForm(request.POST or None)
            return render(request,'payment.html',{'form':form,'payment':response_payment})
    form = PaymentForm()
    context = {
        'form':form
    }
    return render(request,'payment.html',context)

def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }
    client = razorpay.Client(auth=('rzp_test_5xu39CbqhRl6vA','sbHd8Laqb7WbCoSkT3tOLcz4'))
    try:
        status = client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id = response['razorpay_order_id'])
        payment.razorpay_payment_id = response['razorpay_payment_id']
        payment.paid = True
        payment.save()
        return render(request,'success.html',{'status':True})
    except:
        return render(request,'success.html',{'status':False})