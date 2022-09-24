import pygame
import sys
from constants import *
import numpy as np

# --- pygame setup ---
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TicTacToe Game!")
win.fill(BG_COLOUR)
MSG_FONT = pygame.font.SysFont('Fantasy', 90, False, False)
BUTTON_FONT = pygame.font.SysFont('comicsans', 75, False, False)
SCORE_FONT = pygame.font.SysFont('comicsans', 50, False, False)
image = pygame.image.load('image.png')


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def check_winner(self):
        """ return 0 for no win yet
            return 1 if player 1 wins
            return 2 if player 2 wins
        """
        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                s_pos = (col * SQSIZE + 100, 20)
                e_pos = (col * SQSIZE + 100, 580)
                if self.squares[0][col] == 1:
                    pygame.draw.line(win, CROSS_COLOUR, s_pos, e_pos, CROSS_WIDTH + 5)
                    pygame.time.delay(500)
                elif self.squares[0][col] == 2:
                    pygame.draw.line(win, CIRC_COLOUR, s_pos, e_pos, CIRC_WIDTH)
                    pygame.time.delay(500)
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                s_pos = (20, row * SQSIZE + 100)
                e_pos = (580, row * SQSIZE + 100)
                if self.squares[row][0] == 1:
                    pygame.draw.line(win, CROSS_COLOUR, s_pos, e_pos, CROSS_WIDTH + 5)
                    pygame.time.delay(500)
                elif self.squares[row][0] == 2:
                    pygame.draw.line(win, CIRC_COLOUR, s_pos, e_pos, CIRC_WIDTH)
                    pygame.time.delay(500)
                return self.squares[row][0]

        # desc diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if self.squares[1][1] == 1:
                pygame.draw.line(win, CROSS_COLOUR, (20, 20), (580, 580), CROSS_WIDTH + 5)
                pygame.time.delay(500)
            elif self.squares[1][1] == 2:
                pygame.draw.line(win, CIRC_COLOUR, (20, 20), (580, 580), CIRC_WIDTH)
                pygame.time.delay(500)
            return self.squares[1][1]
        # asc diagonal wins
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            if self.squares[1][1] == 1:
                pygame.draw.line(win, CROSS_COLOUR, (20, 580), (580, 20), CROSS_WIDTH + 5)
                pygame.time.delay(500)
            elif self.squares[1][1] == 2:
                pygame.draw.line(win, CIRC_COLOUR, (20, 580), (580, 20), CIRC_WIDTH)
                pygame.time.delay(500)
            return self.squares[1][1]
        # no win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


class Game:
    def __init__(self):
        self.board = Board()
        # self.ai = AI()
        self.player = 1  # 1 - cross, 2 - circle
        self.gamemode = 'pvp'  # or 'ai'
        self.running = True
        self.show_lines()

    def show_lines(self):
        # vertical
        pygame.draw.line(win, LINE_COLOUR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(win, LINE_COLOUR, (SQSIZE * 2, 0), (SQSIZE * 2, HEIGHT), LINE_WIDTH)
        # horizontal
        pygame.draw.line(win, LINE_COLOUR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(win, LINE_COLOUR, (0, SQSIZE * 2), (WIDTH, SQSIZE * 2), LINE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def draw_fig(self, row, col):
        center = (col * SQSIZE + 100, row * SQSIZE + 100)
        if self.player == 1:
            # draw cross
            pygame.draw.line(win, CROSS_COLOUR, (center[0] - 50, center[1] - 50), (center[0] + 50, center[1] + 50),
                             CROSS_WIDTH)
            pygame.draw.line(win, CROSS_COLOUR, (center[0] - 50, center[1] + 50), (center[0] + 50, center[1] - 50),
                             CROSS_WIDTH)
        elif self.player == 2:
            # draw circle
            pygame.draw.circle(win, CIRC_COLOUR, center, RADIUS, CIRC_WIDTH)


def screen(i, p1, p2, d):
    global image
    win.fill(BG_COLOUR)
    if i == 0:
        # Opening Window
        # title
        text = SCORE_FONT.render("Welcome to", True, WHITE)
        win.blit(text, ((WIDTH - 200 - text.get_width()) // 2, 30))
        text = MSG_FONT.render("TicTacToe", True, BLUE)
        win.blit(text, ((WIDTH - 200 - text.get_width()) // 2, 90))
        win.blit(image, (400,20))


        # game mode buttons
        # player vs player
        pygame.draw.rect(win, WHITE, pygame.Rect(50, 285, 500, 80), border_radius=15)
        text = BUTTON_FONT.render("Player1 vs Player2", True, CROSS_COLOUR)
        win.blit(text, ((WIDTH - text.get_width()) // 2, 300))
        # player vs Bot
        pygame.draw.rect(win, WHITE, pygame.Rect(100, 435, 400, 80), border_radius=15)
        text = BUTTON_FONT.render("Player vs Bot", True, CROSS_COLOUR)
        win.blit(text, ((WIDTH - text.get_width()) // 2, 450))
    if i != 0:
        # show score
        text = MSG_FONT.render("___Score___", False, BLUE)
        win.blit(text, ((WIDTH - text.get_width()) // 2, 20))
        l1 = ["Player1", "Player2", "Draw"]
        l2 = [p1, p2, d]
        l3 = [CROSS_COLOUR, CIRC_COLOUR, RED]
        for count in range(3):
            x = 45 + count * 170
            text = SCORE_FONT.render(l1[count], True, l3[count])
            win.blit(text, (x + (170 - text.get_width()) // 2, 100))
            text = SCORE_FONT.render(str(l2[count]), True, l3[count])
            win.blit(text, (x + (170 - text.get_width()) // 2, 150))

        # play again button
        pygame.draw.rect(win, WHITE, pygame.Rect(50, 285, 500, 80), border_radius=15)
        text = BUTTON_FONT.render("Play Again", True, CROSS_COLOUR)
        win.blit(text, ((WIDTH - text.get_width()) // 2, 300))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                point = event.pos
                if point[0] - 50 <= 500 and point[1] - 285 <= 80:
                    return True
                else:
                    return False


def main():
    global p1, p2, d
    # mainloop
    win.fill(BG_COLOUR)
    game = Game()
    board = game.board
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col):
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    pygame.display.update()

                check_winner = board.check_winner()
                pygame.display.update()

                if check_winner == 1:
                    pygame.time.wait(1000)
                    win.fill(BG_COLOUR)
                    text = MSG_FONT.render('Player 1 WON!', True, BLUE)
                    win.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    p1 += 1
                    run = False
                elif check_winner == 2:
                    pygame.time.wait(1000)
                    win.fill(BG_COLOUR)
                    text = MSG_FONT.render('Player 2 WON!', True, BLUE)
                    win.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    p2 += 1
                    run = False
                elif check_winner == 0:
                    if board.isfull():
                        pygame.time.wait(1000)
                        win.fill(BG_COLOUR)
                        text = MSG_FONT.render('Its a DRAW!', True, BLUE)
                        win.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        d += 1
                        run = False
                    else:
                        game.next_turn()
            pygame.display.update()


i = 0
p1, p2, d = 0, 0, 0
while True:
    signal = screen(i, p1, p2, d)
    if signal:
        main()

    i += 1

# ____ END OF CODE____
