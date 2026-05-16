# 🤖 Bot de Atendimento Inteligente com Telegram

Um chatbot assíncrono para Telegram integrado com inteligência artificial (Ollama/Llama3), capaz de manter conversas contextualizadas com persistência em banco de dados.

## ✨ Funcionalidades

- 🔐 **Autenticação de Usuário** - Validação via compartilhamento de contato Telegram
- 💬 **Chat Inteligente** - Respostas geradas por modelo LLM (Llama3:8b)
- 📝 **Histórico Persistente** - Todas as conversas são armazenadas em banco de dados
- ⚡ **Assíncrono** - Processamento não-bloqueante para múltiplas requisições simultâneas
- 🗄️ **Banco de Dados Robusto** - SQLAlchemy 2.0 com PostgreSQL
- 🎯 **Contexto Preservado** - A IA mantém histórico para respostas coerentes

## 🛠️ Stack Tecnológico

| Componente | Tecnologia |
|-----------|-----------|
| **Bot/API** | Python-Telegram-Bot (AsyncTeleBot) |
| **ORM** | SQLAlchemy 2.0 |
| **Banco de Dados** | PostgreSQL (async) |
| **IA/LLM** | Ollama + Llama3:8b |
| **Validação** | Pydantic |
| **Async Runtime** | AsyncIO |
| **Configuração** | python-dotenv |

## 📋 Pré-requisitos

- Python 3.10+
- PostgreSQL instalado e rodando
- Ollama instalado com modelo Llama3:8b
- Token do Bot Telegram (@BotFather)

## 🚀 Instalação

### 1. Clone o Repositório
```bash
git clone <seu-repositorio>
cd botelegram-db
```

### 2. Crie um Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
TELETOKEN=seu_token_do_bot_aqui
ENGINE=postgresql+asyncpg://usuario:senha@localhost:5432/botelegram
```

### 5. Inicie o Ollama
```bash
ollama serve
```

### 6. Execute o Bot
```bash
python main.py
```

## 📁 Estrutura do Projeto

```
botelegram-db/
├── bot.py           # Handlers e orquestração do bot Telegram
├── dados.py         # Modelos SQLAlchemy (Usuario, Historico)
├── ia.py            # Motor de IA com integração Ollama
├── config.py        # Carregamento de variáveis de ambiente
├── sessao.py        # Context manager para banco de dados
├── main.py          # Ponto de entrada da aplicação
├── .env             # Variáveis de ambiente (não incluir no git)
├── requirements.txt # Dependências do projeto
└── README.md        # Este arquivo
```

## 🔑 Componentes Principais

### bot.py
**Responsável por:** Handlers de mensagens e callbacks do Telegram

**Funcionalidades:**
- `botao_permissao()` - Cria botão de compartilhamento de contato
- `receber_contato()` - Processa contato do usuário e armazena no banco
- `callback_query()` - Gerencia cliques em botões inline
- `comecar()` - Handler principal de mensagens de IA
- `comeco()` - Handler fallback para usuários não autenticados

### dados.py
**Responsável por:** Modelagem de dados e configuração do banco

**Modelos:**
- `Usuario` - Tabela de usuários com id Telegram e número de telefone
- `Historico` - Tabela de histórico de mensagens (user/assistant)

**Engine:**
- Configuração assíncrona de PostgreSQL
- SessionMaker para gerenciamento de sessões

### ia.py
**Responsável por:** Integração com modelo de IA

**Funcionalidades:**
- `IA.prompt()` - Processa pergunta do usuário
  - Busca usuário no banco
  - Recupera histórico de mensagens
  - Envia para modelo Llama3
  - Armazena resposta no banco

**Pydantic Models:**
- `Message` - Validação de mensagens (role + content)

### config.py
**Responsável por:** Gerenciamento de configuração segura

- Carrega variáveis de `.env`
- Exporta `TELETOKEN` e `ENGINESQL`

### sessao.py
**Responsável por:** Context manager de banco de dados

- `abrir_conexao()` - Gerencia sessão assíncrona com garantia de fechamento

### main.py
**Responsável por:** Inicialização da aplicação

- Cria tabelas do banco de dados
- Inicia polling infinito do bot

## 💡 Fluxo de Funcionamento

```
1. Usuário inicia conversa
   ↓
