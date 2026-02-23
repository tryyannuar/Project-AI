import os
import requests
from dotenv import load_dotenv
from ai.tools import search_wikipedia, get_weather, search_news, search_general, get_current_date

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """
Kamu adalah Focalors, AI elegan, tenang, cerdas, dan percaya diri.

Gaya bicara:
- Ringkas, tajam, tidak bertele-tele.
- Prioritaskan kepadatan informasi. Hindari filler.
- Jawaban yang terlalu panjang dianggap gagal menjaga karakter.
- Maksimal 3–5 kalimat untuk pertanyaan normal.
- Maksimal 8 kalimat untuk topik kompleks.
- Hindari paragraf panjang.
- Jangan menjelaskan sesuatu yang tidak diminta.

Aturan:
- Jika pertanyaan sederhana → jawab 1–2 kalimat.
- Jangan mengulang pertanyaan pengguna.
- Jangan memberi pembukaan generik seperti "Baik, saya akan menjelaskan".
- Jika sapaan diulang → beri variasi kecil dan sadar konteks.

Kepribadian:
- Percaya diri tanpa dramatis.
- Sedikit superior tapi tetap elegan.
- Tidak cerewet.
- Tidak mengaku sebagai AI umum.

Identitas:
Nama: Focalors
Versi: v1.3

Identitas pengembang:
Nama: Try Yannuar
Umur: 17 tahun
"""


def detect_tool(user_message):
    lower = user_message.lower()

    try:
        if "cuaca" in lower:
            city = lower.replace("cuaca", "").strip()
            return get_weather(city if city else "Jakarta")

        if "berita" in lower:
            topic = lower.replace("berita", "").strip()
            return search_news(topic if topic else "Indonesia")

        if "siapa" in lower or "apa itu" in lower:
            return search_wikipedia(user_message)

        return search_general(user_message)

    except Exception:
        return "Informasi real-time tidak tersedia."



def chat_with_focalors(history):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    latest_user_message = history[-1]["content"].strip()
    lower_msg = latest_user_message.lower()

    date_keywords = [
        "tanggal hari ini",
        "hari ini tanggal berapa",
        "tanggal sekarang",
        "sekarang tanggal berapa"
    ]

    if any(k in lower_msg for k in date_keywords):
        return f"Hari ini adalah {get_current_date()}"

    internet_info = detect_tool(latest_user_message)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "system",
            "content": f"""
Gunakan informasi berikut sebagai data faktual real-time.
Jangan mengatakan bahwa kamu tidak memiliki akses internet.
Jika relevan, jawab berdasarkan data ini:

{internet_info}
"""
        }
    ] + history

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)

        if response.status_code != 200:
            return f"Error dari API: {response.text}"

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except requests.exceptions.RequestException as e:
        return f"Koneksi ke API gagal: {str(e)}"
