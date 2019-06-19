
import random
import numpy as np

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

    def select_action(self,possibility_tables,playable_cards,possible_cards,dead_cards,hint_count):
        if not self.check_whether_playable_card(possibility_tables,playable_cards)[0] == -1:
            return ['PLAY', self.check_whether_playable_card(possibility_tables,playable_cards)]
        elif (np.sum(playable_cards) + (50-np.sum(np.sum(possible_cards)))) < 5 and self.check_dead_card(possibility_tables,dead_cards) >= 0:
            return ['DISCARD', self.check_dead_card(possibility_tables,dead_cards)]
        elif hint_count > 0:
            return ['HINT']
        elif self.check_dead_card(possibility_tables,dead_cards) >= 0:
            return ['DISCARD', self.check_dead_card(possibility_tables,dead_cards)]
        elif self.check_whether_card_known_duplicate(possibility_tables):
            return["DON'T FORGET TO IMPLEMENT STEP 5 IN ALGORITHM"]
        elif self.check_whether_dispensable_card_known(possibility_tables):
            return["DON'T FORGET TO IMPLEMENT STEP 6 IN ALGORITHM"]
        else:
            return['DISCARD',0]
        action = 'PASS'
        return action

    def check_whether_playable_card(self,possibility_tables,playable_cards):
        for card in range(0,4):
            if np.sum(np.sum(possibility_tables[self.id,card,:,:])) == 1:
                play_card_col, play_card_val = np.where(possibility_tables == 1)
                if playable_cards[play_card_col] == play_card_val:
                    return [card,play_card_col, play_card_val]
        return [-1,-1]

    def check_dead_card(self, possibility_tables, dead_cards):
        for card in range(0,4):
            possibly_all_dead = True
            for color in range(0,5):
                for value in range(0,5):
                    if possibility_tables[self.id,card,color,value] != 0 and value > dead_cards[color]:
                        possibly_all_dead = False
                        break
                if not possibly_all_dead:
                    break
            if possibly_all_dead:
                return card
        return -1

    def check_whether_card_known_duplicate(self,possibility_tables):
        return "still needs to be implemented!"

    def check_whether_dispensable_card_known(self,possibility_tables):
        return "still needs to be implemented!"



class Game:
    def __init__(self, nplayers, ncards, ncolors):
        self.colors_all = ['white', 'blue', 'red', 'green', 'yellow', 'orange']
        self.colors_all = self.colors_all[:ncolors]
        self.cardlist = [0,0,0,1,1,2,2,3,3,4]
        self.hint_count = 8
        self.mistake_count = 3
        self.score = 0
        self.play_token = 1
        self.nplayers = nplayers
        self.ncards = ncards
        self.ncolors = ncolors
        self.center = {}
        self.playable_cards = np.zeros((ncolors))
        self.dead_cards = np.zeros((ncolors)) -1
        print(self.playable_cards)
        self.discard_pile = []
        self.commondicts = {'center': self.center,
                            'discard_dict': self.discard_pile
                            }
        playerlist = self.create_players(self.nplayers, self.commondicts)
        self.playerlist = playerlist
        self.deck = self.create_deck(self.colors_all[0:self.ncolors+1], self.cardlist)
        self.possibility_tables = np.zeros((nplayers,ncards,ncolors,5)) + 1
        self.possible_cards = np.array([[3,2,2,2,1],[3,2,2,2,1],[3,2,2,2,1],[3,2,2,2,1],[3,2,2,2,1]])


# function that updates the number of cards still possible to have in your hand,
# for every card (i.e. not discarded or played)
    def update_possible_cards(self,card_color,card_value):
        self.possible_cards[card_color,card_value] -= 1
        # if the number of cards of this type becomes equal to 0, this is common
        # knowledge and this card is for no one possible to have in their hand
        if self.possible_cards[card_color, card_value] == 0:
            self.possibility_tables[:,:,card_color, card_value] = 0

# Hints also have to be incorporated wordly
    def incorporate_hint_wordly(self,player,card,value_color,color_hint):
        if color_hint:
            for color in range(0,self.ncolors):
                if color != value_color:
                    self.possibility_tables[player,card,color,:] = 0
        else:
            for value in range(0,5):
                if value != value_color:
                    self.possibility_tables[player,card,:, value] = 0

