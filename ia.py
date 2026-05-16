from ollama import AsyncClient
from pydantic import BaseModel
from typing import Literal
from dados import Usuario
from sessao import abrir_conexao

MODEL = "llama3:8b"


class Message(BaseModel):

    role: Literal[
        'system',
        'user',
        'assistant'
    ]

    content: str



class IA:
    def __init__(self):
        self.messages: list[Message] = [
            Message(role='system',
                    content='Você é um chatbot'                    
                    )
        ]

    def prompt(self, pergunta: str) -> str:
        pergunta = Message(
            role='user',
            content=pergunta
        )
        self.messages.append(pergunta)

        resposta = chat(
            model=MODEL,
            messages=[
            mensagem.model_dump()
            for mensagem in self.messages
            ]
        )

        response = resposta['message']['content']
            
        mensagem_ia = Message(
            role='assistant',
            content=response
        )

        self.messages.append(mensagem_ia)

        return resposta['message']['content']