from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=False, null=False)
    contact_number = models.IntegerField(null=False, blank=False)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.name} {self.id}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.id}"

class Order(models.Model):
    order_number = models.CharField(max_length=10,unique=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.all().order_by('-id').first()
            if last_order:
                last_order_number = int(last_order.order_number[3:])
                new_order_number = f"ORD{str(last_order_number + 1).zfill(5)}"
            else:
                new_order_number = "ORD00001"
            self.order_number = new_order_number
        super().save(*args, **kwargs)

    
    
    def __str__(self):
        return f"{self.address} {self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(null=False)

    def get_item_weight(self):
        return self.product.weight * self.quantity
    
    def __str__(self):
        return f"{self.quantity}"
    

