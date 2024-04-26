from bot import TeleBot
from handlers.tic_tac_toe_handlers.choose_mode import *
from handlers.tic_tac_toe_handlers.choose_dimension import *

def choose_player(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int, user_id: int): 
    # Tag Playernya
    msg_id = (chat_id, message_id)
    
    teleBot.bot.editMessageText(msg_id, 'Silahkan tag teman anda:')
    # Bot akan mengirim pesan Undangan
    
    # Player 2 setuju, maka game dimulai
    def on_chat_message(msg):
        content_type, chat_type, chat_id = teleBot.glance(msg)
        if content_type == 'text':
            # Check if the message is from the host
            if msg['from']['id'] == user_id:
                # Check if the message contains a username to tag
                if '@' in msg['text']:
                    # Extract the username from the message
                    tagged_username = msg['text'].split('@')[-1].strip()
                    # Check if the tagged username is valid and present in the group
                    if tagged_username in [member['username'] for member in teleBot.bot.getChatMembers(chat_id)]:
                        # Proceed to choose dimensions
                        size_buttons(teleBot, query_id, chat_id, message_id, user_id, tagged_username)
                    else:
                        # Send message informing that the username is not valid
                        teleBot.bot.sendMessage(chat_id, 'Username tidak ada pada grup ini, silahkan coba lagi')
                elif msg['text'] == 'Batal':
                    # Send cancellation message
                    teleBot.bot.sendMessage(chat_id, 'Anda telah membatalkan permainan, terima kasih sudah bermain!')
                else:
                    # Send message informing that the input is not valid
                    teleBot.bot.sendMessage(chat_id, 'Perintah tidak valid, silahkan tag teman Anda atau ketik "Batal" untuk membatalkan')
            else:
                # Send message informing that only the host can initiate the game
                teleBot.bot.sendMessage(chat_id, 'Hanya host yang dapat memulai permainan')

    teleBot.bot.message_loop({'chat': on_chat_message})
