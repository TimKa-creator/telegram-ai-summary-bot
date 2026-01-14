import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import doc_module
import ai_module
import youtube_module

TOKEN = "your token"

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

user_styles = {}

STYLES = {
    "standard": {
        "name": "📋 Стандарт",
        "prompt": "Зроби класичний конспект. Стиль: діловий, чіткий."
    },
    "short": {
        "name": "⚡️ Стисло",
        "prompt": "Максимально коротко. Тільки сухі факти (3 пункти)."
    },
    "long": {
        "name": "🧐 Детально",
        "prompt": "Зроби дуже розгорнутий аналіз. Опиши всі деталі, дати, цифри та імена. Розбий на розділи (вступ, основна частина, висновок)."
    },
    "child": {
        "name": "👶 Для дитини",
        "prompt": "Поясни як для 5-річної дитини, стисло та дуже коротко, використовуй веселі емодзі."
    },
    "bullets": {
        "name": "📝 Список",
        "prompt": "Тільки маркований список фактів, без вступу і води."
    }
}

def get_style_keyboard():
    buttons = [
        [InlineKeyboardButton(text="📋 Стандарт", callback_data="style_standard"),
         InlineKeyboardButton(text="⚡️ Стисло", callback_data="style_short")],
        [InlineKeyboardButton(text="🧐 Детально", callback_data="style_long"),
         InlineKeyboardButton(text="👶 Для дитини", callback_data="style_child")],
        [InlineKeyboardButton(text="📝 Список фактів", callback_data="style_bullets")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def smart_reply(message: types.Message, text: str):
    MAX_LENGTH = 4000
    parts = []
    current_part = ""

    lines = text.split('\n')

    for line in lines:
        if len(current_part) + len(line) + 1 > MAX_LENGTH:
            parts.append(current_part)
            current_part = line + "\n"
        else:
            current_part += line + "\n"
    
    if current_part:
        parts.append(current_part)

    for part in parts:
        try:
            await message.answer(part, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"⚠️ Помилка HTML: {e}. Відправляю текстом.")
            await message.answer(part, parse_mode=None)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "👋 <b>Привіт!</b> Я — <b>Izi Vyzhymka Bot</b>.\n"
        "Кидай файл або посилання на YouTube, а я зроблю з нього конспект.\n\n"
        "🎨 Тисни /style щоб змінити формат конспекту."
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "🆘 <b>Довідка</b>\n\n"
        "Я вмію робити конспекти з:\n"
        "🎥 <b>YouTube</b> (відео з субтитрами)\n"
        "📄 <b>Файлів</b> (.pdf, .docx, .txt)\n\n"
        "⚙️ <b>Налаштування:</b>\n"
        "Натисни /style щоб обрати стиль (стисло, детально, для дітей).\n\n"
        "⚠️ <i>Якщо файл дуже великий, я прочитаю перші 30-40 сторінок.</i>"
    )

@dp.message(Command("style"))
async def change_style_command(message: types.Message):
    current = user_styles.get(message.from_user.id, "standard")
    style_name = STYLES[current]["name"]
    await message.answer(
        f"🎨 <b>Налаштування стилю</b>\n\n"
        f"Зараз: <b>{style_name}</b>\n"
        "Обери новий формат:",
        reply_markup=get_style_keyboard()
    )

@dp.callback_query(F.data.startswith("style_"))
async def set_style(callback: CallbackQuery):
    new_style = callback.data.split("_")[1]
    user_styles[callback.from_user.id] = new_style
    style_name = STYLES[new_style]["name"]
    await callback.message.edit_text(f"✅ Готово! Тепер стиль: <b>{style_name}</b>")
    await callback.answer()


async def process_content(message: types.Message, text: str, content_type: str):
    user_id = message.from_user.id
    
    style_key = user_styles.get(user_id, "standard")
    style_prompt = STYLES[style_key]["prompt"]
    style_name = STYLES[style_key]["name"]

    wait_msg = await message.answer(f"🧠 Аналізую (<b>{style_name}</b>)...")

    summary = await ai_module.summarize(text, custom_prompt=style_prompt)
    
    try:
        await wait_msg.delete()
    except:
        pass
    
    await message.answer(f"📄 <b>Конспект ({content_type}):</b>")
    await smart_reply(message, summary)

@dp.message(F.document)
async def handle_files(message: types.Message):
    doc = message.document
    if not doc.file_name.lower().endswith(('.pdf', '.docx', '.txt')):
        await message.answer("❌ Тільки .pdf, .docx, .txt")
        return

    wait_msg = await message.answer("📥 Скачую...")
    try:
        file_info = await bot.get_file(doc.file_id)
        path = f"downloads/{doc.file_name}"
        os.makedirs("downloads", exist_ok=True)
        await bot.download_file(file_info.file_path, path)
        
        text = await asyncio.to_thread(doc_module.extract_text_from_file, path)
        os.remove(path)

        if not text:
            try:
                await wait_msg.edit_text("❌ Пустий файл або скан-копія.")
            except:
                await message.answer("❌ Пустий файл або скан-копія.")
            return
            
        try:
            await wait_msg.delete()
        except:
            pass

        await process_content(message, text, doc.file_name)

    except Exception as e:
        print(f"Error handling file: {e}")
        try:
            await wait_msg.edit_text(f"Помилка: {e}")
        except:
            await message.answer(f"Помилка: {e}")

@dp.message(F.text.contains("youtu"))
async def handle_youtube(message: types.Message):
    wait_msg = await message.answer("⏳ Шукаю субтитри...")
    text = await asyncio.to_thread(youtube_module.get_video_transcript, message.text)
    
    if not text:
        try:
            await wait_msg.edit_text("❌ Субтитри не знайдено.")
        except:
            await message.answer("❌ Субтитри не знайдено.")
        return

    try:
        await wait_msg.delete()
    except:
        pass

    await process_content(message, text, "YouTube Відео")

async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="🚀 Запуск"),
        BotCommand(command="style", description="🎨 Налаштування"),
        BotCommand(command="help", description="🆘 Допомога"),
    ])
    print("✅ Бот запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


