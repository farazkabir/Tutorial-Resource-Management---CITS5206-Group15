# Tutorial Resource Management — CITS5206 Group 15

## Project Purpose

A **tutorial resource platform** for the WMAA (Western Martial Arts Academy), built to help members learn how to manage and use the WMAA WordPress website through categorized guides, videos, and documents.

- **Visitors** — browse tutorials on the public homepage, view rich-text guides, watch embedded YouTube videos, read inline PDFs, and follow external document links.
- **Admins** — log in to create, edit, and delete tutorials with a dynamic form that adapts to the content type (text, video, document, or mixed media). Upload thumbnails, PDFs, and video files.

### Features

- Tutorials organised by category (WordPress Basics, Astra Theme, Elementor, Media & Embeds, Site Administration, Troubleshooting)
- Four media types with a dynamic admin form — fields show/hide based on selection
- Rich text editor (Quill.js) for formatted content
- YouTube video embedding
- PDF and video file uploads with inline preview
- External document URL support (Google Docs, Elementor Help Center, etc.)
- Publish/draft status and display ordering
- Responsive design (Tailwind CSS)

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask, SQLAlchemy, Flask-Login, Flask-Migrate |
| Frontend | Tailwind CSS (CDN), Quill.js, AOS scroll animations |
| Database | SQLite (`instance/app.db` in development) |

## Prerequisites

- **Python 3.10+** — check with `python --version`
- **pip** — included with Python
- **Git** (optional) — to clone the repository

## Quick Start

### 1. Clone and open the project

```bash
cd Tutorial-Resource-Management---CITS5206-Group15
```

### 2. Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialise the database

Migrations are already included in the `migrations/` folder. Apply them to create tables:

```bash
flask --app wsgi:app db upgrade
```

If you are setting up a **brand-new** project without existing migrations, run:

```bash
flask --app wsgi:app db init
flask --app wsgi:app db migrate -m "initial"
flask --app wsgi:app db upgrade
```

### 5. Seed the database

The seed script loads an admin account, categories, and WordPress tutorials (Astra theme, Elementor, etc.):

```bash
python seed.py
```

| Command | What it does |
|---------|----------------|
| `python seed.py` | Creates missing data; **updates** tutorials that match by title |
| `python seed.py --reset` | **Deletes all tables**, recreates them, then seeds from scratch |

**Default admin login** (created by seed):

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin` |

Change this password after first login via **Admin → Settings → Change Password**.

**What gets seeded:**

- 1 admin user
- 6 categories (WordPress Basics, Astra Theme, Elementor, Media & Embeds, Site Administration, Troubleshooting)
- 12 tutorials — text guides, YouTube videos (Astra/Elementor), and external document links

### 6. Run the application

```bash
flask --app wsgi:app run --debug
```

Open **http://127.0.0.1:5000** in your browser.

To listen on all interfaces (e.g. test from a phone on the same network):

```bash
flask --app wsgi:app run --debug --host=0.0.0.0
```

### 7. Stop the server

Press **Ctrl+C** in the terminal where Flask is running.

---

## Common Workflows

### First-time setup (full sequence)

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows
pip install -r requirements.txt
flask --app wsgi:app db upgrade
python seed.py --reset
flask --app wsgi:app run --debug
```

### Refresh sample data only

```bash
python seed.py --reset
```

### Add or refresh tutorials without wiping the database

```bash
python seed.py
```

Edits to tutorial definitions in `seed.py` are applied to existing rows when the **title** matches.

### After changing database models

```bash
flask --app wsgi:app db migrate -m "describe your change"
flask --app wsgi:app db upgrade
```

---

## Environment Variables (optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `dev-secret-change-me` | Flask session signing key — set in production |
| `DATABASE_URL` | `sqlite:///app.db` | SQLAlchemy database URI |

Example (PowerShell):

```powershell
$env:SECRET_KEY = "your-production-secret"
flask --app wsgi:app run
```

---

## Routes

| Route | Description |
|-------|-------------|
| `/` | Public homepage — browse all tutorials |
| `/materials` | Tutorial list with optional `?category_id=` filter |
| `/materials/<id>` | View a single tutorial (video, PDF, rich text) |
| `/auth/login` | Admin login page |
| `/auth/logout` | Log out |
| `/auth/change-password` | Change password (logged in) |
| `/admin/` | Admin dashboard — list, edit, delete tutorials |
| `/admin/materials/create` | Create a new tutorial |
| `/admin/materials/<id>/edit` | Edit an existing tutorial |
| `/admin/materials/<id>/delete` | Delete a tutorial (POST) |

---

## Project Structure

```
├── wsgi.py                   # Flask entry point (imports create_app)
├── seed.py                   # Database seed script (admin, categories, tutorials)
├── requirements.txt          # Python dependencies
├── web/
│   ├── __init__.py           # Application factory (create_app)
│   ├── config.py             # Configuration (DB, uploads, secret key)
│   ├── extensions.py         # Flask extensions (db, login, migrate)
│   ├── models.py             # SQLAlchemy models (User, Category, Material, Attachment)
│   ├── main/routes.py        # Public routes (home, materials, view)
│   ├── auth/routes.py        # Login, logout, change password
│   ├── admin/routes.py       # Admin CRUD and file uploads
│   ├── templates/            # Jinja2 HTML templates
│   └── static/
│       ├── css/home.css      # Supplemental styles (nav links, etc.)
│       └── uploads/          # User-uploaded thumbnails, PDFs, videos
├── instance/app.db           # SQLite database (created on first run)
└── migrations/               # Alembic migration files
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Activate `.venv` and run `pip install -r requirements.txt` |
| Database is empty / no tutorials | Run `python seed.py` or `python seed.py --reset` |
| `OperationalError: no such table` | Run `flask --app wsgi:app db upgrade` |
| Port 5000 already in use | Stop the other process or use `flask --app wsgi:app run --port 5001` |
| Uploaded files not showing | Check `web/static/uploads/` exists and the app has write permission |

---

## Development Notes

- **Upload limit:** 50 MB per request (`web/config.py`)
- **Allowed uploads:** PDF, DOC/DOCX, images, common video formats (see `web/admin/routes.py`)
- **Seed data source:** All sample WordPress/Astra/Elementor content is defined in `seed.py`

## License

Academic project — CITS5206 Group 15, UWA.
