from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def get_symbol_buttons(game: TicTacToe):
	def symbol_buttons(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int, username: int, chat_type: str):
		teleBot.bot.answerCallbackQuery(query_id, text='Memulai game Tic Tac Toe')
		msg_id = (chat_id, message_id)

		buttons = []
		current_players = ''

		all_buttons = [[InlineKeyboardButton(text='❌', callback_data='symbol_x')], 
			[InlineKeyboardButton(text='⭕️', callback_data='symbol_o')],
			[InlineKeyboardButton(text='🔼', callback_data='symbol_y')],]

		for i in range(max(game.player_count, 2)):
			if game.player_tags_role[i] == '':
				buttons.append(all_buttons[i])
			else:
				current_players += '- @' + game.player_tags_role[i] + f' sebagai {game.player_symbols[i]}\n'

		inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

		teleBot.bot.editMessageText(msg_id, 'Pilih simbolmu:\n' + current_players)
		teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=inline_keyboard)
	return symbol_buttons
	
def get_symbol_handler(symbol: str):
	"""
	Mengenerate handler untuk tombol simbol (pilihan X atau O sebelum permainan)
	"""
	def handler(teleBot: TeleBot, query_id, chat_id, message_id, username, chat_type):
		# Jawab callback query dengan menampilkan informasi simbol yang dipilih
		teleBot.bot.answerCallbackQuery(query_id, text=f'Anda memilih menjadi {symbol}, selamat bermain!')
		# Buat game TicTacToe baru dengan simbol yang dipilih
		game: TicTacToe = TicTacToe.load(message_id)
		msg_id = (chat_id, message_id)
		print('Hello')
		if game.player_tags_role[game.player_symbols.index(symbol)] == '':
			print(game.player_symbols.index(symbol))
			game.assign_symbol_username(username, symbol)
			game.save()
			if game.player_count == 1:
				print('AI MOVE')
				if game.get_current_username() == 'Bot':
					game.make_ai_move()
				game.save()
				teleBot.bot.editMessageText(msg_id, game.get_text_giliran())
				teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=game.generate_markup())
				return
			for i in range(max(game.player_count, 2)):
				if game.player_tags_role[i] == '':
					get_symbol_buttons(game)(teleBot, query_id, chat_id, message_id, username, chat_type)
					return
			
			teleBot.bot.editMessageText(msg_id, game.get_text_giliran())
			teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=game.generate_markup())
	return handler
