"""
Database seed script for Tutorial Resource Management.

Populates:
    - Admin user (username/password: admin / admin)
    - Categories (WordPress, Astra, Elementor, etc.)
    - Sample tutorials with HTML content and YouTube URLs

Usage:
    python seed.py          # create missing rows; update tutorials matched by title
    python seed.py --reset  # DROP all tables, recreate schema, then seed

Requires:
    Flask app context (uses wsgi:app). Run after ``flask db upgrade``.
"""

import sys

from wsgi import app
from web.extensions import db
from web.models import Category, Material, User


def seed() -> None:
    """
    Insert or update seed data inside an active Flask application context.

    Idempotent for admin user and categories. Tutorials are upserted by title
    so you can edit seed.py and re-run without --reset.
    """
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
        ("WordPress Basics", "getting_started"),
        ("Astra Theme", "astra_theme"),
        ("Elementor", "elementor"),
        ("Media & Embeds", "media"),
        ("Site Administration", "account"),
        ("Troubleshooting", "troubleshooting"),
    ]
    cats = {}
    for name, slug in category_defs:
        cat = Category.query.filter_by(slug=slug).first()
        if not cat:
            cat = Category(name=name, slug=slug)
            db.session.add(cat)
            print(f"  + Category: {name}")
        elif cat.name != name:
            cat.name = name
            print(f"  ~ Updated category: {name}")
        else:
            print(f"  • Category '{name}' exists, skipping")
        cats[slug] = cat

    db.session.flush()

    # ── WordPress / Astra / Elementor tutorials ──────────────────
    # Each dict maps to Material columns; "category" is resolved to Category FK.
    # video_url: full YouTube watch links; document_url: external help pages.
    tutorials = [
        {
            "title": "Getting Started with WordPress for Your WMAA Site",
            "description": (
                "Overview of the WordPress dashboard, plugins, and how the WMAA "
                "site is built with Astra and Elementor."
            ),
            "content": (
                "<h2>What You Need Before You Begin</h2>"
                "<p>Your WMAA website runs on <strong>WordPress</strong> — the world's "
                "most popular content management system. You will manage pages, menus, "
                "and media from the WordPress admin area at <code>/wp-admin</code>.</p>"
                "<h3>Core pieces of your stack</h3>"
                "<ul>"
                "<li><strong>WordPress</strong> — hosts your pages, posts, users, and settings</li>"
                "<li><strong>Astra theme</strong> — lightweight, fast base design and layout</li>"
                "<li><strong>Elementor</strong> — drag-and-drop page builder for visual editing</li>"
                "<li><strong>Plugins</strong> — add features such as forms, SEO, and security</li>"
                "</ul>"
                "<h3>First login steps</h3>"
                "<ol>"
                "<li>Go to your site URL and append <code>/wp-admin</code></li>"
                "<li>Sign in with the administrator credentials provided by your team</li>"
                "<li>Open <strong>Dashboard → Updates</strong> and apply any pending updates</li>"
                "<li>Visit <strong>Appearance → Themes</strong> and confirm <strong>Astra</strong> is active</li>"
                "<li>Confirm <strong>Elementor</strong> appears under <strong>Plugins</strong></li>"
                "</ol>"
                "<p>Work through the Astra and Elementor tutorials in order for the smoothest learning path.</p>"
            ),
            "media_type": "text",
            "category": "getting_started",
            "is_published": True,
            "display_order": 1,
        },
        {
            "title": "Install & Activate the Astra Theme",
            "description": (
                "Step-by-step video: install Astra from the WordPress theme directory, "
                "activate it, and create a child theme to protect customizations."
            ),
            "video_url": "https://www.youtube.com/watch?v=X63_S2bsEmg",
            "content": (
                "<h2>Why Astra?</h2>"
                "<p><strong>Astra</strong> is one of the most popular free WordPress themes. "
                "It is lightweight, loads quickly, and pairs perfectly with Elementor. "
                "It uses modern JavaScript instead of jQuery for better performance.</p>"
                "<h3>After watching the video</h3>"
                "<ol>"
                "<li>In WordPress go to <strong>Appearance → Themes → Add New</strong></li>"
                "<li>Search for <strong>Astra</strong>, install, and click <strong>Activate</strong></li>"
                "<li>Optional: install <strong>Astra Child</strong> if you plan custom CSS or PHP</li>"
                "<li>Open <strong>Appearance → Customize</strong> to set site identity (logo, colors)</li>"
                "</ol>"
                "<p><em>Video credit:</em> Avra Tuts — install Astra and child theme walkthrough.</p>"
            ),
            "media_type": "video",
            "category": "astra_theme",
            "is_published": True,
            "display_order": 2,
        },
        {
            "title": "Set Up Astra Starter Templates",
            "description": (
                "Import a professional pre-built layout in minutes using the Astra "
                "Starter Templates plugin."
            ),
            "video_url": "https://www.youtube.com/watch?v=zGkl7K-TC40",
            "content": (
                "<h2>Starter Templates</h2>"
                "<p>Astra Starter Templates let you import full demo sites (homepage, "
                "about, contact) and then replace text and images with your WMAA content.</p>"
                "<h3>Setup checklist</h3>"
                "<ol>"
                "<li>Install and activate <strong>Astra Starter Templates</strong> from Plugins</li>"
                "<li>In the Astra dashboard, enable the <strong>Starter Templates</strong> module</li>"
                "<li>Pick a layout that suits a martial arts / community site (clean, bold hero)</li>"
                "<li>Import the template and wait for plugins Elementor may require</li>"
                "<li>Replace demo logo, menu links, and contact details with WMAA information</li>"
                "</ol>"
                "<p><em>Video credit:</em> Avra Tuts — quick starter templates guide.</p>"
            ),
            "media_type": "video",
            "category": "astra_theme",
            "is_published": True,
            "display_order": 3,
        },
        {
            "title": "Build Your Site with Astra & Elementor (Full Walkthrough)",
            "description": (
                "Complete beginner tutorial: hosting, WordPress setup, Astra theme, "
                "Elementor pages, menus, and launch checklist."
            ),
            "video_url": "https://www.youtube.com/watch?v=J4tFCVCE9qQ",
            "content": (
                "<h2>End-to-End Website Build</h2>"
                "<p>This comprehensive tutorial walks through building a WordPress site "
                "with <strong>Astra</strong> and <strong>Elementor</strong> — the same "
                "combination used for many modern club and academy sites.</p>"
                "<h3>Key chapters to focus on for WMAA</h3>"
                "<ul>"
                "<li>Installing WordPress and claiming your domain</li>"
                "<li>Installing and activating the Astra theme</li>"
                "<li>Installing Elementor and choosing a starter template</li>"
                "<li>Customizing pages with Elementor (hero, classes, timetable, contact)</li>"
                "<li>Creating navigation menus and footer links</li>"
                "<li>Previewing on mobile before publishing</li>"
                "</ul>"
                "<p><em>Video credit:</em> Stewart Gauld — Astra + Elementor website for beginners.</p>"
            ),
            "media_type": "video",
            "category": "astra_theme",
            "is_published": True,
            "display_order": 4,
        },
        {
            "title": "Elementor Page Builder — Basics in 15 Minutes",
            "description": (
                "Fast introduction to the Elementor editor: sections, columns, widgets, "
                "and publishing your first page."
            ),
            "video_url": "https://www.youtube.com/watch?v=3YG3XLmBX4A",
            "content": (
                "<h2>Elementor Structure</h2>"
                "<p>Elementor organizes content in a simple hierarchy:</p>"
                "<ul>"
                "<li><strong>Section</strong> — full-width horizontal band (e.g. hero banner)</li>"
                "<li><strong>Column</strong> — vertical area inside a section</li>"
                "<li><strong>Widget</strong> — individual element (heading, image, button, video)</li>"
                "</ul>"
                "<h3>Quick workflow</h3>"
                "<ol>"
                "<li>Edit any page and click <strong>Edit with Elementor</strong></li>"
                "<li>Drag widgets from the left panel onto the canvas</li>"
                "<li>Click an element to change content and style in the left sidebar</li>"
                "<li>Use the responsive mode icons to check tablet and mobile layouts</li>"
                "<li>Click <strong>Update</strong> or <strong>Publish</strong> when finished</li>"
                "</ol>"
            ),
            "media_type": "video",
            "category": "elementor",
            "is_published": True,
            "display_order": 5,
        },
        {
            "title": "Elementor Complete Tutorial — Page Builder Deep Dive",
            "description": (
                "In-depth Elementor course covering templates, theme builder, forms, "
                "responsive design, and advanced widgets."
            ),
            "video_url": "https://www.youtube.com/watch?v=KrEgYrXD9SI",
            "content": (
                "<h2>When to Use This Tutorial</h2>"
                "<p>Use this longer course after the 15-minute basics video. It covers "
                "pro-level workflows useful for maintaining the WMAA site long term.</p>"
                "<h3>Topics covered</h3>"
                "<ul>"
                "<li>Global colors and typography</li>"
                "<li>Header and footer templates (Theme Builder)</li>"
                "<li>Reusable sections and saved templates</li>"
                "<li>Contact forms and call-to-action buttons</li>"
                "<li>Performance tips and common mistakes to avoid</li>"
                "</ul>"
                "<p>Bookmark sections you use often — e.g. editing the homepage hero or class timetable block.</p>"
            ),
            "media_type": "video",
            "category": "elementor",
            "is_published": True,
            "display_order": 6,
        },
        {
            "title": "Customizing Astra Theme Settings",
            "description": (
                "Text guide: typography, colors, layout width, header options, and "
                "Customizer settings that work alongside Elementor."
            ),
            "content": (
                "<h2>Astra Customizer Essentials</h2>"
                "<p>Go to <strong>Appearance → Customize</strong> while Astra is active. "
                "Many global settings apply site-wide; Elementor controls individual page layout.</p>"
                "<h3>Recommended settings for WMAA</h3>"
                "<ul>"
                "<li><strong>Site Identity</strong> — upload the WMAA logo and set tagline</li>"
                "<li><strong>Global → Colors</strong> — match brand primary/secondary colors</li>"
                "<li><strong>Global → Typography</strong> — choose readable fonts for body and headings</li>"
                "<li><strong>Header Builder</strong> — logo left, menu right; enable sticky header if desired</li>"
                "<li><strong>Footer</strong> — copyright, social icons, contact link</li>"
                "<li><strong>Layout → Container</strong> — set content width (often 1200px) for consistency with Elementor</li>"
                "</ul>"
                "<h3>Astra + Elementor together</h3>"
                "<p>Use Astra for site-wide header/footer and defaults; use Elementor for page body content. "
                "If a change does not appear, clear any caching plugin and refresh Elementor "
                "<strong>Tools → Regenerate CSS</strong>.</p>"
            ),
            "media_type": "text",
            "category": "astra_theme",
            "is_published": True,
            "display_order": 7,
        },
        {
            "title": "Elementor: Widgets, Sections & Responsive Design",
            "description": (
                "How to build WMAA pages with headings, images, icon boxes, spacers, "
                "and mobile-friendly layouts in Elementor."
            ),
            "content": (
                "<h2>Widgets You'll Use Most</h2>"
                "<ul>"
                "<li><strong>Heading</strong> — page titles and section labels</li>"
                "<li><strong>Text Editor</strong> — paragraphs and bullet lists</li>"
                "<li><strong>Image</strong> — photos of classes, instructors, events</li>"
                "<li><strong>Icon Box</strong> — feature highlights (timetable, grading, membership)</li>"
                "<li><strong>Button</strong> — links to join, contact, or book a trial</li>"
                "<li><strong>Spacer / Divider</strong> — control vertical rhythm between sections</li>"
                "</ul>"
                "<h3>Responsive editing</h3>"
                "<ol>"
                "<li>At the bottom of the Elementor panel, switch to <strong>Tablet</strong> or <strong>Mobile</strong></li>"
                "<li>Hide or reorder columns that crowd small screens</li>"
                "<li>Reduce heading font sizes on mobile (Typography → Size)</li>"
                "<li>Test tap targets — buttons should be easy to press on phones</li>"
                "</ol>"
                "<h3>Saving time</h3>"
                "<p>Right-click a section → <strong>Save as Template</strong> to reuse banners or "
                "CTA blocks across multiple pages.</p>"
            ),
            "media_type": "text",
            "category": "elementor",
            "is_published": True,
            "display_order": 8,
        },
        {
            "title": "Embedding YouTube Videos with Elementor",
            "description": (
                "Add training demos, grading clips, or promotional videos to WordPress "
                "pages using Elementor's Video widget."
            ),
            "content": (
                "<h2>Add a YouTube Video to Any Page</h2>"
                "<ol>"
                "<li>On YouTube, open your video and click <strong>Share → Copy link</strong></li>"
                "<li>In WordPress, edit the page with <strong>Edit with Elementor</strong></li>"
                "<li>Drag the <strong>Video</strong> widget into your section</li>"
                "<li>Paste the URL into the <strong>Link</strong> field (Source: YouTube)</li>"
                "<li>Adjust aspect ratio, play icon overlay, and lazy load for performance</li>"
                "<li>Update the page and test playback on desktop and mobile</li>"
                "</ol>"
                "<h3>Useful options</h3>"
                "<ul>"
                "<li><strong>Lazy Load</strong> — delays loading until the user scrolls (faster pages)</li>"
                "<li><strong>Image Overlay</strong> — custom thumbnail before play</li>"
                "<li><strong>Privacy mode</strong> — use youtube-nocookie.com if required by policy</li>"
                "</ul>"
                "<p>For official Elementor documentation on the Video widget, see the Elementor Help Center link in the related tutorial.</p>"
            ),
            "media_type": "text",
            "category": "media",
            "is_published": True,
            "display_order": 9,
        },
        {
            "title": "Managing WordPress Users & Roles",
            "description": (
                "Add editors for content updates, understand Administrator vs Editor "
                "roles, and keep the admin account secure."
            ),
            "content": (
                "<h2>User Roles</h2>"
                "<ul>"
                "<li><strong>Administrator</strong> — full access including plugins and themes</li>"
                "<li><strong>Editor</strong> — publish and edit all posts/pages (good for content volunteers)</li>"
                "<li><strong>Author</strong> — edit own posts only</li>"
                "<li><strong>Subscriber</strong> — read-only; no admin bar editing</li>"
                "</ul>"
                "<h3>Adding a new editor</h3>"
                "<ol>"
                "<li>Go to <strong>Users → Add New</strong></li>"
                "<li>Enter username, email, and a strong password</li>"
                "<li>Set role to <strong>Editor</strong> unless they need plugin access</li>"
                "<li>Send login details through a secure channel — not public email if possible</li>"
                "</ol>"
                "<p>Limit the number of Administrator accounts. Enable two-factor authentication if your host supports it.</p>"
            ),
            "media_type": "text",
            "category": "account",
            "is_published": True,
            "display_order": 10,
        },
        {
            "title": "Troubleshooting WordPress, Astra & Elementor",
            "description": (
                "Fix common issues: white screen, Elementor not loading, style not "
                "updating, and plugin conflicts."
            ),
            "content": (
                "<h2>Elementor Won't Load</h2>"
                "<ol>"
                "<li>Increase PHP memory limit (ask host or set in wp-config.php)</li>"
                "<li>Deactivate other plugins temporarily to find conflicts</li>"
                "<li>Switch to a default theme briefly — if Elementor works, check Astra updates</li>"
                "<li>Elementor → <strong>Tools → Regenerate CSS & Data</strong></li>"
                "</ol>"
                "<h2>Changes Not Visible on the Front End</h2>"
                "<ul>"
                "<li>Clear browser cache and any caching plugin (WP Rocket, LiteSpeed, etc.)</li>"
                "<li>Confirm you clicked <strong>Update</strong> in Elementor, not just preview</li>"
                "<li>Check you edited the correct page (Pages list shows last modified date)</li>"
                "</ul>"
                "<h2>Astra Layout Looks Broken</h2>"
                "<p>Ensure Elementor and Astra are both updated. Re-import starter template only on "
                "a staging copy — it can overwrite page content.</p>"
                "<p>When stuck, export a backup via your host or a backup plugin before major changes.</p>"
            ),
            "media_type": "text",
            "category": "troubleshooting",
            "is_published": True,
            "display_order": 11,
        },
        {
            "title": "Elementor Official Help Center",
            "description": (
                "External reference documentation for Elementor widgets, Theme Builder, "
                "and troubleshooting from the Elementor team."
            ),
            "document_url": "https://elementor.com/help/",
            "content": (
                "<h2>Official Documentation</h2>"
                "<p>The Elementor Help Center is the authoritative source for widget guides, "
                "Theme Builder setup, forms, popups (Pro), and compatibility notes.</p>"
                "<h3>Suggested articles for WMAA admins</h3>"
                "<ul>"
                "<li>Getting started with the editor</li>"
                "<li>How to use the Video widget</li>"
                "<li>Creating and applying page templates</li>"
                "<li>Responsive editing modes</li>"
                "</ul>"
                "<p>Open the link above in a new tab and use the search bar for specific features.</p>"
            ),
            "media_type": "document",
            "category": "elementor",
            "is_published": True,
            "display_order": 12,
        },
    ]

    for t in tutorials:
        cat_slug = t.pop("category")
        title = t["title"]
        mat = Material.query.filter_by(title=title).first()
        if mat:
            for key, value in t.items():
                setattr(mat, key, value)
            mat.category = cats[cat_slug]
            print(f"  ~ Updated tutorial: {title}")
        else:
            mat = Material(**t, category=cats[cat_slug])
            db.session.add(mat)
            print(f"  + Tutorial: {title}")

    db.session.commit()
    print("\nDone! Seeded successfully.")


if __name__ == "__main__":
    with app.app_context():
        if "--reset" in sys.argv:
            # WARNING: destroys all tutorials, users, and uploads metadata
            print("Resetting database...")
            db.drop_all()
            db.create_all()
            print("Tables recreated.\n")

        print("Seeding database...")
        seed()
