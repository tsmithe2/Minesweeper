import pygame as py
from constants import Constants as Const
import random

window = py.display.set_mode((800, 600))
screen = 0
MODE = ""
flags = 0
game_mode_arr = []
button_state = []
adjacent_to_mines = []
mine_numbers = []
unflagged = []


def DrawScreen():
    global window
    py.display.set_caption("Minesweeper")
    window.fill(Const.light_grey)


def ScreenMessage(msg, color, font_size, x, y):
    global window
    font = py.font.SysFont(None, font_size)
    text = font.render(msg, True, color)
    window.blit(text, [x, y])


def DrawButton(x, y, width, height, inner_color, outer_color):
    global window
    py.draw.rect(window, outer_color, (x, y, width, height))
    py.draw.rect(window, inner_color, (x + 5, y + 5, width - 10, height - 10))


def LeftMouseDown(x, y, width, height):
    mouse = py.mouse.get_pos()
    click = py.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        if click[0] == 1:
            return True


def RightMouseDown(x, y, width, height):
    mouse = py.mouse.get_pos()
    click = py.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        if click[2] == 1:
            return True


def MainMenu():
    global screen
    global window
    screen = 0
    DrawScreen()
    ScreenMessage("Minesweeper", Const.black, 80, 210, 100)
    DrawButton(320, 200, 120, 60, Const.medium_grey, Const.black)  # play button
    DrawButton(320, 315, 120, 60, Const.medium_grey, Const.black)  # help button
    ScreenMessage("Play", Const.black, 50, 345, 215)
    ScreenMessage("Help", Const.black, 50, 345, 330)
    if LeftMouseDown(320, 200, 120, 60):  # play button
        screen = 1
    if LeftMouseDown(320, 315, 120, 60):  # help button
        screen = 2


def GameOptions():
    global screen
    global MODE
    global window
    screen = 1
    DrawScreen()
    ScreenMessage("Select Difficulty", Const.black, 70, 210, 100)
    DrawButton(240, 200, 300, 60, Const.medium_grey, Const.black)  # easy mode
    DrawButton(240, 315, 300, 60, Const.medium_grey, Const.black)  # medium mode
    DrawButton(240, 430, 300, 60, Const.medium_grey, Const.black)  # hard mode
    DrawButton(20, 500, 120, 60, Const.medium_grey, Const.black)  # Back button
    ScreenMessage("Easy             5x5", Const.black, 50, 265, 215)
    ScreenMessage("Medium   10x10", Const.black, 50, 265, 330)
    ScreenMessage("Hard         15x15", Const.black, 50, 265, 445)
    ScreenMessage("Back", Const.black, 50, 35, 515)
    py.event.wait()
    if LeftMouseDown(240, 200, 300, 60):  # easy mode
        MODE = "easy"
        SetValues()
        screen = 3
        py.event.wait()
    if LeftMouseDown(240, 315, 300, 60):  # medium mode
        MODE = "medium"
        window = py.display.set_mode((1000, 800))
        SetValues()
        screen = 3
        py.event.wait()
    if LeftMouseDown(240, 430, 300, 60):  # hard mode
        MODE = "hard"
        window = py.display.set_mode((1300, 1080))
        SetValues()
        screen = 3
        py.event.wait()
    if LeftMouseDown(20, 500, 120, 60):  # back button
        screen = 0


def Help():
    global screen
    screen = 2
    DrawScreen()
    ScreenMessage("How to play", Const.black, 50, 300, 50)
    ScreenMessage("1.) Select a game mode (Easy, Medium, or Hard).", Const.black, 30, 50, 100)
    ScreenMessage("2.) there will be 5 mines in Easy mode, 20 mines in Medium mode,", Const.black, 30, 50, 140)
    ScreenMessage("     and 50 mines in Hard mode.", Const.black, 30, 50, 160)
    ScreenMessage("3.) Left click any cell on the screen to see if there are nearby mines", Const.black, 30, 50, 200)
    ScreenMessage("4.) If you think you know that a cell contains a mine, then you can", Const.black, 30, 50, 240)
    ScreenMessage("     flag it by right clicking that cell.", Const.black, 30, 50, 260)
    ScreenMessage("5.) You win the game by flagging all the mines and clicking all the", Const.black, 30, 50, 300)
    ScreenMessage("     remaining cells.", Const.black, 30, 50, 320)
    DrawButton(20, 500, 120, 60, Const.medium_grey, Const.black)  # Back button
    ScreenMessage("Back", Const.black, 50, 35, 515)
    if LeftMouseDown(20, 500, 120, 60):  # back button
        screen = 0


