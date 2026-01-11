from telegram import Bot
import razorpay
import asyncio
from django.conf import settings
from .models import Order

def send_telegram_message(msg):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    bot = Bot(token=token)
    try:
        asyncio.run(bot.send_message(chat_id=chat_id, text=msg))
    except Exception as e:
        pass

def razorpay_gateway(amount):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create(dict(amount=amount, currency='INR'))
    return order["id"]

def init_cookie(request):
    if not 'order_id' in request.COOKIES:
        new_order = Order.objects.create()
        return new_order.id
    else:
        return request.COOKIES['order_id']
