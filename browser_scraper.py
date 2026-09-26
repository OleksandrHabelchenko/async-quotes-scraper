import asyncio
from playwright.async_api import async_playwright
from db import save_quote, init_db

BASE_URL = "http://quotes.toscrape.com/js/"

async def scrape_browser():
    async with async_playwright() as p:
        broswer = await p.chromium.launch(headless=True)
        page = await broswer.new_page()
        await page.goto(BASE_URL)

        page_num = 1
        while True:
            quotes = await page.query_selector_all("div.quote")
            for quote in quotes:
                text_el = await quote.query_selector("span.text")
                author_el = await quote.query_selector("small.author")
                tag_els = await quote.query_selector_all("div.tags a.tag")

                text = await text_el.inner_text()
                author = await author_el.inner_text()
                tags = [await t.inner_text() for t in tag_els]

                await save_quote(text=text, author=author, tags=tags, source="browser")

            print(f"Scraped browser page {page_num}")

            next_button = await page.query_selector("li.next a")
            if next_button:
                await next_button.click()
                await page.wait_for_timeout(2000)
                page_num += 1
            else:
                break

        await broswer.close()
        print("Browser scraping completed.")


if __name__ == "__main__":
    asyncio.run(init_db())
    asyncio.run(scrape_browser())

