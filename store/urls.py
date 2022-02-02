from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    create_supplier,
    create_buyer,
    create_office,
    create_drop,
    create_product,
    create_order,
    create_delivery,
    product_list,
    SupplierListView,
    RecipientListView,
    LocationListView,
    SectionListView,
    #ProductListView,
    OrderListView,
    DeliveryListView,
    search_products,
)

urlpatterns = [
    path('create-supplier/', create_supplier, name='create-supplier'),
    path('create-buyer/', create_buyer, name='create-buyer'),
    path('create-office/', create_office, name='create-office'),
    path('create-drop/', create_drop, name='create-drop'),
    path('create-product/', create_product, name='create-product'),
    path('create-order/', create_order, name='create-order'),
    path('create-delivery/', create_delivery, name='create-delivery'),

    path('supplier-list/', SupplierListView.as_view(), name='supplier-list'),
    path('buyer-list/', RecipientListView.as_view(), name='buyer-list'),
    path('office-list/', LocationListView.as_view(), name='office-list'),
    path('drop-list/', SectionListView.as_view(), name='drop-list'),
    path('product-list/', product_list, name='product-list'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('delivery-list/', DeliveryListView.as_view(), name='delivery-list'),
    path('create-order/search-products', csrf_exempt(search_products), name='search-products'),
]
