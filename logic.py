DIM = 8

WHITE = 0
BLACK = 1

WHITE_PAWN = 1
WHITE_KNIGHT = 3
WHITE_BISHOP = 4
WHITE_ROOK = 5
WHITE_QUEEN = 9
WHITE_KING = 10

BLACK_PAWN  = 11
BLACK_KNIGHT  = 13
BLACK_BISHOP  = 14
BLACK_ROOK  = 15
BLACK_QUEEN  = 19
BLACK_KING  = 20

################################################################################
############################### Helper Functions ###############################
################################################################################
            
def map_l(letter):
    assert(letter in ["a","b","c","d","e","f","g","h"])
    return ord(letter) - 97

def map_n(number):
    number = int(number)
    assert(number > 0)
    assert(number < 9)
    return number - 1

################################################################################
############################ Chess Class Definition ############################
################################################################################


class chessGame(object):

    def __init__(self):

        self.board = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(0)
            self.board.append(row)

        self.moves = []

        self.print_board()
        self.init_board()

        print
        print "##################"
        print "Initialized board"
        print "##################"

        self.print_board()

    def init_board(self):
        self.set_square(WHITE_PAWN, "a2")
        self.set_square(WHITE_PAWN, "b2")
        self.set_square(WHITE_PAWN, "c2")
        self.set_square(WHITE_PAWN, "d2")
        self.set_square(WHITE_PAWN, "e2")
        self.set_square(WHITE_PAWN, "f2")
        self.set_square(WHITE_PAWN, "g2")
        self.set_square(WHITE_PAWN, "h2")

        self.set_square(WHITE_ROOK, "a1")
        self.set_square(WHITE_ROOK, "h1")
        self.set_square(WHITE_KNIGHT, "b1")
        self.set_square(WHITE_KNIGHT, "g1")
        self.set_square(WHITE_BISHOP, "c1")
        self.set_square(WHITE_BISHOP, "f1")
        self.set_square(WHITE_QUEEN, "d1")
        self.set_square(WHITE_KING, "e1")                        
                
        self.set_square(BLACK_PAWN, "a7")
        self.set_square(BLACK_PAWN, "b7")
        self.set_square(BLACK_PAWN, "c7")
        self.set_square(BLACK_PAWN, "d7")
        self.set_square(BLACK_PAWN, "e7")
        self.set_square(BLACK_PAWN, "f7")
        self.set_square(BLACK_PAWN, "g7")
        self.set_square(BLACK_PAWN, "h7")                

        self.set_square(BLACK_ROOK, "a8")
        self.set_square(BLACK_ROOK, "h8")
        self.set_square(BLACK_KNIGHT, "b8")
        self.set_square(BLACK_KNIGHT, "g8")
        self.set_square(BLACK_BISHOP, "c8")
        self.set_square(BLACK_BISHOP, "f8")
        self.set_square(BLACK_QUEEN, "d8")
        self.set_square(BLACK_KING, "e8")

    # s is square coordinates
    def set_square(self, piece, s):

        self.board[map_l(s[0])][map_n(s[1])] = piece
        
    def print_board(self):
        for i in range(DIM):
            print self.board[i]

    def do_move(self, a, b, c, d):
        self.board[c][d] = self.board[a][b]
        self.board[a][b] = 0
        

    def is_legal_move(self, i0, j0, i1, j1):

        piece = self.board[i0][j0]
        if piece == 0:
            return False
        if ((i1 == i0) and (j1 == j0)):
            return False
        
        print piece
        
        if piece == WHITE_PAWN:
            return self.legal_WHITE_PAWN(i0, j0, i1, j1)
        
        if piece == WHITE_KNIGHT:
            return self.legal_WHITE_KNIGHT(i0, j0, i1, j1)
        
        if piece == WHITE_BISHOP:
            return self.legal_WHITE_BISHOP(i0, j0, i1, j1)
        
        if piece == WHITE_ROOK:
            return self.legal_WHITE_ROOK(i0, j0, i1, j1)
        
        if piece == WHITE_QUEEN:
            return self.legal_WHITE_QUEEN(i0, j0, i1, j1)
        
        if piece == WHITE_KING:
            return self.legal_WHITE_KING(i0, j0, i1, j1)
        
        if piece == BLACK_PAWN:
            return self.legal_BLACK_PAWN(i0, j0, i1, j1)

        if piece == BLACK_KNIGHT:
            return self.legal_BLACK_KNIGHT(i0, j0, i1, j1)
        
        if piece == BLACK_BISHOP:
            return self.legal_BLACK_BISHOP(i0, j0, i1, j1)
        
        if piece == BLACK_ROOK:
            return self.legal_BLACK_ROOK(i0, j0, i1, j1)
        
        if piece == BLACK_QUEEN:
            return self.legal_BLACK_QUEEN(i0, j0, i1, j1)
        
        if piece == BLACK_KING:
            return self.legal_BLACK_KING(i0, j0, i1, j1)

        # Check, Castled, en passant, etc
        
    def legal_WHITE_PAWN(self, a, b, c, d):
        if c == a:
            if self.board[c][d] == 0:

                if d == b + 1:
                    return True
            
                elif d == b + 2:
                    if ((b == 1) and self.board[a][b + 1] == 0):
                        return True
        elif ((c == a - 1) or (c == a + 1)):
            if d == b + 1:
                if self.board[c][d] > 10:
                    return True
        return False
    
    def legal_WHITE_KNIGHT(self, a, b, c, d):
        if ((self.board[c][d] == 0) or (self.board[c][d] > 10)):
            A = c-a
            B = d-b
            if (((abs(A)==1) and abs(B)==2) or (((abs(A)==2) and abs(B)==1))):
                return True

        return False

    def legal_WHITE_BISHOP(self, a, b, c, d):
        if (abs(d - b) == abs(c - a)):

            A = 0
            B = 0
            if (c != a):
                A = (c-a)/abs(c-a)
            if (d != b):
                B = (d-b)/abs(d-b)
            for i in range(1, max(abs(c-a), abs(d-b))):
                if self.board[a + A*i][b + B*i] != 0:
                    print i, A, B
                    print a + A*i, b + B*i
                    print "A!"
                    return False
            if ((self.board[c][d]==0) or (self.board[c][d] > 10)):
                return True
        print "B!"
        return False

    def legal_WHITE_ROOK(self, a, b, c, d):
        if ((d - b) * (c - a) == 0):

            A = 0
            B = 0
            if (c != a):
                A = (c-a)/abs(c-a)
            if (d != b):
                B = (d-b)/abs(d-b)
            for i in range(1, max(abs(c-a), abs(d-b))):
                if self.board[a + A*i][b + B*i] != 0:
                    print i, A, B
                    print a + A*i, b + B*i
                    print "A!"
                    return False
            if ((self.board[c][d]==0) or (self.board[c][d] > 10)):
                return True
        print "B!"
        return False

    def legal_WHITE_QUEEN(self, a, b, c, d):
        if (((d - b) * (c - a) == 0) or (abs(d - b) == abs(c - a))):

            A = 0
            B = 0
            if (c != a):
                A = (c-a)/abs(c-a)
            if (d != b):
                B = (d-b)/abs(d-b)
            for i in range(1, max(abs(c-a), abs(d-b))):
                if self.board[a + A*i][b + B*i] != 0:
                    print i, A, B
                    print a + A*i, b + B*i
                    print "A!"
                    return False
            if ((self.board[c][d]==0) or (self.board[c][d] > 10)):
                return True
        print "B!"
        return False

    def legal_WHITE_KING(self, a, b, c, d):
        if ((abs(d - b) <= 1) and (abs(c - a) <= 1)):
            if ((self.board[c][d]==0) or (self.board[c][d] > 10)):
                return True
        return False

    def legal_BLACK_PAWN(self, a, b, c, d):
        if c == a:
            if self.board[c][d] == 0:

                if d == b - 1:
                    return True
            
                elif d == b - 2:
                    if ((b == 6) and self.board[a][b - 1] == 0):
                        return True
        elif ((c == a - 1) or (c == a + 1)):
            if d == b - 1:
                if self.board[c][d] < 11:
                    return True
        return False
    
    def legal_BLACK_KNIGHT(self, a, b, c, d):
        if self.board[c][d] < 11:
            A = c-a
            B = d-b
            if (((abs(A)==1) and abs(B)==2) or (((abs(A)==2) and abs(B)==1))):
                return True

        return False

    def legal_BLACK_BISHOP(self, a, b, c, d):
        if (abs(d - b) == abs(c - a)):

            A = 0
            B = 0
            if (c != a):
                A = (c-a)/abs(c-a)
            if (d != b):
                B = (d-b)/abs(d-b)
            for i in range(1, max(abs(c-a), abs(d-b))):
                if self.board[a + A*i][b + B*i] != 0:
                    print i, A, B
                    print a + A*i, b + B*i
                    print "A!"
                    return False
            if (self.board[c][d] < 11):
                return True
        print "B!"
        return False

    def legal_BLACK_ROOK(self, a, b, c, d):
        if ((d - b) * (c - a) == 0):

            A = 0
            B = 0
            if (c != a):
                A = (c-a)/abs(c-a)
            if (d != b):
                B = (d-b)/abs(d-b)
            for i in range(1, max(abs(c-a), abs(d-b))):
                if self.board[a + A*i][b + B*i] != 0:
                    print i, A, B
                    print a + A*i, b + B*i
                    print "A!"
                    return False
            if (self.board[c][d] < 11):
                return True
        print "B!"
        return False

    def legal_BLACK_QUEEN(self, a, b, c, d):
        if (((d - b) * (c - a) == 0) or (abs(d - b) == abs(c - a))):

            A = 0
            B = 0
            if (c != a):
                A = (c-a)/abs(c-a)
            if (d != b):
                B = (d-b)/abs(d-b)
            for i in range(1, max(abs(c-a), abs(d-b))):
                if self.board[a + A*i][b + B*i] != 0:
                    print i, A, B
                    print a + A*i, b + B*i
                    print "A!"
                    return False
            if (self.board[c][d] < 11):
                return True
        print "B!"
        return False

    def legal_BLACK_KING(self, a, b, c, d):

        if ((abs(d - b) <= 1) and (abs(c - a) <= 1)):
            if ((self.board[c][d]==0) or (self.board[c][d] < 11)):
                return True
        return False
