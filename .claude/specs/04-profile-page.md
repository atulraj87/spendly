# Spec: Profile Page

## Overview
Implement the `/profile` route so authenticated users can view their account details. The GET handler must enforce a login-required guard — unauthenticated visitors are redirected to `/login`. Once authenticated, the route fetches the full user record from the database (name, email, member-since date) and renders a real profile page. This step also wires the user's name in the navbar to link to `/profile`, completing the logged-in navigation experience introduced in Step 3.

## Depends on
- Step 1 — Database setup (`get_db()` and the `users` table must be complete)
- Step 2 — Registration (users must exist in the database)
- Step 3 — Login/Logout (`session["user_id"]` must be set on login)

## Routes
- `GET /profile` — display logged-in user's profile — logged-in only (redirect to `/login` if session missing)

## Database changes
No database changes. The `users` table already has `id`, `name`, `email`, `password_hash`, and `created_at`.

## Templates
- **Modify:** `templates/profile.html` — replace the placeholder with a real profile card showing:
  - User's full name
  - Email address
  - Member since date (formatted from `created_at`, e.g. "June 2026")
- **Modify:** `templates/base.html` — make the user's name in the logged-in navbar a link to `url_for('profile')` (currently it may be plain text)

## Files to change
- `app.py` — replace the `/profile` stub body with:
  1. Login-required guard: if `"user_id"` not in `session`, `redirect(url_for("login"))`
  2. Query: `SELECT id, name, email, created_at FROM users WHERE id = ?` using `session["user_id"]`
  3. If no row found (deleted account edge case), clear session and redirect to landing
  4. Pass `user` row to `render_template("profile.html", user=user)`
- `templates/profile.html` — build out the profile card (see Templates above)
- `templates/base.html` — link the logged-in user name to `/profile`

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with werkzeug — do not read or display `password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Login guard must come first — check `session["user_id"]` before any DB call
- Format `created_at` in the template using Jinja's `strptime`/`strftime` or pass a pre-formatted string from the route
- Keep all logic inside the existing `profile()` function in `app.py` — no separate modules

## Definition of done
- [ ] Visiting `/profile` without being logged in redirects to `/login`
- [ ] After login, `/profile` displays the user's name and email
- [ ] The member-since date is shown in a human-readable format (e.g. "June 2026")
- [ ] The user's name in the navbar links to `/profile` when logged in
- [ ] The demo user (`demo@spendly.com` / `demo123`) can view their profile after login
- [ ] App starts without errors
