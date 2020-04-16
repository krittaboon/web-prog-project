from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from app.models import Program,Order
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
# Create your views here.
def home(request):
    programs = None
    programs = Program.objects.all().filter(available=True)
    return render(request,'index.html',{'programs':programs})

def register(request) :
    programs = None
    programs = Program.objects.all().filter(available=True)
    return render(request,'register.html',{'programs':programs})

def register_result(request) :
    username = request.POST.get('username')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    repassword = request.POST.get('repassword')

    if password==repassword:
        if User.objects.filter(username=username).exists():
            messages.info(request,'user exist')
            print("user exist")
            return redirect('/register')
        elif User.objects.filter(email=email).exists():
            print("email exist")
            messages.info(request,'email exist')
            return redirect('/register')
        else:    
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=firstname,
                last_name=lastname)

            user.save()    
            return redirect('/')
    else:
         messages.info(request,'Not match password')
         return redirect('/register')

def login(request) :
    programs = None
    programs = Program.objects.all().filter(available=True)
    return render(request,'login.html',{'programs':programs})

def login_result(request) :
    username = request.POST.get('username')
    password = request.POST.get('password')

    user=auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        return redirect('/')
    else:
        messages.info(request,'Username and/or Password incorrect.')
        return redirect('/login')

def logout(request):
    
    auth.logout(request)
    return redirect('/')

 

def programPage(request,program_slug):

    programs = None
    programs = Program.objects.all().filter(available=True)   
    try:
        program = Program.objects.get(slug=program_slug) 
       
    except Exception as e :
        raise e  

    return render(request,'program_page.html',{'program':program,'programs':programs})

@login_required(login_url='login')
def programBook(request,program_slug):

    stripe.api_key=settings.SECRET_KEY
    
    description="Payment Online"
    data_key=settings.PUBLIC_KEY

    checkin_date = request.GET.get('checkin_date')
    adults = request.GET.get('adults')
    children = request.GET.get('children')
    

    programs = None
    programs = Program.objects.all().filter(available=True)   
    try:
        program = Program.objects.get(slug=program_slug) 
       
    except Exception as e :
        raise e 



    total = (int(children)+int(adults))*program.promotion_price 
    net = total*11/10
    stripe_total=int(net*100) 

    if request.method=="POST":
        try :
            token=request.POST['stripeToken']
            email=request.POST['stripeEmail']
            name=request.POST['stripeBillingName']
            address=request.POST['stripeBillingAddressLine1']
            city=request.POST['stripeBillingAddressCity']
            postcode=request.POST['stripeShippingAddressZip']
            customer=stripe.Customer.create(
                email=email,
                source=token
            )
            charge=stripe.Charge.create(
                amount=stripe_total,
                currency='thb',
                description=description,
                customer=customer.id
            )
            
            order=Order.objects.create(
                name=name,
                address=address,
                city=city,
                postcode=postcode,
                total=total,
                email=email,
                token=token,
                program=program.name,
                checkin_date=checkin_date,
                adults=adults,
                children=children
            )
            order.save()

           
            return redirect('/')

        except stripe.error.CardError as e :
            return False , e

    messages.info(request,"Trip date : "+checkin_date)
    messages.info(request,"Guests : "+str(int(children)+int(adults)))
    messages.info(request,"Trip cost : ฿"+str(total))
    messages.info(request,"Booking free + Tax : ฿"+str(total/10))
    messages.info(request,"Accident insurance : Free")
    messages.info(request,"Total price : ฿"+str(total*11/10)) 

    return render(request,'program_book.html',dict(program=program,programs=programs,data_key=data_key,stripe_total=stripe_total,description=description)) 






