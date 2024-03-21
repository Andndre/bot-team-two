from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def tic_tac_toe_handler(teleBot: TeleBot, query_id, chat_id, message_id):
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
		teleBot.bot.answerCallbackQuery(query_id, text=f'Bot berfikir...')
		game = teleBot.get_t3_game(message_id) # Mendapatkan game TicTacToe dengan message_id
		msg_id = (chat_id, message_id)
		moved = game.make_move_current(row, col)
		if moved: # Jika pergerakan valid, lanjutkan dengan pergerakan bot
			game.make_ai_move()
			if (game.game_over != 'None'):
				teleBot.bot.editMessageText(msg_id, game.get_text_game_over())
				return
		teleBot.bot.editMessageText(msg_id, game.get_text_giliran())
		teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=game.generate_markup())
	return handler

def get_symbol_handler(symbol: str):
	"""
	Mengenerate handler untuk tombol simbol (pilihan X atau O sebelum permainan)
	"""
	def handler(teleBot: TeleBot, query_id, chat_id, message_id):
		teleBot.bot.answerCallbackQuery(query_id, text=f'Anda memilih menjadi {symbol}, selamat bermain!')
		game = TicTacToe(symbol)
		msg_id = (chat_id, message_id)
		teleBot.add_t3_game(message_id, game)
		teleBot.bot.editMessageText(msg_id, game.get_text_giliran())
		teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=game.generate_markup())
	return handler

def add_tic_tac_toe_handlers(teleBot: TeleBot):
	# Menambahkan semua handler ke teleBot
	teleBot.add_handler('tic_tac_toe', tic_tac_toe_handler)
	teleBot.add_handler('symbol_x', get_symbol_handler('X'))
	teleBot.add_handler('symbol_o', get_symbol_handler('O'))
	for row in range(3):
		for col in range(3):
			teleBot.add_handler(f'pos_{row}_{col}', get_pos_handler(row, col))
