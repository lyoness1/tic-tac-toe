class Player(object):

    def __init__(self, char, opponent=None):
        self.char = char
        self.opponent = opponent


class Board(object):

    def __init__(self, game):
        self.game = game
        self.cells = [[".", ".", "."] for _ in xrange(3)]
        self.num_moves = 0

    def is_full(self):
        if self.num_moves == 9:
            return True
        return False

    def place_move(self, player, row, col):
        self.cells[row][col] = player.char
        self.num_moves += 1
        return self

    def check_condition(self):
        if self.is_full():
            raise GameTieException()
        elif self.check_rows() or self.check_cols() or self.check_diags():
            raise GameWinException()

    def check_rows(self):
        for row in self.cells:
            out = ""
            for cell in row:
                out += cell
            if out == "XXX" or out == "OOO":
                return True

    def check_cols(self):
        for i in xrange(3):
            out = self.cells[0][i] + self.cells[1][i] + self.cells[2][i]
            if out == "XXX" or out == "OOO":
                return True

    def check_diags(self):
        if (self.cells[0][0] + self.cells[1][1] + self.cells[2][2] == "XXX" or
            self.cells[0][2] + self.cells[1][1] + self.cells[2][0] == "XXX" or
            self.cells[0][0] + self.cells[1][1] + self.cells[2][2] == "OOO" or
            self.cells[0][2] + self.cells[1][1] + self.cells[2][0] == "OOO"):
            return True


    def show(self):
        rows = ["A", "B", "C"]
        cols = ["1", "2", "3"]

        print "\n"
        print " ",
        for col in cols:
            print col,
        for i, row in enumerate(self.cells):
            print "\n"
            print rows[i], 
            for cell in row:
                print cell,


class Game(object):

    def __init__(self):
        self.player_X = Player("X")
        self.player_O = Player("O", self.player_X)
        self.player_X.opponent = self.player_O
        self.board = Board(self)
        self.curr_player = self.player_X

    def get_move(self):
        while True:
            try:
                move = raw_input("\n\nPlayer " +
                                 self.curr_player.char +
                                 ", enter a move ('row col', like 'C2'): ")

                row = ord(move[0].upper()) - ord('A') # A->0, B->1, etc.
                col = int(move[1]) - 1

                if self.board.cells[row][col] == ".":
                    return row, col
                else:
                    print "\nSquare is already taken. Try again."
                    self.board.show()

            except (IndexError, EOFError) as e: 
                print "\n%s: Try again.\n" % e
                self.board.show()

    def play(self):
        try:
            while True:
                self.board.show()
                row, col = self.get_move()
                self.board.place_move(self.curr_player, row, col).check_condition()
                # player is only toggled if check_condition() continues
                self.curr_player = self.curr_player.opponent

        except GameTieException:
            end = "The game is a tie."

        except GameWinException:
            end = "Player " + self.curr_player.char + " wins!!"

        self.board.show()
        print "\n" + end


class GameTieException(Exception):
    """Raised if the game is a tie"""


class GameWinException(Exception):
    """Raised when game is won"""





if __name__ == '__main__':
    Game().play()

