from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def tic_tac_toe_handler(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int):
	"""
	Handler untuk tombol memulai game Tic Tac Toe
	"""
	teleBot.bot.answerCallbackQuery(query_id, text='Memulai game Tic Tac Toe')
	msg_id = (chat_id, message_id)

	buttons = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text='❌', callback_data='symbol_x'),
		InlineKeyboardButton(text='⭕️', callback_data='symbol_o')]
	])

	teleBot.bot.editMessageText(msg_id, 'Pilih simbolmu:')
	teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=buttons)

def get_pos_handler(row, col):
	"""
	Mengenerate handler untuk tombol posisi (row, col)
	"""
	def handler(teleBot: TeleBot, query_id, chat_id, message_id):
		"""
		Jawab callback query dari tombol posisi dan proses pergerakan
		"""
		# Mendapatkan game TicTacToe dengan message_id
		game = teleBot.get_t3_game(message_id)
		# Abaikan klik jika game sudah selesai
		if game.game_over != 'None':
			return

		msg_id = (chat_id, message_id)
		moved = game.make_move_current(row, col)
		if moved: # Jika pergerakan valid, lanjutkan dengan pergerakan bot
			teleBot.bot.answerCallbackQuery(query_id, text='Bot berfikir...')
			game.make_ai_move()
			if (game.game_over != 'None'): # Cek apakah game sudah selesai
				# Edit message dengan pesan game over dan hapus reply markup
				teleBot.bot.editMessageText(msg_id, game.get_text_game_over())
				teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=game.generate_markup())
				return
			# Jika game belum selesai, edit message dengan pesan giliran
			teleBot.bot.editMessageText(msg_id, game.get_text_giliran())
			# Edit reply markup untuk menampilkan board baru
			teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=game.generate_markup())
	return handler
def get_symbol_handler(symbol: str):
	"""
	Mengenerate handler untuk tombol simbol (pilihan X atau O sebelum permainan)
	"""
	def handler(teleBot: TeleBot, query_id, chat_id, message_id):
		# Jawab callback query dengan menampilkan informasi simbol yang dipilih
		teleBot.bot.answerCallbackQuery(query_id, text=f'Anda memilih menjadi {symbol}, selamat bermain!')
		# Buat game TicTacToe baru dengan simbol yang dipilih
		game = TicTacToe(symbol)
		# Simpan game untuk digunakan di pesan yang sama
		msg_id = (chat_id, message_id)
		teleBot.add_t3_game(message_id, game)
		# Edit pesan untuk menampilkan pesan giliran
		teleBot.bot.editMessageText(msg_id, game.get_text_giliran())
		# Edit reply markup untuk menampilkan board awal
		teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=game.generate_markup())
	return handler

def add_tic_tac_toe_handlers(teleBot: TeleBot):
	# Menambahkan semua handler ke teleBot
	# Menambahkan handler untuk memulai permainan Tic Tac Toe
	teleBot.add_handler('tic_tac_toe', tic_tac_toe_handler)
	# Menambahkan handler untuk memilih simbol X (pada mulai permainan)
	teleBot.add_handler('symbol_x', get_symbol_handler('X'))
	# Menambahkan handler untuk memilih simbol O (pada mulai permainan)
	teleBot.add_handler('symbol_o', get_symbol_handler('O'))
	# Menambahkan handler untuk pilihan posisi (dalam permainan)
	for row in range(3):
		for col in range(3):
			teleBot.add_handler(
				f'pos_{row}_{col}', get_pos_handler(row, col))
