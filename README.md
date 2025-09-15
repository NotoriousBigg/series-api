# 📺 VideoVak Scraper API

A FastAPI-powered API that scrapes series and episode data from [videovak.com](https://videovak.com). This project allows you to retrieve:

- ✅ Series title, tags, description, number of seasons, and episodes
- ✅ Episode title, description, and torrent source

---

## 🚀 Features

- **Async HTTP requests** using `httpx`
- **HTML parsing** with BeautifulSoup
- **FastAPI framework** for building async APIs
- Custom error handling with meaningful responses

---

## 🧰 Requirements

- Python 3.9+
- pip

---

## 📦 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/videovak-fastapi-scraper.git
cd videovak-fastapi-scraper
```

2. **Create a virtual environment (optional)**:
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## ▶️ Running the API
```bash
uvicorn main:app --reload
```
By default, the API will run at:
📍 http://localhost:8000

# 🛡 Disclaimer

This tool is provided for educational purposes only. Ensure that you have permission to scrape data from any third-party site.

## 🧑‍💻 Author

Kresswell-> [Telegram](https://t.me/cliticaldamage)

Want to collaborate or improve this? Open an issue or PR!