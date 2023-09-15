from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrdersListView.as_view(), name='orders_list'),
    path('create/', views.CreateOrderView.as_view(), name='order_create'),
    path('success/', views.SuccessOrderView.as_view(), name='order_success'),
    path('detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail')
]
