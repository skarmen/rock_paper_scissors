#!/usr/bin/env python3
import random
"""
If both players picked the same move, there is no winner. Otherwise, rock
beats scissors; paper beats rock; and scissors beat paper.
Players can play a single round, or "best of three".
"""
"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""
moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""
# set to false to suppress debug output
DEBUG = False


def debug(*args, **kwargs):
    if DEBUG:
        print('DEBUG', *args, **kwargs)


class Player:
    def __init__(self):
        self.score = 0

    def move(self):
        _move = 'rock'
        print(f"Opponent played {_move}")
        return _move

    def learn(self, my_move, their_move):
        pass


class RandomPlayer(Player):
    def move(self):
        _move = random.choice(moves)
        print(f"Opponent played {_move}")
        return _move


class HumanPlayer(Player):
    def move(self):
        while True:
            choice = input("Rock, paper, scissors?").lower()
            if choice == "rock":
                print("You played rock.")
                return choice
            elif choice == "paper":
                print("You played paper.")
                return choice
            elif choice == "scissors":
                print("You played scissors.")
                return choice
            else:
                print("Please enter a valid choice: ")


class ReflectPlayer(Player):
    def __init__(self):
        super().__init__()
        """
        We need to initialize the value of the property self.their_last_move
        before we can use it. Because the learn() method is onyl called after
        the first move, we need to set it to something here otherwise you'll
        have an attribute error(.their_last_move is not defined)
        """
        self.their_last_move = "rock"

    def learn(self, my_move, their_move):
        """
        The purpose of this function is to remember the value of their_move.
        It does this by assigning the value of their_move, which is passed into
        this function, to the property self.their_last_move, so that we can
        refer to it later on in the move() method.
        """
        self.their_last_move = their_move
        debug("ReflectPlayer.learn() their_move: ", their_move)

    def move(self):
        debug('ReflectPlayer.move()')
        print(f"Opponent played {self.their_last_move}")
        return self.their_last_move


class CyclePlayer(Player):
    def __init__(self):
        super().__init__()
        self.my_last_move = "rock"

    def learn(self, my_move, their_move):
        self.my_last_move = my_move

    def move(self):
        """
        We can define the behaviour of this method by creating a dictionary
        that maps the value of self.my_last_move (a string) to the next move
        (also a string) that we want to play, for every possible value of
        self.my_last_move.
        Then, in order to get the next move, all we need to do is look up the
        value in the dictionary whose key is the current value of
        self.my_last_move.
        """
        move_by_last_move = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock"
        }
        _move = move_by_last_move[self.my_last_move]
        print(f"Opponent played {_move}")
        return _move


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


def to_play_again():
    """ Get the valid_input for play_again"""
    play_again = input("Would you like to play again? (y/n)")
    if play_again == 'y':
        print("Excellent! Restarting the game...")
        main()  # restart the game ( call the main function + intro)
    elif play_again == 'n':
        print("Thanks for playing! See you next time.")
    else: 
        to_play_again()


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def play_round(self):
        debug('moving p1')
        move1 = self.p1.move()
        debug('moving p2')
        move2 = self.p2.move()
        print(f"Player 1: {move1}  Player 2: {move2}")
        if move1 == move2:
            print("** TIE **")
        elif beats(move1, move2):
            print("** PLAYER ONE WINS**")
            self.p1.score += 1
        elif beats(move2, move1):
            print("** PLAYER TWO WINS **")
            self.p2.score += 1
        else:
            print('Invalid move')
            assert 0
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)
        print(f"Score: Player One: {self.p1.score} Player2: {self.p2.score }")

    def play_game(self):
        print("Game start!")
        for round in range(3):
            print(f"Round {round}:")
            self.play_round()
        print("Game over!")
        print(f"Score: Player One: {self.p1.score} Player2: {self.p2.score }")
        if self.p1.score > self.p2.score:
            print("** PLAYER ONE WON THE GAME **")
        elif self.p1.score < self.p2.score:
            print("** PLAYER TWO WON THE GAME **")
        else:
            print("The game is tie.")
        to_play_again()


def main():
    choice = HumanPlayer()
    choice2 = ReflectPlayer()
    #game = Game(choice, choice2)
    #game.play_game()
    
    players = [HumanPlayer(), ReflectPlayer(), CyclePlayer()]
    choice = random.choice(players)
    choice2 = random.choice(players)
    
    game = Game(choice, choice2)
    game.play_game()
    

if __name__ == '__main__':
    main()
