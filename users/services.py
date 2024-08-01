import stripe
from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_product_stripe(instance):
    """Создание продукта в stripe"""
    title_product = f'{instance.payment_course}' if instance.payment_course else f'{instance.payment_lesson}'
    stripe_product = stripe.Product.create(name=f'{title_product}')
    return stripe_product.get('id')


def create_price_stripe(payment_sum, product):
    """Создание цены в stripe"""
    return stripe.Price.create(
        currency='rub',
        unit_amount=payment_sum * 100,
        product=product
    )


def create_session_stripe(price):
    """Сессия на оплату в stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')