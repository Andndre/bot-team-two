from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def size_buttons(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int, user_id: int):
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
	def handler(teleBot: TeleBot, query_id, chat_id, message_id, user_id):
		# Buat game TicTacToe baru dengan ukuran board yang dipilih
		game = teleBot.get_t3_game(message_id)
		game.set_dimension(size)
		# Simpan game untuk digunakan di pesan yang sama
		msg_id = (chat_id, message_id)

		# Jika game belum selesai, edit message dengan pesan giliran
		teleBot.bot.editMessageText(msg_id, game.get_text_giliran(user_id))
		teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=game.generate_markup())

	return handler
