from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from market_place.models import food, r_attribute, c_attribute, order, sub_order, staff_attribute
from collab.models import order_data
import json


# Create your views here.


def home(request):
    return render(request, 'root/RootLogin.html')


def root_login_handle(request):
    if request.method=='POST':
        username = request.POST.get('login-username')
        password = request.POST.get('login-password')

        user = authenticate(username = username, password = password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, f'Access granted! Welcome {user.username}')
                return redirect(f'/root/user/{user.username}')

            else:
                messages.warning(request, 'You are not authorised to access this page.')
                return redirect('/root')

        else:
            messages.error(request, "Invalid username or password...")
            return redirect('/root')



def root_user(request, name):
    if request.method=='POST':
        query=request.POST.get('rest_search')

        l=query.split(' ')

        nill_count=0
        for i in l:
            if i=='':
                nill_count+=1

        if nill_count==len(l):
            l=[]

        if len(l)==0:
            return redirect(f'/root/user/{request.user}')

        restaurants = []
        for i in r_attribute.objects.all():
            l=i.parent.username.split(' ')

            for j in l:
                if j[:len(j)//2-1].lower() in query and j[:len(j)//2-1]!='':
                    if i not in restaurants:
                        restaurants.append(i)

        return render(request, 'root/root_home.html', {'restaurants': restaurants})

    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.user.username==name:
                restaurants = r_attribute.objects.all()
                return render(request, 'root/root_home.html', {'restaurants': restaurants})



def paids(request, name, restaurant):
    user = request.user
    parameters={}
    if user.is_authenticated:
        if request.user.is_staff:
            if user.username==name:
                all_SubOrders = sub_order.objects.all()
                SubOrders = []

                parent_restaurant=[]
                for sub in all_SubOrders:
                    get_order_ids=sub.ordered_ids.split(',')
                    order_ids = [i.split(':') for i in get_order_ids]

                    rest=User.objects.filter(username=restaurant)[0]

                    for i, j in order_ids:
                        FoodItem=food.objects.filter(food_id=int(i), by_restaurant=rest)

                        if len(FoodItem)==0:
                            continue
                        else:
                            if sub not in SubOrders:
                                SubOrders.append(sub)

                l1=[]

                total_amount_paid=0

                for order in SubOrders:
                    l2=[]
                    get_order_ids=order.ordered_ids.split(',')
                    order_ids = [i.split(':') for i in get_order_ids]

                    for i, j in order_ids:
                        FoodItem=food.objects.filter(food_id=int(i))[0]
                        parent_restaurant.append(FoodItem.by_restaurant.username)
                        l2.append([FoodItem, int(j)])

                    original_price=(10/11)*order.cost

                    their_cut=int(original_price+(original_price*(2/100)))

                    if order.paid:
                        l1.append([l2, order.parent_order, order.sub_order_id, their_cut, order.order_date, "Paid" if order.paid else "UnPaid", order.paid_by])
                    
                        total_amount_paid+=their_cut


                if len(l1)==0:
                    message = "Paid data not available!"
                    parameters={'empty_cart_message': message}
                parameters['orders'] = l1
                parameters['paid_amount'] = total_amount_paid
                parameters['rest'] = parent_restaurant[0]
                return render(request, 'root/paid_amounts.html', parameters)



def unpaids(request, name, restaurant):
    user = request.user
    user_attrib=staff_attribute.objects.filter(parent=request.user)[0]

    parameters={}

    if user.is_authenticated:
        if request.user.is_staff:
            if user.username==name:
                all_SubOrders = sub_order.objects.all()
                SubOrders = []

                parent_restaurant=[]
                
                for sub in all_SubOrders:
                    get_order_ids=sub.ordered_ids.split(',')
                    order_ids = [i.split(':') for i in get_order_ids]

                    rest=User.objects.filter(username=restaurant)[0]

                    for i, j in order_ids:
                        FoodItem=food.objects.filter(food_id=int(i), by_restaurant=rest)

                        if len(FoodItem)==0:
                            continue
                        else:
                            if sub not in SubOrders:
                                SubOrders.append(sub)

                l1=[]

                total_amount_paid=0

                for order in SubOrders:
                    l2=[]
                    get_order_ids=order.ordered_ids.split(',')
                    order_ids = [i.split(':') for i in get_order_ids]

                    for i, j in order_ids:
                        FoodItem=food.objects.filter(food_id=int(i))[0]
                        parent_restaurant.append(FoodItem.by_restaurant.username)
                        l2.append([FoodItem, int(j)])

                    original_price=(10/11)*order.cost

                    their_cut=int(original_price+(original_price*(2/100)))

                    if not order.paid:
                        l1.append([l2, order.parent_order, order.sub_order_id, their_cut, order.order_date, "Paid" if order.paid else "UnPaid"])
                    
                        total_amount_paid+=their_cut

                if len(l1)==0:
                    message = "UnPaid data not available!"
                    parameters={'empty_cart_message': message}

                parameters['orders'] = l1
                parameters['paid_amount'] = total_amount_paid
                parameters['rest'] = parent_restaurant[0]
                parameters['key'] = user_attrib.security_key
                return render(request, 'root/unpaid_orders.html', parameters)



def now_paid(request, name, item, restaurant):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            if user.username==name:
                if item=='all':
                    all_SubOrders = sub_order.objects.all()
                    SubOrders = []

                    for sub in all_SubOrders:
                        get_order_ids=sub.ordered_ids.split(',')
                        order_ids = [i.split(':') for i in get_order_ids]

                        rest=User.objects.filter(username=restaurant)[0]

                        for i, j in order_ids:
                            FoodItem=food.objects.filter(food_id=int(i), by_restaurant=rest)

                            if len(FoodItem)==0:
                                continue
                            else:
                                if sub not in SubOrders:
                                    SubOrders.append(sub)

                    for i in SubOrders:
                        i.paid=True
                        i.paid_by=request.user
                        i.save()

                else:
                    this=''
                    for i in item:
                        if i==' ':
                            break
                        this+=i

                    SubOrder = sub_order.objects.filter(sub_order_id=int(this))[0]
                    SubOrder.paid=True
                    SubOrder.paid_by=request.user
                    SubOrder.save()

                messages.success(request, 'Payment status updated successfully!')
                return redirect(f'/root/user/{user.username}/')
