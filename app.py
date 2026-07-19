from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
load_dotenv()
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get("SMTP_USER")       # your Gmail address
SMTP_PASS = os.environ.get("SMTP_PASS")       # the app password from step 1
app = Flask(__name__)

limiter = Limiter(get_remote_address, app=app, default_limits=[])
# ---------------------------------------------------------------------------
# Site content lives here so you can edit your info without touching HTML.
# ---------------------------------------------------------------------------
SITE = {
    "name": "Justin Brian Solamillo",
    "role": "Full Stack Developer",
    "tagline": "BSIT Student | Web Developer",
    "intro": (
        "I build clean, scalable, and user-friendly web applications "
        "using Python, Flask, JavaScript, and modern web technologies."
    ),
    "email": "jbs.soll29@gmail.com.com",
    "phone": "+63 951 597 0363",
    "location": "Philippines",
    "socials": {
        "github": "https://github.com/",
        "linkedin": "https://linkedin.com/",
        "email": "mailto:jbs.soll29@gmail.com",
    },
    "about": {
        "eyebrow": "About Me",
        "heading": "Get to know me",
        "paragraphs": [
            "I'm a BSIT student with a passion for building web applications and solving real-world problems through code.",
            "I enjoy working with Python Flask for the backend and modern web technologies on the frontend.",
            "I'm always eager to learn new technologies and take on challenging projects.",
        ],
        "traits": [
            {"icon": "puzzle", "title": "Problem Solver", "desc": "I love solving problems and turning ideas into functional solutions."},
            {"icon": "file-check-2", "title": "Details Oriented", "desc": "I focus on writing clean, efficient, and maintainable code."},
            {"icon": "zap", "title": "Fast Learner", "desc": "I adapt quickly to new technologies and tools."},
            {"icon": "users", "title": "Team Player", "desc": "I enjoy collaborating and building great things with others."},
        ],
    },
    "projects": [
        {
            "title": "Mrs. Brave Cake Shop",
            "desc": "A full-stack cake shop platform where customers order premade cakes or fully customize their own, book pickup/delivery slots, and track orders in real time. Includes live in-app chat between customer and shop (Firebase onSnapshot) and real-time delivery tracking, plus an admin dashboard for sales, bookings, and inventory analytics. Built as lead developer for our capstone project.",
            "tags": ["Flask", "JavaScript","Firebase", "Firestore","Firebase Authentication", "PWA"],
            "category": "Web App",
            "featured": True,
            "color": "from-amber-500/30 to-rose-500/20",
            "repo_url": "https://github.com/StressWare/Capstone-CakeShop",
            "live_url": "https://mrs-braves-cakes.onrender.com/",
            "image": "",
        },
        {
            "title": "Library Management System",
            "desc": "A Flask-based system for managing a library's day-to-day operations — cataloging books, tracking borrow and return transactions, monitoring availability, and giving staff an admin view to manage the collection. Built as a 2nd-year academic project.",
            "tags": ["Flask", "Python", "MySQL"],
            "category": "Web App",
            "featured": True,
            "color": "from-teal-500/30 to-emerald-400/20",
            "repo_url": "",
            "live_url": "",
            "image": "",
        },
        {
            "title": "MyCar Rental Services",
            "desc": "A car rental frontend for Western Visayas — browse the fleet, view vehicle details, book a car or tour, and check available drivers, with a dedicated admin view. Currently a static HTML/CSS/JS build; backend and booking logic are the next step.",
            "tags": ["HTML", "CSS", "JavaScript"],
            "category": "Web App",
            "featured": False,
            "color": "from-orange-500/30 to-red-400/20",
            "repo_url": "https://github.com/devpoohtah/car-rental-",
            "live_url": "https://devpoohtah.github.io/car-rental-/",
            "image": "",
        },
        {
            "title": "Android Java Apps",
            "desc": "Collection of Android apps including BMI Calculator, Converter, and more.",
            "tags": ["Java"],
            "featured": False,
            "category": "Mobile App",
            "color": "from-emerald-500/30 to-teal-400/20",
        },
        {
            "title": "Secure CRUD System",
            "desc": "A Flask app built for an Information Assurance and Security course, focused on secure data handling: user accounts with role-based access and block/unblock controls, full product CRUD, hashed passwords, and encrypted data at rest to protect sensitive records.",
            "tags": ["Flask", "Python", "Security","MySQL"],
            "category": "Web App",
            "featured": False,
            "color": "from-slate-500/30 to-blue-500/20",
            "repo_url": "https://github.com/jualsolamilloui-hash/IAS-2",
            "live_url": "",
            "image": "",
        },
        {
            "title": "Gem Rush Game",
            "desc": "An obstacle-dodging arcade runner: weave past hazards, grab gems along the way, and sprint to the finish line before your luck runs out.",
            "tags": ["Godot", "GDScript"],
            "category": "Game",
            "featured": False,
            "color": "from-violet-500/30 to-fuchsia-400/20",
            "repo_url": "https://github.com/kriselda-web/krizzy-foru",
            "live_url": "",
            "image": "",
        },
        {
            "title": "Barangay Portal System",
            "desc": "A web-based platform where residents file complaints, view official announcements, and request documents like clearances and certificates online — cutting down on walk-in queues and manual paperwork.",
            "tags": ["Flask", "MySQL", "Bootstrap"],
            "category": "Web App",
            "featured": True,
            "color": "from-blue-500/30 to-indigo-400/20",
            "repo_url": "https://github.com/jualsolamilloui-hash/Platform-tech",
            "live_url": "",
            "image": "",
        },
        {
            "title": "Expenses Logger",
            "desc": "A simple offline expense tracker (PWA) for daily budgeting — set a budget for an event or outing, log expenses by category and item, and watch total spent and remaining balance update in real time. Includes expense history with PDF export and a clear-all option.",
            "tags": ["JavaScript", "HTML", "CSS", "PWA"],
            "category": "Web App",
            "featured": False,
            "color": "from-lime-500/30 to-green-400/20",
            "repo_url": "https://github.com/devpoohtah/expenses-tracker",
            "live_url": "https://devpoohtah.github.io/expenses-tracker/",
            "image": "",
        },
        {
            "title": "BMI Calculator",
            "desc": "Built the same BMI calculator to explore different platforms — a Python console program, a Java desktop app with a GUI, and a native Kotlin Android app in Android Studio. Each version takes height and weight and returns the calculated BMI with its health category.",
            "tags": ["Python", "Java", "Kotlin"],
            "category": "Mobile App",
            "featured": False,
            "color": "from-purple-500/30 to-pink-400/20",
            "repo_url": "",
            "live_url": "",
            "image": "",
        },
        {
            "title": "E-Commerce Website",
            "desc": "A basic e-commerce website built with HTML and CSS — product listings and a storefront layout. A 1st-year project focused on frontend fundamentals.",
            "tags": ["HTML", "CSS"],
            "category": "Web App",
            "featured": False,
            "color": "from-yellow-500/30 to-amber-400/20",
            "repo_url": "",
            "live_url": "",
            "image": "",
        },
        {
            "title": "E-Commerce Website (Grandeur)",
            "desc": "A full e-commerce platform built with PHP, MySQL, and Bootstrap — product catalog, styled storefront, and a database-backed backend. A 2nd-year project focused on full-stack web development.",
            "tags": ["PHP", "MySQL", "Bootstrap"],
            "category": "Web App",
            "featured": False,
            "color": "from-rose-500/30 to-red-400/20",
            "repo_url": "",
            "live_url": "",
            "image": "",
        },
    ],
    "skills": [
        {"name": "Python", "level": 90},
        {"name": "Flask", "level": 85},
        {"name": "HTML", "level": 90},
        {"name": "CSS", "level": 75},
        {"name": "JavaScript", "level": 70},
        {"name": "Firebase", "level": 60},
        {"name": "Git & GitHub", "level": 80},
    ],
    "tech_icons": [
        "python", "flask", "javascript", "html5",
        "css", "bootstrap", "firebase", "git",
        "github", "chartdotjs", "mysql", "android",
    ],
    "timeline": [
        {"year": "2022", "title": "Started BSIT", "desc": "Began my Bachelor of Science in Information Technology."},
        {"year": "2024", "title": "Learned Flask", "desc": "Started building backend applications with Python Flask."},
        {"year": "2026", "title": "Graduated BSIT", "desc": "Completed my degree and started building a portfolio of real projects."},
    ],
}


