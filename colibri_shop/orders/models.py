from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User
from products.models import Basket


class Order(models.Model):
    class StatusChoice(models.TextChoices):
        CREATED = 0, _('Создан')
        PAID = 1, _('Оплачен')
        ON_WAY = 2, _('В пути')
        DELIVERED = 3, _('Доставлен')

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=350)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=StatusChoice.CREATED, choices=StatusChoice.choices)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return (f'Заказ #{self.id} |  '
                f'Имя: {self.first_name}, '
                f'Фамилия: {self.last_name}, '
                f'Адрес получателя: {self.address}')

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.StatusChoice.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()

    class Meta:
        ordering = ('-id',)
