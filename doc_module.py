import os
import pypdf
from docx import Document

def extract_text_from_file(file_path: str) -> str:
    """Визначає тип файлу і витягує з нього текст."""
    
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    text = ""

    try:
        if extension == ".pdf":
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        elif extension == ".docx":
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        elif extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        else:
            return None

        return text

    except Exception as e:
        print(f"Помилка читання файлу: {e}")
        return None
