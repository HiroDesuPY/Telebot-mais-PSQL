from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import ENGINESQL

engine = create_async_engine(ENGINESQL, echo=True)

AsyncSessionlocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()



class Usuario(Base):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_id: Mapped[int] = mapped_column(BigInteger, index=True)
    numero: Mapped[int] = mapped_column(BigInteger, nullable=True, unique=True)
    mensagens: Mapped[list['Historico']] = relationship('Historico', back_populates='usuario', cascade='all, delete-orphan')


class Historico(Base):
    __tablename__ = 'historicos'


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero: Mapped[int] = mapped_column(BigInteger, ForeignKey('usuarios.numero'))
    historico: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='mensagens', primaryjoin='Historico.numero == Usuario.numero')