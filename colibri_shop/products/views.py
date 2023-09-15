from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView

from common.views import CategoriesMixin
from products.models import Product, ProductCategory, Basket, ProductBrands, Favorite


class IndexView(TemplateView):
    template_name = 'products/index.html'


class ProductsListView(CategoriesMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 12
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        sex = self.kwargs.get('sex')
        queryset = Product.objects.filter(sex__in=[sex, 'unisex'])

        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sex = self.kwargs.get('sex')
        context['sex'] = sex
        return context


class ProductsDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'product'


class BrandsListView(ListView):
    model = ProductBrands
    template_name = 'products/products.html'
    paginate_by = 18
    context_object_name = 'brands'

    def get_queryset(self):
        brand_id = self.kwargs.get('brand_id')
        queryset = ProductBrands.objects.all()

        if brand_id:
            queryset = Product.objects.filter(brand_id=brand_id)
            self.context_object_name = 'products'
            return queryset

        return queryset


# class BrandsDetailView(DetailView):
#     model = ProductBrands
#     template_name = 'products/products.html'
    # paginate_by = 18
    # context_object_name = 'brands'

    # def get_queryset(self):
    #     category_id = self.kwargs.get('category_id')
    #     sex = self.kwargs.get('sex')
    #     queryset = Product.objects.filter(sex__in=[sex, 'unisex'])
    #
    #     return queryset.filter(category_id=category_id) if category_id else queryset


def favorite_add(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    product.add_to_favorites(user)

    return redirect(request.META['HTTP_REFERER'])


def favorite_remove(request, product_id):
    relate_favorite = Favorite.objects.get(
        product_id=product_id, user_id=request.user.id
    )
    relate_favorite.delete()
    return redirect(request.META['HTTP_REFERER'])


class FavoriteListView(ListView):
    model = Favorite
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = self.request.user.favorite_product.all()
        return queryset


class BasketListView(ListView):
    model = Basket
    template_name = 'products/profile/basket.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Basket.objects.filter(user=user)

        return queryset


def basket_add(request, product_id):
    Basket.create_or_update(product_id, request.user)
    return redirect(request.META['HTTP_REFERER'])


def product_remove_basket(request, product_id):
    Basket.remove_product_in_basket(product_id, request.user)
    return redirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return redirect(request.META['HTTP_REFERER'])
