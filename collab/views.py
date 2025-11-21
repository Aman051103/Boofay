from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from market_place.models import food, r_attribute, c_attribute, order, sub_order, Otp_Confirmation
from collab.models import order_data
import json
import datetime
from django import forms
from .form import GetFood, GetProfile


def home(request):
    if not request.user.is_staff:
        existance_check=r_attribute.objects.filter(parent=request.user)
        if not len(existance_check)==0:
            return redirect(f'/collab/restaurant/admin/{request.user}/')
        else:
            return render(request, 'collabs/pending_profile.html')


def profile(request, name):
    if request.method=='POST':
        form=GetProfile(data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()

            this_rest = r_attribute.objects.filter(restaurant_user_id=request.user.id)
            for i in this_rest:
                i.parent=request.user
                i.save()

            messages.success(request, 'Successfully added profile!')
            return redirect(f'/collab/restaurant/admin/{request.user}')

        else:
            form=GetProfile()
            messages.error(request, 'Error updating Profile... Please try again!')
            return render(request, 'collabs/rest_profile.html', {'username': request.user})


    user = request.user
    if user.is_authenticated:
        if user.username==name:
            if not request.user.is_staff:
                confirm=Otp_Confirmation.objects.filter(parent=request.user)
                form=GetProfile()
                if not len(confirm)==0:
                    if confirm[0].confirmation_status:
                        return render(request, 'collabs/rest_profile.html', {'form': form, 'user': request.user.id})
                else:
                    return render(request, 'pending_authentication.html')



def restaurant_auth(request, name):
    parameters = {'user': request.user, 'username': request.user.username}

    user = request.user
    if user.is_authenticated:
        if user.username==name:
            if not request.user.is_staff:
                existance_check=r_attribute.objects.filter(parent=request.user)
                if not len(existance_check)==0:
                    all_SubOrders = sub_order.objects.filter(delivery_status=False)
                    SubOrders = []

                    l2=[]
                    for sub in all_SubOrders:
                        get_order_ids=sub.ordered_ids.split(',')
                        order_ids = [i.split(':') for i in get_order_ids]

                        for i, j in order_ids:
                            FoodItem=food.objects.filter(food_id=int(i), by_restaurant=request.user.id)

                            if len(FoodItem)==0:
                                continue
                            else:
                                if sub not in SubOrders:
                                    SubOrders.append(sub)

                    if len(SubOrders)==0:
                        message = "No orders pending!"
                        parameters['empty_cart_message'] = message

                    l1=[]
                    for order in SubOrders:
                        l2=[]
                        get_order_ids=order.ordered_ids.split(',')
                        order_ids = [i.split(':') for i in get_order_ids]

                        for i, j in order_ids:
                            FoodItem=food.objects.filter(food_id=int(i))[0]
                            l2.append([FoodItem, int(j)])

                        contact=c_attribute.objects.filter(parent=order.parent_order.ordered_by)
                        l1.append([l2, order.parent_order, order.sub_order_id, contact])

                    parameters['orders'] = l1
                    return render(request, 'collabs/rest_admin.html', parameters)
                else:
                    return render(request, 'collabs/pending_profile.html')


def prepared(request, name, item):
    user = request.user
    if user.is_authenticated:

        if user.username==name:
            existance_check=r_attribute.objects.filter(parent=request.user)
            if not len(existance_check)==0:
                this=''
                for i in item:
                    if i==' ':
                        break
                    this+=i

                SubOrder = sub_order.objects.filter(sub_order_id=int(this))[0]
                SubOrder.preparation_status=True
                SubOrder.save()
                return redirect(f'/collab/restaurant/admin/{user.username}')
            else:
                return render(request, 'collabs/pending_profile.html')


def stock(request, name, item):
    user = request.user
    if user.is_authenticated:

        if user.username==name:
            existance_check=r_attribute.objects.filter(parent=request.user)
            if not len(existance_check)==0:
                item=int(item)

                if request.method=='POST':
                    stock = request.POST.get(f'stock-{item}')
                    no = request.POST.get(f'no-{item}')

                    if stock=='yes':
                        foods = food.objects.filter(food_id=int(item))[0]
                        foods.in_stock=True
                        foods.save()

                    elif no=='yes':
                        foods = food.objects.filter(food_id=int(item))[0]
                        foods.in_stock=False
                        foods.save()

                    return redirect(f'/collab/restaurant/admin/{user.username}/my-foods/')
            else:
                return render(request, 'collabs/pending_profile.html')



def restaurant_signup_handle(request):
    if request.method == 'POST':
        username = request.POST.get('r_name', '')
        fname = request.POST.get('o_fname', '')
        lname = request.POST.get('o_lname', '')
        email = request.POST.get('r_email', '')
        pass1 = request.POST.get('r_pass1', '')
        pass2 = request.POST.get('r_pass2', '')

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
                messages.success(request, f'Account created successfully! Your Restaurant Username is: "{username}"')

                return redirect(f'/send-otp/')


        except Exception as e:
            messages.error(request, f"Account already exists with {username}.")
            return render(request, 'restaurant_signup.html')



def payment_data(request, name):
    parameters = {'user': request.user, 'username': request.user.username}

    user = request.user
    if user.is_authenticated:
        if not request.user.is_staff:
            if user.username==name:
                existance_check=r_attribute.objects.filter(parent=request.user)
                if not len(existance_check)==0:
                    all_SubOrders = sub_order.objects.all()
                    SubOrders = []

                    l2=[]
                    for sub in all_SubOrders:
                        get_order_ids=sub.ordered_ids.split(',')
                        order_ids = [i.split(':') for i in get_order_ids]

                        for i, j in order_ids:
                            FoodItem=food.objects.filter(food_id=int(i), by_restaurant=request.user.id)

                            if len(FoodItem)==0:
                                continue
                            else:
                                if sub not in SubOrders:
                                    SubOrders.append(sub)

                    if len(SubOrders)==0:
                        message = "Payment data not available!"
                        parameters['empty_cart_message'] = message

                    l1=[]
                    total_cost=0
                    total_amount_unpaid=0
                    total_amount_paid=0
                    unpaid_orders=[]
                    paid_orders=[]

                    for order in SubOrders:
                        l2=[]
                        get_order_ids=order.ordered_ids.split(',')
                        order_ids = [i.split(':') for i in get_order_ids]

                        for i, j in order_ids:
                            FoodItem=food.objects.filter(food_id=int(i))[0]
                            l2.append([FoodItem, int(j)])

                        original_price=(10/11)*order.cost

                        their_cut=int(original_price+(original_price*(2/100)))

                        l1.append([l2, order.parent_order, order.sub_order_id, their_cut, order.order_date, "Paid" if order.paid else "UnPaid"])
                        
                        total_cost+=their_cut

                        if not order.paid:
                            unpaid_orders.append([l2, order.parent_order, order.sub_order_id, their_cut, order.order_date, "Paid" if order.paid else "UnPaid"])

                            total_amount_unpaid+=their_cut
                            parameters['unpaid_orders'] = unpaid_orders

                        else:
                            paid_orders.append([l2, order.parent_order, order.sub_order_id, their_cut, order.order_date, "Paid" if order.paid else "UnPaid"])

                            total_amount_paid+=their_cut
                            parameters['paid_orders'] = paid_orders
                    

                    parameters['orders'] = l1
                    parameters['total_cost'] = total_cost
                    parameters['paid_amount'] = total_amount_paid
                    parameters['unpaid_amount'] = total_amount_unpaid
                    return render(request, 'collabs/orders_data.html', parameters)

                else:
                    return render(request, 'collabs/pending_profile.html')


def my_foods(request, name):
    parameters = {'user': request.user, 'username': request.user.username}

    user = request.user
    if user.is_authenticated:
        if user.username==name:
            existance_check=r_attribute.objects.filter(parent=request.user)
            if not len(existance_check)==0:

                if request.method=='POST':
                    query=request.POST.get('food_search', '')

                    parameters['query'] = query

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
                        return redirect(f'/collab/restaurant/admin/{request.user}/my-foods/')

                    nill_count = 0
                    for i in l:
                        if i=='':
                            nill_count+=1
                    
                    for i in range(nill_count):
                            l.remove('')

                    foods = [i for i in food.objects.filter(by_restaurant=request.user) if searchMatch(l, i)]

                    parameters['foods']=foods

                    if len(l)>7:
                        messages.warning(request, "Too long query entered, search ignored!")
                    elif len(foods)==0:
                        messages.info(request, "Please try searching a valid query!")
                    
                    return render(request, 'collabs/my_foods.html', parameters)


                foods = food.objects.filter(by_restaurant=request.user)
                parameters['foods']=foods
                return render(request, 'collabs/my_foods.html', parameters)
            else:
                return render(request, 'collabs/pending_profile.html')


def searchMatch(query, item):
    for words in query:
        words = words.lower()
        if len(words)<=2:
            continue

        else:
            if len(words)>=6:
                if words[:len(words)//2-1] in item.name.lower() or words[:len(words)//2] in item.sub_category.lower() or words[:len(words)//2] in item.category.lower():
                    return True
            else:
                if words in item.name.lower() or words in item.sub_category.lower() or words in item.category.lower():
                    return True


def add_foods(request, name):
    if request.user.is_authenticated:
        if request.user.username==name:
            existance_check=r_attribute.objects.filter(parent=request.user)
            if not len(existance_check)==0:
                form=GetFood()
                return render(request, 'collabs/add_foods.html', {'username': request.user, 'form': form, 'user': request.user.id})
            else:
                return render(request, 'collabs/pending_profile.html')


def item_added(request, name):
    if request.user.is_authenticated:
        if request.user.username==name:
            existance_check=r_attribute.objects.filter(parent=request.user)
            if not len(existance_check)==0:
                if request.method=='POST':
                    form=GetFood(data=request.POST, files=request.FILES)

                    if form.is_valid():
                        form.save()
                        this_food = food.objects.filter(parent_id=request.user.id)
                        for i in this_food:
                            i.by_restaurant=request.user
                            i.price=int((11/10)*i.price)+1
                            i.save()

                        messages.success(request, 'Item uploaded successfully!')
                        return redirect(f'/collab/restaurant/admin/{request.user}/my-foods/')

                    else:
                        form=GetFood()

                        messages.error(request, 'Error Uploading Item... Please try again!')
                        return render(request, 'collabs/add_foods.html', {'username': request.user})
            else:
                return render(request, 'collabs/pending_profile.html')

