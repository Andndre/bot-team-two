from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import random

class TicTacToe:
    def __init__(self, choose_symbol: str):
        self.board = [[' ']*3 for _ in range(3)]
        self.player1 = 'X'
        self.player2 = 'O'
        self.current_player = self.player1
        self.game_over = 'None'
        self.choose_symbol = choose_symbol
        self.bot_symbol = 'X' if choose_symbol == 'O' else 'O'
        if choose_symbol == 'O':
            # Bot berjalan pertama
            # self.make_ai_move() -> Akan menghasilkan pergerakan di (0, 0)
            # Untuk mempersingkat waktu:
            self.make_move(0, 0, self.bot_symbol)
    
    def generate_markup(self):
        """
        Menghasilkan tombol 3x3 berisi simbol X dan O sesuai state game saat ini
        """
        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=f'{self.get_symbol_emoji_at(i, j)}', callback_data=f'pos_{i}_{j}') for j in range(3)
            ] for i in range(3)
        ])
        return buttons

    def get_text_giliran(self):
        """
        Text untuk menunjukkan giliran saat ini:
        ex. "Giliran X (Anda)"
        ex. "Giliran O (Bot)"
        """
        return f'Giliran {self.get_symbol_emoji_current()} {"(Anda)" if self.choose_symbol == self.current_player else "(Bot)"}'
    
    def get_text_game_over(self):
        """
        Text ketika game over
        ex. "Anda menang!"
        ex. "Game Draw!"
        ex. "Bot menang!"
        """
        if self.game_over == 'Win':
            return "Anda menang!" if self.current_player == self.choose_symbol else "Bot menang!"
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
        for i in range(3):
            # Horizontal
            if all(self.board[i][j] == player for j in range(3)):
                return True
			# Vertikal
            if all(self.board[j][i] == player for j in range(3)):
                return True
		# Diagonal dari kiri atas ke kanan bawah
        if all(self.board[i][i] == player for i in range(3)):
            return True
		# Diagonal dari kanan atas ke kiri bawah
        return all(self.board[i][2-i] == player for i in range(3))
    
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

    def make_move(self, row, col, player) -> bool:
        """
        Membuat pergerakan untun {player} pada cell (row, col).
        Mengembalikan True jika pergerakan valid, False jika tidak
        """

        # Cek apakah posisi yang dipilih kosong
        if self.board[row][col] == ' ':
            # Jika kosong isi dengan simbol player
            self.board[row][col] = player
            win = self.is_winner(self.current_player)
            if win:
                self.game_over = 'Win'
                return True
            elif self.is_full():
                self.game_over = 'Draw'
                return True
            self.switch_player()
            return True
        return False
    
    def get_symbol_emoji_current(self):
        """
        Mendapatkan emoji simbol player saat ini
        """
        if self.current_player == self.player1:
            return '❌'
        else:
            return '⭕️'
    
    def get_symbol_emoji_at(self, row, col):
        """
        Mendapatkan emoji simbol pada cell (row, col).
        "." jika cell (row, col) kosong
        """
        if self.board[row][col] == self.player1:
            return '❌'
        elif self.board[row][col] == self.player2:
            return '⭕️'
        else:
            return '.'
    
    def make_move_current(self, row, col):
        """
        Membuat pergerakan player saat ini pada cell (row, col)
        """
        return self.make_move(row, col, self.current_player)

    def switch_player(self):
        """
        Mengganti current_player ke player lain
        """
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
    
    def get_opponent(self):
        """
        Mendapatkan player lawan dari current_player
        """
        return self.player2 if self.current_player == self.player1 else self.player1

    def minimax(self, depth, alpha, beta, is_maximizing):
        """
        Algoritma minimax, untuk mencari pergerakan yang paling optimal
        """

        # Cek apakah ada pemenang
        winner = self.get_winner()
        if winner:
            if winner == self.bot_symbol:
                return 10 - depth # Mengurangi depth jika player bot menang
            else:
                return depth - 10 # Mengurangi depth jika player pemain menang
        elif self.is_full():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                breaking = False
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.bot_symbol
                        score = self.minimax(depth + 1, alpha, beta, False)
                        self.board[i][j] = ' '
                        best_score = max(score, best_score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            breaking = True
                            break
                if breaking:
                    break
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                breaking = False
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.choose_symbol
                        score = self.minimax(depth + 1, alpha, beta, True)
                        self.board[i][j] = ' '
                        best_score = min(score, best_score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            breaking = True
                            break
                if breaking:
                    break
            return best_score

    def find_best_move(self):
        """
        Mengecek semua kemungkinan pergerakan player bot dengan Minimax,
        dan mengembalikan pergerakan yang paling optimal (dengan score paling tinggi)
        """
        best_move = (-1, -1)
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.bot_symbol
                    score = self.minimax(0, -float('inf'), float('inf'), False)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move
