import asyncio
from bot import bot






async def main():
    await bot.infinity_polling()


if __name__ == '__main__':
    print('bot rodando...')
    asyncio.run(main())