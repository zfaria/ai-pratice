from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Inicializa o modelo OpenAI
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo"
)

# Template para o chatbot
template = """
Você é um assistente atencioso para WhatsApp.
Usuário: {pergunta}
Assistente:
"""
prompt = PromptTemplate(
    input_variables=["pergunta"],
    template=template
)

# Cria a chain
chain = LLMChain(llm=llm, prompt=prompt)
