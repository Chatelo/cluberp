from rest_framework import generics
from .models import Order, Payment, Drink, Supplier, Sale
from .serializers import OrderSerializer, PaymentSerializer, SupplierSerializer
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from datetime import date
from rest_framework.decorators import api_view
from .forms import DrinkForm
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def create_drink(request):
    if request.method == 'POST':
        form = DrinkForm(request.POST)
        if form.is_valid():
            drink_name = form.cleaned_data['name']
            if Drink.objects.filter(name=drink_name).exists():
                messages.error(request, 'A drink with that name already exists!')
            else:
                form.save()
                messages.success(request, 'Drink created successfully!')
                return redirect('bar:drink_list')  # Update the URL name for redirection
    else:
        form = DrinkForm()
    template_name = 'bar/create_drink.html'  # Update the template path
    context = {'form': form}
    return render(request, template_name, context)



def drink_list(request):
    drinks = Drink.objects.all()
    return render(request, 'bar/drink_list.html', {'drinks': drinks})

def drink_detail(request, drink_id):
    drink = get_object_or_404(Drink, pk=drink_id)
    return render(request, 'bar/drink_detail.html', {'drink': drink})

# def sell_drink(request, drink_id):
#     drink = get_object_or_404(Drink, pk=drink_id)
#     if request.method == 'POST':
#         quantity = int(request.POST.get('quantity', 1))
#         if quantity <= 0:
#             messages.error(request, 'Invalid quantity.')
#         else:
#             # Check if the available quantity is sufficient
#             if drink.quantity < quantity:
#                 messages.error(request, f'Insufficient stock for {drink.name}.')
#             else:
#                 # Update the quantity and save the order
#                 drink.quantity -= quantity
#                 drink.save()
#                 order = Order.objects.create(drink=drink, quantity=quantity)
#                 messages.success(request, f'Successfully sold {quantity} {drink.name}(s).')
#                 return redirect('drink_list')  # Redirect to the drink list or another view

#     return render(request, 'bar/sell_drink.html', {'drink': drink})

def sell_drink(request, drink_id):
    drink = get_object_or_404(Drink, pk=drink_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            messages.error(request, 'Invalid quantity.')
        else:
            # Check if the available quantity is sufficient
            if drink.quantity < quantity:
                messages.error(request, f'Insufficient stock for {drink.name}.')
            else:
                # Update the quantity and save the order
                drink.quantity -= quantity
                drink.save()
                order = Order.objects.create(drink=drink, quantity=quantity)
                messages.success(request, f'Successfully sold {quantity} {drink.name}(s).')
                return redirect(reverse('bar:drink_detail', args=[drink.id]))  # Redirect to the drink detail view

    return render(request, 'bar/sell_drink.html', {'drink': drink})


@login_required
def process_sale(request):
    if request.method == 'POST':
        # Retrieve the quantities from the form data
        quantities = {key[9:]: int(value) for key, value in request.POST.items() if key.startswith('quantity_')}
        
        # Update the inventory and calculate the total cost
        total_cost = 0
        for drink_id, quantity in quantities.items():
            drink = Drink.objects.get(id=drink_id)
            if drink.quantity >= quantity:
                drink.quantity -= quantity
                drink.save()
                total_cost += drink.price * quantity
            else:
                messages.error(request, f"Not enough quantity available for {drink.name}")

        # Record the sale
        # You need to define the Sale model with necessary fields such as customer, timestamp, and total_cost

        messages.success(request, "Sale processed successfully!")
    return redirect('sell_drink')

def home(request):
    template_name = 'bar/home.html'
    drinks = Drink.objects.all()
    context = {'drinks': drinks}
    return render(request, template_name, context)


def order(request):
    template_name = 'bar/order.html'  # Update the template path
    return render(request, template_name)

def sales_reports(request):
    template_name = 'bar/sales_reports.html'  # Update the template path
    return render(request, template_name)

def supplier(request):
    template_name = 'bar/supplier.html'  # Update the template path
    return render(request, template_name)

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class OrderCreateView(APIView):
    def post(self, request):
        waiter = request.user
        drinks_data = request.data.get('drinks')
        drinks = [get_object_or_404(Drink, pk=drink_data['id']) for drink_data in drinks_data]
        order = Order.objects.create(waiter=waiter)
        order.drinks.set(drinks)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

@api_view(['GET'])
def sales_report(request):
    today = date.today()
    orders = Order.objects.filter(timestamp__date=today)
    total_sales = orders.aggregate(total_sales=Sum('drinks__price'))['total_sales'] or 0
    serializer = OrderSerializer(orders, many=True)
    return Response({'total_sales': total_sales, 'orders': serializer.data})

@api_view(['GET', 'POST'])
def supplier_list(request):
    if request.method == 'GET':
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)






