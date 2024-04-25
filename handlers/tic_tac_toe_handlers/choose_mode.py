from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from choose_dimension import size_buttons

def choose_mode(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int): 
	msg_id = (chat_id, message_id)

	buttons = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text='Single Player', callback_data='single'),
		InlineKeyboardButton(text='Duo Player', callback_data='duo'),
  		InlineKeyboardButton(text='Tripe Player', callback_data='triple')]
	])
 
	teleBot.bot.editMessageText(msg_id, 'Pilih Mode:')
	teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=buttons)

def get_choose_mode_handler(mode):
	def handler(teleBot: TeleBot, query_id, chat_id, message_id):
		teleBot.bot.answerCallbackQuery(query_id, text='Mode: ' + mode)
		game = teleBot.get_t3_game(message_id)
		if mode == 'Single Player':
			game.set_symbol_player_count(1)
			size_buttons(teleBot, query_id, chat_id, message_id)
		if mode == 'Duo Player':
			game.set_symbol_player_count(2)
			# TODO: tampilan untuk multi player, lanjut ke Choose Player
		if mode == 'Triple Player':
			game.set_symbol_player_count(3)
			# TODO: tampilan untuk multi player		
		
	return handler
