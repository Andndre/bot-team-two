from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.tic_tac_toe_handlers.choose_symbol import *
from handlers.tic_tac_toe_handlers.choose_dimension import *

def level_buttons(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int, username: str, chat_type: str):
	teleBot.bot.answerCallbackQuery(query_id, text='Memulai game Tic Tac Toe')
	msg_id = (chat_id, message_id)

	buttons = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text='Easy', callback_data='easy_mode'),
		InlineKeyboardButton(text='Medium', callback_data='medium_mode'),
		InlineKeyboardButton(text='Impossible', callback_data='impossible_mode')]
	])

	teleBot.bot.editMessageText(msg_id, 'Pilih level yang kamu inginkan:')
	teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=buttons)
	
def get_level_handler(level: str):
	"""
	Mengenerate handler untuk tombol simbol (pilihan X atau O sebelum permainan)
	"""
	def handler(teleBot: TeleBot, query_id, chat_id, message_id, username, chat_type):
		# Jawab callback query dengan menampilkan informasi simbol yang dipilih
		teleBot.bot.answerCallbackQuery(query_id, text=f'Anda memilih menjadi {level}, selamat bermain!')
		# Buat game TicTacToe baru dengan simbol yang dipilih
		# Simpan game untuk digunakan di pesan yang sama
		msg_id = (chat_id, message_id)
		game: TicTacToe = TicTacToe.load(message_id)
		
		if level == 'Easy':
			game.level = 1
		elif level == 'Medium':
			game.level = 2
		elif level == 'Impossible':
			game.level = 3

		game.save()
		get_symbol_buttons(game)(teleBot, query_id, chat_id, message_id, username, chat_type)
	return handler
