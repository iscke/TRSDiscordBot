import random, json

class Card:
    def __init__(self, rank, suit=None):
        '''
        Valid Suits:
        spades
        diamonds
        clubs
        hearts
        Valid Cards:
        ace
        two/three/four/five/six/seven/eight/nine/ten
        jack
        queen
        king
        joker (no suit)
        '''
        self.rank = rank
        self.suit = suit
        if self.suit:
            self.name = f"{rank.capitalize()} of {suit.capitalize()}"
        else:
            self.name = rank.capitalize()

    def jsonize(self):
        if self.suit:
            return f"{self.rank},{self.suit}"
        else:
            return "joker"

    def __str__(self):
        return self.name

class Deck:
    def __init__(self, deck=None, name=None):
        self.name = name
        self.deck = deck

    def generate(self, jokers=True):
        self.deck = [Card("joker"), Card("joker")]
        for suit in ["spades","diamonds","clubs","hearts"]:
            for rank in ["ace","two","three","four","five","six","seven","eight","nine","ten","jack","queen","king"]:
                self.deck.append(Card(rank, suit))
                
    def shuffle(self):
        random.shuffle(self.deck)
        return True

    def draw(self, amount):
        cards = []
        for index in range(amount):
            cards.append(self.deck[index])
        for _ in range(amount):
            self.deck.pop(0)
        return cards

    def jsonize(self):
        return [i.jsonize() for i in self.deck]


class DeckHandler:
    def __init__(self):
        self.decks = {}

        json_decklist = {}
        try:
            with open("deck.json") as f:
                json_decklist = json.load(f)
        except FileNotFoundError:
            pass

        #Load the decks from string formatted json into our local objects Card, Deck
        for deck_name in json_decklist.keys():
            #iterate through each deck and create an object for each
            json_deck = json_decklist[deck_name]
            new_deck = []
            
            for card in json_deck:
                #iterate through cards
                card_info = card.split(',') #formatted rank,suit OR joker
                if len(card_info) == 2:
                    new_deck.append(Card(card_info[0], suit=card_info[1]))
                else: #joker
                    new_deck.append(Card("joker"))
            self.decks[deck_name] = Deck(deck=new_deck, name=deck_name)

    async def handle(self, args):
        return_message = "Please specify what you would like to do: create, shuffle, save"
        if len(args) > 0:
            #This command has subcommands, which are listed here
            #Validation and the command is generally handled in the side there. validation could be separated.
            if args[0] == 'create':
                return_message = self.command_create(args[1:])

            if args[0] == 'shuffle':
                return_message = self.command_shuffle(args[1:])

            if args[0] == 'list':
                return_message = self.command_list(args[1:])

            if args[0] == 'save':
                return_message = self.command_save(args[1:])

            if args[0] == 'draw':
                return_message = self.command_draw(args[1:])

        return return_message

    def command_create(self, args):
        if len(args) > 0:
            name = args[0]
            if name in self.decks:
                return_message = "This deck already exists. Please delete it first or use a different name."
            else:
                deck = Deck(name=name)
                deck.generate()
                self.decks[name] = deck
                return_message = f'A new deck "{name}" was created.'
        else:
            return_message = "Please provide a name to refer to this deck."
        return return_message

    def command_shuffle(self, args):
        if len(args) > 0:
            name = args[0]
            if name in self.decks:
                self.decks[name].shuffle()
                return_message = "The deck has been shuffled. Beware, the chances of it still being in the same order are 1/10^68!"
            else:
                return_message = "The deck could not be found."
        else:
            return_message = "Please give the name of the deck."
        return return_message

    def command_list(self, args):
        decks = [i for i in self.decks.keys()]
        total = len(decks)
        if total > 1:
            return_message = f"You have {str(total)} decks: {', '.join(decks)}"
        elif total == 0:
            return_message = "You don't have any decks."
        else:
            return_message = f"You have 1 deck: {decks[0]}"
        return return_message

    def command_save(self, args):
        jsonized_decks = {}
        for deck_name in self.decks.keys():
            jsonized_decks[deck_name] = self.decks[deck_name].jsonize()
        with open("deck.json",'w') as f:
            json.dump(jsonized_decks, f)
        return "The current deck list was saved. It will be loaded automatically upon starting the bot." 

    def command_draw(self, args):
        return_message = "Please enter the deck name and number of cards to draw."
        if len(args) > 0:
            name = args[0]
            if name in self.decks:
                if len(args) > 1:
                    if args[1].isdigit():
                        draw_amount = int(args[1])
                        #validation done:
                        cards = self.decks[name].draw(draw_amount)
                        string_cards = '\n'.join([card.name for card in cards])
                        return_message = f"Cards drawn:\n{string_cards}"
                else:
                    #validation done:
                    card = self.decks[name].draw(1)[0]
                    return_message = f"Card drawn:\n{card.name}"

            else:
                return_message = "The deck could not be found."
        return return_message