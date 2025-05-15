# 🛒 ecommerce_website

A fully functional **eCommerce web application** built with Django, featuring seller and customer login, product listings with multiple image support, a shopping cart, order management, real-time notifications, and more — all inspired by Flipkart.

---

## 📌 Features

- 👥 Separate login/registration for **Customers** and **Sellers**
- 🛍️ **Product listing** with support for **multiple images** (JPG, PNG, WebP)
- ❤️ Add to **Wishlist**, **Buy Now**, or add to **Cart**
- 📦 **Order tracking** with status updates and **PDF invoices**
- 🔔 **Real-time notifications** for order events
- 🧾 **Seller dashboard** with stock & product management
- 📊 Admin panel for superuser
- 🎨 Modern UI styled like **Flipkart**

---

## 🖥️ Tech Stack

- **Backend**: Django 4.x, Python 3.x
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: SQLite (default) / PostgreSQL (optional)
- **Auth**: Django's built-in User model (extended)
- **PDF Invoices**: `xhtml2pdf`
- **Media Storage**: Django File Uploads

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.10 or higher
- Git & pip
- Virtualenv (recommended)

### ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/nileshyadav12/ecommerce_website.git
cd ecommerce_website

# Create virtual environment
python -m venv env
# Activate it
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver
