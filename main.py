from bot import TeleBot
from handlers.arduino import add_arduino_handlers
from handlers.t3_handler import add_tic_tac_toe_handlers
import os
from dotenv import load_dotenv

load_dotenv()

# Get the API token from the environment variable
TOKEN = os.environ.get('TOKEN')

# Main function yang dipanggil saat program dijalankan secara langsung
if __name__ == "__main__":
    # Membuat objek TeleBot dengan token yang diambil dari environment variable
    tele_bot = TeleBot(TOKEN)
    # Menambahkan handler untuk perintah arduino
    add_arduino_handlers(tele_bot)
    # Menambahkan handler untuk perintah tic tac toe
    add_tic_tac_toe_handlers(tele_bot)
    # Menjalankan bot
    tele_bot.run()
