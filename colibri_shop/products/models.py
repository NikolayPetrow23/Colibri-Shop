from django.db import models

from django.utils.translation import gettext_lazy as _

from users.models import User


class ProductCategory(models.Model):
    class CategorySex(models.TextChoices):
        men = 'men', _('Мужчинам')
        women = 'women', _('Женщинам')
        unisex = 'unisex', _('Унисекс')

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    sex = models.CharField(
        max_length=6,
        choices=CategorySex.choices,
        default=CategorySex.unisex
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class ProductBrands(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='brands_images', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'
        ordering = ('image',)


class Product(models.Model):
    class RoleProductSex(models.TextChoices):
        men = 'men', _('Мужская одежда')
        women = 'women', _('Женская одежда')
        unisex = 'unisex', _('Унисекс')

    class SizeProduct(models.TextChoices):
        xs = 'xs', _("Размер xs")
        s = 's', _("Размер s")
        m = 'm', _("Размер m")
        l = 'l', _("Размер l")
        xl = 'xl', _("Размер xl")

    name = models.CharField(max_length=128)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    size = models.CharField(
        max_length=2, choices=SizeProduct.choices,
    )
    sex = models.CharField(
        max_length=6, choices=RoleProductSex.choices,
    )
    category = models.ForeignKey(ProductCategory,
                                 on_delete=models.PROTECT,
                                 related_name='product')
    brand = models.ForeignKey(ProductBrands,
                              on_delete=models.PROTECT,
                              related_name='brand')
    is_favorited = models.ManyToManyField(
        User,
        related_name='favorite_product',
        blank=True,
        through='Favorite'
    )

    def __str__(self):
        return (f'Продукт: {self.name} | '
                f'Категория: {self.category.name} | '
                f'Брэнд: {self.brand.name}')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)

    def add_to_favorites(self, user):
        if self not in user.favorite_product.all():
            user.favorite_product.add(self)


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def yookassa_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина: {self.user.email} | Товар: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id, user):
        basket = Basket.objects.filter(
            user=user, product_id=product_id
        )
        is_created = False

        if not basket.exists():
            obj = Basket.objects.create(
                user=user, product_id=product_id, quantity=1
            )
            is_created = True
            return obj, is_created

        basket = basket.first()
        basket.quantity += 1
        basket.save()

        return basket, is_created

    @classmethod
    def remove_product_in_basket(cls, product_id, user):
        basket = Basket.objects.filter(
            user=user, product_id=product_id
        )

        if not basket.exists():
            message = 'Такого товара нет в корзине!'
            return message

        basket = basket.first()
        quantity = basket.quantity

        if quantity > 1:
            basket.quantity -= 1
            basket.save()
            return basket

        basket.delete()


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favorite_products'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_favorite_products'
    )
    is_favorited = models.BooleanField(default=False)

    def __str__(self):
        return f'Товар {self.product} в избранном у {self.user}'

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
