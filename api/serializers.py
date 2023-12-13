from django.utils import timezone
import datetime
from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate_name(self, value):
        if Customer.objects.filter(name=value).exists():
            raise serializers.ValidationError("Customer with this name is already exists.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_product_name(self, value):
        if Product.objects.filter(name=value).exists():
             raise serializers.ValidationError("Product with this name already exists.")
        return value

    def validate_weight(self,value):
        if value <=0 or value >=25:
            raise serializers.ValidationError("Weight must be a positive decimal and not more than 25kg.")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product','quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['order_number','customer','order_date','address','order_items']
        read_only = ['order_number']

    def create(self,validated_data):
        order_items_data = validated_data.pop('order_items',[])
        order = Order.objects.create(**validated_data)
        for item in order_items_data:
            OrderItem.objects.create(order=order,**item)
        return order

    def validate_order_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value
    

    def validate_order_items_weight(self, order_items_data):
        total_weight = sum(item.get('weight', 0) for item in order_items_data)
        if total_weight > 150:
            raise serializers.ValidationError("Total order weight exceeds 150kg.")



        
        