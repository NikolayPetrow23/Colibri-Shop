from http import HTTPStatus

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from orders.forms import OrderForm
from orders.models import Order
from orders.yookassa_payment import create_payment_yookassa
from products.models import Basket

LAST_ORDER_ID = 0


class CreateOrderView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(CreateOrderView, self).post(request, *args, **kwargs)

        baskets = Basket.objects.filter(user=self.request.user)
        basket_ids = [basket.id for basket in baskets][LAST_ORDER_ID]
        initiator = self.request.user
        order = Order.objects.filter(initiator=initiator).last()

        payment = create_payment_yookassa(baskets, order, basket_ids, initiator)

        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(CreateOrderView, self).form_valid(form)


class SuccessOrderView(TemplateView):
    template_name = 'orders/success.html'


class OrdersListView(ListView):
    model = Order
    template_name = 'orders/orders.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order.html'