def ScanForMines():
    global MODE
    top_right_corner = 0
    bottom_left_corner = 0
    bottom_right_corner = 0
    top_row = []
    bottom_row = []
    left_column = []
    right_column = []
    center_buttons = []
    center_buttons_count = 0
    temp_value = 0
    button_count = 0

    if MODE == "easy":
        top_right_corner = 4
        bottom_left_corner = 20
        bottom_right_corner = 24
        top_row = [1, 2, 3]
        left_column = [5, 10, 15]
        bottom_row = [21, 22, 23]
        right_column = [9, 14, 19]
        center_buttons_count = 9
        button_count = 25

    if MODE == "medium":
        top_right_corner = 9
        bottom_left_corner = 90
        bottom_right_corner = 99
        top_row = [1, 2, 3, 4, 5, 6, 7, 8]
        left_column = [10, 20, 30, 40, 50, 60, 70, 80]
        bottom_row = [91, 92, 93, 94, 95, 96, 97, 98]
        right_column = [19, 29, 39, 49, 59, 69, 79, 89]
        center_buttons_count = 64
        button_count = 100

    if MODE == "hard":
        top_right_corner = 14
        bottom_left_corner = 210
        bottom_right_corner = 224
        top_row = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        left_column = [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195]
        bottom_row = [211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223]
        right_column = [29, 44, 59, 74, 89, 104, 119, 134, 149, 164, 179, 194, 209]
        center_buttons_count = 169
        button_count = 225

    while len(center_buttons) != center_buttons_count:
        temp_value += 1
        if temp_value != top_right_corner and temp_value != bottom_left_corner \
                and temp_value != bottom_right_corner and temp_value not in top_row \
                and temp_value not in bottom_row and temp_value not in left_column \
                and temp_value not in right_column:
            center_buttons.append(temp_value)

    for x in range(button_count):
        value = []
        if MODE == "easy":
            value = [x - 6, x - 5, x - 4, x - 1, x + 1, x + 4, x + 5, x + 6]
        if MODE == "medium":
            value = [x - 11, x - 10, x - 9, x - 1, x + 1, x + 9, x + 10, x + 11]
        if MODE == "hard":
            value = [x - 16, x - 15, x - 14, x - 1, x + 1, x + 14, x + 15, x + 16]

        if game_mode_arr[x] == 0:
            if game_mode_arr[value[4]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[7]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[6]] in mine_numbers:
                adjacent_to_mines[x] += 1
        if game_mode_arr[x] == top_right_corner:
            if game_mode_arr[value[3]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[5]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[6]] in mine_numbers:
                adjacent_to_mines[x] += 1
        if game_mode_arr[x] == bottom_left_corner:
            if game_mode_arr[value[1]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[2]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[4]] in mine_numbers:
                adjacent_to_mines[x] += 1
        if game_mode_arr[x] == bottom_right_corner:
            if game_mode_arr[value[3]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[0]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[1]] in mine_numbers:
                adjacent_to_mines[x] += 1

        if game_mode_arr[x] in top_row:
            if game_mode_arr[value[3]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[4]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[5]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[6]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[7]] in mine_numbers:
                adjacent_to_mines[x] += 1

        if game_mode_arr[x] in left_column:
            if game_mode_arr[value[1]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[2]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[4]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[6]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[7]] in mine_numbers:
                adjacent_to_mines[x] += 1

        if game_mode_arr[x] in bottom_row:
            if game_mode_arr[value[0]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[1]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[2]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[3]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[4]] in mine_numbers:
                adjacent_to_mines[x] += 1

        if game_mode_arr[x] in right_column:
            if game_mode_arr[value[0]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[1]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[3]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[5]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[6]] in mine_numbers:
                adjacent_to_mines[x] += 1

        if game_mode_arr[x] in center_buttons:
            if game_mode_arr[value[0]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[1]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[2]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[3]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[4]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[5]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[6]] in mine_numbers:
                adjacent_to_mines[x] += 1
            if game_mode_arr[value[7]] in mine_numbers:
                adjacent_to_mines[x] += 1


