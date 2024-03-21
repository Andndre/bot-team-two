# Telegram Bot Team 2

## How to run
```bash
cp .env.example .env
```

Ubah `TOKEN` dengan token bot telegram

```bash
python main.py
```

## Project structure:
```bash
BOT_PROJECT
│   .env								# Environment variable
│   .env.example						# Environment variable example
│   .gitignore 							# Git ignore
│   bot.py 								# Bot
│   main.py								# Main
│   README.md	
│   tic_tac_toe.py 						# Game Logic
│
├───handlers 							# Handlers (tombol click)
│   │		arduino.py 					# Arduino Handler
│   │   t3_handler.py					# Tic Tac Toe Handler
```
