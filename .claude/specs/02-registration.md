# Spec: Registration

## Overview
Implement the POST handler for `/register` so new users can create a Spendly account. The GET route and template already exist; this step wires up form processing: validate inputs, check for duplicate emails, hash the password, insert the user row, and redirect to the login page on success. Error messages are rendered back into the existing `register.html` form.

## Depends on
Step 1 — Database setup (`database/db.py` must be complete with `get_db()`, `init_db()`, `seed_db()`).

## Routes
- `POST /register` — process registration form — public

(The `GET /register` route already exists and returns `register.html`; add the POST handler inside the same `@app.route` decorator using `methods=["GET", "POST"]`.)

## Database changes
No database changes. The `users` table already exists with the required schema:
- `id`, `name`, `email` (UNIQUE), `password_hash`, `created_at`

## Templates
- **Modify:** `templates/register.html` — already supports `{{ error }}` display; no changes needed unless repopulating form fields on error (optional: re-render `name` and `email` values so the user doesn't retype them).

## Files to change
- `app.py`
  - Add `request`, `redirect`, `url_for`, `flash` (or `session`) to the Flask import line
  - Import `get_db`, `init_db`, `seed_db` from `database.db` and call `init_db()` + `seed_db()` inside an `app.app_context()` block at startup (per Step 1 spec — if not already done)
  - Change `@app.route("/register")` to `@app.route("/register", methods=["GET", "POST"])`
  - Add POST branch inside the `register()` view function

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` is already installed.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use string formatting in SQL
- Hash passwords with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validation order: check all fields non-empty → password length ≥ 8 → check duplicate email → insert
- On duplicate email, show a user-friendly error (e.g. "An account with that email already exists.") and re-render `register.html` with `name` and `email` pre-filled
- On success, redirect to `url_for('login')` — do not auto-login (login is Step 3)
- Keep all logic inside the existing `register()` function in `app.py` — no separate modules

## Definition of done
- [ ] Submitting the form with valid data creates a new row in `users` with a hashed password
- [ ] Submitting again with the same email shows an inline error without crashing
- [ ] Submitting with an empty field shows a validation error
- [ ] Submitting with a password shorter than 8 characters shows a validation error
- [ ] On success the browser redirects to `/login`
- [ ] The password stored in the database is a hash, never plaintext
- [ ] Existing GET `/register` still renders the empty form correctly
- [ ] App starts without errors (`init_db` and `seed_db` called on startup)
