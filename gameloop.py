
import random

class Card:
    def __init__(self, color, number, id):
        self.color = color
        self.number = number
        self.id = id
        self.known_color = False
        self.known_number = False

class Player:
    def __init__(self, id, hand, otherplayers, commondicts):
        self.id = id
        self.hand = hand
        self.otherplayers = otherplayers
        self.commondicts = commondicts
        self.known_hand = [('black',0),('black',0),('black',0),('black',0)] #0 is unknown, so is black

    def update_info(self, otherplayers, commondicts):
        self.otherplayers = otherplayers
        self.commondicts = commondicts

    def select_action(self):
        action = 'PASS'
        return action

class Game:
    def __init__(self, nplayers, ncards, ncolors):
        self.colors_all = ['white', 'blue', 'red', 'green', 'yellow', 'orange']
        self.cardlist = [1,1,1,2,2,3,3,4,4,5]
        self.hint_count = 8
        self.mistake_count = 3
        self.score = 0
        self.play_token = 1
        self.nplayers = nplayers
        self.ncards = ncards
        self.ncolors = ncolors
        self.center = {}
        self.discard_pile = []
        self.commondicts = {'center': self.center,
                            'discard_dict': self.discard_pile
                            }
        playerlist = self.create_players(self.nplayers, self.commondicts)
        self.playerlist = playerlist
        self.deck = self.create_deck(self.colors_all[0:self.ncolors+1], self.cardlist)


    def create_players(self, nplayers, commondicts):
        playerlist = {}
        pids = range(1,self.nplayers+1)
        for pid in pids:
            otherplayers = {}
            others = [p for p in pids if p is not pid]
            for other in others:
                otherplayers.update({other:[]})
            #print (otherplayers)
            playerlist.update({pid:Player(id=pid, hand=[], commondicts=commondicts, otherplayers=otherplayers)})
        return playerlist

    def create_deck(self, colors, cardlist):
        deck = []
        id = 1
        for c in colors:
            for n in cardlist:
                #newcard = Card(id = id, color=c, number=int(n))
                newcard = [c,n]
                deck.append(newcard)
                random.shuffle(deck)
                id+=1
        return deck

    def deal_initial(self):
        for i in range(1, self.ncards+1):
            pids = self.playerlist.keys()
            for j in pids:
                self.deal_card(pid=j)
        return True

    def deal_card(self, pid): #Currently being corrected
        if (len(self.playerlist.get(pid).hand) < self.ncards):
            card = self.deck.pop()
            playerinfo = self.playerlist.get(pid)
            h = playerinfo.hand.append(card)
        else:
            print ('Hand already full')

    def print_player_info(self):
        for id in self.playerlist.keys():
            print('Player ID: ',id)
            this_player = self.playerlist.get(id)
            #print ('Hand:',[[c.color,c.number] for c in this_player.hand])
            print ('Hand:',[c for c in this_player.hand])

    def update_player_info(self):
        commondicts = self.commondicts
        for pid in self.playerlist.keys():
            thisplayer = self.playerlist.get(pid)
            othersdict = {}
            others = [x for x in self.playerlist.keys() if x is not pid]
            for other in others:
                h = self.playerlist.get(other).hand
                othersdict.update({other:h})
            #print (othersdict)
            thisplayer.update_info(otherplayers=othersdict, commondicts=commondicts)

    def play_hint(self, origin_player_id, target_player_id, hint):
        self.hint_count = self.hint_count-1

    def play_card(self, player_id, card):
        #remove card from player, draw card later
        self.score += 1

    def play_discard(self, player_id, card):
        self.discard_pile.append(card)


    def play_game(self):
        #select player to start
        self.turn_token = 1 #randomize

        #loop till you out of tokens
        while self.mistake_count>=0:
            #Update player info
            self.update_player_info()

            #Call to player for action
            this_act = self.playerlist.get(self.turn_token).select_action()
            #get all details required for action
            print (this_act)

            if this_act == 'HINT':
                self.play_hint()
            if this_act == 'DISC':
                self.play_discard()
            if this_act == 'PLAY':
                self.play_card()
            else:
                self.play_token = self.play_token+1 if self.play_token != self.nplayers else 1

            self.mistake_count-=1



def gameloop():
    manager = Game(4,4,3)
    print (manager.playerlist)
    manager.deal_initial()
    manager.print_player_info()
    manager.play_game()
    #get latest game elements
    #decide action
        #hint
        #discard
        #play
        #updates lie within action code
    #next turn

#gameloop()
manager = Game(4,4,3)
print (manager.playerlist)
manager.deal_initial()
manager.print_player_info()
manager.play_game()