def SetValues():
    global MODE
    global flags
    global game_mode_arr
    global button_state
    global adjacent_to_mines
    global mine_numbers
    global unflagged

    mine_count = 0
    arr_max = 0
    button_count = 0

    if MODE == "easy":
        mine_count = 5
        arr_max = 24
        button_count = 25
        flags = 5
    if MODE == "medium":
        mine_count = 20
        arr_max = 99
        button_count = 100
        flags = 20
    if MODE == "hard":
        mine_count = 50
        arr_max = 224
        button_count = 225
        flags = 50

    while len(mine_numbers) != mine_count:
        a = random.randint(0, arr_max)
        while a not in mine_numbers:
            mine_numbers.append(a)

    '''
    mine_numbers.append(0)
    mine_numbers.append(1)
    mine_numbers.append(2)
    mine_numbers.append(3)
    mine_numbers.append(4)
    mine_numbers.append(5)
    mine_numbers.append(6)
    mine_numbers.append(7)
    mine_numbers.append(8)
    mine_numbers.append(9)
    mine_numbers.append(10)
    #mine_numbers.append(11)
    #mine_numbers.append(12)
    #mine_numbers.append(13)
    #mine_numbers.append(14)
    #mine_numbers.append(15)
    '''

    adjacent_to_mines.clear()

    for x in range(button_count):
        game_mode_arr.append(x)
        button_state.append(0)
        adjacent_to_mines.append(0)
        unflagged.append(0)

    ScanForMines()


def GameOver(outcome):
    global screen
    global flags
    global game_mode_arr
    global button_state
    global adjacent_to_mines
    global mine_numbers
    global unflagged
    global MODE
    global window

    game_mode_arr.clear()
    button_state.clear()
    mine_numbers.clear()
    unflagged.clear()

    modeX_text = 0
    modeY_text = 0
    buttonX1 = 0
    buttonY = 0
    buttonX2 = 0
    button_textX = 0
    button_textY = 0

    if MODE == "easy":
        modeX_text = 270
        modeY_text = 500
        buttonX1 = 50
        buttonY = 500
        buttonX2 = buttonX1 + 490
        button_textX = 60
        button_textY = 510

    if MODE == "medium":
        modeX_text = 380
        modeY_text = 700
        buttonX1 = 157
        buttonY = 700
        buttonX2 = buttonX1 + 490
        button_textX = 167
        button_textY = 710

    if MODE == "hard":
        modeX_text = 510
        modeY_text = 950
        buttonX1 = 287
        buttonY = 950
        buttonX2 = buttonX1 + 490
        button_textX = 297
        button_textY = 960

    if outcome == "win":
        ScreenMessage("You win!", Const.black, 80, modeX_text + 5, modeY_text)
    if outcome == "lose":
        ScreenMessage("You lose!", Const.black, 80, modeX_text, modeY_text)
    DrawButton(buttonX1, buttonY, 205, 50, Const.medium_grey, Const.black)
    DrawButton(buttonX2, buttonY, 200, 50, Const.medium_grey, Const.black)
    ScreenMessage("Main Menu", Const.black, 50, button_textX, button_textY)
    ScreenMessage("Play Again", Const.black, 50, button_textX + 490, button_textY)
    if LeftMouseDown(buttonX1, buttonY, 205, 50):
        screen = 0
        window = py.display.set_mode((800, 600))
    if LeftMouseDown(buttonX2, buttonY, 200, 50):
        SetValues()
        screen = 3


