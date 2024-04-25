from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.tic_tac_toe_handlers.choose_dimension import *

def choose_mode(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int, user_id: int): 
	msg_id = (chat_id, message_id)

	buttons = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text='Single Player', callback_data='single'),
		InlineKeyboardButton(text='Duo Player', callback_data='duo'),
  		InlineKeyboardButton(text='Triple Player', callback_data='triple')]
	])
 
	teleBot.bot.editMessageText(msg_id, 'Pilih Mode:')
	teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=buttons)

def get_choose_mode_handler(jumlah_player: int):
	def handler(teleBot: TeleBot, query_id, chat_id, message_id, user_id):
		teleBot.bot.answerCallbackQuery(query_id, text='Mode: ' + str(jumlah_player) + ' player')
		game = teleBot.get_t3_game(message_id)
		msg_id = (chat_id, message_id)
		if jumlah_player == 1:
			game.set_symbol_player_count(1)
			size_buttons(teleBot, query_id, chat_id, message_id, user_id)
		if jumlah_player == 2:
			game.set_symbol_player_count(2)
			teleBot.bot.editMessageText(msg_id, 'Tag lawan Anda!')
			teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=None)
		if jumlah_player == 3:
			game.set_symbol_player_count(3)
			# TODO: tampilan untuk multi player		
		
	return handler
