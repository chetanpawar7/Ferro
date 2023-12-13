from rest_framework import generics
from .models import Customer, Product, Order,OrderItem
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer,OrderItemSerializer
from django.db.models import Q

# Create your views here.
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderSearchView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        products_query = Q(order_items__product__name__icontains=query)
        customer_query = Q(customer__name__icontains=query)
        queryset = Order.objects.filter(products_query | customer_query).distinct()
        return queryset