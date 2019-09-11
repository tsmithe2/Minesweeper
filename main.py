import pygame as py
import board

done = False
clock = py.time.Clock()
py.init()

py.display.set_mode((800, 600))


while not done:
    for event in py.event.get():
        if event.type == py.QUIT:
            done = True
    if board.screen == 0:
        board.MainMenu()
    if board.screen == 1:
        board.GameOptions()
    if board.screen == 2:
        board.Help()
    if board.screen == 3:
        board.GameMode()
    if board.screen == 4:
        board.GameOver("lose")
    if board.screen == 5:
        board.GameOver("win")
    py.display.flip()
    clock.tick(40)

py.quit()
