from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import food, r_attribute, c_attribute, order, sub_order, Otp_Confirmation
import json
import datetime


# Create your views here.

def home(request):
    user = request.user
    if user.is_authenticated:
        check = ''
        for i in user.email:
            if i=='@':
                break
            else:
                check+=i

        parent=r_attribute.objects.filter(parent=user)

        if check==user.username and len(parent)==0:
            existance_check=c_attribute.objects.filter(parent=request.user)

            if not len(existance_check)==0:
                if datetime.datetime.now().hour>20 or datetime.datetime.now().hour<9:
                    return render (request , 'night.html')

                messages.info(request, 'In case the restaurant/restaurants you are ordering from are far away from you, order at your own risk.')

                return redirect(f'/market-place/user/{user.username}')
            else:
                return render(request, 'market/pending_profile.html')

        else:
            existance_check=r_attribute.objects.filter(parent=request.user)
            if not len(existance_check)==0:
                if not request.user.is_staff:
                    return redirect(f'/collab/restaurant/admin/{user.username}')
            else:
                return render(request, 'collabs/pending_profile.html')
    return redirect('/')



def foods(request, category):
    if datetime.datetime.now().hour>20 or datetime.datetime.now().hour<9:
        return render (request , 'night.html')

    foods=food.objects.filter(category=category, in_stock=True)
    user=request.user.username
    
    parameters = {'foods': foods, 'category': category, 'username': user}
    return render(request, 'market/foods.html', parameters)



def restaurant(request, name):
    if datetime.datetime.now().hour>20 or datetime.datetime.now().hour<9:
        return render (request , 'night.html')
    user = User.objects.filter(username=name)[0]
    parent_id = user.id
    rest = r_attribute.objects.filter(parent=parent_id)[0]
    
    customer=request.user.username
    
    food_categories = food.objects.values('category', 'by_restaurant')
    food_categories = food_categories.filter(by_restaurant=parent_id)

    menu=[]

    categories = {item['category'] for item in food_categories}
    for category in categories:
        foods=food.objects.filter(category=category, by_restaurant=parent_id, in_stock=True)
        menu.append([category, foods])
    
    parameters = {'restaurant': rest, 'menu': menu, 'username': customer}
    return render(request, 'market/restaurant.html', parameters)



def customer_auth(request, name):
    if datetime.datetime.now().hour>20 or datetime.datetime.now().hour<9:
        return render (request , 'night.html')

    messages.info(request, 'In case the restaurant/restaurants you are ordering from are far away from you, order at your own risk.')

    food_categories = food.objects.values('category', 'food_id')

    feeds = food.objects.all()
    feed_list=[[i.feedback, i.food_id] for i in feeds]
    feed_list.sort()
    feed_list=feed_list[-1:-6:-1]

    feed_list=[i[1] for i in feed_list]

    best_sellers=[]
    for i in feed_list:
        if food.objects.filter(food_id=i)[0].in_stock:
            best_sellers.append(food.objects.filter(food_id=i)[0])

    restaurants = r_attribute.objects.all()
    menu = []

    categories = {item['category'] for item in food_categories}
    for category in categories:
        foods=food.objects.filter(category=category, in_stock=True)
        menu.append([category, foods])

    parameters = {'menu': menu, 'best_sellers': best_sellers, 'restaurants': restaurants, 'user': request.user, 'username': request.user.username, 'current_time': datetime.datetime.now().hour}

    user = request.user
    if user.is_authenticated:
        check = ''
        for i in user.email:
            if i=='@':
                break
            else:
                check+=i

        parent=r_attribute.objects.filter(parent=user)

        if check==name and len(parent)==0:
            existance_check=c_attribute.objects.filter(parent=request.user)

            if not len(existance_check)==0:
                Orders = order.objects.filter(ordered_by=request.user, net_delivery_status=False)
                l=[]

                if len(Orders)==0:
                    message = "No orders pending!"
                    parameters['empty_cart_message'] = message

                for item in Orders:
                    SubOrders = sub_order.objects.filter(parent_order=item, delivery_status=False)

                    if len(SubOrders)==0:
                        item.net_delivery_status = True
                        item.save()
                        return redirect(f'/market-place/user/{request.user}/')

                    l2=[]
                    for sub in SubOrders:
                        get_order_ids=sub.ordered_ids.split(',')
                        order_ids = [i.split(':') for i in get_order_ids]

                        l1=[[], sub.total_preparation_time_in_minutes, sub]

                        for i, j in order_ids:
                            FoodItem=food.objects.filter(food_id=int(i))[0]
                            FoodItem.feedback += 1
                            FoodItem.save()

                            l1[0].append([FoodItem, int(j)])
                            food_parent = FoodItem.by_restaurant

                        l1.append(r_attribute.objects.filter(parent=food_parent)[0].guardian_phone_number)

                        l1.append(r_attribute.objects.filter(parent=food_parent)[0].address)

                        l1.append(r_attribute.objects.filter(parent=food_parent)[0].location)

                        l2.append(l1)
                    l.append([l2, item.dynamic_order_id])
                
                parameters['orders'] = l
                return render(request, 'market/home.html', parameters)
            else:
                return render(request, 'market/pending_profile.html')



