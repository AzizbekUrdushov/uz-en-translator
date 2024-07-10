import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import logging

API_TOKEN = '6544046407:AAFeR6aaZFiLDv5MhA5dCvSxdnmaiqGN1vk'  # Replace with your actual API token

# Initialize bot
bot = telebot.TeleBot(API_TOKEN)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Dictionary to keep track of users in translation mode
user_translation_mode = {}

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'yordam'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = KeyboardButton('Tarjima qil')
    markup.add(btn)
    bot.reply_to(message, "Salom, men Muzaf tarjimon botman. Menga xabar yuboring, men Ingliz tiliga tarjima qilaman.", reply_markup=markup)

@bot.message_handler(commands=['restart'])
def restart_process(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = KeyboardButton('Tarjima qil')
    markup.add(btn)
    bot.reply_to(message, "'Tarjima qil' tugmasi orqali tarjima qilish rejimini qaytadan ishga tushurishingiz mumkin.", reply_markup=markup)

# Handle 'Tarjima qil' button
@bot.message_handler(func=lambda message: message.text == 'Tarjima qil')
def start_translation(message):
    if user_translation_mode.get(message.chat.id, False):
        del user_translation_mode[message.chat.id]
        bot.send_message(message.chat.id, 'Tarjima rejimi to\'xtatildi. Qayta ishga tushurish uchun yana "Tarjima qil" tugmasini bosing.')
    else:
        user_translation_mode[message.chat.id] = True
        bot.send_message(message.chat.id, 'Matn yuboring. Tarjima rejimini to\'xtatish uchun /stop yozing.')

# Handle '/stop' command
@bot.message_handler(commands=['stop'])
def stop_translation(message):
    if message.chat.id in user_translation_mode:
        del user_translation_mode[message.chat.id]
    bot.send_message(message.chat.id, 'Tarjima rejimi to\'xtatildi. Qayta ishga tushurishni hohlasangiz /restart buyrug\'ini kiriting')

# Handle messages for translation
@bot.message_handler(func=lambda message: user_translation_mode.get(message.chat.id, False))
def handle_translation(message):
    bot.send_message(message.chat.id, 'Biroz kuting⌛️')
    try:
        translated_text = translate(message.text)
        bot.reply_to(message, translated_text)
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        bot.send_message(message.chat.id, "Tarjima qilishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")

# Function to handle translation requests
def translate(text):
    """Translate text using the Translate Plus API."""
    url = "https://translate-plus.p.rapidapi.com/translate"

    payload = {
        "text": text,
        "source": 'uz',
        "target": 'en'
    }
    headers = {
        "x-rapidapi-key": '5e832cf164msh0ad709d7f02e074p1fd156jsn374af7c6c36a',
        "x-rapidapi-host": "translate-plus.p.rapidapi.com",
        "Content-Type": "application/json"
    }
        
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    try:
        answer = response.json()['translations']['translation'].capitalize()
    except KeyError as e:
        logging.error(f"Unexpected response structure: {response.json()}")
        raise ValueError("Unexpected response structure from translation API")

    return answer

# Start polling
bot.polling()


