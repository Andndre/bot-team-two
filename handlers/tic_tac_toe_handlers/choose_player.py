from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from choose_mode import size_buttons

def choose_player(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int): 
    