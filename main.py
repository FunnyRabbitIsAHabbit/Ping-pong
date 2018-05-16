"""Project 3 Ping and Pong, and Game
Developer: Ermokhin S.A."""

from tkinter import *
from random import randrange

# Globals ---------------------------------------------------------

score_left = 0
score_right = 0

after_id = ''


def score(pad):
    """Updating players' score points"""

    global score_left, score_right

    if pad == 'left_pad':
        score_left += 1
        left['text'] = score_left

    elif pad == 'right_pad':
        score_right += 1
        right['text'] = score_right


def jump(event=None):
    """Ball jumping when hit"""
    global x, y

    if event == 'hit':
        y = randrange(0, 6)
        x = -x

    else:
        y = -y


def set_ball_position():
    """Ball set to main ball position"""

    canvas.coords(ball, main_ball_position[0],
                  main_ball_position[1],
                  main_ball_position[2],
                  main_ball_position[3])


# ------------------------------------------------------------------
# Main Tkinter window ----------------------------------------------


root = Tk()
root.title('GAME')

# Frames and labels, and buttons -----------------------------------

top_frame = Frame(root)
top_frame.grid(sticky=N)

middle_frame = Frame(root, width=500)
middle_frame.grid(sticky='ew')

game_frame = Frame(root, width=500, height=500)
game_frame.grid(sticky=S)

title = Label(top_frame, text='PING-PONG',
              font=('Helvetica Bold', 37))
title.grid(sticky=N)

left = Label(middle_frame, text=0,
              font=('Helvetica Bold', 71),
             width=7, fg='orange')
right = Label(middle_frame, text=0,
              font=('Helvetica Bold', 71),
              width=7, fg='green')

left.grid(row=0, column=0)
right.grid(row=0, column=2)
# ------------------------------------------------------------------
# Canvas -----------------------------------------------------------
canvas = Canvas(game_frame, width=500, height=500,
                background='purple')
canvas.pack()

ballsize = 36
main_ball_position = [250-ballsize/2, 250-ballsize/2,
                 250+ballsize/2, 250+ballsize/2]

leftpad = canvas.create_line(10, 200, 10, 300, width=10, fill='orange')
rightpad = canvas.create_line(496, 200, 496, 300, width=10, fill='green')
line = canvas.create_line(250, 0, 250, 500, fill='pink')
ball = canvas.create_oval(main_ball_position, fill='white')

x = 3
y = 0


def ch_ball_position():
    """Function moving ball horizontally and vertically"""

    x_left, y_left,\
    x_right, y_right = canvas.coords(ball)

    ball_center = (y_left+y_right)/2

    if x_right + x < 490 and x_left + x > 10:
        canvas.move(ball, x, y)

    elif x_right == 490 or x_left == 10:
        if x_right > 250:
            if canvas.coords(rightpad)[1] <= ball_center <=\
                    canvas.coords(rightpad)[3]:
                jump('hit')

            else:
                score('left_pad')
                set_ball_position()

        else:
            if canvas.coords(leftpad)[1] <= ball_center <=\
                    canvas.coords(leftpad)[3]:
                jump('hit')

            else:
                score('right_pad')
                set_ball_position()


    else:
        if x_right > 250:
            canvas.move(ball, 490-x_right, y)

        else:
            canvas.move(ball, 10-x_left, y)

    if y_left + y < 0 or y_right + y > 500:
        jump('not_hit')


def ch_pad_position(event):
    """Function moving pad vertically"""

    if event.keysym == 'Up':
        if not canvas.coords(rightpad)[1] < 0:
            canvas.move(rightpad, 0, -30)
    elif event.keysym == 'Down':
        if not canvas.coords(rightpad)[3] > 500:
            canvas.move(rightpad, 0, 30)

    elif event.keysym == 'w':
        if not canvas.coords(leftpad)[1] < 0:
            canvas.move(leftpad, 0, -30)
    elif event.keysym == 's':
        if not canvas.coords(leftpad)[3] > 500:
            canvas.move(leftpad, 0, 30)


def play():
    """Function ungrids a button and grids another one"""

    play_button.grid_forget()
    stop_button.grid(row=0, column=1)

    start()


def start(event=None):
    """Function starts other functions"""

    global after_id

    ch_ball_position()
    after_id = root.after(1, start)


def winner(event=None):
    """Defines the winner and stops the game"""

    root.after_cancel(after_id)
    stop_button.grid_forget()
    play_button.grid(row=0, column=1)

    dict_scores = {score_left: 'Orange', score_right: 'Green'}

    if score_left < score_right:
        Label(top_frame,
              text=dict_scores[score_right]+' player wins!').grid(sticky=S)

    elif score_right < score_left:
        Label(top_frame,
              text=dict_scores[score_left]+' player wins!').grid(sticky=S)

    else:
        Label(top_frame, text='Players played even!').grid(sticky=S)


stop_button = Button(middle_frame, text='STOP', command=winner)
play_button = Button(middle_frame, text='PLAY', command=play)
play_button.grid(row=0, column=1)

canvas.focus_set()
canvas.bind('<KeyPress>', ch_pad_position)

# ------------------------------------------------------------------

root.mainloop()
# End of Tkinter ---------------------------------------------------
