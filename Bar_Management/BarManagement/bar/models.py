from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models



class CustomUser(AbstractUser):
    USER_ROLES = (
        ('owner', 'Owner/Manager'),
        ('counterman', 'Counterman'),
        ('waiter', 'Waiter'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES)
    
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')

    class Meta:
        # Add a unique app_label to avoid clashes
        app_label = 'bar'

class Drink(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_level = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    waiter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    drinks = models.ManyToManyField(Drink)
    timestamp = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


