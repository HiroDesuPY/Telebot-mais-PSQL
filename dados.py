from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from config import ENGINESQL

Base = declarative_base()
engine = create_async_engine(ENGINESQL, echo=True)
AsyncSessionlocal = async_sessionmaker(engine, AsyncEngine, expire_on_commit=False)


class Usuario(Base):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('login.id'), nullable=False)
    historico: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)