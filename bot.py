import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop
from typing import Dict
from telepot import Bot
from tic_tac_toe import TicTacToe

class TeleBot:
    def __init__(self, token: str) -> None:
        self.bot: Bot = Bot(token)
        self.lamp_status: str = "Off"
        self.t3_games: Dict[int, TicTacToe] = {}
        self.handlers: Dict[str, function] = {}

    def handle_start(self, msg: Dict) -> None:
        chat_id = msg['chat']['id']
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
			[InlineKeyboardButton(text=f'Lampu : {self.lamp_status}', callback_data='toggle_lamp')],
			[InlineKeyboardButton(text='Cek Jarak', callback_data='cek_jarak')],
			[InlineKeyboardButton(text='Main Tic Tac Toe', callback_data='tic_tac_toe')]
		])
        self.bot.sendMessage(chat_id, 'Halo selamat datang di Bot, silahkan pilih opsi dibawah:', reply_markup=keyboard)
    
    def add_t3_game(self, message_id: int, game: TicTacToe) -> None:
        self.t3_games[message_id] = game
    
    def get_t3_game(self, message_id: int) -> TicTacToe:
        return self.t3_games[message_id]

    def run(self) -> None:
        MessageLoop(self.bot, {'chat': self.handle_start, 'callback_query': self.on_callback_query}).run_as_thread()
        print('Bot sedang berjalan...')
        while True:
            pass
            
    def add_handler(self, command: str, handler) -> None:
        self.handlers[command] = handler

    def on_callback_query(self, msg: Dict) -> None:
        query_id, _, query_data = telepot.glance(msg, flavor='callback_query')
        chat_id = msg['message']['chat']['id']
        message_id = msg['message']['message_id']

        self.handlers[query_data](self, query_id, chat_id, message_id)
