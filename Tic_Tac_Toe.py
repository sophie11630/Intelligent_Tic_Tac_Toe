# BUS 216F-1: Python and Applications to Business Analytics II
# Yutong Li
# We are using a graphics package (from Zelle, Python programming: an intro to computer science, 3rd edition, chapter 4, from Pg113-Pg120).
from Board import Board
from graphics import *


class Button:
    def __init__(self, win, center, width, height, label):
        w, h = width / 2, height / 2
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)

        # create rectangle, color it, draw it, label it
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)

        # button starts off deactivated
        self.deactivate()

    # clicked method returns True if button activate and point is inside it
    def clicked(self, p):
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    # accessor method returns the label
    def get_label(self):
        return self.label.getText()

    # sets button to active
    def activate(self):
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = True

    # set button to un-active
    def deactivate(self):
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = False


class Selection_Box:
    # constructor sets up the entire window
    def __init__(self):
        self.win = GraphWin("Tic_Tac_Toe!", 200, 300)
        self.win.setCoords(0, 0, 200, 300)
        self.win.setBackground("mistyrose")

        text1 = Text(Point(100, 2000), "Welcome to Tic_Tac_Toe!")
        text2 = Text(Point(100, 180), "Do you want to play or quit?")
        text1.draw(self.win)
        text1.setSize(13)
        text2.draw(self.win)
        text2.setSize(13)

        # create buttons for play and quit, and activate
        self.play = Button(self.win, Point(50, 80), 60, 40, "Play!")
        self.play.activate()
        self.quit = Button(self.win, Point(150, 80), 60, 40, "Quit!")
        self.quit.activate()

    # close the window
    def close(self):
        self.win.close()

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.play.clicked(pt):
                return "Play!"
            if self.quit.clicked(pt):
                return "Quit!"


def main():
    ai_win = 0
    player_win = 0
    tie = 0

    while True:
        # create input box,also ask users whether to fire or quit the game
        selection_box = Selection_Box()
        choice = selection_box.interact()
        selection_box.close()
        board = Board(180, "gold")
        try:
            result_win.close()
        except UnboundLocalError:
            pass

        # end the loop if the user clicks quit
        if choice == "Quit!":
            break

        # else we need to continue the game
        else:
            # play game: draw board
            board.draw_board()

            while True:
                if board.get_board_length() >= 9 or board.check_winner() != "":
                    break

                if board.current_player == "O" and board.check_winner() == "":
                    board.best_move()

                if board.current_player == "X" and board.check_winner() == "":
                    while True:
                        one_click = board.win.getMouse()
                        board.make_human_move(one_click)
                        break
            print(board.board)
            board.close()

            # create output dialog
            result_win = GraphWin("Result", 120, 150)
            result_win.setBackground("seashell")
            result_win.setCoords(0, 0, 120, 150)
            winner = board.check_winner()

            if winner == "O":
                text = Text(Point(60, 120), "AI wins!")
                ai_win += 1
            elif winner == "X":
                text = Text(Point(60, 120), "You win!")
                player_win += 1
            else:
                text = Text(Point(60, 120), "Tie!")
                tie += 1

            text.draw(result_win)

            # close the play board
            board.close()

            # AI score
            text_ai = Text(Point(60, 80), "AI wins: {}".format(ai_win))
            text_ai.draw(result_win)

            # player score
            text_player = Text(Point(60, 60), "Player wins: {}".format(player_win))
            text_player.draw(result_win)

            # tie score
            text_tie = Text(Point(60, 40), "Tie: {}".format(tie))
            text_tie.draw(result_win)

    # draw again the result win
    # create output dialog
    result_win = GraphWin("Result", 120, 150)
    result_win.setBackground("seashell")
    result_win.setCoords(0, 0, 120, 150)
    text = Text(Point(60, 120), "Game quited!")
    text.draw(result_win)

    # AI score
    text_ai = Text(Point(60, 80), "AI wins: {}".format(ai_win))
    text_ai.draw(result_win)

    # player score
    text_player = Text(Point(60, 60), "Player wins: {}".format(player_win))
    text_player.draw(result_win)

    # tie score
    text_tie = Text(Point(60, 40), "Tie: {}".format(tie))
    text_tie.draw(result_win)

    # get one more click to quit
    result_win.getMouse()
    result_win.close()
    board.close()


if __name__ == "__main__":
    main()
