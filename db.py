import aiosqlite

DB_NAME = "quotes.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT NOT NULL,
                tags TEXT,
                source TEXT NOT NULL
            )
            """
        )
        await db.commit()

async def save_quote(text, author, tags, source):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO quotes (text, author, tags, source) VALUES (?, ?, ?, ?)",
            (text, author,", ".join(tags), source),
        )
        await db.commit()


