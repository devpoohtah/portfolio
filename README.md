# Portfolio — Flask + Tailwind

A single-page developer portfolio built with Flask, Tailwind CSS (CDN), AOS
scroll animations, and Lucide icons. Matches the dark hero / light content /
dark footer layout with a blue accent, glassmorphism cards, a mouse glow
effect over the dark sections, an animated typing role, and a working
contact form endpoint.

## Run locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit http://127.0.0.1:5000

## Edit your content

Everything text-based (name, bio, projects, skills, contact info, social
links) lives in the `SITE` dict at the top of `app.py` — no HTML editing
required for basic content changes.

- **Projects**: edit the `SITE["projects"]` list. `color` is a Tailwind
  gradient class used for the card's cover art.
- **Skills**: edit `SITE["skills"]` (progress bars) and
  `SITE["tech_icons"]` (icon grid — names come from https://simpleicons.org,
  e.g. `python`, `flask`, `react`).
- **Resume**: replace `static/cv/resume.pdf` with your real CV, keeping the
  same filename (or update the `url_for('static', filename='cv/...')`
  references in `templates/index.html`).
- **Profile photo**: the hero currently uses a placeholder panel. Drop a
  photo into `static/images/` and swap the placeholder `<div>` in the hero
  section of `templates/index.html` for an `<img>` tag.

## Contact form

`POST /api/contact` validates the payload and currently just prints it to
the console (see the `# TODO` in `app.py`). Wire it up to real email
delivery with something like:

```bash
pip install Flask-Mail
```

or call an email API (SendGrid, Resend, Postmark) from that same route.

## Deploy to Render

1. Push this project to a GitHub repo.
2. On Render: **New → Web Service** → connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app` (already set via `Procfile`).
5. Deploy.

## Project structure

```
portfolio/
├── app.py                 # Flask app, routes, site content
├── requirements.txt
├── Procfile                # Render/gunicorn start command
├── templates/
│   └── index.html          # Single-page layout (Jinja2)
└── static/
    ├── css/style.css       # Custom styles beyond Tailwind utilities
    ├── js/script.js        # Nav state, typing effect, mouse glow,
    │                       # scroll progress, skill bars, contact form
    ├── cv/resume.pdf       # Placeholder — replace with your real CV
    └── images/             # Add your photo / project screenshots here
```

## Notes

- Tailwind is loaded via the CDN Play script for zero build-step setup.
  For a production build with tree-shaking, swap this for the Tailwind CLI
  or PostCSS pipeline later — the class names will carry over unchanged.
- Tech icons are pulled live from `cdn.simpleicons.org`; swap in local SVGs
  under `static/images/` if you want to work offline or need brand colors.
- Respects `prefers-reduced-motion` for AOS/animations.
