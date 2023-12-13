from django.urls import path
from .views import CustomerListCreateView,CustomerUpdateView , ProductListCreateView ,OrderListCreateView, OrderUpdateView,OrderSearchView
urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>', CustomerUpdateView.as_view(), name='customer-update'),
    path('products/',ProductListCreateView.as_view(),name='product-list-create'),
    path('orders/',OrderListCreateView.as_view(),name='order-list-create'),
    path('orders/<int:pk>',OrderUpdateView.as_view(),name='order-update'),
    path('orders/', OrderSearchView.as_view(), name='order-search'),
]







