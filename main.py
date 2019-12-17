from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import random
from random import randrange
from functools import partial
import os
import time
#########################################Logic board###############################################

#varible
num_mine = 50 #99
side = 24
mine = set()
board = [] # real board
canOpen = []# bool for show can click this cell

def isValid(row,col):
    return row>=0 and row<side and col>=0 and col<side

def countMine(row,col,board):
    count = 0
    for i in range(row-1,row+2,1):
        for j in range(col-1,col+2,1):
            if(i==row and j==col):
                continue
            if(not isValid(i,j)):
                continue
            if(board[i][j]==-1):
                count+=1
    return count

def createBoard():
    board.clear()
    canOpen.clear()
    mine.clear()
    for i in range(side):
        board.append([])
        canOpen.append([])
        for j in range(side):
            board[i].append(-2)
            canOpen[i].append(1)

    while(len(mine)!=num_mine):
        x = randrange(side)
        y = randrange(side)
        if((x,y) not in mine):
            mine.add((x,y))

    for (x,y) in mine:
        board[x][y] = -1 #-1 = mine

    for i in range(side):
        for j in range(side):
            if(board[i][j]==-1):
                continue
            x = countMine(i,j,board)
            board[i][j] = x
createBoard()


###############################################Tinker##############################################
master = tk.Tk()
master.title('Minsweeper Greedy Slover')
master.geometry("582x690") #"582x650"
master.resizable(0, 0)
matrix = [] #show board
isEnd = False
speed = 250


def getValue(row,col):
    global isEnd
    if(isEnd):
        messagebox.showinfo("Game End", "Game is End,click new game to play again")
        return
    button = matrix[row][col]
    if(board[row][col]==-1 and canOpen[row][col]==1):
        canOpen[row][col] = 0
        button['text'] = str(board[row][col])
        button['bg'] = 'red'
        messagebox.showinfo("Game End", "You Lose!")
        #Die
        isEnd = True
    elif(canOpen[row][col]):
        canOpen[row][col] = 0
        button['text'] = str(board[row][col])
        button['bg'] = 'green'
        for i in range(row-1,row+2,1):
            for j in range(col-1,col+2,1):
                if(i==row and j==col):
                    continue
                if(not isValid(i,j)):
                    continue
                prob = random.random()
                if(prob>=0.5):
                    canOpen[i][j] = 0
                    button_prob = matrix[i][j]
                    if(board[i][j]==-1):
                        button_prob['text'] = str(board[i][j])
                        button_prob['bg'] = 'red'
                    else:
                        button_prob['text'] = str(board[i][j])
                        button_prob['bg'] = 'green'
        countNotOpen = 0
        for i in range(side):
            for j in range(side):
                if(canOpen[i][j]==1):
                    countNotOpen += 1
        if(countNotOpen==num_mine):
            messagebox.showinfo("Game End", "You Win!")
            #Win
            isEnd = True

for i in range(24):  
    matrix.append([])
    frame = Frame(master)
    frame.pack()
    for j in range(24):
        button = tk.Button(frame,height=1,width=2,bg='grey',command=partial(getValue,i,j))
        button.pack(side=LEFT)
        matrix[i].append(button)

def clearMatrix():
    for i in range(24):  
        for j in range(24):
            button = matrix[i][j]
            button['text'] = ''
            button['bg'] = 'grey'

def newGame():
    global isEnd
    isEnd = False
    createBoard()
    clearMatrix()


def runAlgo():
    global side
    global canOpen
    global isEnd
    global master
    global speed

    if(isEnd):
        return
    solve_board = []
    for row in range(side):
        solve_board.append([])
        for col in range(side):
            discount = 0
            for i in range(row-1,row+2,1):
                for j in range(col-1,col+2,1):
                    if(isValid(i,j) and board[i][j]==-1 and canOpen[i][j]==0):
                        discount += 1
            solve_board[row].append(board[row][col]-discount)

    dp = []
    dp.clear()
    for i in range(side):
        dp.append([])
        for _ in range(side):
            dp[i].append(float('Inf'))#-1 mean not have info

    for row in range(side):
        for col in range(side):
            if(canOpen[row][col]==1 or board[row][col]==-1):
                continue
            # print(board_solve[row][col])
            for i in range(row-1,row+2,1):
                for j in range(col-1,col+2,1):
                    if(i==row and j==col):
                        continue
                    if(not isValid(i,j)):
                        continue
                    if(dp[i][j]==float('Inf')):
                        dp[i][j] = 0
                    dp[i][j] += solve_board[row][col]
    min_mine = float('Inf')
    rowIdx = -1
    colIdx = -1
    for i in range(side):
        for j in range(side):
            if(canOpen[i][j]==1):
                button = matrix[i][j]
                button['text'] = str(dp[i][j])
                button['bg'] = 'purple'
            if(dp[i][j]<=min_mine and canOpen[i][j]==1):
                min_mine = dp[i][j]
                rowIdx = i
                colIdx = j
    # print(min_mine)
    # print(rowIdx,colIdx)
    getValue(rowIdx,colIdx)
    master.after(speed,runAlgo)

def set_speed(val):
    global speed
    speed = 750 - int(val)

def set_mine():
    global mineBox
    global num_mine
    num_mine = int(mineBox.get())
    newGame()

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb   

#Button on Bottom
lastFrame = Frame(master)
lastFrame.pack()
newBtn = tk.Button(lastFrame,height=1,width=40,text='New Game',bg=_from_rgb((3, 252, 240)),command=partial(newGame))
runBtn = tk.Button(lastFrame,height=1,width=40,text='Run algo',bg=_from_rgb((3, 252, 240)),command=partial(runAlgo))
newBtn.pack(side=LEFT)
runBtn.pack(side=LEFT)


settingFrame = Frame(master,borderwidth=10)
settingFrame.pack()
textSpeed = Label(settingFrame,text="Speed = ")
textSpeed.pack(side=LEFT)
speedBtn = Scale(settingFrame,from_=0, to=500,width = 15,orient = HORIZONTAL,showvalue=False,command=set_speed)
speedBtn.pack(side=LEFT)

textMine = Label(settingFrame,text="Mine = ")
textMine.pack(side=LEFT)
mineBox = Spinbox(settingFrame, from_ = 50,to = 99,state="readonly",command = set_mine)
mineBox.pack()



# mineValue = Entry(speedFrame)


# print(board)

# for i in range(len(matrix)):
#     for j in range(len(matrix[i])):
#         button = matrix[i][j]
#         button['text'] = randrange(3)
#print(len(matrix),len(matrix[0]))

# print(len(matrix)*len(matrix[0]))
master.mainloop()
#######################################################################################################