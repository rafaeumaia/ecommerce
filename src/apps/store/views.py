import json

from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from django.views.generic.base import ContextMixin

from apps.store.models import Product, Order, OrderItem


# Create your views here.

class CartContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cart_items = order.cart_items
        else:
            items = []
            order = {'cart_total': 0, 'cart_items': 0, 'shipping': False}
            cart_items = order['cart_items']

        context['items'] = items
        context['order'] = order
        context['cart_items'] = cart_items
        return context


class StoreList(CartContextMixin, ListView):
    model = Product
    template_name = 'store/store.html'


class CartView(CartContextMixin, TemplateView):
    template_name = 'store/cart.html'


class CheckoutView(CartContextMixin, TemplateView):
    template_name = 'store/checkout.html'


def updateitem(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    print('action', action)
    print('productId', product_id)

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created, = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)
