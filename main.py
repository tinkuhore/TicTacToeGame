import copy
import random
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

    def check_winner(self, draw=True):
        """ return 0 for no win yet
            return 1 if player 1 wins
            return 2 if player 2 wins
        """
        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if draw:
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
                if draw:
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
            if draw:
                if self.squares[1][1] == 1:
                    pygame.draw.line(win, CROSS_COLOUR, (20, 20), (580, 580), CROSS_WIDTH + 5)
                    pygame.time.delay(500)
                elif self.squares[1][1] == 2:
                    pygame.draw.line(win, CIRC_COLOUR, (20, 20), (580, 580), CIRC_WIDTH)
                    pygame.time.delay(500)
            return self.squares[1][1]
        # asc diagonal wins
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            if draw:
                if self.squares[1][1] == 1:
                    pygame.draw.line(win, CROSS_COLOUR, (20, 580), (580, 20), CROSS_WIDTH + 5)
                    pygame.time.delay(500)
                elif self.squares[1][1] == 2:
                    pygame.draw.line(win, CIRC_COLOUR, (20, 580), (580, 20), CIRC_WIDTH)
                    pygame.time.delay(500)
            return self.squares[1][1]
        # no win yet
        return 0

    def announce(self, check_winner, mode, result):
        if check_winner == 0:
            pygame.time.wait(1000)
            win.fill(BG_COLOUR)
            text = MSG_FONT.render('Its a DRAW!', True, BLUE)
            win.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            result[2] += 1
            return result, False  # [P1, P2, D], Bool
        player1 = ['Player 1', 'You']
        player2 = ['Player2', 'Bot']
        if check_winner == 1:
            pygame.time.wait(1000)
            win.fill(BG_COLOUR)
            if mode == 'pvp':
                text = MSG_FONT.render(player1[check_winner - 1] + ' WON!', True, BLUE)
            else:
                text = MSG_FONT.render(player1[check_winner] + ' WON!', True, BLUE)
            win.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            result[0] += 1
            return result, False  # [P1, P2, D], Bool
        if check_winner == 2:
            pygame.time.wait(1000)
            win.fill(BG_COLOUR)
            if mode == 'pvp':
                text = MSG_FONT.render(player2[check_winner - 2] + ' WON!', True, BLUE)
            else:
                text = MSG_FONT.render(player2[check_winner - 1] + ' WON!', True, BLUE)
            win.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            result[1] += 1
            return result, False  # [P1, P2, D], Bool

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs  # returns list of co-ordinates of empty squares

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


class AI:
    def __init__(self, level, player=2):
        self.level = level
        self.player = player

    def rnd_choice(self, board):
        empty_sqrs = board.get_empty_sqrs()
        return random.choice(empty_sqrs)  # (row, col)

    def minimax(self, board, maximizing):

        # terminal cases
        case = board.check_winner(False)

        # player 1 wins
        if case == 1:
            return None, 1
        # player 2 wins
        if case == 2:
            return None, -1
        # draw
        elif board.isfull():
            return None, 0

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[1]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return best_move, max_eval
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[1]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return best_move, min_eval

    def analyse(self, main_board):
        if self.level == 0:
            # random choice
            move, eval = self.rnd_choice(main_board), None
        else:
            # AI algo choice
            move, eval = self.minimax(main_board, False)
        print(f'AI has marked the square at position {move} with the evaluation = {eval}')
        return move


class Game:
    def __init__(self, gamemode, level):
        self.board = Board()
        self.ai = AI(level)
        self.player = 1  # 1 - cross, 2 - circle
        self.gamemode = gamemode
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