2. Bot solicita compartilhamento de contato
   ↓
3. Usuário compartilha número (válida e armazena)
   ↓
4. Bot oferece botão "Começar"
   ↓
5. Usuário clica em "Começar"
   ↓
6. Bot ativa modo IA (ia_ativa = True)
   ↓
7. Cada mensagem:
   - Busca histórico da conversa
   - Envia para Ollama/Llama3
   - Armazena pergunta e resposta no banco
   - Retorna resposta ao usuário
```

## 🗄️ Schema do Banco de Dados

### Tabela: usuarios
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | Integer | PK auto-increment |
| nome_id | BigInteger | ID único do Telegram (indexed) |
| numero | BigInteger | Número de telefone (unique, nullable) |

### Tabela: historicos
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | Integer | PK auto-increment |
| numero | BigInteger | FK para usuarios.numero |
| historico | String | Conteúdo da mensagem |
| role | String | 'user' ou 'assistant' |

## ⚙️ Configuração Avançada

### Alterar Modelo de IA
Em `ia.py`, linha 11:
```python
MODEL = "llama3:8b"  # Altere para outro modelo disponível no Ollama
```

### Customizar Prompt do Sistema
Em `ia.py`, linhas 45-49:
```python
msg_sistema = Message(
    role='system',
    content="Você é um assistente robô de uma empresa chamado Botelegram..."
)
```

### Pool de Conexões
Em `dados.py`, ajuste o engine se necessário:
```python
engine = create_async_engine(
    ENGINESQL, 
    echo=True,
    pool_size=20,
    max_overflow=40
)
```

## 🧪 Testando a Aplicação

### Teste de Conexão com Ollama
```bash
curl http://localhost:11434/api/tags
```

### Teste de Banco de Dados
```bash
psql -U usuario -d botelegram -c "\dt"
```

### Teste com o Bot
1. Inicie o bot: `python main.py`
2. Abra Telegram e envie `/start`
3. Compartilhe seu contato
4. Clique em "Começar"
5. Teste uma pergunta: "Olá, tudo bem?"

## 📊 Monitoramento

### Ver Log de Requisições do Ollama
```bash
# Em outro terminal
tail -f logs/ollama.log
```

### Ver Histórico de um Usuário
```sql
SELECT * FROM historicos WHERE numero = 5511999999999 ORDER BY id DESC LIMIT 10;
```

## 🐛 Troubleshooting

### Erro: "Module not found: telebot"
```bash
pip install pyTelegramBotAPI
```

### Erro: "Connexion refused: Ollama"
- Verifique se Ollama está rodando: `curl localhost:11434`
- Execute: `ollama serve`

### Erro: "Database connection error"
- Verifique credenciais do PostgreSQL
- Confirme que o banco existe: `createdb botelegram`

### Timeout na resposta da IA
- Aumente timeout em `bot.py`
- Considere usar modelo mais leve (ex: mistral)

## 📈 Performance

- **Concorrência:** Suporta múltiplas conversas simultâneas
- **Latência:** Típica de 2-10s (depende do modelo)
- **DB Queries:** Indexado em `nome_id` para busca rápida

## 🔒 Segurança

- ✅ Token do bot em variável de ambiente
- ✅ Credenciais do DB em `.env` (ignorado no git)
- ✅ Query injection prevention (SQLAlchemy)
- ✅ Validação de entrada com Pydantic

## 📝 Dependências

```
pyTelegramBotAPI>=4.14.0
sqlalchemy>=2.0.0
asyncpg>=0.28.0
ollama>=0.1.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

## 🤝 Contribuindo

1. Crie uma branch: `git checkout -b feature/minha-feature`
2. Commit: `git commit -m "Adiciona minha feature"`
3. Push: `git push origin feature/minha-feature`
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT.

## 👨‍💻 Autor

Desenvolvido como projeto de Chatbot IA integrado com Telegram.

---

**Última atualização:** Maio 2026

Para dúvidas ou melhorias, entre em contato! 🚀
