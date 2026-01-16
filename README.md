# 🤖 Izi Vyzhymka Bot (Telegram AI Summary)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![AI](https://img.shields.io/badge/AI-Google_Gemini-orange)
![YouTube](https://img.shields.io/badge/YouTube-yt--dlp-red)
![Telegram](https://img.shields.io/badge/Interface-Aiogram-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A Telegram bot that converts **YouTube videos** and **documents (PDF, DOCX)** into concise, structured **summaries**.

The bot uses a smart pipeline to extract subtitles or text, bypasses YouTube restrictions using browser cookies, and leverages **Google Gemini 1.5 Flash** to generate high-quality content summaries in various styles.

---

## 🚀 Features

* **📺 Smart YouTube Analysis:** Uses **yt-dlp** with cookie support to extract subtitles (including auto-generated ones) from videos, bypassing common "429 Too Many Requests" errors.
* **📄 Multi-Format Support:** Processes **PDF**, **DOCX**, and **TXT** files, automatically extracting text for analysis.
* **🧠 AI Summarization:** Utilizes **Google Gemini 1.5 Flash** for deep context understanding and generation.
* **🎨 Adaptive Styles:**
    * **📋 Standard:** Balanced, professional summary.
    * **⚡️ Short:** Bullet points, only key facts (3 items).
    * **🧐 Detailed:** In-depth analysis with structure.
    * **👶 Explain Like I'm 5:** Simple language with emojis.
* **🛡️ Robust Error Handling:** Implements **Retry Logic** to handle AI rate limits automatically without crashing.

---

## 🛠️ Tech Stack & Architecture

The processing pipeline consists of 4 stages:

1.  **Input:** User sends a YouTube link or a document via Telegram (`aiogram`).
2.  **Extraction:**
    * **YouTube:** `yt-dlp` uses `cookies.txt` to authenticate and download subtitles (`.vtt`).
    * **Docs:** `pypdf` or `python-docx` extracts raw text from files.
3.  **Analysis:** The text is cleaned and sent to **Google Gemini API** with a specific style prompt.
4.  **Output:** The generated summary is formatted in HTML and sent back to the user via Telegram.

---

## ⚙️ Installation

### Prerequisites
* **Python 3.10+** (Developed on 3.12)
* **Google Gemini API Key**
* **Telegram Bot Token**
* **Cookies File** (For YouTube support)

### Steps

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/TimKa-creator/telegram-ai-summary-bot.git](https://github.com/TimKa-creator/telegram-ai-summary-bot.git)
    cd telegram-ai-summary-bot
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration (Keys)**
    Set your environment variables (recommended) or edit `main.py` and `ai_module.py` locally:
    * `BOT_TOKEN`: From BotFather.
    * `GEMINI_API_KEY`: From Google AI Studio.

5.  **Setup YouTube Cookies (Crucial for Anti-Ban)** 🍪
    * Install **"Get cookies.txt LOCALLY"** extension in your browser.
    * Log in to YouTube.
    * Export cookies in **Netscape** format.
    * Save the file as `cookies.txt` in the project root folder.

6.  **Run the bot**
    ```bash
    python main.py
    ```

---

## 📂 Project Structure

* `main.py` - Bot entry point. Handles commands (`/style`, `/start`) and message routing.
* `ai_module.py` - AI logic. Manages API calls to Gemini, handles quotas (429 errors), and switches models if needed.
* `youtube_module.py` - YouTube logic. Wraps `yt-dlp` to download and parse subtitles.
* `doc_module.py` - Document handlers for `.pdf` and `.docx`.
* `cookies.txt` - Authentication file for YouTube (Do not commit to GitHub!).

---

## 🐛 Troubleshooting

* **Error 429 (Google AI):** The bot has built-in retry logic. If it persists, check your Google Cloud quota or switch to a new API key/Project.
* **Error 429 (YouTube):** Ensure `cookies.txt` is present in the root folder and is up to date. YouTube cookies may expire.
* **Bot not replying:** Check the console for logs. If using `edit_text` fails, the bot automatically falls back to sending a new message.

---

## 📜 License

This project is open-source. Feel free to use it for educational purposes.