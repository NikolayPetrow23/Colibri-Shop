import json
import os
import uuid

from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from yookassa import Configuration
from yookassa import Payment
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory

from orders.models import Order

load_dotenv()

Configuration.account_id = 249293
Configuration.secret_key = 'test_c8i8iXe-fBZMbbwGCxi1cYUfKvcSrjqPpAxTgeCiZj8'


def create_payment_yookassa(
        baskets, order, basket_id, initiator
):
    payment = Payment.create({
        "amount": {
            "value": f"{baskets.total_sum()}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            # "return_url": f"http://{os.getenv('DOMAIN_NAME')}{reverse('orders:orders_list')}"
            "return_url": (f"https://df2f-93-157-43-155.ngrok-free.app"
                           f"{reverse('orders:orders_list')}")
        },
        "capture": True,
        "description": f"Заказ #{order.id}",
        "metadata": {
            "order_id": f"{order.id}",
            "basket_id": f"{basket_id}",
            "user_id": f"{initiator.id}"
        }
    }, uuid.uuid4())

    return payment


@csrf_exempt
def yookassa_webhook_handler(request):
    event_json = json.loads(request.body)
    objects = event_json.get('object')
    metadata = objects.get('metadata')

    try:
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object

        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
        else:
            return HttpResponse(status=400)

        Configuration.configure(Configuration.account_id, Configuration.secret_key)
        payment_info = Payment.find_one(some_data['paymentId'])

        if payment_info:
            payment_status = payment_info.status
        else:
            return HttpResponse(status=400)

    except Exception:
        return HttpResponse(status=400)

    fulfill_order(metadata)
    return HttpResponse(status=200)


def fulfill_order(metadata: dict):
    order_id = int(metadata['order_id'])
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