def GameMode():
    global MODE
    global screen
    global game_mode_arr
    global button_state
    global mine_numbers
    global flags
    global adjacent_to_mines

    modeI = 0
    modeJ = 0
    modeX = 0
    flagX = 0
    flagY = 0
    mode_title = ""
    mode_size = 0
    top_row = []
    bottom_row = []
    left_column = []
    right_column = []
    value = []

    if MODE == "easy":
        mode_title = "Easy Mode"
        modeI = 5
        mode_size = 25
        top_row = [0, 1, 2, 3, 4]
        bottom_row = [20, 21, 22, 23, 24]
        left_column = [0, 5, 10, 15, 20]
        right_column = [4, 9, 14, 19, 24]
        modeJ = 4
        modeX = 300
        flagX = 330
        flagY = 410

    if MODE == "medium": #include corner buttons in rows and columns
        mode_title = "Medium Mode"
        modeI = 10
        mode_size = 100
        top_row = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        bottom_row = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
        left_column = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        right_column = [9, 19, 29, 39, 49, 59, 69, 79, 89, 99]
        modeJ = 9
        modeX = 400
        flagX = 440
        flagY = 650

    if MODE == "hard":
        mode_title = "Hard Mode"
        modeI = 15
        mode_size = 400
        top_row = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        left_column = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210]
        bottom_row = [210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224]
        right_column = [14, 29, 44, 59, 74, 89, 104, 119, 134, 149, 164, 179, 194, 209, 224]
        modeJ = 14
        modeX = 545 #for the mode_title
        flagX = 565
        flagY = 900

    DrawScreen()
    ScreenMessage(mode_title, Const.black, 50, modeX, 50)
    initial_x = 265
    initial_y = 120
    x = 0
    for i in range(modeI):
        for j in range(modeI):
            if unflagged[game_mode_arr[x]] == 1:
                if RightMouseDown(initial_x, initial_y, 50, 50):
                    unflagged[game_mode_arr[x]] = 0
                else:
                    button_state[game_mode_arr[x]] = 0
            if button_state[game_mode_arr[x]] == 0:
                DrawButton(initial_x, initial_y, 50, 50, Const.medium_grey, Const.black)
                if RightMouseDown(initial_x, initial_y, 50, 50):
                    if flags > 0:
                        button_state[game_mode_arr[x]] = 2
                        flags -= 1
                if LeftMouseDown(initial_x, initial_y, 50, 50):
                    if unflagged[game_mode_arr[x]] == 1:
                        unflagged.clear()
                        for p in range(mode_size):
                            unflagged.append(0)
                    button_state[game_mode_arr[x]] = 1
                ScreenMessage("Flags: " + str(flags), Const.black, 40, flagX, flagY)
            if button_state[game_mode_arr[x]] == 1:
                if game_mode_arr[x] in mine_numbers:
                    DrawButton(initial_x, initial_y, 50, 50, Const.red, Const.black)
                    screen = 4
                else:
                    DrawButton(initial_x, initial_y, 50, 50, Const.dark_grey, Const.black)
                    if adjacent_to_mines[x] > 0:
                        ScreenMessage(str(adjacent_to_mines[x]), Const.black, 50, initial_x + 15, initial_y + 10)
                    elif adjacent_to_mines[x] == 0:
                        if MODE == "easy":
                            value = [x - 6, x - 5, x - 4, x - 1, x + 1, x + 4, x + 5, x + 6]
                        if MODE == "medium":
                            value = [x - 11, x - 10, x - 9, x - 1, x + 1, x + 9, x + 10, x + 11]
                        if MODE == "hard":
                            value = [x - 16, x - 15, x - 14, x - 1, x + 1, x + 14, x + 15, x + 16]
                        if game_mode_arr[x] not in right_column:
                            if button_state[value[4]] != 2:
                                if adjacent_to_mines[value[4]] == 0:
                                    button_state[value[4]] = 1
                                if adjacent_to_mines[value[4]] > 0:
                                    button_state[value[4]] = 1
                        if game_mode_arr[x] not in left_column:
                            if button_state[value[3]] != 2:
                                if adjacent_to_mines[value[3]] == 0:
                                    button_state[value[3]] = 1
                                if adjacent_to_mines[value[3]] > 0:
                                    button_state[value[3]] = 1
                        if game_mode_arr[x] not in top_row:
                            if button_state[value[1]] != 2:
                                if adjacent_to_mines[value[1]] == 0:
                                    button_state[value[1]] = 1
                                if adjacent_to_mines[value[1]] > 0:
                                    button_state[value[1]] = 1
                        if game_mode_arr[x] not in bottom_row:
                            if button_state[value[6]] != 2:
                                if adjacent_to_mines[value[6]] == 0:
                                    button_state[value[6]] = 1
                                if adjacent_to_mines[value[6]] > 0:
                                    button_state[value[6]] = 1

            if button_state[game_mode_arr[x]] == 2:
                DrawButton(initial_x, initial_y, 50, 50, Const.green, Const.black)
                if LeftMouseDown(initial_x, initial_y, 50, 50):
                    flags += 1
                    button_state[game_mode_arr[x]] = 0
                    unflagged[game_mode_arr[x]] = 1
                    py.event.wait()
                if flags == 0 and 0 not in button_state:
                    screen = 5
            x += 1
            initial_x += 50
            if j == modeJ:
                initial_x = 265
                initial_y += 50
