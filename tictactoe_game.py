import tkinter as tk
from tkinter import messagebox
import random
import time

root = tk.Tk()
root.title("Tic-Tac-Toe AI 🧠")

game_board = [' ']*9
buttons = []
turn = 'X'
your_score = 0
ai_score = 0
timer = None
difficulty = 'medium'

# 🎯 Score display
score_label = tk.Label(root, text="You: 0  |  AI: 0", font=('Helvetica', 12))
score_label.grid(row=4, column=0, columnspan=3)

# ⏰ Timer
time_label = tk.Label(root, text="", font=('Helvetica', 10), fg='red')
time_label.grid(row=5, column=0, columnspan=3)

def update_score():
    score_label.config(text=f"You: {your_score}  |  AI: {ai_score}")

def check_winner(board, sign):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    return any(board[i] == board[j] == board[k] == sign for i,j,k in wins)

def get_empty(board):
    return [i for i, x in enumerate(board) if x == ' ']

def full_board(board):
    return ' ' not in board

def refresh_board():
    global game_board, turn, timer
    game_board = [' '] * 9
    for btn in buttons:
        btn.config(text='', state='normal', bg='white')
    turn = 'X'
    time_label.config(text="")
    if timer: root.after_cancel(timer)
    start_timer()

def click_box(i):
    global turn
    if game_board[i] == ' ' and turn == 'X':
        game_board[i] = 'X'
        buttons[i].config(text='X', state='disabled', disabledforeground='blue')
        if check_end(): return
        turn = 'O'
        root.after(700, ai_move)

def check_end():
    global your_score, ai_score
    if check_winner(game_board, 'X'):
        messagebox.showinfo("Result", "🎉 You Win!")
        your_score += 1
        update_score()
        disable_board()
        return True
    elif check_winner(game_board, 'O'):
        messagebox.showinfo("Result", "💀 AI Wins!")
        ai_score += 1
        update_score()
        disable_board()
        return True
    elif full_board(game_board):
        messagebox.showinfo("Result", "🤝 It's a Draw!")
        disable_board()
        return True
    return False

def disable_board():
    for btn in buttons:
        btn.config(state='disabled')
    if timer: root.after_cancel(timer)
    time_label.config(text="")

def ai_move():
    global turn
    if difficulty == 'easy':
        move = random.choice(get_empty(game_board))
    elif difficulty == 'medium':
        move = find_best_medium()
    else:
        move = find_best_move()
    game_board[move] = 'O'
    buttons[move].config(text='O', state='disabled', disabledforeground='red')
    if check_end(): return
    turn = 'X'
    start_timer()

def find_best_medium():
    for i in get_empty(game_board):
        game_board[i] = 'O'
        if check_winner(game_board, 'O'):
            return i
        game_board[i] = ' '
    for i in get_empty(game_board):
        game_board[i] = 'X'
        if check_winner(game_board, 'X'):
            game_board[i] = ' '
            return i
        game_board[i] = ' '
    return random.choice(get_empty(game_board))

def find_best_move():
    def minimax(board, is_max):
        if check_winner(board, 'O'): return 1
        if check_winner(board, 'X'): return -1
        if full_board(board): return 0
        if is_max:
            best = -1000
            for i in get_empty(board):
                board[i] = 'O'
                val = minimax(board, False)
                board[i] = ' '
                best = max(best, val)
            return best
        else:
            best = 1000
            for i in get_empty(board):
                board[i] = 'X'
                val = minimax(board, True)
                board[i] = ' '
                best = min(best, val)
            return best

    best_score = -1000
    best_move = None
    for i in get_empty(game_board):
        game_board[i] = 'O'
        score = minimax(game_board, False)
        game_board[i] = ' '
        if score > best_score:
            best_score = score
            best_move = i
    return best_move

# ⏱ 10-second move timer
seconds = 10
def update_timer():
    global seconds, timer
    time_label.config(text=f"⏱ Time left: {seconds}s")
    if seconds > 0:
        seconds -= 1
        timer = root.after(3000, update_timer)
    else:
        time_label.config(text="⏰ You missed your move!")
        ai_move()

def start_timer():
    global seconds
    seconds = 20
    update_timer()

# 🎮 Create buttons
for i in range(9):
    b = tk.Button(root, text='', font=('Arial', 24), width=5, height=2, bg='white',
                  command=lambda i=i: click_box(i))
    b.grid(row=i//3, column=i%3)
    buttons.append(b)

# 🔄 Reset button
reset_btn = tk.Button(root, text="🔄 Play Again", font=('Arial', 10), command=refresh_board)
reset_btn.grid(row=6, column=0, columnspan=3, pady=10)

# 🎚️ Difficulty selector
def set_level(val):
    global difficulty
    difficulty = val
    messagebox.showinfo("Difficulty", f"Level set to: {val.upper()}")

menu_bar = tk.Menu(root)
level_menu = tk.Menu(menu_bar, tearoff=0)
for lvl in ['easy', 'medium', 'hard']:
    level_menu.add_command(label=lvl.title(), command=lambda lvl=lvl: set_level(lvl))
menu_bar.add_cascade(label="🎚 Difficulty", menu=level_menu)
root.config(menu=menu_bar)

# 🚀 Start
refresh_board()
root.mainloop()
