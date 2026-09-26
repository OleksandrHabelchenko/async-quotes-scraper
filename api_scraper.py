import asyncio

import aiohttp

from db import save_quote, init_db

API_URL = "http://quotes.toscrape.com/api/quotes?page={}"

BATCH_SIZE = 5

async def fetch_page(session, page):
    url = API_URL.format(page)
    async with session.get(url) as response:
        return await response.json()

async def scrape_api():
    async with aiohttp.ClientSession() as session:
        page = 1
        has_next = True

        while has_next:
            batch_pages = list(range(page, page + BATCH_SIZE))
            tasks = [fetch_page(session, p) for p in batch_pages]

            results = await asyncio.gather(*tasks)

            for result in results:
                for quote in result["quotes"]:
                    await save_quote(
                        quote["text"],
                        quote["author"]["name"],
                        quote["tags"],
                        source="api"
                    )

            has_next = results[-1]["has_next"]
            page += BATCH_SIZE
            print(f"Scraped pages {page -1}")

        print("Scraping completed.")

if __name__ == "__main__":
    asyncio.run(init_db())
    asyncio.run(scrape_api())