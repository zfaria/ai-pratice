import os
from flask import Flask, request
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Carrega variáveis do .env
load_dotenv()

# Inicializa Flask
app = Flask(__name__)

# Inicializa o modelo OpenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# Prompt base
prompt = PromptTemplate(
    input_variables=["mensagem"],
    template="Você é um assistente no WhatsApp. Responda a esta mensagem de forma útil e natural:\n\nMensagem: {mensagem}"
)

# Cria a chain com LangChain
chain = LLMChain(llm=llm, prompt=prompt)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """Webhook para lidar com mensagens recebidas do WhatsApp via Twilio"""
    try:
        msg = request.form.get("Body", "").strip()
        sender = request.form.get("From", "")

        if not msg:
            resposta_texto = "Não consegui ler sua mensagem. Pode repetir?"
        else:
            # Usa o método correto para versões novas do LangChain
            resposta_texto = chain.invoke({"mensagem": msg})["text"]

        # Cria resposta Twilio
        twilio_resp = MessagingResponse()
        twilio_resp.message(resposta_texto)
        return str(twilio_resp)

    except Exception as e:
        print(f"[ERRO] Falha no webhook: {e}")
        twilio_resp = MessagingResponse()
        twilio_resp.message("Desculpe, ocorreu um erro interno no bot.")
        return str(twilio_resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

