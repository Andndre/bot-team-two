from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from choose_mode import choose_mode

def level_buttons(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int, user_id: int):
	teleBot.add_t3_game(message_id, TicTacToe())

	teleBot.bot.answerCallbackQuery(query_id, text='Memulai game Tic Tac Toe')
	msg_id = (chat_id, message_id)

	buttons = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text='Easy', callback_data='easy_mode'),
		InlineKeyboardButton(text='Medium', callback_data='medium_mode'),
		InlineKeyboardButton(text='Impossible', callback_data='impossible_mode')]
	])

	teleBot.bot.editMessageText(msg_id, 'Pilih level yang kamu inginkan:')
	teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=buttons)
	
def get_level_handler(level: str):
	"""
	Mengenerate handler untuk tombol simbol (pilihan X atau O sebelum permainan)
	"""
	def handler(teleBot: TeleBot, query_id, chat_id, message_id, user_id):
		# Jawab callback query dengan menampilkan informasi simbol yang dipilih
		teleBot.bot.answerCallbackQuery(query_id, text=f'Anda memilih menjadi {level}, selamat bermain!')
		# Buat game TicTacToe baru dengan simbol yang dipilih
		# Simpan game untuk digunakan di pesan yang sama
		msg_id = (chat_id, message_id)
		game = teleBot.get_t3_game(message_id)

		if level == 'Easy':
			game.set_level(1)
		elif level == 'Medium':
			game.set_level(2)
		elif level == 'Impossible':
			game.set_level(3)
		
		choose_mode(teleBot, query_id, chat_id, message_id, user_id)
	return handler
