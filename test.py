#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Angie
#
# Created:     17/11/2012
# Copyright:   (c) Angie 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from tkinter import *
from random import random

root = Frame()
root.pack()
root.config(padx = 100, pady = 100)

class GameState:
    def __init__(self, goal = 10, p1="Player 1", p2 = "Player 2"):
        self.p1name, self.p2name = p1, p2
        self.p1turn, self.goal = True, goal
        self.p1score, self.p2score = 0, 0

    def take_turn(self, correctbutton, selectedbutton):
        if correctbutton == selectedbutton:
            score = 1
        else:
            score = 0
        if self.p1turn:
            self.p1score += score
        else:
            self.p2score += score
        if not self.over:
            self.p1turn = not self.p1turn
        return score

    @property
    def p1(self):
        return 'P1: {} Points: {}'.format(self.p1name, self.p1score)

    @property
    def p2(self):
        return 'P2: {} Pts: {}'.format(self.p2name, self.p2score)

    @property
    def winner(self):
        return None if not self.over else self.p1name if self.p1turn \
                    else self.p2name

    @property
    def over(self):
        return max(self.p1score, self.p2score) >= self.goal

class GUI:
    def __init__(self, frame, state):
        self.state = state
        self.status = Label(frame, font=text_font)
        self.dex_num = self.get_num(len(imgs)-1)
        self.init_pokemon(frame, self.dex_num)
        self.init_player_labels(frame)


        self.init_buttons(frame)
        self.status.pack()

        self.display_state()

    def get_num(self, num):
        num = random() *  num + 1
        decimal = num % 1
        while decimal >= 1:
            decimal = decimal % 1
        num = int(num - decimal)
        if decimal >= .5:
            return num + 1
        return int(num)

    def display_state(self):
        """Updates the scores of both players at the current state of
        the game."""
        # Q2: updating scores
        self.p1_label.config(text=self.state.p1)
        self.p2_label.config(text=self.state.p2)
        if self.state.p1turn:
            self.p1_label.config(**focused)
            self.p2_label.config(**unfocused)
        else:
            self.p1_label.config(**unfocused)
            self.p2_label.config(**focused)

    def display_end(self):
        """Display the winner of the game in the status bar."""
        assert self.state.over, 'Who cheats to end a Pokemon game?'
        # Q4: displaying the winner in self.status
        self.status.config("The winner is " + str(self.state.winner) + "!")

    def take_turn(self, name):
        if self.state.over:
            return
        score = self.state.take_turn(self.name, name)
        self.display_status(not self.state.p1turn, score)

    def display_status(self, p1_scored, score):
        """Displays the status (i.e. what a player scored)"""
        msg = '{} scored {} points'
        if p1_scored:
            self.status.config(text=msg.format(self.state.p1name,
                                               score))
        else:
            self.status.config(text=msg.format(self.state.p2name,
                                               score))

    #INITIALIZATIONS
    def init_pokemon(self, master, num):
        self.image = Label(master,
                            image = imgs[self.dex_num])
        self.name = names[self.dex_num-1]
        self.image.pack()

    def init_player_labels(self, master):
        self.p1_label = Label(master,
                              font=text_font,
                              borderwidth=5,
                              padx=25,
                              text=str(state.p1))
        self.p2_label = Label(master,
                              font=text_font,
                              borderwidth=5,
                              padx=25,

                              text=str(state.p2))
        self.p1_label.pack(side=TOP)
        self.p2_label.pack(side=TOP)

    def init_buttons(self, master):
        self.entry_button = Button(master,
                                   text=self.name,
                                   font=text_font,
                                   bg=button_bg,
                                   command=self.take_turn(self.name))
        ans = [self.entry_button]
        others = self.pick_others(master, self.dex_num)
        for name in others:
            ans.append(Button(master,
                            text=name,
                            font=text_font,
                            bg=button_bg,
                            command=self.take_turn(name)))
        ans = self.randomize_buttons(master, ans)
        for button in ans:
            button.pack(side=BOTTOM)

    def pick_others(self,master, num):
        copy = list(names)
        copy.remove(self.name)
        ans = []
        for _ in range(3):
            num = self.get_num(len(copy) - 1) - 1
            ans.append(copy[num])
            copy.remove(copy[num])
        return ans

    def randomize_buttons(self, master, buttons):
        ans = []
        while len(buttons) > 0:
            pick = self.get_num(len(buttons)- 1) - 1
            ans.append(buttons[pick])
            buttons.remove(buttons[pick])
        return ans

def make_image_dictionary():
    ans = {}
    for num in range(1,26):
        ans[num] = PhotoImage(file='images/'+ str(num) + '.gif')
    return ans

def make_name_dictionary():
    text = open('names.txt').read()
    text = text.split()
    return text

def handle_button():
    print("Button pushed.")


imgs = make_image_dictionary()
names = make_name_dictionary()

button_bg = '#66FFFF'
focused = {'bg': button_bg, 'relief': RAISED}
unfocused = {'bg': 'light grey', 'relief': FLAT}
text_font = ('Arial', 14, "bold")
game_start = {'goal': 10, 'p1': 'Player 1', 'p2': 'Player 2'}

state = GameState(**game_start)
gui = GUI(root, state)

#a = Label(root)
#pokeymon = int(random() * 24 + 1)
#a.config(image = imgs[pokeymon])
#button = Button(root, text = "Press me!", command = handle_button, bg = button_bg)
#button.pack()
#a.pack(side = LEFT)

root.mainloop()