def home_screen():
    global image
    win.fill(BG_COLOUR)
    # Opening Window
    # title
    text = SCORE_FONT.render("Welcome to", True, WHITE)
    win.blit(text, ((WIDTH - 200 - text.get_width()) // 2, 30))
    text = MSG_FONT.render("TicTacToe", True, BLUE)
    win.blit(text, ((WIDTH - 200 - text.get_width()) // 2, 90))
    win.blit(image, (400, 20))

    # game mode buttons
    # player vs player
    pygame.draw.rect(win, WHITE, pygame.Rect(50, 285, 500, 80), border_radius=15)
    text = BUTTON_FONT.render("Player1 vs Player2", True, CROSS_COLOUR)
    win.blit(text, ((WIDTH - text.get_width()) // 2, 300))
    # player vs Bot
    pygame.draw.rect(win, WHITE, pygame.Rect(100, 435, 400, 80), border_radius=15)
    text = BUTTON_FONT.render("Player vs Bot", True, CROSS_COLOUR)
    win.blit(text, ((WIDTH - text.get_width()) // 2, 450))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                point = event.pos
                if 0 < point[0] - 50 < 500 and 0 < point[1] - 285 < 80:
                    return 'pvp'
                elif 0 < point[0] - 100 < 400 and 0 < point[1] - 435 < 80:
                    return 'ai'


def difficulty():
    win.fill(BG_COLOUR)
    text = MSG_FONT.render("Select", False, BLUE)
    win.blit(text, ((WIDTH - text.get_width()) // 2, 60))
    text = MSG_FONT.render("Difficulty Level", False, RED)
    win.blit(text, ((WIDTH - text.get_width()) // 2, 120))
    # Easy button
    pygame.draw.rect(win, WHITE, pygame.Rect(200, 285, 200, 80), border_radius=15)
    text = BUTTON_FONT.render("Easy", True, CROSS_COLOUR)
    win.blit(text, ((WIDTH - text.get_width()) // 2, 300))
    # Hard button
    pygame.draw.rect(win, WHITE, pygame.Rect(200, 435, 200, 80), border_radius=15)
    text = BUTTON_FONT.render("Hard", True, CROSS_COLOUR)
    win.blit(text, ((WIDTH - text.get_width()) // 2, 450))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                point = event.pos
                if 0 < point[0] - 200 < 200 and 0 < point[1] - 285 < 80:
                    return 0
                elif 0 < point[0] - 200 < 200 and 0 < point[1] - 435 < 80:
                    return 1


def score_update(result, mode):
    # show score
    win.fill(BG_COLOUR)
    text = MSG_FONT.render("___Score___", False, BLUE)
    win.blit(text, ((WIDTH - text.get_width()) // 2, 20))
    l1 = ["Player1", "Player2", "Draw"]
    if mode == 'ai':
        l1[0] = 'You'
        l1[1] = 'Bot'
    l2 = result
    l3 = [CROSS_COLOUR, CIRC_COLOUR, RED]
    for count in range(3):
        x = 45 + count * 170
        text = SCORE_FONT.render(l1[count], True, l3[count])
        win.blit(text, (x + (170 - text.get_width()) // 2, 100))
        text = SCORE_FONT.render(str(l2[count]), True, l3[count])
        win.blit(text, (x + (170 - text.get_width()) // 2, 150))

    # play again button
    pygame.draw.rect(win, WHITE, pygame.Rect(100, 285, 400, 80), border_radius=15)
    text = BUTTON_FONT.render("Play Again", True, CROSS_COLOUR)
    win.blit(text, ((WIDTH - text.get_width()) // 2, 300))
    # home
    pygame.draw.rect(win, WHITE, pygame.Rect(100, 435, 400, 80), border_radius=15)
    text = BUTTON_FONT.render("Home Page", True, CROSS_COLOUR)
    win.blit(text, ((WIDTH - text.get_width()) // 2, 450))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                point = event.pos
                if 0 < point[0] - 100 < 400 and 0 < point[1] - 285 < 80:
                    return True
                elif 0 < point[0] - 100 < 400 and 0 < point[1] - 435 < 80:
                    return False


def main(mode, level):
    global result
    # mainloop
    if mode == 'pvp':
        pygame.display.set_caption("TicTacToe Game! (P vs P Mode)")
    else:
        pygame.display.set_caption("TicTacToe Game! (AI Mode)")
    win.fill(BG_COLOUR)
    game = Game(mode, level)
    board = game.board
    ai = game.ai
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

                check_winner = int(board.check_winner())
                pygame.display.update()
                if check_winner == 0:
                    if board.isfull():
                        result, run = board.announce(check_winner, game.gamemode, result)
                    else:
                        game.next_turn()
                else:
                    result, run = board.announce(check_winner, game.gamemode, result)

            if game.gamemode == 'ai' and game.player == ai.player:
                # ai move
                row, col = ai.analyse(board)
                board.mark_sqr(row, col, game.player)
                game.draw_fig(row, col)
                pygame.display.update()

                check_winner = int(board.check_winner())
                pygame.display.update()
                if check_winner == 0:
                    if board.isfull():
                        result, run = board.announce(check_winner, game.gamemode, result)
                    else:
                        game.next_turn()
                else:
                    result, run = board.announce(check_winner, game.gamemode, result)
                    break
            # pygame.display.update()


while True:
    # initiating result = [p1, p2, d]
    result = [0, 0, 0]

    # reading selected mode
    mode = home_screen()
    level = difficulty() if mode == 'ai' else None
    print(mode, level)
    signal = True
    while signal:
        main(mode, level)
        signal = score_update(result, mode)

# ____ END OF CODE____
