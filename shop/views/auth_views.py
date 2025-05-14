

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from shop.forms import SignUpForm, SellerSignUpForm, CustomerSignUpForm

User = get_user_model()

# ------------------------
# LOGIN VIEWS
# ------------------------

def customer_login(request):
    return user_login(request, user_type='customer')


def seller_login(request):
    return user_login(request, user_type='seller')


def user_login(request, user_type=None):
    """Handles login for both customers and sellers."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on user type
            if user.is_customer:
                return redirect('customer_dashboard')
            elif user.is_seller:
                return redirect('seller_dashboard')
            else:
                return redirect('home')  # Default redirection if no role is assigned
        else:
            messages.error(request, 'Invalid credentials, please try again.')
            return render(request, 'shop/login.html', {
                'user_type': user_type,
                'msg': 'Invalid username or password.'
            })
    else:
        return render(request, 'shop/login.html', {'user_type': user_type})


# ------------------------
# LOGOUT VIEW
# ------------------------

def user_logout(request):
    """Logs the user out and redirects to login page."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')



def customer_dashboard(request):
    return render(request, 'shop/customer_dashboard.html')


def customer_signup(request):
    if request.method == "POST":
        form =  CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in immediately after signup
            
            # Success message
            messages.success(request, "Signup successful! Welcome to your dashboard.")
            
            return redirect('customer_dashboard')  # Replace with the name of your dashboard view
    else:
        form = CustomerSignUpForm()
    
    return render(request,'shop/signup_customer.html', {'form': form})




# ------------------------
# SELLER SIGNUP
# ------------------------

def seller_signup(request):
    """Handles seller signup process."""
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_seller = True
            
            # user.set_password(form.cleaned_data['password']) 
            user.is_staff = True  # Make seller a staff member, ensure you want this
            user.set_password(form.cleaned_data['password1'])  # Ensure password is hashed
            user.save()

            # Automatically log the user in after signup
            login(request, user)

            messages.success(request, f"Welcome {user.username}! Your seller account has been created.")
            return redirect('seller_dashboard')  # Ensure this URL is defined in urls.py
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SellerSignUpForm()

    return render(request, 'shop/signup_seller.html', {'form': form})


# ------------------------
# GENERIC LOGIN VIEW (with AuthenticationForm)
# ------------------------

def login_view(request):
    """A generic login view that uses Django's built-in AuthenticationForm."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Redirect user to their respective dashboard
                if user.is_seller:
                    return redirect('seller_dashboard')
                elif user.is_customer:
                    return redirect('customer_dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Invalid login credentials. Please try again.")
                return redirect('login')  # Redirect back to login page if authentication fails
        else:
            messages.error(request, "Form is not valid. Please try again.")
            return redirect('login')  # Redirect back to login page if form is not valid
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})
