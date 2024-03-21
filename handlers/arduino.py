from bot import TeleBot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from serial import Serial
import time

ser = Serial("COM3", 9600)

def toggle_lamp_handler(teleBot: TeleBot, query_id, chat_id, message_id):
	"""
	Handler untuk tombol lampu
	"""
	global ser
	if teleBot.lamp_status == 'On':
		teleBot.bot.answerCallbackQuery(query_id, text='Mematikan lampu...')
		teleBot.lamp_status = 'Off'
		ser.write(b'2\n')
		time.sleep(1)
	else:
		teleBot.bot.answerCallbackQuery(query_id, text='Menghidupkan lampu...')
		teleBot.lamp_status = 'On'
		ser.write(b'1\n')
		time.sleep(1)

	new_button_text: str = f'Lampu : {teleBot.lamp_status}'

	jarak = teleBot.distance

	keyboard = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text=new_button_text, callback_data='toggle_lamp')],
		[InlineKeyboardButton(text=f'Cek Jarak (saat ini: {jarak} cm)' if jarak is not None else 'Cek Jarak', callback_data='cek_jarak')],
		[InlineKeyboardButton(text='Main Tic Tac Toe', callback_data='tic_tac_toe')]
	])
	teleBot.bot.editMessageReplyMarkup((chat_id, message_id), reply_markup=keyboard)

def cek_jarak_handler(teleBot: TeleBot, query_id, chat_id, message_id):
	"""
	Handler untuk tombol cek jarak
	"""
	global ser
	teleBot.bot.answerCallbackQuery(query_id, text='Mengecek jarak...')
	ser.write(b'j\n')
	time.sleep(1)
	response = ser.readline().decode().strip()
	teleBot.distance = int(response)
	keyboard = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text=f"Lampu: {teleBot.lamp_status}", callback_data='toggle_lamp')],
		[InlineKeyboardButton(text=f'Cek Jarak (saat ini: {response} cm)', callback_data='cek_jarak')],
		[InlineKeyboardButton(text='Main Tic Tac Toe', callback_data='tic_tac_toe')]
	])
	teleBot.bot.editMessageReplyMarkup((chat_id, message_id), reply_markup=keyboard)

def add_arduino_handlers(teleBot: TeleBot):
	# Menambahkan handler ke teleBot
	teleBot.add_handler('toggle_lamp', toggle_lamp_handler)
	teleBot.add_handler('cek_jarak', cek_jarak_handler)
	