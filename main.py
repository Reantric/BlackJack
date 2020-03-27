from random import random, randint
import math
from time import sleep


def assign(amt, lst=['d', 'h', 'c', 's']):
    m = []
    royal = ["J", "Q", "K", "A"]
    for e in range(len(lst)):
        idt = lst[e]
        for i in range(2, (amt // len(lst)) + 2):
            if i >= 11:
                m.append(royal[i - 11] + idt)
            else:
                m.append(str(i) + idt)
    return m


def check(inp, Error):
    while True:
        try:
            r = inp
            break
        except Error:
            continue
    return r


def hChance(n):
    val = math.ceil(1 / (1 + math.exp(2.5 * (n - 15))) * 100000) / 100000
    # print(f"P(hit) is now {val} ({val * 100}%)")
    return random() < val


# s = 21 jump = 11 n = self.sum

class BlackJack:
    currentGame = 0
    hWins = 0
    cWins = 0

    def __init__(self, human, gAmt=-1, fm=random() < 0.5):
        self.gameOn = gAmt
        self.fm = fm
        self.h = human
        self.c = Computer()
        self.Deck = assign(52)

    def deal(self):
        return self.Deck.pop(randint(0, len(self.Deck) - 1))

    def setGameAmt(self, amt):
        self.gameOn = amt

    @staticmethod
    def sumHand(Hand):
        s = 0
        for e in Hand:
            if e[0] in ['Q', 'K', 'J'] or e[0:2] == "10":
                s += 10
            elif e[0] == 'A':
                s += 11
            else:
                s += int(e[0])
        return s

    @staticmethod
    def winCheck(Hand):
        s = BlackJack.sumHand(Hand)
        if s > 21:
            return False
        return None if s < 21 else True

    def reset(self):
        self.Deck = assign(52)
        self.h.reset()
        self.c.reset()

    def play(self):
        # print(self.fm)
        while self.gameOn == -1 or self.currentGame < self.gameOn:
            #    print(f"Playing game {self.currentGame + 1} {self.fm}")
            if self.fm:  # Human goes first
                self.h.play()
                self.c.play()

            else:
                if self.h.hasWon is not None:
                    self.c.play(self.h.finalSum)
                else:
                    self.c.play()
                self.h.play()

            sleep(1)

            print(f"Game: {self.currentGame + 1}")
            if self.h.finalSum == self.c.finalSum:
                print("Tie.\n")
            elif self.h.finalSum > self.c.finalSum:
                print("You win!\n")
                self.hWins += 1
            else:
                print("Computer win!\n")
                self.cWins += 1

            sleep(3)
            self.currentGame += 1
            self.reset()

            print(f"Current score: (H:C) {self.hWins}:{self.cWins} \n")

        if self.hWins == self.cWins:
            print(f"It was a tie! {self.hWins}:{self.cWins}")
            return None
        elif self.hWins > self.cWins:
            print(f"You beat the computer by a score of {self.hWins}:{self.cWins}")
            return True
        else:
            print(f"The computer beat you by a score of {self.hWins}:{self.cWins}")
            return False


class Entity:

    def __init__(self):
        self.Hand = []
        self.finalSum = 0
        self.hitting = True  # able to still hit?!
        self.hasWon = None

    def hit(self):
        self.Hand += [b.deal()]

    def reset(self):
        self.Hand = []
        self.hitting = True
        self.hasWon = None
        self.finalSum = 0


class Human(Entity):
    def __init__(self, bal=1000, wd=0, dep=0):
        super().__init__()
        self.balance = bal
        self.balance += dep
        while wd > self.balance:
            try:
                wd = int(input(f"Please enter a number less than or equal to {self.balance}: "))
            except ValueError:
                pass
        self.balance -= wd

    def influx(self, dep):
        self.balance += dep
        print(f"Your balance is now {self.balance}")

    def start(self):
        gAmt = check(int(input("How many games would you like to play? (-1 for indefinite) ")), ValueError)

        if gAmt != -1:
            betAmt = check(int(input("How much money would you like to bet? (Cannot bet over your initial money!) ")),
                           ValueError)
            while betAmt > self.balance:
                betAmt = check(int(input("How much money would you like to bet? (Cannot bet over your initial money!) ")),
                               ValueError)

            b.setGameAmt(gAmt)

            if b.play():
                self.influx(betAmt)
            elif not b.play() and b.play() is not None:
                self.influx(-betAmt)
        else:
            b.play()

    def play(self):

        while self.hitting:
            self.hit()
            self.hasWon = BlackJack.winCheck(self.Hand)
            print(self.Hand, BlackJack.sumHand(self.Hand))

            if self.hasWon:
                print("Congratulations, you win!\n")
                self.finalSum = 21
                break

            if not self.hasWon and self.hasWon is not None:
                print("Unfortunately, you went over 21.\n")
                self.finalSum = 0
                break

            self.hitting = input("Do you wish to hit? \n").lower().startswith("y")
        else:
            self.finalSum = BlackJack.sumHand(self.Hand)
            print(f"\nYou finished with a score of {self.finalSum}\n")


class Computer(Entity):
    def __init__(self):
        super().__init__()

    def play(self, HumanFinalSum=22):
        while self.hitting:
            self.hit()
            self.hasWon = BlackJack.winCheck(self.Hand)
            currentSum = BlackJack.sumHand(self.Hand)
            print(f"Computer Hand:{self.Hand}, Total sum: {currentSum}")
            self.hitting = currentSum < HumanFinalSum and hChance(currentSum)

            if self.hasWon:
                print("The computer wins!\n")
                self.finalSum = 21
                break

            if not self.hasWon and self.hasWon is not None:
                print("Computer has busted! You win!\n")
                self.finalSum = 0
                break

            sleep(2)
        else:
            self.finalSum = BlackJack.sumHand(self.Hand)
            print(f"\nThe computer finished with a score of {self.finalSum}\n")


h = Human()
b = BlackJack(h, gAmt=-1)
h.start()