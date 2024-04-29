from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.tic_tac_toe_handlers.choose_level import *

def size_buttons(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int, username: str):
	"""
	Menambahkan handler untuk tombol ukuran (ukuran board)
	"""
	# Menambahkan handler untuk tombol ukuran (ukuran board)

	teleBot.bot.answerCallbackQuery(query_id, text='Pilih ukuran board:')
	msg_id = (chat_id, message_id)

	buttons = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text='3 x 3', callback_data='3_by_3'),
		InlineKeyboardButton(text='4 x 4', callback_data='4_by_4'),
		InlineKeyboardButton(text='5 x 5', callback_data='5_by_5')]
	])

	teleBot.bot.editMessageText(msg_id, 'Pilih ukuran board:')
	teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=buttons)

def get_size_handler(size: int):
	"""
	Mengenerate handler untuk tombol ukuran (ukuran board)
	"""
	def handler(teleBot: TeleBot, query_id, chat_id, message_id, username):
		# Buat game TicTacToe baru dengan ukuran board yang dipilih
		game: TicTacToe = TicTacToe.load(message_id)
		game.set_dimension(size)
		game.save()

		# Jika game belum selesai, edit message dengan pesan giliran
		level_buttons(teleBot, query_id, chat_id, message_id, username)

	return handler
