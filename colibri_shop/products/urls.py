from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('products/<str:sex>/', views.ProductsListView.as_view(), name='products_with_category'),
    path('products/<str:sex>/<int:category_id>/', views.ProductsListView.as_view(), name='sex_category'),
    path('products/page/<int:page>/', views.ProductsListView.as_view(), name='paginator'),
    path('product/<int:pk>/', views.ProductsDetailView.as_view(), name='product'),

    path('basket/add/<int:product_id>/', login_required(views.basket_add), name='basket_add'),
    path('basket/remove/product/<int:product_id>/', views.product_remove_basket, name='product_remove_in_basket'),
    path('basket/remove/<int:basket_id>/', login_required(views.basket_remove), name='basket_remove'),
    path('basket/', views.BasketListView.as_view(), name='basket_list'),

    path('brands/', views.BrandsListView.as_view(), name='brands'),
    path('brands/<int:brand_id>/', views.BrandsListView.as_view(), name='brand'),

    path('favorite/add/<int:product_id>/', login_required(views.favorite_add), name='favorite_add'),
    path('favorite/remove/<int:product_id>/', login_required(views.favorite_remove), name='favorite_remove'),
    path('favorites/', login_required(views.FavoriteListView.as_view()), name='favorites')
]

