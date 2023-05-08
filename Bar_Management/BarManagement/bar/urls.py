from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('order/', views.order, name='order'),
    path('sales_reports/', views.sales_reports, name='sales_reports'),
    path('supplier/', views.supplier, name='supplier'),
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'), # API endpoints
    path('orders/create/', views.OrderCreateView.as_view(), name='order-create'),
    # path('payments/', views.PaymentListCreateView.as_view(), name='payment-list-create'),# API endpoints
    # path('sales/report/', views.sales_report, name='sales-report'),
    # path('suppliers/', views.supplier_list, name='supplier-list'),
    # Add more endpoints for other functionalities
]
