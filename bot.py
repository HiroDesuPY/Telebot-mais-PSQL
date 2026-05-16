from sqlalchemy.future import select
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from config import TELETOKEN
from ia import IA
from sessao import abrir_conexao
from dados import Usuario, AsyncSessionlocal

bot = AsyncTeleBot(TELETOKEN)


ia = IA()


ativos_ia = {
}


def botao_permissao():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    permissao = types.KeyboardButton(text="Permitir o contato", request_contact=True,)
    markup.add(permissao)
    return markup




@bot.message_handler(content_types=['contact'])
async def receber_contato(message):
    telegram_id = message.contact.user_id
    numero_tel = message.contact.phone_number.replace("+", "")
    chat_id = message.chat.id

    async with AsyncSessionlocal() as sessao:
        query = select(Usuario).where(Usuario.nome_id == telegram_id)
        resultado = await sessao.execute(query)
        usuario = resultado.scalars().first()


        if usuario:
            usuario.numero = numero_tel

        else:
            novo_usuario = Usuario(
                nome_id = telegram_id,
                numero=numero_tel
            )
            sessao.add(novo_usuario)


        await sessao.commit()

    if chat_id not in ativos_ia:
        ativos_ia[chat_id] = {}

    ativos_ia[chat_id]['contato_enviado'] = True

    markup = types.InlineKeyboardMarkup()
    botao_comecar = types.InlineKeyboardButton(text="Começar", callback_data='comecar')
    markup.add(botao_comecar)

    await bot.send_message(
        chat_id, "✅ Número verificado com sucesso! Clique abaixo para iniciar o chat.",
        reply_markup=markup
    )











@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    chat_id = call.message.chat.id
    if chat_id not in ativos_ia:
        ativos_ia[chat_id] = {}



    match call.data:
        case "comecar":
            ativos_ia[chat_id]['ia_ativa'] = True
            texto = "Oi, bem vindo! Eu sou um assistente virtual. Como posso ajudar você hoje? "
            await bot.send_message(call.message.chat.id, texto)
        case 'sair':
            ativos_ia[chat_id]['ia_ativa'] = False
            texto = "Até mais! "
            await bot.send_message(call.message.chat.id, texto)
        


@bot.message_handler(func=lambda message: ativos_ia.get(message.chat.id, {}).get('ia_ativa'))
async def comecar(message):
    markup = types.InlineKeyboardMarkup()
    sair = types.InlineKeyboardButton("Sair", callback_data="sair")
    markup.add(sair)

    await bot.send_chat_action(message.chat.id, "typing")


    try:
        async for sessao in abrir_conexao():
            resposta = await ia.prompt(
                sessao=sessao,
                nome_id=message.chat.id,
                pergunta=message.text
            )

            await bot.send_message(message.chat.id, resposta, reply_markup=markup)
            break



    except Exception as e:
        await bot.send_message(message.chat.id, f'Erro: {e}')







@bot.message_handler(func=lambda message: True)
async def comeco(message):
    chat_id = message.chat.id
    if ativos_ia.get(message.chat.id, {}).get('contato_enviado'):

        markup = types.InlineKeyboardMarkup()
        botao_comecar = types.InlineKeyboardButton(text="Começar", callback_data='comecar')
        markup.add (botao_comecar)

        await bot.send_message(
            chat_id, "Começar atendimento.",
            reply_markup=markup
        )
        return
    

    texto = "Por favor, compartilhar o numero para melhorar a experiencia do atendimento."
    await bot.send_message(chat_id, texto, reply_markup=botao_permissao())

    