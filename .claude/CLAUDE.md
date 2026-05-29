# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the dev server (port 5001)
python app.py

# Or via Flask CLI
flask run --port 5001 --debug

# Run all tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Run a specific test
pytest tests/test_auth.py::test_login_success
```

Dependencies are pinned in `requirements.txt`. Install into the local venv:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Architecture

**Spendly** is a Flask expense-tracker web app (INR/₹). It follows a simple monolithic structure — no blueprints, no ORM, plain SQLite via a thin `database/` helper.

### Key files

- `app.py` — all Flask routes. Currently has live routes for landing, auth pages, terms/privacy, plus stub routes (returning strings) for logout, profile, and expense CRUD.
- `database/db.py` — intended to expose three functions: `get_db()`, `init_db()`, `seed_db()`. The file is a stub; students implement it in Step 1.
- `templates/base.html` — master layout with navbar and footer. All pages extend this. Google Fonts (DM Serif Display + DM Sans) are loaded here.
- `static/css/style.css` — global styles (navbar, footer, auth forms, utilities).
- `static/css/landing.css` — landing-page-only styles (hero, features, CTA, modal).
- `static/js/main.js` — placeholder; page-specific JS lives in `{% block scripts %}` inside each template.

### Template conventions

- All templates use `{% extends "base.html" %}`.
- Page-specific CSS is injected via `{% block head %}`.
- Page-specific JS is injected via `{% block scripts %}` (after `main.js`).
- Flask's `url_for()` is used for all internal links — no hardcoded paths except legacy `action="/login"` and `action="/register"` form attributes.

### Planned implementation steps (stub routes exist for all of these)

The project is scaffolded step-by-step for students:
1. Database setup (`database/db.py`)
2. User registration (POST `/register`)
3. Login/logout with sessions
4. Profile page
5–9. Expense CRUD (add, edit, delete, list, filter)

When implementing new steps, add POST handlers to the existing route functions in `app.py` rather than creating separate files — the project intentionally stays in a single module.

### Database

SQLite, accessed via raw `sqlite3`. The connection helper (`get_db()`) should set `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`. No migrations framework — use `CREATE TABLE IF NOT EXISTS` in `init_db()`.

### Testing

Uses `pytest` + `pytest-flask`. Test files belong in a `tests/` directory (not yet created). Use a test app fixture with an in-memory SQLite database (`":memory:"`).
