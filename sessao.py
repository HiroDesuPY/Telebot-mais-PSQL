from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from dados import AsyncSessionlocal

async def abrir_conexao():
    async with AsyncSessionlocal() as sessao:
        try:
            yield sessao

        finally:
            await sessao.close()



