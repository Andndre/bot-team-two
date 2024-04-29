from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import random
import pickle
import os

class TicTacToe:
    
    def __init__(self, message_id: int):
        self.game_over = 'None'
        self.size = 0
        self.level = 1
        self.player_count = 1
        self.player_turn = 0
        self.player_emoji = ['❌', '⭕️', '🔼']
        self.player_symbols = ['X', 'O', 'Y']
        self.board: list[list[str]] = []
        self.player_tags = ['', '', '']
        self.player_tags_role = ['', '', '']
        self.message_id = message_id

    def save(self):
        # create folder
        if not os.path.exists('saved_games'):
            os.makedirs('saved_games')
        with open(f'saved_games/{self.message_id}.pickle', 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load(message_id: int):
        with open(f'saved_games/{message_id}.pickle', 'rb') as f:
            return pickle.load(f)
    
    def set_dimension(self, size: int = 3):
        self.size = size
        self.board = [[' ']*size for _ in range(size)]
    
    def get_symbol_index(self, symbol: str):
        return self.player_symbols.index(symbol)
    
    def set_symbol_player_count(self, player_count: int = 1):
        if player_count in [1, 2]:
            self.player_symbols = ['X', 'O']
            self.player_emoji = ['❌', '⭕️']

        self.player_count = player_count

    def get_current_player(self):
        return self.player_symbols[self.player_turn]

    def get_current_username(self):
        self.player_tags_role[self.player_turn]

    # TODO 
    # def set_multiplayer(self, *player_tags):
    #     self.player_tags = player_tags

    def make_random_move(self):
        (i, j) = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        self.make_move(i, j, self.get_current_player())
    
    def set_level(self, level: int):
        self.level = level

    def generate_markup(self):
        """
        Menghasilkan tombol 3x3, 4x4, atau 5x5 berisi simbol X dan O (atau dan Y) sesuai state game saat ini
        """
        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=f'{self.get_symbol_emoji_at(i, j)}', callback_data=f'pos_{i}_{j}') for j in range(self.size)
            ] for i in range(self.size)
        ])
        return buttons

    def get_text_giliran(self, username: str):
        """
        Text untuk menunjukkan giliran saat ini:
        ex. "Giliran X (Anda)"
        ex. "Giliran O (Bot)"
        """
        return f'Giliran {self.get_symbol_emoji_current(username)} @{self.player_tags_role[self.player_turn]}'
    
    def get_text_game_over(self):
        """
        Text ketika game over
        ex. "Anda menang!"
        ex. "Game Draw!"
        ex. "Bot menang!"
        """
        self.switch_player()
        if self.player_count == 3: self.switch_player()
        if self.game_over == 'Win':
            return f"@{self.player_tags_role[self.player_turn]} menang!"
        elif self.game_over == 'Draw':
            return "Game Draw!"
    
    def make_ai_move(self):
        """
        Mencari pergerakan bot dengan minimax alpha beta pruning
        dan membuat pergerakan
        """
        (i, j) = self.find_best_move()
        self.make_move(i, j, self.current_player)

    def is_winner(self, player) -> bool:
        """
        Mengecek apakah {player} menang
        """
        for i in range(self.size):
            # Horizontal    
            if all(self.board[i][j] == player for j in range(self.size)):
                return True
			# Vertikal
            if all(self.board[j][i] == player for j in range(self.size)):
                return True
		# Diagonal dari kiri atas ke kanan bawah
        if all(self.board[i][i] == player for i in range(self.size)):
            return True
		# Diagonal dari kanan atas ke kiri bawah
        return all(self.board[i][self.size - 1 - i] == player for i in range(3))
    
    def get_winner(self):
        """
        Mengembalikan player yang menang.
        None jika tidak/belum ada player yang menang
        """
        if self.is_winner(self.player1):
            return self.player1
        elif self.is_winner(self.player2):
            return self.player2
        else:
            return None
    
    def is_full(self):
        """
        Mengecek apakah semua cell tidak kosong
        """
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))
    
    def is_draw(self):
        """
        Mengecek apakah game draw/seri
        """
        return (self.get_winner() is not None) and self.is_full()

    def assign_symbol_username(self, username: str, symbol: str):
        index = self.get_symbol_index(symbol)
        self.player_tags.append(username)
        self.player_tags_role[index] = username

    def make_move(self, row, col) -> bool:
        """
        Membuat pergerakan untun {player} pada cell (row, col).
        Mengembalikan True jika pergerakan valid, False jika tidak
        """

        symbol = self.player_symbols[self.player_turn]
        self.switch_player()

        # Cek apakah posisi yang dipilih kosong
        if self.board[row][col] == ' ':
            # Jika kosong isi dengan simbol player
            # Jika kosong isi dengan simbol player
            self.board[row][col] = symbol
            # Cek apakah player menang
            win = self.is_winner(symbol)
            if win:
                # Jika menang, game over
                self.game_over = 'Win'
                # Return True untuk menunjukkan pergerakan valid
                return True
            # Cek apakah board penuh
            elif self.is_full():
                # Jika board penuh, game draw
                self.game_over = 'Draw'
                # Return True untuk menunjukkan pergerakan valid
                return True
            # Switch player jika pergerakan valid (dan belum menang/belum penuh)
            self.switch_player()
            # Return True untuk menunjukkan pergerakan valid
            return True
        # Return False jika pergerakan tidak valid
        return False
    
    def get_symbol_emoji_current(self, username: str):
        """
        Mendapatkan emoji simbol player saat ini
        """
        index = self.player_tags_role.index(username)
        return self.player_emoji[index]
        
    def get_symbol_emoji_at(self, row, col):
        """
        Mendapatkan emoji simbol pada cell (row, col).
        "." jika cell (row, col) kosong
        """
        if self.board[row][col] == 'X':
            return '❌'
        elif self.board[row][col] == 'O':
            return '⭕️'
        elif self.board[row][col] == 'Y':
            return '🔼'
        else:
            return '.'

    
    def make_move_current(self, row, col):
        """
        Membuat pergerakan player saat ini pada cell (row, col)
        """
        return self.make_move(row, col)

    def switch_player(self):
        self.player_turn += 1
        if self.player_turn == self.player_count:
            self.player_turn = 0
        
    # Level Imposible
    def minimax(self, depth, alpha, beta, is_maximizing):
        """
        Algoritma minimax untuk mencari pergerakan yang paling optimal
        pada game Tic-Tac-Toe. Algoritma ini menggunakan
        alpha-beta pruning untuk meningkatkan kecepatan pencarian.

        Returns:
            Score yang didapat dari fase pencarian tersebut. Score yang lebih
            tinggi untuk player bot, dan score yang lebih rendah untuk player
            pemain.
        """

        # Cek apakah ada pemenang
        winner = self.get_winner()
        if winner:
            # Jika pemenang adalah player bot, maka nilai scorenya diubah menjadi
            # 10 - depth, yang artinya lebih tinggi daripada score lainnya.
            # Jika pemenang adalah player pemain, maka nilai scorenya diubah menjadi
            # depth - 10, yang artinya lebih rendah daripada score lainnya.
            if winner == self.bot_symbol:
                return 10 - depth
            else:
                return depth - 10
        elif self.is_full():
            # Jika board penuh, maka scorenya 0
            return 0
        
        # Jika board masih ada cell yang kosong dan belum ada pemenang,
        # maka algoritma akan melanjutkan pencarian.
        
        # Jika fase pencarian ini untuk player bot
        if is_maximizing:
            # Membuat variabel untuk menyimpan score terbaik dari fase pencarian
            best_score = -float('inf')
            # Mencari semua kemungkinan pergerakan player bot
            for i in range(3):
                # Mencari semua cell yang masih kosong pada baris i
                breaking = False
                for j in range(3):
                    # Jika cell (i, j) masih kosong
                    if self.board[i][j] == ' ':
                        # Membuat pergerakan pada cell tersebut
                        self.board[i][j] = self.bot_symbol
                        # Mencari score pada fase pencarian berikutnya
                        score = self.minimax(depth + 1, alpha, beta, False)
                        # Mengembalikan pergerakan pada cell tersebut
                        self.board[i][j] = ' '
                        # Mengupdate score terbaik dari fase pencarian ini
                        best_score = max(score, best_score)
                        # Mengupdate nilai alpha untuk menghemat waktu pencarian
                        alpha = max(alpha, score)
                        # Cek apakah beta sudah lebih kecil dari alpha,
                        # jika ya maka break dari loop
                        if beta <= alpha:
                            breaking = True
                            break
                # Break dari loop jika breaking == True
                if breaking:
                    break
            # Mengembalikan score terbaik dari fase pencarian ini
            return best_score
        
        # Jika fase pencarian ini untuk player pemain
        # Membuat variabel untuk menyimpan score terrendah dari fase pencarian
        best_score = float('inf')
        # Mencari semua kemungkinan pergerakan player pemain
        for i in range(3):
            # Mencari semua cell yang masih kosong pada baris i
            breaking = False
            for j in range(3):
                # Jika cell (i, j) masih kosong
                if self.board[i][j] == ' ':
                    # Membuat pergerakan pada cell tersebut
                    self.board[i][j] = self.choose_symbol
                    # Mencari score pada fase pencarian berikutnya
                    score = self.minimax(depth + 1, alpha, beta, True)
                    # Mengembalikan pergerakan pada cell tersebut
                    self.board[i][j] = ' '
                    # Mengupdate score terrendah
                    best_score = min(score, best_score)
                    # Mengupdate nilai beta
                    beta = min(beta, score)
                    # Cek apakah beta sudah lebih kecil dari alpha,
                    # jika ya maka break dari loop pergerakan player pemain
                    if beta <= alpha:
                        breaking = True
                        break
            # Break dari loop jika breaking == True
            if breaking:
                break
        # Mengembalikan score terrendah
        return best_score

    def find_best_move(self):
        """
        Mengecek semua kemungkinan pergerakan player bot dengan Minimax,
        dan mengembalikan pergerakan yang paling optimal (dengan score paling tinggi)
        """
        # Variabel untuk menyimpan pergerakan yang paling optimal (dengan score paling tinggi)
        best_move = (-1, -1)
        # Variabel untuk menyimpan score terendah dari semua pergerakan player bot
        best_score = -float('inf')
        # Mencari semua kemungkinan pergerakan player bot
        for i in range(3):
            # Mencari semua cell yang masih kosong pada baris i
            for j in range(3):
                # Jika cell (i, j) masih kosong
                if self.board[i][j] == ' ':
                    # Membuat pergerakan pada cell tersebut
                    self.board[i][j] = self.bot_symbol
                    # Mencari score pada fase pencarian berikutnya
                    score = self.minimax(0, -float('inf'), float('inf'), False)
                    # Mengembalikan pergerakan pada cell tersebut
                    self.board[i][j] = ' '
                    # Jika score dari pergerakan tersebut lebih tinggi dari best_score
                    if score > best_score:
                        # Update best_score dengan score tersebut
                        best_score = score
                        # Update best_move dengan pergerakan tersebut
                        best_move = (i, j)
        # Mengembalikan pergerakan yang paling optimal (dengan score paling tinggi)
        return best_move
