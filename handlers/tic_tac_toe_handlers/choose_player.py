from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from choose_mode import size_buttons

def choose_player(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int, user_id: int): 
    # Tag Playernya
    msg_id = (chat_id, message_id)
    
    teleBot.bot.editMessageText(msg_id, 'Silahkan tag teman anda:')
    # Bot akan mengirim pesan Undangan
    
    # Player 2 setuju, maka game dimulai
