import telegram
import razorpay


def send_telegram_message(msg):
    token = '1476623880:AAGCjhLjuSzDBym_j1zgZKIpFkMlDDAdX7Q'
    chat_id = 1426070442
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)

def razorpay_gateway(amount):
    client = razorpay.Client(auth=("rzp_test_BzpuQZbbNkr9jv","McdtiUVkfbSjBybiNhgR12pk"))
    order = client.order.create(dict(amount=amount, currency='INR'))
    return order["id"]