from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

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
            self.make_ai_move()
    
    def generate_markup(self):
        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=f'{self.get_symbol_emoji_at(i, j)}', callback_data=f'pos_{i}_{j}') for j in range(3)
            ] for i in range(3)
        ])
        return buttons
    
    def make_ai_move(self):
        (i, j) = self.find_best_move()
        self.make_move(i, j, self.bot_symbol)

    def is_winner(self, player) -> bool:
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
        if self.is_winner(self.player1):
            return self.player1
        elif self.is_winner(self.player2):
            return self.player2
        else:
            return None
    
    def is_full(self):
        # cek apakah semua cell tidak kosong 
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))
    
    def is_draw(self):
        return (self.get_winner() is not None) and self.is_full()

    def make_move(self, row, col, player):
        #cek apakah posisi yang dipilih kosong
        if self.board[row][col] == ' ':
            #jika kosong isi dengan simbol player
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

    def reset_game(self):
        self.board = [[' ']*3 for _ in range(3)]
    
    def get_symbol_emoji_current(self):
        if self.current_player == self.player1:
            return '❌'
        else:
            return '⭕️'
    
    def get_symbol_emoji_at(self, row, col):
        if self.board[row][col] == self.player1:
            return '❌'
        elif self.board[row][col] == self.player2:
            return '⭕️'
        else:
            return '.'
    
    def make_move_current(self, row, col):
        return self.make_move(row, col, self.current_player)

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def minimax(self, depth, is_maximizing):
        if self.is_winner(self.player1):
            return -10 + depth
        elif self.is_winner(self.player2):
            return 10 - depth
        elif self.is_full():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':#cek kotak kosong
                        self.board[i][j] = self.player2
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.player1
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def find_best_move(self):
        best_move = (-1, -1)
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.current_player
                    score = self.minimax(0, False)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move