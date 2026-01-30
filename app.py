from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# --- CONFIGURAÇÃO GEMINI ---
# Substitua pela sua chave real!
# Mude DISSO:
# GEMINI_API_KEY = "AIzaSy..."

# Para ISSO:
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# A PERSONA ANOS 2000 (Idêntica à anterior)
INSTRUCOES_ANOS_2000 = """
Data atual simulada: 15 de Maio de 2000.
Você é o "CyberBuddy_2000", um bot de bate-papo no MSN Messenger.

REGRAS RÍGIDAS:
1. CONHECIMENTO ZERO PÓS-2000: Você NÃO sabe o que é iPhone, Android, YouTube, Facebook, Instagram, TikTok, ChatGPT ou Wi-Fi rápido.
2. TECNOLOGIA ATUAL: Sua realidade é Internet discada (dial-up), Windows 98 SE, ICQ, Napster, gravadores de CD e disquetes.
3. CULTURA POP: O filme do momento é Matrix ou Missão Impossível 2. Música é Britney Spears, NSYNC e Backstreet Boys.
4. ESTILO DE FALA: Use gírias da época ("tc", "naum", "blz", "vc", "falow"). Use emoticons clássicos como :-) :-( ;-).
5. REAÇÃO AO FUTURO: Se perguntarem sobre algo moderno (ex: "O que é um smartphone?"), responda com confusão: "Smartphone? Tipo aqueles celulares tijolão da Nokia que só fazem ligação? Naum entendi."

OBJETIVO: Manter a ilusão do ano 2000 no MSN a qualquer custo.
"""

# Configuração do modelo
generation_config = {
    "temperature": 0.9,
    "max_output_tokens": 500,
}
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
    system_instruction=INSTRUCOES_ANOS_2000
)

chat_session = model.start_chat(history=[])

# --- ROTAS DO FLASK ---

@app.route("/")
def index():
    # Serve a página HTML principal
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    # Recebe a mensagem do frontend
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "Mensagem vazia"}), 400

    try:
        # Envia para o Gemini e pega a resposta
        response = chat_session.send_message(user_message)
        bot_reply = response.text
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print(f"Erro Gemini: {e}")
        return jsonify({"reply": "Ops, minha conexão discada caiu aqui... tenta de novo? :-("})

if __name__ == "__main__":
    app.run(debug=True)
