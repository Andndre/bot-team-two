from tic_tac_toe import TicTacToe
from bot import TeleBot

def play_again_handler(teleBot: TeleBot, query_id, chat_id, message_id, username, chat_type):
	game: TicTacToe = TicTacToe.load(message_id)
	game.reset_board()
	game.save()
	teleBot.bot.editMessageText((chat_id, message_id), game.get_text_giliran())
	teleBot.bot.editMessageReplyMarkup((chat_id, message_id), reply_markup=game.generate_markup())
