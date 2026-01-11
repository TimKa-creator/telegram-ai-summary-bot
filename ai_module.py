import google.generativeai as genai

GOOGLE_API_KEY = "yourkey"

genai.configure(api_key=GOOGLE_API_KEY)

async def summarize(text: str, custom_prompt: str = None) -> str:
    model_name = 'models/gemini-2.0-flash'

    try:
        model = genai.GenerativeModel(model_name)
        
        safe_text = text[:40000]
        
        format_instruction = (
            "ВАЖЛИВО: Ти формуєш відповідь для Telegram бота.\n"
            "Дотримуйся суворих правил форматування HTML:\n"
            "✅ ДОЗВОЛЕНО: <b>жирний</b>, <i>курсив</i>, <a href='URL'>посилання</a>, <code>код</code>.\n"
            "❌ ЗАБОРОНЕНО: <p>, <br>, <h1>, <h2>, <ul>, <li>, [Markdown].\n"
            "Для списків використовуй звичайні тире (- ) або емодзі.\n"
            "Для нового рядка просто роби відступ (Enter).\n\n"
        )

        if not custom_prompt:
            base_prompt = (
                "Проаналізуй цей текст і зроби конспект українською.\n"
                "Структура: 🎯 Головна думка, 🔑 5-7 тез, 💡 Висновок."
            )
        else:
            base_prompt = custom_prompt
        
        full_prompt = f"{format_instruction}{base_prompt}\n\nТекст:\n{safe_text}"
        
        response = await model.generate_content_async(full_prompt)
        
        clean_text = response.text
        clean_text = clean_text.replace("<p>", "").replace("</p>", "\n")
        clean_text = clean_text.replace("##", "").replace("**", "") 
        
        return clean_text
        
    except Exception as e:
        return f"Помилка AI: {e}"
        return clean_text
        
    except Exception as e:

        return f"Помилка AI: {e}"
