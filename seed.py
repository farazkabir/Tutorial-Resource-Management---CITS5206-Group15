"""
Seed script — populates the database with an admin user, categories,
and sample tutorials so the app has content out of the box.

Usage:
    python seed.py          # seed everything
    python seed.py --reset  # drop all tables first, then seed
"""

import sys

from wsgi import app
from web.extensions import db
from web.models import Category, Material, User


def seed():
    # ── Admin user ───────────────────────────────────────────────
    if not User.query.filter_by(username="admin").first():
        u = User(username="admin", is_admin=True)
        u.set_password("admin")
        db.session.add(u)
        print("  + Created admin user (admin / admin)")
    else:
        print("  • Admin user already exists, skipping")

    # ── Categories ───────────────────────────────────────────────
    category_defs = [
        ("Getting Started", "getting_started"),
        ("Navigation", "navigation"),
        ("Account", "account"),
        ("Features", "features"),
        ("Media", "media"),
        ("Troubleshooting", "troubleshooting"),
    ]
    cats = {}
    for name, slug in category_defs:
        cat = Category.query.filter_by(slug=slug).first()
        if not cat:
            cat = Category(name=name, slug=slug)
            db.session.add(cat)
            print(f"  + Category: {name}")
        else:
            print(f"  • Category '{name}' exists, skipping")
        cats[slug] = cat

    db.session.flush()

    # ── Sample tutorials ─────────────────────────────────────────
    tutorials = [
        {
            "title": "Welcome to the WMAA Platform",
            "description": "A quick overview of what the WMAA tutorial platform offers and how to navigate it.",
            "content": (
                "<h2>Getting Started</h2>"
                "<p>Welcome to the WMAA Tutorial Resources platform! This site is your "
                "one-stop destination for learning how to use the WMAA website effectively.</p>"
                "<h3>What you'll find here</h3>"
                "<ul>"
                "<li><strong>Text guides</strong> — step-by-step written walkthroughs</li>"
                "<li><strong>Video tutorials</strong> — screen recordings with narration</li>"
                "<li><strong>Documents</strong> — downloadable PDFs and reference sheets</li>"
                "</ul>"
                "<p>Use the navigation bar at the top to browse tutorials, or search by category.</p>"
            ),
            "media_type": "text",
            "category": "getting_started",
            "is_published": True,
            "display_order": 1,
        },
        {
            "title": "How to Create Your WMAA Account",
            "description": "Step-by-step guide to registering a new account on the WMAA website.",
            "content": (
                "<h2>Registration Process</h2>"
                "<ol>"
                "<li>Visit the WMAA homepage and click <strong>Sign Up</strong> in the top right.</li>"
                "<li>Enter your full name, email address, and choose a password.</li>"
                "<li>Verify your email by clicking the link sent to your inbox.</li>"
                "<li>Log in and complete your profile with a photo and bio.</li>"
                "</ol>"
                "<p>If you run into issues, check the Troubleshooting section or contact support.</p>"
            ),
            "media_type": "text",
            "category": "account",
            "is_published": True,
            "display_order": 2,
        },
        {
            "title": "Navigating the Dashboard",
            "description": "Learn how to use the main dashboard to find tutorials, track progress, and manage your profile.",
            "content": (
                "<h2>Dashboard Overview</h2>"
                "<p>After logging in you will see the main dashboard with three sections:</p>"
                "<ul>"
                "<li><strong>Recent Tutorials</strong> — the newest content added to the platform</li>"
                "<li><strong>Your Progress</strong> — tutorials you've started or completed</li>"
                "<li><strong>Quick Links</strong> — shortcuts to popular categories</li>"
                "</ul>"
                "<p>Click on any tutorial card to open the full content page.</p>"
            ),
            "media_type": "text",
            "category": "navigation",
            "is_published": True,
            "display_order": 3,
        },
        {
            "title": "Uploading and Managing Media",
            "description": "A video walkthrough showing how admins can upload videos, PDFs, and images.",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "content": (
                "<p>This video demonstrates the full media upload workflow for administrators, "
                "including thumbnail selection, PDF attachment, and YouTube embedding.</p>"
            ),
            "media_type": "video",
            "category": "media",
            "is_published": True,
            "display_order": 4,
        },
        {
            "title": "Using the Rich Text Editor",
            "description": "Learn how to format tutorial content with headings, lists, links, and more.",
            "content": (
                "<h2>Formatting Your Content</h2>"
                "<p>The built-in editor supports:</p>"
                "<ul>"
                "<li><strong>Bold</strong>, <em>italic</em>, and <u>underline</u> text</li>"
                "<li>Headings (H1, H2, H3)</li>"
                "<li>Ordered and unordered lists</li>"
                "<li>Hyperlinks to external resources</li>"
                "</ul>"
                "<h3>Tips</h3>"
                "<p>Keep paragraphs short for readability. Use headings to break up long content "
                "into scannable sections.</p>"
            ),
            "media_type": "text",
            "category": "features",
            "is_published": True,
            "display_order": 5,
        },
        {
            "title": "Troubleshooting Login Issues",
            "description": "Common login problems and how to resolve them quickly.",
            "content": (
                "<h2>Can't Log In?</h2>"
                "<p>Try these steps in order:</p>"
                "<ol>"
                "<li><strong>Check your email</strong> — make sure you're using the address you registered with.</li>"
                "<li><strong>Reset your password</strong> — click 'Forgot Password' on the login page.</li>"
                "<li><strong>Clear browser cache</strong> — sometimes stale cookies cause issues.</li>"
                "<li><strong>Try a different browser</strong> — rules out browser-specific problems.</li>"
                "</ol>"
                "<p>If none of these work, contact <a href='mailto:support@wmaa.org'>support@wmaa.org</a>.</p>"
            ),
            "media_type": "text",
            "category": "troubleshooting",
            "is_published": True,
            "display_order": 6,
        },
        {
            "title": "WMAA Membership Guide (PDF)",
            "description": "An external document with full details on WMAA membership tiers and benefits.",
            "document_url": "https://docs.google.com/document/d/example-membership-guide",
            "content": (
                "<p>This document covers membership tiers, pricing, renewal deadlines, and "
                "member-exclusive benefits. Click the link above to view the full document.</p>"
            ),
            "media_type": "document",
            "category": "account",
            "is_published": True,
            "display_order": 7,
        },
        {
            "title": "Advanced Search & Filters",
            "description": "Discover how to use category filters and search to find tutorials faster.",
            "content": (
                "<h2>Finding What You Need</h2>"
                "<p>The platform offers several ways to locate content:</p>"
                "<ul>"
                "<li><strong>Category browsing</strong> — click a category badge to see all related tutorials.</li>"
                "<li><strong>Search bar</strong> — type keywords to filter tutorials by title or description.</li>"
                "<li><strong>Sort options</strong> — order by newest, oldest, or display order.</li>"
                "</ul>"
                "<p>Combine filters for the most precise results.</p>"
            ),
            "media_type": "text",
            "category": "features",
            "is_published": False,
            "display_order": 8,
        },
    ]

    existing_count = Material.query.count()
    if existing_count > 0:
        print(f"  • {existing_count} tutorial(s) already exist, skipping sample data")
    else:
        for t in tutorials:
            cat_slug = t.pop("category")
            mat = Material(**t, category=cats[cat_slug])
            db.session.add(mat)
            print(f"  + Tutorial: {mat.title}")

    db.session.commit()
    print("\nDone! Seeded successfully.")


if __name__ == "__main__":
    with app.app_context():
        if "--reset" in sys.argv:
            print("Resetting database...")
            db.drop_all()
            db.create_all()
            print("Tables recreated.\n")

        print("Seeding database...")
        seed()
