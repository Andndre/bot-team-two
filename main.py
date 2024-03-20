from bot import TeleBot
from handlers.arduino import add_arduino_handlers
from handlers.t3_handler import *

if __name__ == "__main__":        
    tele_bot = TeleBot('6803335035:AAEsIx4P874EfbjP0OP0w9XpUVPB_0tOuoo')
    add_arduino_handlers(tele_bot)
    add_tic_tac_toe_handlers(tele_bot)
    tele_bot.run()
