# shop/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from shop.models import Product, Address, Order, OrderItem, Payment

# Get the custom user model if you're using one
User = get_user_model()

# -------------------------------
# Login Form
# -------------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

# Customer and Seller Login forms
class CustomerLoginForm(AuthenticationForm):
    pass

class SellerLoginForm(AuthenticationForm):
    pass

# -------------------------------
# User Sign Up Forms
# -------------------------------

# SignUpForm for generic user creation
class SignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

# Customer SignUp form (inherits from UserCreationForm)
class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Seller SignUp form with additional business-related fields
class SellerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    # Add any other fields relevant to the seller signup here.

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'company_name']

# -------------------------------
# Edit Profile Form
# -------------------------------
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This email is already in use by another account.")
        return email

# -------------------------------
# Product Form
# -------------------------------
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'image']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise ValidationError("Stock quantity cannot be negative.")
        return quantity

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Image size must not exceed 5MB.")
            if hasattr(image, 'content_type') and image.content_type not in ['image/jpeg', 'image/png']:
                raise ValidationError("Only JPG and PNG formats are allowed.")
        return image

# -------------------------------
# Address Form
# -------------------------------
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'zip_code', 'country', 'is_billing_address']

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not zip_code.isdigit():
            raise ValidationError("Zip code must be numeric.")
        if len(zip_code) < 5 or len(zip_code) > 10:
            raise ValidationError("Zip code must be between 5 and 10 digits.")
        return zip_code

# -------------------------------
# Order & OrderItem Forms
# -------------------------------
class OrderForm(forms.ModelForm):
    shipping_address = forms.ModelChoiceField(queryset=Address.objects.all(), required=True, label="Shipping Address")

    class Meta:
        model = Order
        fields = ['shipping_address']

    def clean_shipping_address(self):
        shipping_address = self.cleaned_data.get('shipping_address')
        if not shipping_address:
            raise ValidationError("Please select a valid shipping address.")
        return shipping_address

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')

        if product and quantity and quantity > product.quantity:
            raise ValidationError(f"Not enough stock available for {product.name}.")
        return cleaned_data

# -------------------------------
# Payment Form
# -------------------------------
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'emi_months', 'emi_amount', 'card_number']

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('payment_method')
        emi_amount = cleaned_data.get('emi_amount')
        emi_months = cleaned_data.get('emi_months')
        card_number = cleaned_data.get('card_number')

        if method == 'EMI':
            if not emi_months or not emi_amount:
                raise ValidationError("EMI months and amount are required for EMI.")
            if hasattr(self.instance, 'order') and self.instance.order.total_price < emi_amount * emi_months:
                raise ValidationError("EMI total exceeds order amount.")
        
        if method in ['Credit Card', 'Debit Card'] and not card_number:
            raise ValidationError("Card number is required for selected card payment.")
        return cleaned_data

# -------------------------------
# Checkout Form
# -------------------------------
class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    address = forms.CharField(max_length=1024)
    city = forms.CharField(max_length=255)
    state = forms.CharField(max_length=255)
    postal_code = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()
    payment_method = forms.ChoiceField(choices=[ 
        ('cash_on_delivery', 'Cash on Delivery'),
        ('credit', 'Credit Card'),
        ('paypal', 'PayPal')
    ])

# -------------------------------
# Shipping Details Form
# -------------------------------
class ShippingDetailsForm(forms.Form):
    shipping_address = forms.ModelChoiceField(queryset=Address.objects.all(), required=True, label="Shipping Address", empty_label="Select a shipping address")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass user to filter addresses
        super().__init__(*args, **kwargs)
        if user:
            self.fields['shipping_address'].queryset = Address.objects.filter(user=user)
