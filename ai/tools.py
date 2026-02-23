import os
import requests
from datetime import datetime
from dotenv import load_dotenv

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def search_wikipedia(query):
    url = "https://id.wikipedia.org/api/rest_v1/page/summary/" + query
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return data.get("extract", "Tidak ditemukan.")
    return "Tidak ditemukan."

def get_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    return "Data cuaca tidak tersedia."

def search_news(query):
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "language": "id",
        "sortBy": "publishedAt",
        "pageSize": 3,
        "apiKey": os.getenv("NEWS_API_KEY")
    }

    try:
        r = requests.get(url, params=params, timeout=10)

        if r.status_code != 200:
            return "Gagal mengambil berita terbaru."

        articles = r.json().get("articles", [])

        if not articles:
            return "Tidak ditemukan berita terbaru untuk topik tersebut."

        return "\n".join([a["title"] for a in articles[:3]])

    except requests.exceptions.RequestException:
        return "Koneksi ke layanan berita gagal."

def search_general(query):
    # contoh pakai DuckDuckGo instant answer
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json"}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        data = r.json()
        return data.get("AbstractText", "Tidak ditemukan.")
    return "Tidak ditemukan."

def get_current_date():
    return datetime.now().strftime("%d %B %Y")
