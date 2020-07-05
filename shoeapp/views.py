from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.


def index(request):
    proobj = Product.objects.all()
    menobj = Product.objects.filter(category='MEN')
    womenobj = Product.objects.filter(category='WOMEN')
    if request.session.has_key('user_id'):
        userobj = request.session['user_id']
        logobj = Login.objects.get(pk=userobj)
        userobjs = User.objects.get(loginid=logobj)
        cartobj = Cart.objects.filter(user_id=logobj).count()
        return render(request, 'index.html', {'user_info': userobjs, 'pros': proobj,'cartitems':cartobj,'mens': menobj, 'womens': womenobj})
    return render(request, 'index.html', {'user_info': False, 'pros': proobj,'mens': menobj, 'womens': womenobj})


def dashboard(request):
    proobj = Product.objects.all()[:10]
    userobj = User.objects.all()
    bookingobj = Booking.objects.exclude(status='Delivered')
    bookitems = Bookingitem.objects.all()
    bookaddress = BookingAddress.objects.all()
    totalorders = Booking.objects.all().count()
    return render(request, 'adminhome/dashboard.html',{'bookaddress':bookaddress,'bookitems': bookitems,'pro': proobj, 'user': userobj,'bookings':bookingobj,'totalorders': totalorders})


def removeproduct(request, prd_id):
    try:
        proobj = Product.objects.get(pk=prd_id)
    except:
        return dashboard(request)
    else:
        proobj.delete()
    return dashboard(request)


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')

        if username == 'admin' and password == 'admin':
            return dashboard(request)
        else:
            if Login.objects.filter(username=username, password=password).exists():
                logobj = Login.objects.get(username=username, password=password)
                request.session['user_id'] = logobj.id
                userobj = User.objects.get(loginid=logobj.id)
                return index(request)
            else:
                return HttpResponse("Wrong Password or Username")
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        paword = request.POST.get('password')
        loginobj = Login()
        loginobj.username = uname
        loginobj.password = paword
        loginobj.save()

        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        regobj = User()
        regobj.loginid = loginobj
        regobj.fname = fname
        regobj.lname = lname
        regobj.email = email
        regobj.gender = gender
        regobj.isapprove = True
        regobj.isdelete = False
        regobj.save()
        return render(request, 'login.html')
    return render(request, 'register.html')


def logout(request):
    try:
        del request.session['user_id']
    except:
        return index(request)
    return render(request, 'index.html')


def showuser(request):
    userobj = User.objects.all()
    return render(request, 'adminhome/userdetails.html', {'userinfo':userobj})


def removeuser(request, user_id):
    try:
        userobj = Login.objects.get(pk=user_id)
    except:
        return showuser(request)
    else:
        userobj.delete()
        return showuser(request)


def addproduct(request):
    if request.method == "POST":
        productname = request.POST.get('pname')
        brandname = request.POST.get('bname')
        material = request.POST.get('leather')
        colour = request.POST.get('color')
        price = request.POST.get('price')
        category = request.POST.get('category')
        producttype = request.POST.get('ptype')
        size = request.POST.get('size')
        image = request.FILES['image']
        qty = request.POST.get('stock')

        proobj = Product()
        proobj.productname = productname
        proobj.brandname = brandname
        proobj.material = material
        proobj.colour = colour
        proobj.price = price
        proobj.quantity = qty
        proobj.category = category
        proobj.producttype = producttype
        proobj.image = image
        proobj.size = size
        proobj.save()
        return dashboard(request)
    return render(request, 'adminhome/addproduct.html')


def showcart(request):
    if request.session.has_key('user_id'):
        logobj = Login.objects.get(pk=request.session['user_id'])
        userobj = User.objects.get(loginid=logobj)
        cartobj = Cart.objects.filter(user_id=logobj)
        prdobj = Product.objects.all()
        return render(request, 'cart.html', {'products':prdobj, 'carts': cartobj, 'userinfo':userobj})
    else:
        return render(request, 'login.html')


def mycart(request, prd_id):
    if request.session.has_key('user_id'):
        logobj = Login.objects.get(pk=request.session['user_id'])
        prdobj = Product.objects.get(pk=prd_id)

        if Cart.objects.filter(prd_id=prdobj, user_id=logobj).exists():
            return HttpResponse("Item already in Cart")
        else:
            cartobj = Cart()
            cartobj.user_id = logobj
            cartobj.prd_id = prdobj
            cartobj.save()
            print("item added to cart")
    else:
        return render(request, 'login.html')
    return index(request)


