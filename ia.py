from ollama import AsyncClient
from pydantic import BaseModel
from typing import Literal, List, Dict, Any
from dados import Usuario
from sessao import abrir_conexao
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


MODEL = "llama3:8b"


class Message(BaseModel):

    role: Literal[
        'system',
        'user',
        'assistant'
    ]

    content: str



class IA:
    def __init__(self) -> None:
        self.client: AsyncClient = AsyncClient()

    async def prompt(self, sessao: AsyncSession, nome_id: int, pergunta: str) -> str:
        query = select(Usuario).where(Usuario.nome_id == nome_id)    
        resultado = await sessao.execute(query)
        mensagens_banco: List[Usuario] = list(resultado.scalars().all())

        mensagens_formatadas: List[Dict[str,str]] = []

        if not mensagens_banco:
            msg_sistema = Message(
                role='system',
                content="Você é um bot"
            )
            mensagens_formatadas.append(msg_sistema.model_dump()) 

        else:
            for msg in mensagens_banco:
                msg_validada = Message(
                    role=msg.role,
                    content=msg.historico
                )       
                mensagens_formatadas.append(msg_validada.model_dump()) 
        
        
        

        nova_pergunta = Message(
            role='user',
            content=pergunta
        )
        mensagens_formatadas.append(nova_pergunta.model_dump()) 



        nova_msg_usuario = Usuario(
            nome_id = nome_id,
            role='user',
            historico=pergunta
        )
        sessao.add(nova_msg_usuario)





        resposta_ollama: Dict[str,Any] = await self.client.chat(
            model=MODEL,
            messages=mensagens_formatadas
        )

        response_text: str = resposta_ollama['message']['content']

        resposta_ia = Message(
            role='assistant',
            content=response_text
        )

        nova_msg_ia = Usuario(
            nome_id=nome_id,
            role=resposta_ia.role,
            historico=resposta_ia.content
        )

        sessao.add(nova_msg_ia)

        await sessao.commit()

        return response_text