import random


colors_all = ['Red', 'Green', 'Yellow', 'Blue', 'Black', 'Orange']
cards_all = ['A','B','C','D','E']
players_all = ['P1', 'P2', 'P3', 'P4', 'P5']
hint_count = 8
mistake_count = 3

class Player:
    def __init__(self, num_of_cards, num_of_players, num_of_colors):
        num_of_cards = num_of_cards
        num_of_players = num_of_players
        num_of_colors = num_of_colors
        knowledge = []
        pile_dict, discard_dict, color_cards,val_cards = initialize_dicts(num_of_cards, num_of_players, num_of_colors)


def initialize_dicts(nca, npl, nco):
    pile_dict = {}
    discard_dict = {}
    color_cards = {}
    val_cards = {}
    colors = colors_all[:nco]
    cards = cards_all[:npl]
    col_dict = {}
    val_dict = {}
    for col in colors:
        pile_dict[col] = {'1': 3, '2': 2, '3': 2, '4': 2, '5': 1}
        discard_dict[col] =  {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
        col_dict[col] = 0
    for card in cards:
        color_cards[card] = col_dict
        val_cards[card] = {'1': 0, '2':0, '3':0, '4':0, '5':0}
    return pile_dict, discard_dict, color_cards,val_cards;

class Game:
    def __init__(self, num_of_cards, num_of_players, num_of_colors):
        self.num_of_cards = num_of_cards
        self.num_of_players = num_of_players
        self.num_of_colors = num_of_colors
        self.player_list = []
        self.player_cards = []
        self.colors = colors_all[:num_of_colors]
        self.cards = cards_all[:num_of_players]
        self.pile_dict, self.discard_dict, cc,nc = initialize_dicts(num_of_cards, num_of_players, num_of_colors)
        for i in range(0, num_of_players):
            self.player_list = self.player_list + [Player(self.num_of_cards, self.num_of_players, self.num_of_colors)]
            this_player_cards = []
            for j in range(0, num_of_cards):
                col,val = self.pick_new_card()
                this_player_cards = this_player_cards + [[col,val]]
            self.player_cards = self.player_cards + [this_player_cards]

    def pick_new_card(self):
        possible_cards_c = []
        possible_cards_v = []
        for col,cards in self.pile_dict.items():
            for val,occ in cards.items():
                for i in range(0,occ):
                    possible_cards_c = possible_cards_c + [col]
                    possible_cards_v = possible_cards_v + [val]
        ind = random.randint(0,len(possible_cards_c))
        return possible_cards_c[ind], possible_cards_v[ind]

game = Game(4,4,3)
print(game.player_cards)
