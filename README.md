# Boofay – University Food Court Platform

Boofay is a multi-tenant Django application that lets university residents browse on-campus restaurants, place food orders, and collaborate with dining staff for delivery or pick-up. The project bundles separate apps for customers, restaurant partners, public marketing pages, and site-wide glue, making it a practical reference for medium-sized Django systems.

## Highlights
- **Customer marketplace (`market_place`)** – menu browsing, cart management, OTP-protected checkout, and split orders across multiple restaurants.
- **Restaurant partner console (`collab`)** – onboarding workflow, menu CRUD, live order boards, and staff-specific security keys.
- **Informational pages (`feeds` & `root`)** – public landing, about/contact, and authentication flows powered by Django templates.
- **Media & assets** – built-in support for food and restaurant imagery via `MEDIA_ROOT`, plus pre-bundled static branding.
- **Email + OTP hooks** – SMTP configuration is ready for password resets, account verification, and delivery notifications (see `buffet/settings.py`).

## Tech Stack
- Python 3.8+ with Django 3.0.14
- SQLite for local development (swapable via `DATABASES` in `buffet/settings.py`)
- Bootstrap-powered templates (see `buffet/templates` and per-app `templates/`)
- Pillow for handling uploaded images
- Gunicorn-ready for containerized deployments

## Getting Started
1. **Clone & enter**
   ```bash
   git clone https://github.com/Aman051103/Boofay.git
   cd Boofay
   ```
2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # PowerShell: .venv\Scripts\Activate.ps1
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Add any project-specific packages you introduce (e.g., `python-dotenv`, `psycopg2-binary`) to `requirements.txt`.
4. **Apply migrations & create an admin**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. **Run the site**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` for the customer marketplace and `/admin` for Django’s admin.

## Docker Quickstart
1. Build the image (includes system libs needed for Pillow):
   ```bash
   docker build -t boofay:latest .
   ```
2. Run the container with your database/media bound locally:
   ```bash
   docker run -it --rm -p 8000:8000 -v %cd%/media:/app/media boofay:latest
   ```
   On macOS/Linux, replace `%cd%` with `$(pwd)`. The container uses Gunicorn and listens on `0.0.0.0:8000`.
3. Provide environment variables via `--env-file` or `-e` flags for `SECRET_KEY`, email credentials, and any production DB connection settings before deploying.

## Configuration Notes
- Update `SECRET_KEY`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD` in `buffet/settings.py` (ideally via environment variables) before deploying anywhere public.
- Static files live in `static/`; uploaded media is stored under `media/`. During development Django serves these automatically, but production deployments require a proper web server or CDN.
- If you need a different database (PostgreSQL, MySQL), adjust the `DATABASES` block and install the relevant driver (`psycopg2`, `mysqlclient`, etc.).
- Background tasks are not required, but email OTP delivery depends on Gmail SMTP being enabled (or another provider configured via the standard Django settings).

## Project Layout
```
buffet/          # Core settings, URLs, global templates
market_place/    # Customer ordering domain models and views
collab/          # Restaurant/staff tools and onboarding flows
feeds/           # Marketing pages such as About and Contact
root/            # Shared authentication + high-level views
static/          # Brand assets and CSS
media/           # Example uploaded images (foods, restaurants)
```

## Application Walkthrough
- **Customer flow** – `market_place.views` handles discovery, cart creation, OTP-backed order placement, multi-restaurant splits, and delivery acknowledgment screens.
- **Restaurant flow** – `collab.views` provides profile onboarding via `GetProfile`, inventory/search tooling, live kitchen dashboards, and payment summaries.
- **Admin/staff flow** – `root.views` gives staff-only insights into restaurant rosters, paid/unpaid ledgers, and bulk payment toggles secured by `staff_attribute.security_key`.
- **Marketing & auth** – `feeds` and `buffet/templates` hold public-facing pages, email templates, and password/OTP forms that integrate directly with the configured SMTP backend.
- **Media pipeline** – Uploaded food and restaurant images land under `media/foods/images` and `media/restaurants/images` and are served using Django’s `ImageField` + Pillow stack.

## Useful Commands
- `python manage.py shell` – explore models (`food`, `order`, `sub_order`, etc.).
- `python manage.py collectstatic` – bundle assets before deploying.
- `python manage.py dumpdata market_place.food > food.json` – snapshot menu items to reload later with `loaddata`.

## Contributing
1. Fork and create a feature branch.
2. Run formatting/tests (`python manage.py test`) before opening a PR.
3. Describe UI changes with screenshots whenever possible (templates drive most of the experience).

## Troubleshooting
- **Missing images?** Ensure Pillow is installed and `MEDIA_ROOT` is writable.
- **Emails fail?** Verify Gmail “App Password” or switch to a provider supported by Django’s `EMAIL_HOST` settings.
- **Static assets not updating?** Clear your browser cache or bump the `STATICFILES_DIRS` version.
- **Container won’t start?** Confirm the image built cleanly and that port `8000` is free; check `docker logs` for Gunicorn import errors if dependencies are missing.

Happy hacking, and bon appétit! 🍽️
