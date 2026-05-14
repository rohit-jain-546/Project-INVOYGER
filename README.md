# INVOYGER (link - https://invoyger.rohitj.dev/)

![Django](https://img.shields.io/badge/Django-6.x-0C4B33?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Project-Active-success)
![License](https://img.shields.io/badge/License-MIT-blue)

Role-based Django online marketplace with separate customer/admin workflows, cart + checkout pipeline, order lifecycle, and downloadable PDF invoices.

## Why This Project Stands Out

- Built as a modular multi-app Django architecture, not a single monolith
- Real marketplace flow: browse -> cart -> checkout -> order -> invoice
- Role-based authorization with dedicated dashboards
- Invoice PDFs generated server-side using ReportLab
- Clean foundation for scaling into production (payments, shipping, analytics)

## Demo Screens

Add your screenshots at these exact paths to render automatically:

![Public Home](docs/images/public-home.png)
![Customer Home](docs/images/customer-home.png)
![Cart](docs/images/cart.png)
![Order Summary](docs/images/order-summary.png)
![Admin Dashboard](docs/images/admin-dashboard.png)
![Admin Orders](docs/images/admin-orders.png)

## Features

- Authentication + role profiles (`Customer`, `AdminUser`)
- Product CRUD with image upload, stock, active/inactive status
- Category filtering (Men, Women, Kids, Accessories, Universal)
- Persistent cart and quantity updates
- Checkout that snapshots product data into order items
- Admin order management and status updates
- PDF invoice download for customer and admin

## Tech Stack

- Python, Django 6
- SQLite (dev DB)
- Django Templates + HTML/CSS
- ReportLab (PDF generation)
- Pillow (image support)

## Architecture

```text
authsys/
|-- manage.py
|-- authsys/         # settings, root urls, wsgi/asgi
|-- accounts/        # auth + role models
|-- adminpanel/      # admin dashboard, product/order controls
|-- shop/            # storefront, categories, cart
|-- orders/          # checkout, order success, invoice pdf
|-- static/
`-- media/
```

## Data Model (Core)

- `Product`: catalog item with price, stock, category, image, active status
- `cart` + `cartitem`: user cart persistence and quantities
- `Order`: generated `order_id`, status, total, timestamps
- `OrderItem`: immutable snapshot (`product_name`, `price`, `quantity`, `line_total`)
- `Customer` / `AdminUser`: role profiles linked to `User`

## Local Setup

```bash
git clone <your-repo-url>
cd authsys
python -m venv .venv
```

Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

Install deps and run:

```bash
pip install django reportlab pillow
python manage.py migrate
python manage.py runserver
```

App URL: `http://127.0.0.1:8000/`

## Main Routes

- `/` public home
- `/signup/`, `/login/`, `/logout/`
- `/shop/`, `/shop/cart/`
- `/orders/checkout/`
- `/orders/order-success/<order_id>/`
- `/orders/invoice/<order_id>/`
- `/adminpanel/`
- `/adminpanel/orders/`

## Production Notes

- `DEBUG=True` and `ALLOWED_HOSTS=['*']` are development settings
- Admin signup code in `accounts/views.py` is hardcoded; move to env var
- Use PostgreSQL/MySQL + proper secrets management for deployment

## Roadmap

- Add `requirements.txt` with pinned versions
- Add automated tests for checkout + role access
- Add CI pipeline (lint + tests)
- Integrate payment gateway and shipping updates
- Harden security settings and deployment config

## Author

Rohit Jain  
LinkedIn: https://www.linkedin.com/in/546-rohit-jain

