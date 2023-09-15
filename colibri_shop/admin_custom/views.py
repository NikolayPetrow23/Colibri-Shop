import logging

from django.db.models import BigAutoField
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView

from users.models import User
from admin_custom.forms import AdminUserUpdateForm, AdminProductForm, AdminOrderUpdateForm
from products.models import ProductCategory, ProductBrands, Product, Favorite, Basket
from orders.models import Order

logger = logging.getLogger(__name__)


class AdminCustomView(TemplateView):
    template_name = 'admin_custom/admin_dashboard.html'


def admin_users_view(request):
    user_model = User.objects.all()
    fields = [
        {'field': User._meta.get_field('id'), 'new_name': 'ID'},
        {'field': User._meta.get_field('image'), 'new_name': 'AVATAR'},
        {'field': User._meta.get_field('first_name'), 'new_name': 'NAME'},
        {'field': User._meta.get_field('email'), 'new_name': 'EMAIL'},
        {'field': User._meta.get_field('is_superuser'), 'new_name': 'ROLE'},
    ]

    context = {
        'user_model': user_model,
        'fields': fields,
    }

    return render(request, 'admin_custom/models_list.html', context)


class AdminUserUpdateView(UpdateView):
    model = User
    template_name = 'admin_custom/models_detail.html'
    form_class = AdminUserUpdateForm
    context_object_name = 'users'

    def get_success_url(self):
        return reverse_lazy('admin_custom:admin_users')


def admin_category_view(request):
    category_model = ProductCategory.objects.all()
    fields = [
        {'field': ProductCategory._meta.get_field('id'), 'new_name': 'ID'},
        {'field': ProductCategory._meta.get_field('name'), 'new_name': 'NAME'},
        {'field': ProductCategory._meta.get_field('description'), 'new_name': 'DESCRIPTION'},
        {'field': ProductCategory._meta.get_field('sex'), 'new_name': 'SEX'},
    ]
    context = {
        'category_model': category_model,
        'fields': fields,
    }

    return render(request, 'admin_custom/models_list.html', context)


def admin_brand_view(request):
    brand_model = ProductBrands.objects.all()
    fields = [
        {'field': ProductBrands._meta.get_field('id'), 'new_name': 'ID'},
        {'field': ProductBrands._meta.get_field('image'), 'new_name': 'IMAGE'},
        {'field': ProductBrands._meta.get_field('name'), 'new_name': 'NAME'},
        {'field': ProductBrands._meta.get_field('description'), 'new_name': 'DESCRIPTION'},
    ]
    context = {
        'brand_model': brand_model,
        'fields': fields,
    }

    return render(request, 'admin_custom/models_list.html', context)


def admin_product_view(request):
    product_model = Product.objects.all()
    fields = [
        {'field': Product._meta.get_field('id'), 'new_name': 'ID'},
        {'field': Product._meta.get_field('image'), 'new_name': 'IMAGE'},
        {'field': Product._meta.get_field('name'), 'new_name': 'NAME'},
        {'field': Product._meta.get_field('price'), 'new_name': 'PRICE'},
        {'field': Product._meta.get_field('quantity'), 'new_name': 'QUANTITY'},
    ]
    context = {
        'product_model': product_model,
        'fields': fields,
    }

    return render(request, 'admin_custom/models_list.html', context)


def admin_basket_view(request):
    basket_model = Basket.objects.all()
    fields = [
        {'field': Basket._meta.get_field('id'), 'new_name': 'ID'},
        {'field': Basket._meta.get_field('user'), 'new_name': 'USER'},
        {'field': Basket._meta.get_field('product'), 'new_name': 'PRODUCT'},
        {'field': Basket._meta.get_field('quantity'), 'new_name': 'QUANTITY'},
        {'field': Basket._meta.get_field('date_created'), 'new_name': 'CREATED'},
    ]
    context = {
        'basket_model': basket_model,
        'fields': fields,
    }

    return render(request, 'admin_custom/models_list.html', context)


def admin_order_view(request):
    order_model = Order.objects.all()
    fields = [
        {'field': Order._meta.get_field('id'), 'new_name': 'ID'},
        {'field': Order._meta.get_field('first_name'), 'new_name': 'NAME'},
        {'field': Order._meta.get_field('email'), 'new_name': 'EMAIL'},
        {'field': Order._meta.get_field('status'), 'new_name': 'STATUS'},
        {'field': Order._meta.get_field('initiator'), 'new_name': 'INITIATOR'},
    ]
    context = {
        'order_model': order_model,
        'fields': fields,
    }

    return render(request, 'admin_custom/models_list.html', context)


class AdminProductUpdateView(UpdateView):
    model = Product
    template_name = 'admin_custom/models_detail.html'
    form_class = AdminProductForm
    context_object_name = 'product'

    def get_success_url(self):
        return reverse_lazy('admin_custom:admin_product')


class AdminProductCreateView(CreateView):
    model = Product
    template_name = 'admin_custom/models_detail.html'
    form_class = AdminProductForm
    context_object_name = 'product_create'

    def get_success_url(self):
        return reverse_lazy('admin_custom:admin_product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_create'] = True
        return context

    def form_valid(self, form):
        instance = form.save()
        return super().form_valid(form)


class AdminOrderUpdateView(UpdateView):
    model = Order
    template_name = 'admin_custom/models_detail.html'
    form_class = AdminOrderUpdateForm
    context_object_name = 'order'

    def get_success_url(self):
        return reverse_lazy('admin_custom:admin_order')

    def form_valid(self, form):
        instance = form.save()
        logger.info(f"Обновлен заказ #{instance.id}")
        return super().form_valid(form)
