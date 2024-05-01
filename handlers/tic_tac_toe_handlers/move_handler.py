from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import time

def get_move_handler(row, col):
	"""
	Mengenerate handler untuk tombol posisi (row, col)
	"""
	def handler(teleBot: TeleBot, query_id, chat_id, message_id, username, chat_type):
		"""
		Jawab callback query dari tombol posisi dan proses pergerakan
		"""
		# Mendapatkan game TicTacToe dengan message_id
		game: TicTacToe = TicTacToe.load(message_id)
		# Abaikan klik jika game sudah selesai
		if game.game_over != 'None':
			return

		time.sleep(1)

		# Abaikan klik jika giliran bukan player
		if game.get_current_username() != username:
			return

		msg_id = (chat_id, message_id)
		moved = game.make_move_current(row, col)
		if moved: # Jika pergerakan valid, lanjutkan dengan pergerakan bot
			if game.game_over == 'None' and game.get_current_username() == 'Bot': # Jika pergerakan valid, lanjutkan dengan pergerakan bot
				teleBot.bot.answerCallbackQuery(query_id, text='Bot berfikir...')
				game.make_ai_move()
			game.save()
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
