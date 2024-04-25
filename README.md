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
│   .env               # Environment variable
│   .env.example       # Environment variable example
│   .gitignore         # Git ignore
│   bot.py             # Bot
│   main.py            # Main
│   README.md
│   tic_tac_toe.py     # Game Logic
│
├───handlers           # Handlers (tombol click)
│   │   arduino.py     # Arduino Handler
│   │   t3_handler.py  # Tic Tac Toe Handler
```

# Tugas Tambahan
1. Levelling 
Tingkat kesulitan untuk Singleplayer Mode
- Easy -> Pake sistem random position agar bot terkesan mudah
- Medium -> gunakan algoritma namun tingkat kedalaman dikurangi
- Hard -> Settingan bot sebelumnya
2. Multiplayer
- Ada pilihan duo player, triple player
- Penentuan icon Role masing-masing player (Bulat, Silang, Segitiga)
- Seoarang Player dikatakan Menang jika 3 icon role yang sama tersusun secara vertikal/horizontal/diagonal
- Draw jika tidak ada yang menang/memenuhi syarat menang
- (Jika memungkinkan) ada sistem skor, skor akan direset jika selesai bermain saja, skor tidak direset jika hanya replay game saja
3. Atur dimensi -> sebelum pemilihan mark (O atau X) 3x3 4x4 5x5 (sudah)
4. Sistem retry/replay setelah selesai bermain dan berhenti bermain (sudah)

Gameplay Singleplayer
Start > Tic Tac Toe > Singleplayer > (3x3) / (4x4) / (5x5) > Pilih level (Easy, Medium, Hard) > (Mulai Bermain) > Retry/End Game

Gameplay Multiplayer1
Start > Tic Tac Toe > Multiplayer (2 Pemain) / Multiplayer (3 Pemain) > (Tag Player Pemainnya siapa saja) > (3x3) / (4x4) / (5x5) > (Mulai Bermain) > Retry/End Game

Alur Kode:
Start -> Show_intro -> choose_mode -> 


Syarat Khusus Multiplayer 3 Pemain:
- Tidak bisa memakai dimensi 3x3


