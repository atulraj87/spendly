# Spec: Login and Logout

## Overview
Implement the POST handler for `/login` and the full `/logout` route so users can authenticate into Spendly and end their session. The GET `/login` route and `login.html` template already exist; this step wires up form processing: validate credentials, verify the password hash, store the user's id and name in `session`, and redirect to `/profile` on success. `/logout` clears the session and redirects to the landing page. The navbar in `base.html` must also be updated to show a logged-in state (user name + logout link) versus the current logged-out state (Sign in / Get started).

## Depends on
- Step 1 — Database setup (`get_db()` must be complete)
- Step 2 — Registration (users must be able to exist in the `users` table)

## Routes
- `POST /login` — process login form, set session on success — public
- `GET /logout` — clear session, redirect to landing — public (safe to call when not logged in)

(The `GET /login` route already exists; add `methods=["GET", "POST"]` to its decorator.)

## Database changes
No database changes. The `users` table already has `id`, `name`, `email`, `password_hash`.

## Templates
- **Modify:** `templates/login.html`
  - Add `value="{{ email or '' }}"` to the email `<input>` so it repopulates on error
- **Modify:** `templates/base.html`
  - In the navbar, conditionally show:
    - **Logged out:** existing "Sign in" and "Get started" links
    - **Logged in:** user's name (non-clickable or links to `/profile`) and a "Sign out" link to `url_for('logout')`

## Files to change
- `app.py`
  - Add `session` to the Flask import line
  - Add `check_password_hash` to the `werkzeug.security` import line
  - Set `app.secret_key` — use a hard-coded dev string for now (e.g. `"spendly-dev-secret"`)
  - Change `@app.route("/login")` to `@app.route("/login", methods=["GET", "POST"])` and add POST branch
  - Replace the `/logout` stub body with session-clearing logic
- `templates/login.html` — repopulate email on error (see Templates above)
- `templates/base.html` — conditional navbar (see Templates above)

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use string formatting in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validation order: check both fields non-empty → look up user by email → verify password hash → set session → redirect
- On invalid email or wrong password, show a single generic error: `"Invalid email or password."` (do not reveal which field is wrong)
- On success, store `session["user_id"]` and `session["user_name"]` then redirect to `url_for('profile')`
- `logout()` must call `session.clear()` then redirect to `url_for('landing')`
- Keep all logic inside the existing route functions in `app.py` — no separate modules

## Definition of done
- [ ] Submitting valid credentials sets a session and redirects to `/profile`
- [ ] Submitting a wrong password shows `"Invalid email or password."` inline without crashing
- [ ] Submitting an email that doesn't exist shows `"Invalid email or password."` inline
- [ ] Submitting with an empty field shows a validation error
- [ ] After login, the navbar shows the user's name and a "Sign out" link instead of "Sign in" / "Get started"
- [ ] Visiting `/logout` clears the session and redirects to the landing page
- [ ] After logout, the navbar reverts to the logged-out state
- [ ] The email field is repopulated when the login form is re-rendered with an error
- [ ] The demo user (`demo@spendly.com` / `demo123`) can log in successfully
- [ ] App starts without errors
