from bot import TeleBot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def toggle_lamp_handler(teleBot: TeleBot, query_id, chat_id, message_id):
	"""
	Handler untuk tombol lampu
	"""
	if teleBot.lamp_status == 'On':
		teleBot.bot.answerCallbackQuery(query_id, text='Mematikan lampu...')
		teleBot.lamp_status = 'Off'
	else:
		teleBot.bot.answerCallbackQuery(query_id, text='Menghidupkan lampu...')
		teleBot.lamp_status = 'On'

	new_button_text: str = f'Lampu : {teleBot.lamp_status}'

	keyboard = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text=new_button_text, callback_data='toggle_lamp')],
		[InlineKeyboardButton(text='Cek Jarak', callback_data='cek_jarak')],
		[InlineKeyboardButton(text='Main Tic Tac Toe', callback_data='tic_tac_toe')]
	])
	teleBot.bot.editMessageReplyMarkup((chat_id, message_id), reply_markup=keyboard)

def cek_jarak_handler(teleBot: TeleBot, query_id, chat_id, message_id):
	"""
	Handler untuk tombol cek jarak
	"""
	teleBot.bot.answerCallbackQuery(query_id, text='Mengecek jarak...')
	teleBot.bot.editMessageText((chat_id, message_id), 'Jarak terdeteksi : .... cm')

def add_arduino_handlers(teleBot: TeleBot):
	# Menambahkan handler ke teleBot
	teleBot.add_handler('toggle_lamp', toggle_lamp_handler)
	teleBot.add_handler('cek_jarak', cek_jarak_handler)
	