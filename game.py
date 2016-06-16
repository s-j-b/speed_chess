import Tkinter as tk
from PIL import ImageTk as IM
from logic import *
import sys

# GUI States
ON = 1
OFF = 0

PX = (50)
D = (DIM*PX/8)
DISPLACEMENT = (D/16)
XD = (2.8)
YD = (1.5)
BOX_DIM = (4)

root = tk.Tk()
root.title("Speed Chess")

canvas = tk

################################################################################
################################ Main Function #################################
################################################################################
            
def main():

    print (sys.argv)
    
    w = DIM * PX
    h = DIM * PX

    geom = str(w) + "x" + str(h)

    game = chessGame()
    board = Board(root, game)
    
    root.geometry(geom)

    root.mainloop()

################################################################################
############################ Board Class Definition ############################
################################################################################

class Board(tk.Frame):

    def __init__(self, parent, game):

        frame = tk.Frame.__init__(self, parent)

        self.parent = parent
        self.game = game
        
        self.pack(fill = tk.BOTH, expand=1)
        
        self.canvas = tk.Canvas(self)

        self.canvas.bind("<Button-1>", self.callback)
        
        d = DIM*PX/8

        self.state = OFF

        self.cur_i = 0
        self.cur_j = 0
        self.shapes = []
        
        self.labels = []

        for i in range(8):
            row = []
            for j in range(8):
                row.append(0)
            self.labels.append(row)

        for i in range(8):
            for j in range(8):
                
                if ((i+j)%2==0):

                    col = "#8a8"
                    
                    self.canvas.create_rectangle(i*d, j*d, i*d + d, j*d + d, 
                                                 outline=col, fill=col)

                    if (j==0):

                        if (i==0 or i==7):
                            self.labels[i][j] = self.make_label(parent,
                                                                BLACK_ROOK, col, i, j)
                            
                        if (i==1 or i==6):
                            self.labels[i][j] = self.make_label(parent,
                                                                BLACK_KNIGHT, col, i, j)

                        if (i==2 or i==5):
                            self.labels[i][j] = self.make_label(parent,
                                                                BLACK_BISHOP, col, i, j)
                            
                        if (i==3):
                            self.labels[i][j] = self.make_label(parent,
                                                                BLACK_QUEEN, col, i, j)

                        if (i==4):
                            self.labels[i][j] = self.make_label(parent,
                                                                BLACK_KING, col, i, j)

                    if (j==1):
                        self.labels[i][j] = self.make_label(parent,
                                                            BLACK_PAWN, col, i, j)
                        
                    if (j==6):
                        self.labels[i][j] = self.make_label(parent,
                                                            WHITE_PAWN, col, i, j)

                    if (j==7):                        
                        if (i==0 or i==7):
                            self.labels[i][j] = self.make_label(parent,
                                                                WHITE_ROOK, col, i, j)

                        if (i==1 or i==6):
                            self.labels[i][j] = self.make_label(parent,
                                                                WHITE_KNIGHT, col, i, j)

                        if (i==2 or i==5):
                            self.labels[i][j] = self.make_label(parent,
                                                                WHITE_BISHOP, col, i, j)
                            
                        if (i==3):
                            self.labels[i][j] = self.make_label(parent,
                                                                WHITE_QUEEN, col, i, j)
                            
                        if (i==4):
                            self.labels[i][j] = self.make_label(parent,
                                                                WHITE_KING, col, i, j) 

                else:
                    
                    col = "#369"                    
                    self.canvas.create_rectangle(i*d, j*d, i*d + d, j*d + d, 
                                            outline=col, fill=col)

                    if (j==0):

                        if (i==0 or i==7):
                            self.labels[i][j] = self.make_label(parent,
                                                                BLACK_ROOK, col, i, j)

                        if (i==1 or i==6):
                            self.labels[i][j] = self.make_label(parent,
                                                                BLACK_KNIGHT, col, i, j)

                        if (i==2 or i==5):
                            self.labels[i][j] = self.make_label(parent,
                                                                BLACK_BISHOP, col, i, j)
                                
                        if (i==3):
                            self.labels[i][j] = self.make_label(parent,
                                                                BLACK_QUEEN, col, i, j)
                                
                        if (i==4):
                            self.labels[i][j] = self.make_label(parent,
                                                                BLACK_KING, col, i, j)
                                
                    if (j==1):
                        self.labels[i][j] = self.make_label(parent,
                                                            BLACK_PAWN, col, i, j)
                        
                    if (j==6):
                        self.labels[i][j] = self.make_label(parent,
                                                            WHITE_PAWN, col, i, j)
                    
                    if (j==7):                        
                        if (i==0 or i==7):
                            self.labels[i][j] = self.make_label(parent,
                                                                WHITE_ROOK, col, i, j)
                            
                        if (i==1 or i==6):
                            self.labels[i][j] = self.make_label(parent,
                                                                WHITE_KNIGHT, col, i, j)

                        if (i==2 or i==5):
                            self.labels[i][j] = self.make_label(parent,
                                                                WHITE_BISHOP, col, i, j)
                                
                        if (i==3):
                            self.labels[i][j] = self.make_label(parent,
                                                                WHITE_QUEEN, col, i, j)
                                
                        if (i==4):
                            self.labels[i][j] = self.make_label(parent,
                                                                WHITE_KING, col, i, j)

        self.canvas.pack(fill = tk.BOTH, expand = 1)
        
        self.rows = DIM
        self.columns = DIM

    def make_label(self, parent, piece, col, i, j):
        sz = 27

        if (piece == WHITE_PAWN):
                label = tk.Label(parent, text= u"\u265f", fg="#fff", background=col,
                                 font=("Helvetica", sz))

        if (piece == WHITE_KNIGHT):
                label = tk.Label(parent, text= u"\u265e", fg="#fff", background=col,
                                 font=("Helvetica", sz))

        if (piece == WHITE_BISHOP):
                label = tk.Label(parent, text= u"\u265d", fg="#fff", background=col,
                                 font=("Helvetica", sz))

        if (piece == WHITE_ROOK):
                label = tk.Label(parent, text= u"\u265c", fg="#fff", background=col,
                                 font=("Helvetica", sz))

        if (piece == WHITE_QUEEN):
                label = tk.Label(parent, text= u"\u265b", fg="#fff", background=col,
                                 font=("Helvetica", sz))

        if (piece == WHITE_KING):
                label = tk.Label(parent, text= u"\u265a", fg="#fff", background=col,
                                 font=("Helvetica", sz))

        if (piece == BLACK_PAWN ):
                label = tk.Label(parent, text= u"\u265f", fg="#000", background=col,
                                 font=("Helvetica", sz))

        if (piece == BLACK_KNIGHT ):
                label = tk.Label(parent, text= u"\u265e", fg="#000", background=col,
                                 font=("Helvetica", sz))

        if (piece == BLACK_BISHOP ):
                label = tk.Label(parent, text= u"\u265d", fg="#000", background=col,
                                 font=("Helvetica", sz))

        if (piece == BLACK_ROOK ):
                label = tk.Label(parent, text= u"\u265c", fg="#000", background=col,
                                 font=("Helvetica", sz))

        if (piece == BLACK_QUEEN ):
            
                label = tk.Label(parent, text= u"\u265b", fg="#000", background=col,
                                 font=("Helvetica", sz))

        if (piece == BLACK_KING ):
                label = tk.Label(parent, text= u"\u265a", fg="#000", background=col,
                                 font=("Helvetica", sz))
                
        label.bind("<Button-1>",lambda e,label=label:self.call_label(label, e))
        
        label.pack()
        label.place(x = i * D + DISPLACEMENT*XD,
                    y = j * D + DISPLACEMENT*YD)
        
        return label

    def call_label(self, label, event):
        x = int(label.place_info()["x"]) + event.x
        y = int(label.place_info()["y"]) + event.y

        self.process_click(x,y)
        
    def callback(self, event):
        x = event.x
        y = event.y

        self.process_click(x,y)
        
    def process_click(self, x, y):

        x /= PX
        y /= PX

        if (x > 7):
            x = 7

        if (y > 7):
            y = 7

        if (self.state == OFF):

            a = x*PX
            b = y*PX
            
            self.shapes.append(self.canvas.create_rectangle(a + 0,
                                                            b + 0,
                                                            a + BOX_DIM,
                                                            b + PX,
                                                            outline="#b3f", fill="#b3f"))

            self.shapes.append(self.canvas.create_rectangle(a + 0,
                                                            b + 0,
                                                            a + PX,
                                                            b + BOX_DIM,
                                                            outline="#b3f", fill="#b3f"))

            self.shapes.append(self.canvas.create_rectangle(a + 0,
                                                            b + PX - BOX_DIM,
                                                            a + PX,
                                                            b + PX,
                                                            outline="#b3f", fill="#b3f"))

            self.shapes.append(self.canvas.create_rectangle(a + PX - BOX_DIM,
                                                            b + 0,
                                                            a + PX,
                                                            b + PX,
                                                            outline="#b3f", fill="#b3f"))

            self.cur_i = x
            self.cur_j = y
            self.state = ON

        else:

            if self.game.is_legal_move(self.cur_i, 7 - self.cur_j, x, 7 - y):
                self.process_move(self.cur_i, self.cur_j, x, y)
                
            for shape in self.shapes:
                self.canvas.delete(shape)
            


            self.state = OFF
            
    def process_move(self, i0, j0, i1, j1):

        if ((i1 + j1)%2 == 0):
            col = "#8a8"
        else:
            col = "#369"        
            
        self.labels[i0][j0]["background"] = col

        print self.labels[i0][j0]

        self.labels[i0][j0].place(x = i1 * D + DISPLACEMENT * XD,
                                  y = j1 * D + DISPLACEMENT * YD)

        if self.labels[i1][j1] != 0:
            self.labels[i1][j1].destroy()
            
        self.labels[i1][j1] = self.labels[i0][j0]
        self.labels[i0][j0] = 0

        self.canvas.pack(fill = tk.BOTH, expand = 1)
        
        self.game.do_move(i0, 7 - j0, i1, 7 - j1)

        self.print_labels()

    def print_labels(self):
        for i in range(8):
            for j in range(8):
                if self.labels[i][j] == 0:
                    print 0,
                else:
                    print self.labels[i][j]["text"],
            print ""
        
main()
