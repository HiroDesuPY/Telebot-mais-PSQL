import asyncio
from bot import bot
from dados import engine, Base




async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print('bot rodando com DB...')
    await bot.infinity_polling()

if __name__ == '__main__':
    asyncio.run(main())