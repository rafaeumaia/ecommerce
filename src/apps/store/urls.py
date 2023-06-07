from django.urls import path
from apps.store.views import (
    StoreList,
    CartView,
    CheckoutView
)


urlpatterns = [
    path('', StoreList.as_view(), name='store'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]