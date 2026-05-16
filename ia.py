from ollama import AsyncClient
from pydantic import BaseModel
from typing import Literal, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# 💡 Importamos ambos: Usuario para buscar o número, e Historico para as mensagens
from dados import Usuario, Historico


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
        query_usuario = select(Usuario).where(Usuario.nome_id == nome_id)    
        resultado_usuario = await sessao.execute(query_usuario)
        usuario_atual: Usuario | None = resultado_usuario.scalars().first()

        if not usuario_atual or not usuario_atual.numero:
            return "Erro: Cadastro ou número de telefone não encontrado. Por favor, compartilhe seu contato primeiro."

        numero_do_usuario = usuario_atual.numero

        query_historico = (
            select(Historico)
            .where(Historico.numero == numero_do_usuario)
            .order_by(Historico.id.asc()) # Garante ordem cronológica correta para o Ollama
        )
        resultado_historico = await sessao.execute(query_historico)
        mensagens_banco: List[Historico] = list(resultado_historico.scalars().all())

        mensagens_formatadas: List[Dict[str, str]] = []


        if not mensagens_banco:
            msg_sistema = Message(
                role='system',
                content="Você é um assistente robô de uma empresa chamado Botelegram. Você está aqui para ajudar a empresa com suas tarefas e responder as perguntas dos clientes. Responda de forma simpatica e utilize emojis para a conversa ficar mais divertida."
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

  
        nova_msg_usuario = Historico(
            numero=numero_do_usuario,
            role='user',
            historico=pergunta
        )
        sessao.add(nova_msg_usuario)


        resposta_ollama: Dict[str, Any] = await self.client.chat(
            model=MODEL,
            messages=mensagens_formatadas
        )

        response_text: str = resposta_ollama['message']['content']

        resposta_ia = Message(
            role='assistant',
            content=response_text
        )


        nova_msg_ia = Historico(
            numero=numero_do_usuario,
            role=resposta_ia.role,
            historico=resposta_ia.content
        )
        sessao.add(nova_msg_ia)

        await sessao.commit()

        return response_text