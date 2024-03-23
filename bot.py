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
        self.distance: int = None

    def handle_message(self, msg: Dict) -> None:
        """
        Menangani pesan pada bot telegram
        """
        chat_id = msg['chat']['id']
        if (msg['text'] == '/start') or (msg['text'] == '/start@Teamtwo_bot'):
            self.bot.sendMessage(chat_id, """Untuk menggunakan Bot Tic Tac Toe, user harus mengikuti langkah-langkah berikut:
- Pertama user harus menginput  "/mulai” di Telegram.
- Kemudian, bot akan menampilkan output berupa opsi *"Main Tic Tac Toe"* yang bisa ditekan oleh user.
- Setelah itu, bot akan memberikan opsi user untuk memilih giliran bermain duluan dengan "X” atau bermain setelah bot dengan "O” .
- Terakhir, user akan bermain *Tic Tac Toe* dengan bot hingga bot mengeluarkan output "Anda Menang”, Bot Menang”, atau “Game Draw!”.""", parse_mode="Markdown")
        elif (msg['text'] == '/mulai') or (msg['text'] == '/mulai@Teamtwo_bot'):
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
        MessageLoop(self.bot, {'chat': self.handle_message, 'callback_query': self.on_callback_query}).run_as_thread()
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

