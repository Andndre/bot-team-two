from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def replay(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int):
	"""
	Handler untuk tombol 'Mulai Lagi'
	"""
	teleBot.bot.answerCallbackQuery(query_id, text='Memulai kembali game Tic Tac Toe')
	msg_id = (chat_id, message_id)
	buttons = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text='❌', callback_data='symbol_x'),
		InlineKeyboardButton(text='⭕️', callback_data='symbol_o')]
	])
	teleBot.bot.editMessageText(msg_id, 'Pilih simbolmu:')
	teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=buttons)

def end_game(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int):
	"""
	Handler untuk tombol 'Selesai'
	"""
	teleBot.bot.answerCallbackQuery(query_id, text='Permainan selesai')
	teleBot.bot.sendMessage(chat_id, 'Terima kasih sudah bermain, sampai jumpa!')

def get_text_game_over(self):
	"""
	Mengembalikan teks untuk kondisi akhir permainan
	"""
	if self.game_over == 'Draw':
		return 'Permainan berakhir seri!'
	else:
		winner = self.get_winner()
		return f'Pemenangnya adalah {winner}!'
# Pemanggilan fungsi di folder t3 handler
def add_tic_tac_toe_handlers(teleBot: TeleBot):
	# Menambahkan semua handler ke teleBot
	# Menambahkan handler untuk memilih simbol X (pada mulai permainan)
	teleBot.add_handler('symbol_x', get_symbol_handler('X'))
	# Menambahkan handler untuk memilih simbol O (pada mulai permainan)
	teleBot.add_handler('symbol_o', get_symbol_handler('O'))
	# Menambahkan handler untuk tombol ukuran (ukuran board)
	teleBot.add_handler('3_by_3', get_size_handler(3))
	teleBot.add_handler('4_by_4', get_size_handler(4))
	teleBot.add_handler('5_by_5', get_size_handler(5))
	# Menambahkan handler untuk pilihan multiplayer
	teleBot.add_handler('single', get_choose_mode_handler('Single Player'))
	teleBot.add_handler('duo', get_choose_mode_handler('Duo Player'))
	teleBot.add_handler('triple', get_choose_mode_handler('Multi Player'))
	# Menambahkan handler untuk pilihan posisi (dalam permainan)
	for row in range(3):
		for col in range(3):
			teleBot.add_handler(
				f'pos_{row}_{col}', get_pos_handler(row, col))
	# Menambahkan handler untuk tombol 'Mulai Lagi'
	teleBot.add_handler('replay', replay)
	# Menambahkan handler untuk tombol 'Selesai'
	teleBot.add_handler('end_game', end_game)