# Reading Club

A Django-based web application for tracking your reading life — add books, write reviews, manage collections, and keep a wishlist and read list.

## Features

- Browse and search books by title, genre, and author
- Write and rate reviews
- Create thematic book collections
- Save favorites and mark books as read
- User profiles with reading statistics
- REST API for books and authors
- Async image processing via Celery + Redis

## Tech Stack

- Django 6.0 + Django REST Framework
- PostgreSQL
- Celery + Redis (async tasks)
- Bootstrap 5

## Setup

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd Reading-Club
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create `.env` file

Copy the example below and fill in your values:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=readingclub_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432

CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

### 3. Create the database

```bash
createdb readingclub_db
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run the development server

```bash
python manage.py runserver
```

### 5. Run Celery worker (in a separate terminal)

```bash
celery -A Reading_Club worker -l info
```

## Deployment

Deployed at: ``

For production, set `DEBUG=False` and add your domain to `ALLOWED_HOSTS`.