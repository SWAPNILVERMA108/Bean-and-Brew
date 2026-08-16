# Bean & Brew

Bean & Brew is a Django-based coffee ordering platform where users can explore coffee varieties, find stores, create accounts, and place orders. Store staff receive and manage order requests through a secure dashboard, while users can track their order status.

## Features

- Browse coffee varieties and view their details
- Search stores that serve a selected coffee
- Create an account, log in, and log out
- Send coffee order requests to a store
- Track personal order requests and their status
- View incoming store requests as assigned staff
- Manage coffees, stores, staff assignments, and orders through Django admin
- Responsive interface built with Tailwind CSS

## Technology

- Python and Django
- SQLite
- Django authentication
- Tailwind CSS

## Setup

1. Create and activate a virtual environment.

2. Install the project dependencies.

```bash
pip install django django-tailwind pillow django-browser-reload
```

3. Apply database migrations.

```bash
python manage.py migrate
```

4. Build the Tailwind stylesheet.

```bash
python manage.py tailwind build
```

5. Start the development server.

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Main routes

| Route | Purpose |
| --- | --- |
| `/` | Home page |
| `/coffee/` | Coffee catalogue |
| `/coffee/stores/` | Store finder |
| `/coffee/order/` | Place an order (login required) |
| `/coffee/orders/` | User order history (login required) |
| `/coffee/store-orders/` | Store request queue (staff only) |
| `/accounts/signup/` | Create an account |
| `/accounts/login/` | Log in |
| `/admin/` | Admin dashboard |

## Store order workflow

1. An administrator creates coffee varieties and stores.
2. Each store is linked to the coffee varieties it serves.
3. A customer logs in and submits an order request.
4. The request appears in the assigned store staff queue and Django admin.
5. Store staff update the order status: New, Accepted, Ready, Completed, or Cancelled.

## Assigning store staff

Create a staff user in Django admin, then open the relevant **Store** record and add that user under **Staff members**. The staff member will then see requests for that store in the store queue.
