import asyncio
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from config import TELETOKEN
from ia import IA


bot = AsyncTeleBot(TELETOKEN)


ia = IA()


ativos_ia = {
}



@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    match call.data:
        case "comecar":
            ativos_ia[call.message.chat.id] = True
            texto = "Oi, bem vindo! Eu sou um assistente virtual. Como posso ajudar você hoje? "
            await bot.send_message(call.message.chat.id, texto)
        case 'sair':
            ativos_ia[call.message.chat.id] = False
            texto = "Até mais! "
            await bot.send_message(call.message.chat.id, texto)
        


@bot.message_handler(func=lambda message: ativos_ia.get(message.chat.id))
async def comecar(message):
    markup = types.InlineKeyboardMarkup()
    sair = types.InlineKeyboardButton("Sair", callback_data="sair")
    markup.add(sair)
    await bot.send_chat_action(message.chat.id, "typing")
    
    try:
        resposta = ia.prompt(message.text)
        await bot.send_message(message.chat.id, resposta, reply_markup=markup)

    except Exception as e:
        await bot.send_message(message.chat.id, f'Erro: {e}')
 


@bot.message_handler(func=lambda message: True)
async def comeco(message):
    texto = "Bem-vindo ao bot"
    markup = types.InlineKeyboardMarkup()
    comecar = types.InlineKeyboardButton("Começar", callback_data="comecar")
    markup.add(comecar)
    await bot.send_message(message.chat.id, texto, reply_markup=markup)


