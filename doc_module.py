import os
import pypdf
from docx import Document

def extract_text_from_file(file_path: str) -> str:
    """Визначає тип файлу і витягує з нього текст."""
    
    # Отримуємо розширення файлу (.pdf, .docx, .txt)
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    text = ""

    try:
        # 1. Якщо це PDF
        if extension == ".pdf":
            reader = pypdf.PdfReader(file_path)
            # Збираємо текст з усіх сторінок
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        # 2. Якщо це Word (.docx)
        elif extension == ".docx":
            doc = Document(file_path)
            # Збираємо текст з кожного абзацу
            for para in doc.paragraphs:
                text += para.text + "\n"

        # 3. Якщо це звичайний текст (.txt)
        elif extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        else:
            return None # Невідомий формат

        return text

    except Exception as e:
        print(f"Помилка читання файлу: {e}")
        return None