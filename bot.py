import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
)
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! আমি ফিচার-সমৃদ্ধ Docker Telegram Bot, Fly.io-তে হোস্ট করা!")

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - বট শুরু করো
"
        "/help - সাহায্য
"
        "/now - এখনকার সময় ও তারিখ
"
        "/ayah <সূরা:আয়াত> - কুরআনের আয়াত
"
        "/weather <শহর> - আবহাওয়ার তথ্য
"
        "/quote - ইসলামিক কোটস
"
        "/ask <prompt> - AI Chat
"
        "/image <prompt> - AI ছবি"
    )

# /now command
async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"🕒 এখন সময়: {now}")

# /ayah command
async def ayah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args[0] if context.args else "2:255"
        response = requests.get(f"http://api.alquran.cloud/v1/ayah/{args}/bn.bengali")
        data = response.json()
        if data["status"] == "OK":
            ayah_text = data["data"]["text"]
            await update.message.reply_text(f"📖 আয়াত {args}:
{ayah_text}")
        else:
            await update.message.reply_text("❌ আয়াত পাওয়া যায়নি।")
    except Exception as e:
        await update.message.reply_text("⚠️ আয়াত আনতে সমস্যা হয়েছে।")

# /weather command
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args) if context.args else "Dhaka"
    api_key = os.getenv("WEATHER_API_KEY", "your-weather-api-key")
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()
        if res.get("cod") != 200:
            await update.message.reply_text("❌ শহরের তথ্য পাওয়া যায়নি।")
            return
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        await update.message.reply_text(f"🌤️ {city.title()}: {temp}°C, {desc}")
    except:
        await update.message.reply_text("⚠️ আবহাওয়া আনতে সমস্যা হয়েছে।")

# /quote command
async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = [
        "🕌 "যে আল্লাহর উপর ভরসা করে, আল্লাহ তাকে যথেষ্ট।"",
        "☪️ "নিশ্চয়ই প্রতিটি কষ্টের সাথে স্বস্তি আছে।"",
        "📿 "যে যত বেশি ইবাদত করে, সে তত বেশি শান্তি পায়।""
    ]
    import random
    await update.message.reply_text(random.choice(quotes))

# /ask command (Dummy)
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args) if context.args else "তুমি কে?"
    await update.message.reply_text(f"🤖 AI বলে: '{prompt}' এর উত্তর আসবে এখানে। (ডেমো)")

# /image command (Dummy)
async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args) if context.args else "A cat"
    await update.message.reply_text(f"🖼️ '{prompt}' এর ছবি তৈরি করা হবে এখানে। (ডেমো)")

# Setup app and handlers
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("now", now))
app.add_handler(CommandHandler("ayah", ayah))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("quote", quote))
app.add_handler(CommandHandler("ask", ask))
app.add_handler(CommandHandler("image", image))

app.run_polling()
