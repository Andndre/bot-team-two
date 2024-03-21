import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop
from typing import Dict
from telepot import Bot
from tic_tac_toe import TicTacToe

class TeleBot:
    def __init__(self, token: str) -> None:
        """
        Inisialisasi bot dengan token dan memberikan default value untuk status lampu dan permainan Tic Tac Toe
        """
        self.bot: Bot = Bot(token)
        self.lamp_status: str = "Off"
        self.t3_games: Dict[int, TicTacToe] = {}
        self.handlers: Dict[str, function] = {}

    def handle_start(self, msg: Dict) -> None:
        """
        Menangani pesan /start dan mengirimkan keyboard untuk memilih opsi
        """
        chat_id = msg['chat']['id']
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
			[InlineKeyboardButton(text=f'Lampu : {self.lamp_status}', callback_data='toggle_lamp')],
			[InlineKeyboardButton(text='Cek Jarak', callback_data='cek_jarak')],
			[InlineKeyboardButton(text='Main Tic Tac Toe', callback_data='tic_tac_toe')]
		])
        self.bot.sendMessage(chat_id, 'Halo selamat datang di Bot, silahkan pilih opsi dibawah:', reply_markup=keyboard)
    
    def add_t3_game(self, message_id: int, game: TicTacToe) -> None:
        """
        Menyimpan game Tic Tac Toe berdasarkan message ID
        """
        self.t3_games[message_id] = game
    
    def get_t3_game(self, message_id: int) -> TicTacToe:
        """
        Mengambil game Tic Tac Toe berdasarkan message ID
        """
        return self.t3_games[message_id]

    def run(self) -> None:
        """
        Menjalankan bot dan menangani pesan dengan menggunakan `MessageLoop`
        """
        MessageLoop(self.bot, {'chat': self.handle_start, 'callback_query': self.on_callback_query}).run_as_thread()
        print('Bot sedang berjalan...')
        while True:
            pass
            
    def add_handler(self, command: str, handler) -> None:
        """
        Menambahkan handler untuk command tertentu
        """
        self.handlers[command] = handler

    def on_callback_query(self, msg: Dict) -> None:
        """
        Menangani callback query (ketika tombol ditekan)
        """
        query_id, _, query_data = telepot.glance(msg, flavor='callback_query')
        chat_id = msg['message']['chat']['id']
        message_id = msg['message']['message_id']

        self.handlers[query_data](self, query_id, chat_id, message_id)