@app.route("/")
def home():
    return render_template("index.html", site=SITE, year=datetime.now().year)


@app.route("/api/contact", methods=["POST"])
@limiter.limit("3 per day", error_message="You've reached the daily message limit. Please try again tomorrow, or email me directly.")
def contact():
    data = request.get_json(silent=True) or request.form

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    subject = (data.get("subject") or "").strip()
    message = (data.get("message") or "").strip()

    errors = {}
    if not name:
        errors["name"] = "Please enter your name."
    if not email or "@" not in email:
        errors["email"] = "Please enter a valid email address."
    if not message:
        errors["message"] = "Please enter a message."

    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    if SMTP_USER and SMTP_PASS:
        try:
            msg = MIMEText(f"From: {name} <{email}>\n\n{message}")
            msg["Subject"] = f"[Portfolio] {subject or 'New message from ' + name}"
            msg["From"] = SMTP_USER
            msg["To"] = SITE["email"]
            msg["Reply-To"] = email

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        except Exception as e:
            print(f"[contact] SMTP send failed: {e}")
    else:
        print(f"[contact] {datetime.now().isoformat()} — {name} <{email}> — {subject}\n{message}\n")

    return jsonify({"ok": True, "message": "Thanks! Your message has been sent."})


@app.route("/static/cv/<path:filename>")
def download_cv(filename):
    return send_from_directory(os.path.join(app.root_path, "static", "cv"), filename, as_attachment=True)

@app.route("/projects")
def projects():
    return render_template("projects.html", site=SITE, year=datetime.now().year)

if __name__ == "__main__":
    app.run(debug=True)
