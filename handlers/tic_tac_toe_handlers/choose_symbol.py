from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def get_symbol_buttons(jumlah_player: int):
	def symbol_buttons(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int, username: int):
		teleBot.add_t3_game(message_id, TicTacToe())

		teleBot.bot.answerCallbackQuery(query_id, text='Memulai game Tic Tac Toe')
		msg_id = (chat_id, message_id)

		if jumlah_player == 1 or jumlah_player == 2:
			buttons = InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text='❌', callback_data='symbol_x'),
				InlineKeyboardButton(text='⭕️', callback_data='symbol_o')]
			])
		elif jumlah_player == 3:
			buttons = InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text='❌', callback_data='symbol_x'),
				InlineKeyboardButton(text='⭕️', callback_data='symbol_o')],
				[InlineKeyboardButton(text='🔼', callback_data='symbol_segitiga')],
				InlineKeyboardButton(text='Lanjutkan', callback_data='lanjut_symbol')
			])

		teleBot.bot.editMessageText(msg_id, 'Pilih simbolmu:')
		teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=buttons)
	return symbol_buttons
	
def get_symbol_handler(symbol: str):
	"""
	Mengenerate handler untuk tombol simbol (pilihan X atau O sebelum permainan)
	"""
	def handler(teleBot: TeleBot, query_id, chat_id, message_id, username):
		# Jawab callback query dengan menampilkan informasi simbol yang dipilih
		teleBot.bot.answerCallbackQuery(query_id, text=f'Anda memilih menjadi {symbol}, selamat bermain!')
		# Buat game TicTacToe baru dengan simbol yang dipilih
		game = teleBot.get_t3_game(message_id)
		msg_id = (chat_id, message_id)
		
		if game.player_count == 1:
			game.assign_symbol_username(username, symbol)
			# Simpan game untuk digunakan di pesan yang sama
			# Edit pesan untuk menampilkan pesan giliran
			teleBot.bot.editMessageText(msg_id, game.get_text_giliran(username))
			# Edit reply markup untuk menampilkan board awal
			teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=game.generate_markup())
		else:
			teleBot.bot.answerCallbackQuery(query_id, text='TODO: Fitur belum dibuat')
	return handler
