from django.urls import path
from . import views

app_name = 'bar'


urlpatterns = [
    path('', views.home, name='home'),
    path('order/', views.order, name='order'),
    path('sales-reports/', views.sales_reports, name='sales_reports'),
    path('supplier/', views.supplier, name='supplier'),
    path('create-drink/', views.create_drink, name='create_drink'),
    path('drink_list/', views.drink_list, name='drink_list'),
    path('drink_detail/<int:drink_id>/', views.drink_detail, name='drink_detail'),
    path('sell_drink/<int:drink_id>/', views.sell_drink, name='sell_drink'),
    path('process-sale/', views.process_sale, name='process_sale'),
    #path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'), # API endpoints
    path('orders/create/', views.OrderCreateView.as_view(), name='order-create'),
    # path('payments/', views.PaymentListCreateView.as_view(), name='payment-list-create'),# API endpoints
    # path('sales/report/', views.sales_report, name='sales-report'),
    # path('suppliers/', views.supplier_list, name='supplier-list'),
    # Add more endpoints for other functionalities
]
