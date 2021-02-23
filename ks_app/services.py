import telegram
import razorpay
from .models import Order

def send_telegram_message(msg):
    token = '1476623880:AAGCjhLjuSzDBym_j1zgZKIpFkMlDDAdX7Q'
    chat_id = 1426070442
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)

def razorpay_gateway(amount):
    client = razorpay.Client(auth=("rzp_test_BzpuQZbbNkr9jv","McdtiUVkfbSjBybiNhgR12pk"))
    order = client.order.create(dict(amount=amount, currency='INR'))
    return order["id"]

def init_cookie(request):
    if not 'order_id' in request.COOKIES:
        new_order = Order.objects.create()
        return new_order.id
    else:
        return request.COOKIES['order_id']
