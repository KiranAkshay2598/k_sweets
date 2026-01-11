# The Desi Pantry - Django E-Commerce Application

## About The Project

This is **The Desi Pantry** (internally codenamed *k_sweets*), an e-commerce platform for traditional Indian sweets. 

I originally built this back in **2020** as my first deep dive into web development. My main goal here was to really understand **Backend Architecture** and get hands-on experience with **Django's MVT (Model-View-Template)** flow.

While the core focus was on solid backend logic, I used **Django Template Language (DTL)** and **Jinja2** to handle the frontend dynamic data, integrating it all into a custom HTML/CSS template.

### Key Features
*   **E-Commerce Flow**: Standard shopping experience—browse categories, add products to cart, and checkout.
*   **Telegram Notifications**: A cool feature for the admin—when an order is placed, the owner gets an instant ping on Telegram.
*   **Payments**: Real payment processing integrated with Razorpay.
*   **Dynamic Content**: Everything you see—products, categories, prices—is pulled straight from the SQLite database.

---

## Tech Stack
*   **Backend Framework**: Django 5.2 (Python)
*   **Frontend**: HTML5, CSS3, Bootstrap, Django Template Language (DTL)
*   **Database**: SQLite (Default)
*   **Payment Gateway**: Razorpay
*   **Notifications**: Python Telegram Bot

---

## Getting Started (Installation Guide)

Follow these steps to clone and run the application locally.

### 1. Clone the Repository
```bash
git clone https://github.com/KiranAkshay2598/k_sweets.git
cd k_sweets
```

### 2. Create & Activate Virtual Environment
It is highly recommended to use a virtual environment.
```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named `.env` in the root directory (next to `manage.py`). 
Add the following keys with your own credentials:

```ini
# .env file content

DEBUG=True
SECRET_KEY=your_django_secret_key_here

# Payment Integration (Razorpay)
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# Notification System (Telegram)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

### 5. Database Setup (Migrations)
Initialize the database tables.
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Collect Static Files
The `assets` folder (containing compiled static files) is excluded from version control. You must generate these files locally:
```bash
python manage.py collectstatic
```
*(Type `yes` if prompted)*

### 7. Load Demo Data (Optional)
I have provided a fixture file containing sample categories and products (images included in `fixtures/images`). This allows you to test the website immediately without manual data entry.

**Note:** You are free to create your own data via the Django Admin panel, but this command gives you a head start.

```bash
# Update the database with seed data
python manage.py loaddata catalog_data.json
```

_This will verify that the media is correctly mapped from the `fixtures/` directory._

### 8. Create Superuser (Admin Access)
To access the admin panel and manage orders/products:
```bash
python manage.py createsuperuser
```

### 9. Run the Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to see the app!

---

## Project Structure

*   **/kaviya_sweets** - Inner project folder (Settings, URLs, WSGI)
*   **/ks_app** - Main application logic (Views, Models, Migrations)
*   **/templates** - HTML Templates using DTL
*   **/static** - Source static files (CSS, JS, Images)
*   **/fixtures** - Seed data and demo images
*   **manage.py** - Django entry point
*   **requirements.txt** - Python dependencies


