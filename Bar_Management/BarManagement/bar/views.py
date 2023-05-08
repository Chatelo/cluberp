from rest_framework import generics
from .models import Order, Payment, Drink, Supplier
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

def create_drink(request):
    if request.method == 'POST':
        form = DrinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Drink created successfully!')
            return redirect('drink_list')  # Redirect to a success page or another view
    else:
        form = DrinkForm()
    return render(request, 'create_drink.html', {'form': form})

def home(request):
    template = loader.get_template('bar/home.html')
    return HttpResponse(template.render())

def order(request):
    template = loader.get_template('bar/order.html')
    return HttpResponse(template.render())

def sales_reports(request):
    return render(request, 'bar/sales_reports.html')

def supplier(request):
    return render(request, 'bar/supplier.html')

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






