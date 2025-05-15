from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
        
        
        
class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')  # Custom User model
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return self.name

    def update_stock(self, quantity_sold):
        """
        Update the product stock after a sale.
        Raises a ValidationError if stock is insufficient.
        """
        if quantity_sold > self.quantity:
            raise ValidationError("Not enough stock available.")
        with transaction.atomic():
            self.quantity -= quantity_sold
            self.update_availability()  # Ensure availability is updated after stock is modified
            self.save()

    def is_in_stock(self):
        """
        Check if the product is in stock.
        """
        return self.quantity > 0

    def restock(self, additional_stock):
        """
        Restock the product with additional stock.
        """
        if additional_stock < 0:
            raise ValidationError("Restock quantity cannot be negative.")
        with transaction.atomic():
            self.quantity += additional_stock
            self.update_availability()  # Ensure availability is updated after restocking
            self.save()

    def update_availability(self):
        """
        Update the product's availability based on stock quantity.
        If stock is greater than 0, the product is available.
        """
        self.available = self.is_in_stock()
        self.save()

    class Meta:
        ordering = ['name']
        
class ProductImage(models.Model):
     product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
     image = models.ImageField(upload_to='product_images/')

     def __str__(self):
        return f"{self.product.name} Image"       
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, 
        choices=[('active', 'Active'), ('completed', 'Completed')],
        default='active'
    )

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

    def calculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        return total

    def clear_cart(self):
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Assuming Product is defined in your app
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        # Check if the product is in stock; if not, return 0
        if hasattr(self.product, 'is_in_stock') and self.product.is_in_stock():
            return self.quantity * self.product.price
        return Decimal('0.00')

    def __str__(self):
        return f"{self.product.name} (Qty: {self.quantity})"
    
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    is_billing_address = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

    def clean(self):
        if not self.zip_code.isdigit():
            raise ValidationError("Zip code must be numeric.")
        if len(self.zip_code) < 5 or len(self.zip_code) > 10:
            raise ValidationError("Zip code must be between 5 and 10 digits.")    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('cash_on_delivery', 'Cash on Delivery'),
        ('credit', 'Credit Card'),
        ('paypal', 'PayPal')
    ])
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(default="placeholder@example.com")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def update_status(self, new_status):
        if new_status in ['shipped', 'delivered']:
            for item in self.order_items.all():
                item.product.update_stock(item.quantity)
        self.status = new_status
        self.save()
        self.notify_users()

    def notify_users(self):
        product = self.order_items.first().product
        Notification.create_notification(
            recipient=self.user,
            message=f"Your order for '{product.name}' has been updated to '{self.status}'.",
            order=self,
            product=product
        )
        Notification.create_notification(
            recipient=product.seller,
            message=f"Your product '{product.name}' was purchased by {self.user.username}.",
            order=self,
            product=product
        )


# --- OrderItem ---
class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        if self.status in ['Shipped', 'Delivered']:
            self.product.update_stock(self.quantity)
        elif self.status in ['Cancelled', 'Returned']:
            self.product.restock(self.quantity)
        super().save(*args, **kwargs)


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        ('Cash on Delivery', 'Cash on Delivery'),
        ('EMI', 'EMI'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    EMI_STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    emi_status = models.CharField(max_length=20, choices=EMI_STATUS_CHOICES, default='Not Started', blank=True, null=True)
    emi_months = models.PositiveIntegerField(null=True, blank=True)
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.payment_status}"

    def clean(self):
        if self.payment_method == 'EMI':
            if not self.emi_months or not self.emi_amount:
                raise ValidationError("EMI months and EMI amount are required for EMI.")
            if self.order.total_price < self.emi_amount * self.emi_months:
                raise ValidationError("EMI amount exceeds total order price.")
        if self.payment_method in ['Credit Card', 'Debit Card'] and not self.card_number:
            raise ValidationError("Card number is required for card payments.")
class Review(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'product')

    def __str__(self):
        return f"Review by {self.customer.username} on {self.product.name} - {self.rating}/5"

class Wishlist(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'product')

    def __str__(self):
        return f"{self.customer.username}'s wishlist - {self.product.name}"



class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"

    @classmethod
    def create_notification(cls, recipient, message, order=None, product=None):
        return cls.objects.create(
            recipient=recipient,
            message=message,
            order=order,
            product=product
        )
