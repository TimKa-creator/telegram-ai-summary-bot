import yt_dlp
import os
import glob
import re

def get_video_transcript(url: str) -> str:
    print(f"🔍 [yt-dlp] Починаю завантаження субтитрів: {url}")
    
    for f in glob.glob("subtitle_temp*"):
        try:
            os.remove(f)
        except:
            pass

    cookie_path = None
    if os.path.exists('cookies.txt'):
        cookie_path = 'cookies.txt'
        print("🍪 Використовую cookies.txt")
    elif os.path.exists('cookies.txt.txt'):
        cookie_path = 'cookies.txt.txt'
        print("🍪 Використовую cookies.txt.txt")
    elif os.path.exists('cookies'):
        cookie_path = 'cookies'

    ydl_opts = {
        'skip_download': True,
        'writeautomaticsub': True,
        'writesubtitles': True,
        'subtitleslangs': ['uk', 'en', 'ru'],
        'outtmpl': 'subtitle_temp',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': cookie_path,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"⚠️ Сталася помилка при завантаженні ({e}), але перевіряємо файли...")

    files = glob.glob("subtitle_temp*.vtt")
    
    if not files:
        print("🔴 yt-dlp: Файл субтитрів не знайдено.")
        return None
    
    filename = files[0]
    print(f"✅ Файл успішно знайдено: {filename}")

    text_lines = []
    seen = set()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                if '-->' in line: continue
                if line == 'WEBVTT': continue
                if line.startswith('Kind:'): continue
                if line.startswith('Language:'): continue
                if line.isdigit(): continue
                
                clean_line = re.sub(r'<[^>]+>', '', line)
                clean_line = clean_line.strip()

                if clean_line and clean_line not in seen:
                    text_lines.append(clean_line)
                    seen.add(clean_line)
        
        try:
            os.remove(filename)
        except:
            pass
            
        full_text = " ".join(text_lines)
        return full_text

    except Exception as e:
        print(f"🔴 Помилка обробки файлу: {e}")
        return None