def received(request, name, item):
    if datetime.datetime.now().hour>20 or datetime.datetime.now().hour<9:
        return render (request , 'night.html')
    user = request.user
    if user.is_authenticated:
        check = ''
        for i in user.email:
            if i=='@':
                break
            else:
                check+=i

        parent=r_attribute.objects.filter(parent=request.user)
        if check==name and len(parent)==0:
            existance_check=c_attribute.objects.filter(parent=request.user)

            if not len(existance_check)==0:
                this=''
                for i in item:
                    if i==' ':
                        break
                    this+=i

                SubOrder = sub_order.objects.filter(sub_order_id=int(this))[0]
                SubOrder.delivery_status=True
                SubOrder.save()
                return redirect(f'/market-place/user/{user.username}')
            else:
                return render(request, 'market/pending_profile.html')


def get_cart(request, name, cart):
    if datetime.datetime.now().hour>20 or datetime.datetime.now().hour<9:
        return render (request , 'night.html')
    user = request.user
    if user.is_authenticated:
        check = ''
        for i in user.email:
            if i=='@':
                break
            else:
                check+=i
        if check==name:
            existance_check=c_attribute.objects.filter(parent=request.user)

            if not len(existance_check)==0:
                parameters = {'user': request.user.username, 'cart': cart}
                return render(request, 'market/get_cart.html', parameters)
            else:
                return render(request, 'market/pending_profile.html')



def cart(request, name):
    if datetime.datetime.now().hour>20 or datetime.datetime.now().hour<9:
        return render (request , 'night.html')
    if request.method == "POST":
        cart = request.POST.get('cart')
        cart=cart[:-1].split(',')
        cart=[i.split(':') for i in cart]

        parameters = {'user': request.user, 'username': request.user.username}

        user = request.user
        if user.is_authenticated:
            check = ''
            for i in user.email:
                if i=='@':
                    break
                else:
                    check+=i

            if check==name:
                existance_check=c_attribute.objects.filter(parent=request.user)

                if not len(existance_check)==0:
                    items_list=[]
                    prices = []
                    orders_list = ''

                    for item in cart:
                        my_food = food.objects.filter(food_id=int(item[0]))[0]
                        items_list.append([my_food, int(item[1])])
                        parameters['items'] = items_list

                        orders_list+=f'{my_food.food_id}-{int(item[1])}-{my_food.by_restaurant.id}+'

                        prices.append(my_food.price*int(item[1]))

                    cost=0
                    for i in prices:
                        cost+=i

                    parameters['cost'] = cost
                    parameters['orders_list'] = orders_list[:-1]
                    return render(request, 'market/cart.html', parameters)
                else:
                    return render(request, 'market/pending_profile.html')



def order_placed(request):
    if datetime.datetime.now().hour>20 or datetime.datetime.now().hour<9:
        return render (request , 'night.html')
    if request.method=='POST':
        placed_orders = request.POST.get('placed_orders')

        restaurants = ''
        for i in placed_orders:
            l1=placed_orders.split('+')
            l1=[i.split('-') for i in l1]
        
        s={int(i[-1]) for i in l1}
  
        Order = order(ordered_by=request.user, total_restaurants_associated=len(s), name_of_those_restaurants=s, net_delivery_status=False)
        Order.save()

        for i in s:
            l2=[j for j in l1 if int(j[-1])==i]
            cost = 0
            time = 0
            food_item = food.objects.filter(food_id=l2[0][0])[0]
            temp_string=''
            for j in l2:
                cost+=food_item.price*int(j[1])
                time+=food_item.preparation_time_in_minutes*int(j[1])
                temp_string+=f'{int(j[0])}:{int(j[1])},'

            SubOrder = sub_order(parent_order=Order, ordered_ids=temp_string[:-1], cost=cost, total_preparation_time_in_minutes=time, delivery_status= False)
            SubOrder.save()

        messages.success(request, 'Your order has been placed successfully!')
        return redirect(f'/market-place/user/{request.user.username}')


