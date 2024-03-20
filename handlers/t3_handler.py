from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def tic_tac_toe_handler(teleBot: TeleBot, query_id, chat_id, message_id):
	teleBot.bot.answerCallbackQuery(query_id, text='Memulai game Tic Tac Toe')

	buttons = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text='❌', callback_data='symbol_x'),
		InlineKeyboardButton(text='⭕️', callback_data='symbol_o')]
	])

	teleBot.bot.editMessageText((chat_id, message_id), 'Pilih simbolmu:')
	teleBot.bot.editMessageReplyMarkup((chat_id, message_id), reply_markup=buttons)

def symbol_handler(teleBot: TeleBot, query_id, chat_id, message_id, symbol):
	teleBot.bot.answerCallbackQuery(query_id, text=f'Anda memilih menjadi {symbol}, selamat bermain!')
	game = TicTacToe(symbol)
	teleBot.add_t3_game(message_id, game)
	teleBot.bot.editMessageText((chat_id, message_id), f'Giliran {game.get_symbol_emoji_current()}')
	teleBot.bot.editMessageReplyMarkup((chat_id, message_id), reply_markup=game.generate_markup())

def get_pos_handler(row, col):
	def handler(teleBot: TeleBot, query_id, chat_id, message_id):
		teleBot.bot.answerCallbackQuery(query_id, text=f'Bot berfikir...')
		game = teleBot.get_t3_game(message_id)
		moved = game.make_move_current(row, col)
		if moved:
			game.make_ai_move()
			if (game.game_over != 'None'):
				if game.game_over == 'Win':
					teleBot.bot.editMessageText((chat_id, message_id), "Anda menang!" if game.current_player == game.choose_symbol else "Bot menang!")
					return
				elif game.game_over == 'Draw':
					teleBot.bot.editMessageText((chat_id, message_id), "Game Draw!")
					return
		teleBot.bot.editMessageText((chat_id, message_id), f'Giliran {game.get_symbol_emoji_current()} {"(Anda)" if game.choose_symbol == game.current_player else "(Bot)"}')
		teleBot.bot.editMessageReplyMarkup((chat_id, message_id), reply_markup=game.generate_markup())
	return handler

def symbol_x_handler(teleBot: TeleBot, query_id, chat_id, message_id):
	symbol_handler(teleBot, query_id, chat_id, message_id, 'X')
def symbol_o_handler(teleBot: TeleBot, query_id, chat_id, message_id):
	symbol_handler(teleBot, query_id, chat_id, message_id, 'O')

def add_tic_tac_toe_handlers(teleBot: TeleBot):
	teleBot.add_handler('tic_tac_toe', tic_tac_toe_handler)
	teleBot.add_handler('symbol_x', symbol_x_handler)
	teleBot.add_handler('symbol_o', symbol_o_handler)
	for row in range(3):
		for col in range(3):
			teleBot.add_handler(f'pos_{row}_{col}', get_pos_handler(row, col))
