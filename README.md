# Async Quotes Scraper

Project: scraping quotes from [quotes.toscrape.com](http://quotes.toscrape.com) using two different approaches, with results stored in SQLite.

## Tech Stack

- **Python 3.14**
- **asyncio** — asynchronous execution
- **aiohttp** — async HTTP requests to a JSON API
- **Playwright** — headless browser automation for JS-rendered pages
- **aiosqlite** — async SQLite access

## Project Idea

The target site exposes the same data through two different mechanisms:

1. **`api_scraper.py`** — reverse-engineered AJAX endpoint: the `/scroll` page loads quotes via `GET /api/quotes?page=N`. All pages are fetched concurrently using `asyncio.gather`, in batches of 5.
2. **`browser_scraper.py`** — the `/js/` page renders content via JavaScript with no exposed API. Playwright launches a real headless browser, clicks the "Next" button, and reads the already-rendered DOM.

Both methods write to the same SQLite table, tagged with a `source` field (`api` / `browser`), so the two approaches can be compared directly.

## Setup

\`\`\`bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
\`\`\`

## Usage

\`\`\`bash
python3 main.py --mode api        # API-based scraping only
python3 main.py --mode browser    # browser-based scraping only
python3 main.py --mode both       # both methods (default)
\`\`\`

## Output

Data is stored in `quotes.db` (SQLite), table `quotes`:

| Column | Description |
|---|---|
| id | auto-increment primary key |
| text | quote text |
| author | quote author |
| tags | comma-separated tags |
| source | `api` or `browser` — which method collected this row |