def food_search(request, name):
    if datetime.datetime.now().hour>20 or datetime.datetime.now().hour<9:
        return render (request , 'night.html')

    messages.info(request, 'In case the restaurant/restaurants you are ordering from are far away from you, order at your own risk.')

    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            check = ''
            for i in user.email:
                if i=='@':
                    break
                else:
                    check+=i

            if check==name:
                existance_check=c_attribute.objects.filter(parent=request.user)

                if not len(existance_check)==0:
                    query = request.GET.get('food_search', '')

                    if query == '':
                        l=[]
                    else:
                        try:
                            l = query.split(' ')
                        except:
                            l=[query]

                    count=0
                    for i in l:
                        if i == '':
                            count+=1
                    if count == len(l):
                        l=[]

                    if len(l)==0:
                        return redirect(f'/market-place/user/{request.user}')

                    nill_count = 0
                    for i in l:
                        if i=='':
                            nill_count+=1
                    
                    for i in range(nill_count):
                            l.remove('')

                    foods = [i for i in food.objects.filter(in_stock=True) if food_searchMatch(l, i)]

                    restaurants = []
                    if request.GET.get('include_rests') == 'yes':
                        restaurants = [i for i in r_attribute.objects.all() if rest_searchMatch(l, i)]

                    parameters = {'foods': foods, 'username': user.username, 'restaurants': restaurants, 'query': query}

                    if len(l)>10:
                        messages.warning(request, "Too long query entered, search ignored!")
                    elif len(foods)==0 and len(restaurants)==0:
                        messages.info(request, "Please try searching a valid query!")
                    
                    return render(request, 'market/food_search.html', parameters)
                else:
                    return render(request, 'market/pending_profile.html')


def food_searchMatch(query, item):
    matched = 0
    length=len(query)

    for words in query:
        words = words.lower()

        if len(words)<=2:
            continue

        elif words[:len(words)//2-1] in item.name.lower() or words[:len(words)//2-1] in item.category.lower() or words[:len(words)//2-1] in item.sub_category.lower() or words[:len(words)//2-1] in item.by_restaurant.username.lower():
            matched+=1

    for i in range(1, 11):
        if length==i:
            if matched>i-1:
                return True
    return False


def rest_searchMatch(query, item):
    for words in query:
        words = words.lower()
        if len(words)<=3:
            continue
        elif words[:len(words)//2] in item.parent.username.lower():
            return True



def customer_signup_handle(request):
    if request.method == 'POST':
        fname = request.POST.get('c_fname', '')
        lname = request.POST.get('c_lname', '')
        email = request.POST.get('c_email', '')
        pass1 = request.POST.get('c_pass1', '')
        pass2 = request.POST.get('c_pass2', '')

        username=''
        for i in email:
            if i=='@':
                break
            else:
                username+=i


        if pass1!=pass2:
            messages.warning(request, "Your entered passwords did not match each other. Please try again...")
            return render(request, 'restaurant_signup.html')

        try:
            user = User.objects.create_user(username, email, pass1)
            user.first_name = fname
            user.last_name = lname
            user.save()
            
            user = authenticate(username = username, password = pass1)
            if user is not None:
                login(request, user)
                messages.success(request, f'Account created successfully! Your Customer Username is: "{username}"')

                return redirect(f'/send-otp/')

        except Exception as e:
            messages.error(request, f"Account already exists with {email}.")
            return render(request, 'customer_signup.html')


def profile(request, name):
    if request.method=="POST":
        mobile=request.POST.get('phone')
        gender=request.POST.get('Gender')
        address=request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pin=request.POST.get('pin')

        attrib=c_attribute(parent=request.user, phone_number=mobile, gender=gender, address=address, City=city, State=state, pin_code=pin)
        attrib.save()

        return redirect(f'/market-place/user/{request.user}')

    user = request.user
    if user.is_authenticated:
        check = ''
        for i in user.email:
            if i=='@':
                break
            else:
                check+=i

        if check==name:
            confirm=Otp_Confirmation.objects.filter(parent=request.user)

            if not len(confirm)==0:
                if confirm[0].confirmation_status:
                    return render(request, 'market/cust_profile.html')
            else:
                return render(request, 'pending_authentication.html')


    

def login_handle(request):
    if request.method=='POST':
        username = request.POST.get('login-username')
        password = request.POST.get('login-password')

        user = authenticate(username = username, password = password)

        if user is not None:
            check = ''
            for i in user.email:
                if i=='@':
                    break
                else:
                    check+=i

            parent=r_attribute.objects.filter(parent=user)

            if check==user.username and len(parent)==0:
                existance_check=c_attribute.objects.filter(parent=user)

                if not len(existance_check)==0:
                    login(request, user)
                    messages.success(request, f"successfully logged in as {username}")

                    if datetime.datetime.now().hour>20 or datetime.datetime.now().hour<9:
                        return render (request , 'night.html')

                    messages.info(request, 'In case the restaurant/restaurants you are ordering from are far away from you, order at your own risk.')

                    return redirect(f'/market-place/user/{user.username}')
                else:
                    login(request, user)
                    return render(request, 'market/pending_profile.html')

            if not request.user.is_staff:
                existance_check=r_attribute.objects.filter(parent=user)

                if not len(existance_check)==0:
                    login(request, user)
                    messages.success(request, f"successfully logged in as {username}")
                    return redirect(f'/collab/restaurant/admin/{user.username}')
                else:
                    login(request, user)
                    return render(request, 'collabs/pending_profile.html')

        else:
            messages.error(request, "Invalid username or password...")
            return render(request, 'login.html')