def removecart(request, cart_id):
    cartobj = Cart.objects.get(pk=cart_id)
    cartobj.delete()
    return showcart(request)


def viewbooking(request):
    return render(request, 'booking.html')


def getbookingdata(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        country = request.POST.get('country')

        cartobj = Cart.objects.filter(user_id=request.session['user_id'])
        totalmoney = 0

        try:
            for cart in cartobj:
                itemobj = Product.objects.get(id=cart.prd_id_id)
                itemobj.quantity -= 1
                itemobj.save()
        except:
            return HttpResponse("Sorry something went wrong")
        else:

            for cart in cartobj:
                totalmoney += cart.prd_id.price


            obj1 = Booking()
            obj1.user_id = Login.objects.get(id=request.session['user_id'])
            obj1.totalprice = totalmoney
            obj1.save()

            for cart in cartobj:
                obj2 = Bookingitem()
                obj2.booking_id = obj1
                obj2.product_id = Product.objects.get(id=cart.prd_id_id)
                obj2.save()

            obj3 = BookingAddress()
            obj3.booking_id = obj1
            obj3.address = address
            obj3.country = country
            obj3.pincode = pincode
            obj3.state = state
            obj3.phone = phone
            obj3.email = email
            obj3.save()

            cartobj.delete()

            return index(request)


def viewbymen(request):
    proobj = Product.objects.filter(category='MEN')
    if request.session.has_key('user_id'):
        userobj = request.session['user_id']
        logobj = Login.objects.get(pk=userobj)
        userobjs = User.objects.get(loginid=logobj)
        cartobj = Cart.objects.filter(user_id=logobj).count()
        return render(request, 'index.html', {'user_info': userobjs, 'pros': proobj,'cartitems':cartobj})
    return render(request, 'index.html', {'user_info': False, 'pros': proobj})


def viewbywomen(request):
    proobj = Product.objects.filter(category='WOMEN')
    if request.session.has_key('user_id'):
        userobj = request.session['user_id']
        logobj = Login.objects.get(pk=userobj)
        userobjs = User.objects.get(loginid=logobj)
        cartobj = Cart.objects.filter(user_id=logobj).count()
        return render(request, 'index.html', {'user_info': userobjs, 'pros': proobj,'cartitems':cartobj})
    return render(request, 'index.html', {'user_info': False, 'pros': proobj})


def tracker(request):
    if request.session.has_key('user_id'):
        logobj = Login.objects.get(id=request.session['user_id'])
        if Booking.objects.filter(user_id=logobj).exists():
            obj = Booking.objects.filter(user_id=logobj)
            trackobj = logobj.booking_set.all()
            print(trackobj)
            return render(request, 'tracker.html',{'books':trackobj})
        return render(request, 'tracker.html')
    return login(request)


def updateproduct(request, prdid):
    prdobj = Product.objects.get(id=prdid)
    if request.method == 'POST':
        pname = request.POST.get('pname')
        bname = request.POST.get('bname')
        size = request.POST.get('size')
        types = request.POST.get('leather')
        color = request.POST.get('color')
        price = request.POST.get('price')
        category = request.POST.get('category')
        ptype = request.POST.get('ptype')
        qty = request.POST.get('stock')
        try:
            img = request.FILES['image']
        except:
            pass
        else:
            prdobj.image = img
            prdobj.save()

        prdobj.productname = pname
        prdobj.brandname = bname
        prdobj.size = size
        prdobj.quantity = qty
        prdobj.material = types
        prdobj.colour = color
        prdobj.price = price
        prdobj.producttype = ptype
        prdobj.category = category
        prdobj.save()

        return dashboard(request)

    return render(request, 'adminhome/updateproduct.html',{'prd': prdobj})


def updatebookingstatus(request):
    if request.method == 'POST':
        bookid = request.POST.get('bookid')
        status = request.POST.get('status')

        bookobj = Booking.objects.get(id=bookid)
        bookobj.status = status
        bookobj.save()

        return dashboard(request)