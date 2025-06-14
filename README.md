# Django Blog Site 📝

A simple Django-powered blog platform to manage posts, media, and user dashboards.

## 🔧 Features

- Blog post creation and editing
- Media management
- Admin dashboard
- Clean UI with custom styling
- SQLite3 database by default

## 🚀 Setup

```bash
git clone https://github.com/your-username/blog-site.git
cd blog-site

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

## 📁 Structure

```
Blog Site/
├── blog/
├── dashboard/
├── static/
├── templates/
├── media/
├── db.sqlite3
├── manage.py
```

## 🛡️ License

MIT — Use it freely!
