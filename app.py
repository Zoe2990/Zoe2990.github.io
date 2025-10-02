# app.py
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder="static", static_url_path="")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/healthz")
def healthz():
    return jsonify({"ok": True})

@app.route("/")
def home():
    # / -> static/index.html
    return send_from_directory("static", "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not OPENAI_API_KEY:
        return jsonify({"error": "Server missing OPENAI_API_KEY"}), 500

    data = request.get_json(silent=True) or {}
    user_input = data.get("prompt", "")

    try:
        with open("prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()
    except Exception:
        system_prompt = ""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=messages,
            temperature=0.7,
        )
        answer = resp.choices[0].message.content
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
