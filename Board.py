# BUS 216F-1: Python and Applications to Business Analytics II
# Yutong Li
# We are using a graphics package (from Zelle, Python programming: an intro to computer science, 3rd edition, chapter 4, from Pg113-Pg120).
# Part of the code is quoted from https://www.youtube.com/watch?v=trKjYdBASyQ
from graphics import *
import math
import random


def in_grid(x_coord, y_coord):
    """
    This function will return whether the point is in the grid or not
    :param x_coord: x_coord of the click
    :param y_coord: y_coord of the click
    :return: whether the click is in the grid
    """
    in_line = False

    if 57 < x_coord < 63 or 117 < x_coord < 123 or 57 < y_coord < 63 or 117 < y_coord < 123:
        in_line = True

    return not in_line


class Board:
    scores = {
        "X": -10,
        "O": 10,
        "tie": 0
    }

    def __init__(self, side_length=180, color="gold"):
        """
        This constructor will create a board with a given color
        :param side_length: length of the board
        :param color: color of the board theme
        """
        self.side_length = side_length
        self.color = color

        # use a nested list to really represent our board
        self.board = [
            ["", "", ""],  # [0, 0], [0, 1], [0, 2]
            ["", "", ""],  # [1, 0], [1, 1], [1, 2]
            ["", "", ""]   # [2, 0], [2, 1], [2, 2]
        ]

        self.board_length = 0
        self.current_player = "O"
        # create a window
        self.win = GraphWin("Intelligent Tic Tac Toe with Minimax Algorithm", self.side_length, self.side_length)
        self.win.setCoords(0, 0, self.side_length, self.side_length)
        self.win.setBackground("seashell")

        # gridlines
        # vertical
        self.line1 = Line(Point(self.side_length / 3, 0), Point(self.side_length / 3, self.side_length))
        self.line2 = Line(Point(2 * self.side_length / 3, 0), Point(2 * self.side_length / 3, self.side_length))

        # horizontal
        self.line3 = Line(Point(0, self.side_length / 3), Point(self.side_length, self.side_length / 3))
        self.line4 = Line(Point(0, 2 * self.side_length / 3), Point(self.side_length, 2 * self.side_length / 3))

    # close the board
    def close(self):
        self.win.close()

    def get_board_length(self):
        return self.board_length

    def best_move(self):
        move0 = -1
        move1 = -1

        if self.get_board_length() == 0:
            move0 = random.randint(0, 2)
            move1 = random.randint(0, 2)
        else:
            best_score = - math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.minimax(0, False)
                        self.board[i][j] = ""
                        if score > best_score:
                            best_score = score
                            move0 = i
                            move1 = j

        self.board[move0][move1] = "O"
        # draw AI move
        circle = Circle(Point(60 * move1 + 30, 60 * (2 - move0) + 30), 15)
        circle.draw(self.win)
        circle.setWidth(3)
        circle.setFill("seashell")

        self.board_length += 1
        self.current_player = "X"

    def minimax(self, depth, maximizingPlay):
        # if there is a result: return the score
        result = self.check_winner()
        if result != "":
            return self.scores[result]

        if maximizingPlay:
            max_eval = - math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = ""
                        max_eval = max(max_eval, score)
            return max_eval
        else:
            min_eval = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = ""
                        min_eval = min(min_eval, score)
            return min_eval

    def check_winner(self):
        """
        This function will check the current state of the board
        :return: return the winner
        """
        winner = ""

        # horizontal
        for i in range(3):
            if self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2]:
                winner = self.board[i][0]

        # vertical
        for i in range(3):
            if self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i]:
                winner = self.board[0][i]

        # diagonal
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            winner = self.board[0][0]
        if self.board[2][0] == self.board[1][1] and self.board[1][1] == self.board[0][2]:
            winner = self.board[2][0]

        if winner == "" and self.get_board_length() == 9:
            return 'tie'
        else:
            return winner

    def make_human_move(self, point):
        """
        This function will take the coordinate of a click and return the row, col index in the list
        Note that this function is default to be designed for human moves ("X)
        :param point: a click
        """
        # get the x, y coordinates of a click
        x_coord = point.getX()
        y_coord = point.getY()

        # the click cannot be on the gold line (must in the grid)
        if in_grid(x_coord, y_coord):
            row_index = int(2 - y_coord // 60)
            col_index = int(x_coord // 60)

            # check if the grid if empty, if yes, board_length+1, we draw element
            if self.board[row_index][col_index] == "":
                self.board_length += 1

                # draw "X" for human
                self.board[row_index][col_index] = 'X'
                point1 = Point(60 * (x_coord // 60) + 15, 60 * (y_coord // 60) + 15)
                point2 = Point(60 * (x_coord // 60 + 1) - 15, 60 * (y_coord // 60 + 1) - 15)
                line1 = Line(point1, point2)

                point3 = Point(60 * (x_coord // 60 + 1) - 15, 60 * (y_coord // 60) + 15)
                point4 = Point(60 * (x_coord // 60) + 15, 60 * (y_coord // 60 + 1) - 15)
                line2 = Line(point3, point4)

                line1.draw(self.win)
                line1.setFill("blue")
                line1.setWidth(4)
                line2.draw(self.win)
                line2.setFill("blue")
                line2.setWidth(4)

                # after we can draw "X", it is now AI's turn
                self.current_player = "O"

    def draw_board(self):
        """
        This function will draw every static gridlines on the board
        """
        # draw lines
        # vertical
        self.line1.draw(self.win)
        self.line1.setFill(self.color)
        self.line1.setWidth(6)

        self.line2.draw(self.win)
        self.line2.setFill(self.color)
        self.line2.setWidth(6)

        # horizontal
        self.line3.draw(self.win)
        self.line3.setFill(self.color)
        self.line3.setWidth(6)

        self.line4.draw(self.win)
        self.line4.setFill(self.color)
        self.line4.setWidth(6)
