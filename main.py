#UNDER CONSTRUCTION; NOT FINISHED
#PLAY THE GAME HERE: https://repl.it/@GoogleAdmin/BlackJack

from random import random, randint
from time import sleep
from math import floor

def assign(amt,lst=['d','h','c','s']):
    m = []
    royal = ["J","Q","K","A"]
    for e in range(len(lst)):
        idt = lst[e]
        for i in range(2,(amt//len(lst))+2):
            if i >= 11:
                m.append(royal[i-11] + idt)
            else:
                m.append(str(i) + idt)
    return m

def hChance(n,jump,s):
  return random() < ((n-s) / jump )**3

#s = 21 jump = 11 n = self.sum

class BlackJack:
    Deck = assign(52)
    s = 0
    def __init__(self,fm = random() < 0.5):
        self.fm = fm
        self.c = 0
        self.cs = 0
        self.hs = 0

    def hit(self,hitting=True):
        self.Hand = []
        gAmt = floor(int(input("How many games would you like to play? "))/2)
        while hitting or (self.hs >= gAmt or self.cs >= gAmt):
            print(f'Current Challenge: {self.c if self.c else "null"}')
            self.Hand += [self.Deck.pop(randint(0,len(self.Deck)-1))]
            self.s = 0
            for e in self.Hand:
                if e[0] in ['Q','K','J']:
                    self.s += 10
                elif e[0] == 'A':
                    self.s += 11
                else:
                    self.s += int(e[0])
            print(self.Hand)
            print(self.s)
            if self.s == 21:
                if self.fm:
                    print("You won!")
                    self.hs += 1
                else:
                    print("Seems like the computer has hit the magic number! So sorry!")
                    self.cs += 1
                return True if self.fm else False
            if self.s > 21:
                if self.fm:
                    print("You lost!")
                    self.cs += 1
                else:
                    print("You won! Computer busted!")
                    self.hs += 1
                return False if self.fm else True
            hitting = input("Would you like to continue hitting? ").upper().startswith('Y') if self.fm else hChance(21,11,self.s)
           # print(hitting)
        self.c = self.s
        self.fm = not self.fm
        self.next()

    def next(self):
        if self.fm:
            print(f"The computer currently has {self.c} points. You must either score higher than this or equivalent. Good luck.")
        else:
            print(f"You scored {self.c} points. If the computer scores higher, it wins!")
        sleep(3)
        print(self.fm)
        self.hit()

class Human(BlackJack):
    def __init__(self,bal=1000,wd=0,dep=0,bet=0):
        super().__init__()
        self.balance = bal
        self.balance += dep
        while wd > self.balance:
            try:
                wd = int(input(f"Please enter a number less than or equal to {self.balance}: "))
            except ValueError:
                pass
        self.balance -= wd

        self.bet = bet

    def influx(self,dep):
        self.balance += dep
        print(f"Your balance is now {self.balance}")

    def bet(self):
        pass



class Computer(BlackJack):
    def __init__(self):
        super().__init__()
        if not self.fm:
            self.hit()
        else:
            h = Human(wd=int(input("What value of money would you like to use? ")))
            h.hit()
        pass


b = BlackJack()
h = Human(wd=100)
c = Computer()
