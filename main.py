import asyncio
import argparse
from db import init_db
from api_scraper import scrape_api
from browser_scraper import scrape_browser



async def run(mode):
    await init_db()


    if mode in ("api", "both"):
        print("Starting API scraping...")
        await scrape_api()

    if mode in ("browser", "both"):
        print("Starting browser scraping...")
        await scrape_browser()

    print("Scraping completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape quotes from quotes.toscrape.com")
    parser.add_argument(
        "--mode",
        choices=["api", "browser", "both"],
        default="both",
        help="Choose the scraping mode: 'api', 'browser', or 'both' (default: both)",
    )
    args = parser.parse_args()

    asyncio.run(run(args.mode))