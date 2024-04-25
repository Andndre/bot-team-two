from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def size_buttons(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int):
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
	def handler(teleBot: TeleBot, query_id, chat_id, message_id):
		# Buat game TicTacToe baru dengan ukuran board yang dipilih
		game = TicTacToe(size)
		# Simpan game untuk digunakan di pesan yang sama
		msg_id = (chat_id, message_id)
		game = teleBot.get_t3_game(message_id, game)
		# Edit reply markup untuk menampilkan board awal
		if size == 3:
			game.set_dimension(3)
		elif size == 4:
			game.set_dimension(4)
		elif size == 5:
			game.set_dimension(5)

		teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=game.generate_markup())

	return handler
