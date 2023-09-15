from products.models import ProductCategory


class CategoriesMixin:
    def get_context_data(self, **kwargs):
        sex = self.kwargs.get('sex')
        context = super(CategoriesMixin, self).get_context_data(**kwargs)

        if sex:
            context['categories'] = ProductCategory.objects.filter(sex__in=[sex, 'unisex'])
            return context

        context['categories'] = ProductCategory.objects.filter(sex='unisex')
        context['category_id'] = self.kwargs.get('category_id')
        return context