# return the cards that are targeted this round
    def return_targeted_cards(self):
        targeted_cards = np.zeros((self.nplayers))
        for player in range(0,self.nplayers):
            cards = np.zeros((self.ncards))
            for card in range(0,self.ncards):
                ncards = 0
                nplayable_cards = 0
                for color in range(0,self.ncolors):
                    for value in range(0,5):
                        if self.possibility_tables[player,card,color,value] == 1:
                            ncards += self.possible_cards[color,value]
                            if self.playable_cards[color] == value:
                                nplayable_cards += self.possible_cards[color,value]
                cards[card] = nplayable_cards/ncards
                # print(nplayable_cards)
            targeted_cards[player] = int(np.argmax(cards))
        return targeted_cards

    def targeted_cards_to_hints(self, targeted_cards):

        hint_tables = np.zeros((self.nplayers,self.ncolors,5))
        for player in range(0,self.nplayers):
            # print(targeted_cards[player])
            hint_table = self.possibility_tables[player,int(targeted_cards[player]),:,:] -1
            hintnum = 1
            for value in range(0,5):
                for color in range(0,self.ncolors):
                    if hint_table[color,value] == 0 and self.dead_cards[player] < value:
                        hint_table[color,value] = hintnum
                        if hintnum != 7:
                            hintnum += 1
            u, counts = np.unique(hint_table, return_counts = True)

            if len(counts) ==7:
                if counts[6] > 8:
                    seven_surplus = counts[6]-8
                    six_surplus = 0
                    if seven_surplus > 8:
                        six_surplus = seven_surplus-7
                        seven_surplus = 8
                    for value in range(0,5):
                        for color in range(0,self.ncolors):
                            if (hint_table[color,value] == 7 or hint_table[color,value] == 6) and six_surplus > 0:
                                hint_table[color,value] = 5
                                six_surplus -= 1
                            elif hint_table[color,value] == 7 and seven_surplus >0:
                                hint_table[color,value] = 6
                                seven_surplus -= 1
            hint_tables[player,:,:] = hint_table
        return hint_tables




    def create_players(self, nplayers, commondicts):
        playerlist = {}
        pids = range(0,self.nplayers)
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

    def play_hint(self, origin_player_id,targeted_cards,hint_tables):
        sum = 0
        for coplayers in range(0,self.nplayers):
            if coplayers != origin_player_id:
                hand = self.playerlist.get(coplayers).hand
                # print ('Handsan:',[c for c in hand])
                card_index = targeted_cards[coplayers]
                # print(card_index)
                hint_table = hint_tables[coplayers,:,:]
                true_card = hand[int(card_index)]
                color_int = self.colors_all.index(true_card[0])
                val = true_card[1]
                sum += hint_table[color_int,val]
        hintval = sum%8
        # print(hintval)
        hint = self.convert_val_to_hint(origin_player_id,hintval,targeted_cards)
        print(hint)

        self.hint_count = self.hint_count-1

    def convert_val_to_hint(self,player,hintval,targeted_cards):
        hint_player = (hintval%4 + player)%5
        hint_color = True
        if hintval < 4:
            hint_color = False
        hand = self.playerlist.get(hint_player).hand
        tg = targeted_cards[int(hint_player)]
        # TO DO: IMPLEMENT MOST INFORMATIVE WORDLY HINTS
        # prefer giving hints about colors or values with multiple occurences
        if hint_color:
            if tg != 1:
                return[1,hand[0][0]]
            else:
                return[2,hand[1][0]]
        else:
            if tg != 1:
                return[1,hand[0][1]]
            else:
                return[2,hand[1][1]]




    def play_card(self, player_id, card_to_play, color, value):
        self.dead_cards[color] += 1
        self.playable_cards[color] += 1
        self.update_possible_cards(color,value)
        for card in range(card_to_play,3):
            self.possibility_tables[player_id,card,:,:] = self.possibility_tables[player_id,card + 1,:,:]
        newcard = np.zeros((self.ncolors,5))
        newcard[np.where(self.possible_cards > 0)] = 1
        self.possibility_tables[player_id,3,:,:] = newcard
        self.playerlist.get(player_id).hand.pop(card_to_play)
        print('write a function for dealing a new card')

        ########### A NEW CARD NEEDS TO BE DEALT
        #remove card from player, draw card later
        self.score += 1

    def play_discard(self, player_id, card):
        self.discard_pile.append(card)


    def play_game(self):
        #select player to start
        self.turn_token = 0 #randomize
        self.incorporate_hint_wordly(2,3,1,True)
        self.incorporate_hint_wordly(3,0,0,False)
        self.incorporate_hint_wordly(1,2,3,True)
        # print(self.possibility_tables[4,0])
        tg = self.return_targeted_cards()
        print(self.targeted_cards_to_hints(tg))
        #loop till you out of tokens
        while self.mistake_count>=0:

            #Update player info
            self.update_player_info()
            targeted_cards = self.return_targeted_cards()
            hint_tables = self.targeted_cards_to_hints(targeted_cards)
            #Call to player for action
            this_act = self.playerlist.get(self.turn_token).select_action(self.possibility_tables,self.playable_cards,self.possible_cards, self.dead_cards,self.hint_count)
            #get all details required for action
            if this_act[0] == 'PLAY':
                self.play_card(self.turn_token, this_act[1], this_act[2], this_act[3])
            elif this_act[0] == 'HINT':
                self.play_hint(self.turn_token, targeted_cards,hint_tables)
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
            self.turn_token += 1
            if self.turn_token == self.nplayers:
                self.turn_token = 0



def gameloop():
    manager = Game(5,4,5)
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
manager = Game(5,4,5)
print (manager.playerlist)
manager.deal_initial()
manager.print_player_info()
manager.play_game()
