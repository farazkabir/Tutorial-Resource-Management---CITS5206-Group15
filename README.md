# Tutorial Resource Management — CITS5206 Group 15

## Project Purpose

A **tutorial resource platform** for the WMAA (Western Martial Arts Academy), built to help members learn how to use the WMAA website through categorized guides, videos, and documents.

- **Visitors** — browse tutorials on the public homepage, view rich-text guides, watch embedded YouTube videos, read inline PDFs, and follow external document links.
- **Admins** — log in to create, edit, and delete tutorials with a dynamic form that adapts to the content type (text, video, document, or mixed media). Upload thumbnails, PDFs, and video files.

### Features

- Tutorials organised by category (Getting Started, Navigation, Account, Features, Media, Troubleshooting)
- Four media types with a dynamic form — fields show/hide based on selection
- Rich text editor (Quill.js) for formatted content
- YouTube video embedding
- PDF and video file uploads with inline preview
- External document URL support (Google Docs, Notion, etc.)
- Publish/draft status and display ordering
- Responsive design (Tailwind CSS)

## Tech Stack

- **Backend:** Flask, SQLAlchemy, Flask-Login, Flask-Migrate
- **Frontend:** Tailwind CSS (CDN), Quill.js rich text editor
- **Database:** SQLite (development)

## Quick Start

### 1. Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialise the database

```bash
flask --app wsgi:app db init
flask --app wsgi:app db migrate -m "initial"
flask --app wsgi:app db upgrade
```

### 4. Seed the database (admin user + sample content)

```bash
python seed.py
```

This creates:
- **Admin account** — username `admin`, password `admin`
- **6 categories** — Getting Started, Navigation, Account, Features, Media, Troubleshooting
- **8 sample tutorials** — a mix of text guides, a video tutorial, and a document, with realistic content

Options:

```bash
python seed.py          # add seed data (skips if data already exists)
python seed.py --reset  # drop all tables, recreate, and seed from scratch
```

### 5. Run the app

```bash
flask --app wsgi:app run --debug
```

The app will be available at **http://127.0.0.1:5000**.

## Routes

| Route | Description |
|---|---|
| `/` | Public homepage — browse all tutorials |
| `/materials` | Same as homepage |
| `/materials/<id>` | View a single tutorial (video, PDF, rich text) |
| `/auth/login` | Admin login page |
| `/auth/logout` | Log out |
| `/admin/` | Admin dashboard — list, edit, delete tutorials |
| `/admin/materials/create` | Create a new tutorial |
| `/admin/materials/<id>/edit` | Edit an existing tutorial |
| `/admin/materials/<id>/delete` | Delete a tutorial (POST) |

## Project Structure

```
├── wsgi.py                   # Flask entry point
├── seed.py                   # Database seed script
├── requirements.txt          # Python dependencies
├── web/
│   ├── __init__.py           # App factory
│   ├── config.py             # Configuration (uploads, DB, etc.)
│   ├── extensions.py         # Flask extensions (db, login, migrate)
│   ├── models.py             # SQLAlchemy models
│   ├── main/routes.py        # Public routes
│   ├── auth/routes.py        # Login / logout
│   ├── admin/routes.py       # Admin CRUD
│   ├── templates/            # Jinja2 HTML templates
│   └── static/
│       ├── css/home.css
│       └── uploads/          # User-uploaded files
├── instance/app.db           # SQLite database (auto-created)
└── migrations/               # Alembic migration files
```
