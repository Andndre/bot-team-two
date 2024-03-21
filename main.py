from bot import TeleBot
from handlers.arduino import add_arduino_handlers
from handlers.t3_handler import add_tic_tac_toe_handlers
import os
from dotenv import load_dotenv

load_dotenv()

# Get the API token from the environment variable
TOKEN = os.environ.get('TOKEN')

if __name__ == "__main__":
    tele_bot = TeleBot(TOKEN)
    add_arduino_handlers(tele_bot)
    add_tic_tac_toe_handlers(tele_bot)
    tele_bot.run()
