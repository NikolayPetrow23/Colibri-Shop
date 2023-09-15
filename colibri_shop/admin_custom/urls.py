from django.urls import path

from admin_custom import views

app_name = 'admin_custom'

urlpatterns = [
    path('', views.AdminCustomView.as_view(), name='admin'),

    path('users/', views.admin_users_view, name='admin_users'),
    path('users_detail/<int:pk>/', views.AdminUserUpdateView.as_view(), name='admin_users_update'),

    path('category/', views.admin_category_view, name='admin_category'),

    path('brand/', views.admin_brand_view, name='admin_brand'),

    path('product/', views.admin_product_view, name='admin_product'),
    path('product/update/<int:pk>/', views.AdminProductUpdateView.as_view(), name='admin_product_update'),
    path('product/create/', views.AdminProductCreateView.as_view(), name='admin_product_create'),

    path('basket/', views.admin_basket_view, name='admin_basket'),

    path('order/', views.admin_order_view, name='admin_order'),
    path('order/update/<int:pk>/', views.AdminOrderUpdateView.as_view(), name='admin_order_update'),
]
