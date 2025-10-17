# Dynamic Scraper — Live Headlines

Simple Flask app that scrapes BBC headlines, saves to SQLite, and shows them on a UI.
Use `/scrape` to trigger a scrape. Add `SCRAPE_TOKEN` env var and call `/scrape?token=...` to protect.

Deploy example: Render (Docker) or any container host. Optionally use GitHub Actions to call scrape URL.
