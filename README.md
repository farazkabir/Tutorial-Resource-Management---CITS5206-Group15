# Tutorial-Resource-Management---CITS5206-Group15
# Simple Teaching Video Platform

## Project Purpose

This is a **minimalist teaching video website** (similar to a lightweight version of WordPress), designed specifically for teachers and instructors.

* **Visitors / Regular Users**: Browse categorized teaching videos on the homepage (supports YouTube links or direct video file uploads)
* **Admin Only**: Can upload videos and manage categories
* **Admin Access**: Visit `/admin` to enter the admin login page

Features:

* Homepage displays video cards organized by category
* Supports YouTube embedding and local video uploads
* Simple category system (e.g., programming, mathematics, design, languages, etc.)
* Responsive design for both mobile and desktop

## Tech Stack

* Flask + SQLAlchemy + Flask-Login + Flask-Migrate
* Bootstrap + Chart.js (will gradually be replaced with video display features)
* Supports YouTube iframe embedding

## Installation Steps

```bash
# 1. Create virtual environment
python3 -m venv .venv
.venv/bin/activate    # On Windows use .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Database migration (first time)
flask --app app:create_app db init
flask --app app:create_app db migrate -m "init"
flask --app app:create_app db upgrade

# 4. Run the app
flask --app app:create_app run
```

## Routes

* `/` Home
* `/materials/<id>` View material
* `/auth/login` Login
* `/admin/materials` Admin (requires login + admin user)
