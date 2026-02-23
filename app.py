import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, jsonify, session
from ai.focalors import chat_with_focalors

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"reply": "Kamu diam tapi berharap dijawab. Aneh."})

    # Inisialisasi history kalau belum ada
    if "history" not in session:
        session["history"] = []

    history = session["history"]

    # Tambah pesan user
    history.append({"role": "user", "content": user_message})

    # Kirim seluruh history ke AI
    reply = chat_with_focalors(history)

    # Tambah balasan AI ke history
    history.append({"role": "assistant", "content": reply})

    session["history"] = history

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
