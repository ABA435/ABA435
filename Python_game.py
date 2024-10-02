import random

# Card and DeckOfCards classes you provided
class Card:
    FACES = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    def __init__(self, face, suit):
        self._face = face
        self._suit = suit

    @property
    def face(self):
        return self._face

    @property
    def suit(self):
        return self._suit

    @property
    def value(self):
        """Return a numeric value for comparing cards."""
        return Card.FACES.index(self._face)

    def __repr__(self):
        return f"Card(face='{self.face}', suit='{self.suit}')"

    def __str__(self):
        return f'{self.face} of {self.suit}'

    def __format__(self, format):
        return f'{str(self):{format}}'


class DeckOfCards:
    NUMBER_OF_CARDS = 52  # constant number of Cards

    def __init__(self):
        self._current_card = 0
        self._deck = [Card(Card.FACES[i % 13], Card.SUITS[i // 13]) for i in range(DeckOfCards.NUMBER_OF_CARDS)]

    def shuffle(self):
        self._current_card = 0
        random.shuffle(self._deck)

    def deal_card(self):
        if self._current_card < len(self._deck):
            card = self._deck[self._current_card]
            self._current_card += 1
            return card
        return None

    def __str__(self):
        s = ''
        for index, card in enumerate(self._deck):
            s += f'{self._deck[index]:<19}'
            if (index + 1) % 4 == 0:
                s += '\n'
        return s


# Player class to manage player actions
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.tricks_won = 0

    def receive_card(self, card):
        self.hand.append(card)

    def play_card(self, card_index):
        return self.hand.pop(card_index)

    def bid(self, bid_amount):
        """Player makes a bid"""
        return bid_amount

    def show_hand(self):
        return ', '.join(str(card) for card in self.hand)

    def __str__(self):
        return self.name


# Game class to manage the overall flow
class TarneebGame:
    def __init__(self, players):
        self.players = players
        self.deck = DeckOfCards()
        self.trump_suit = None
        self.bids = {}

    def start_game(self):
        self.deck.shuffle()
        self.deal_cards()
        self.bidding_phase()
        self.play_rounds()

    def deal_cards(self):
        for _ in range(13):
            for player in self.players:
                player.receive_card(self.deck.deal_card())

    def bidding_phase(self):
        """Simplified bidding logic"""
        highest_bid = 0
        highest_bidder = None
        for player in self.players:
            bid = player.bid(random.randint(7, 13))  # Random bid for simplicity
            print(f'{player} bids {bid}')
            if bid > highest_bid:
                highest_bid = bid
                highest_bidder = player

        self.trump_suit = random.choice(Card.SUITS)  # Trump suit chosen by highest bidder (simplified)
        print(f'{highest_bidder} wins the bid with {highest_bid} and chooses {self.trump_suit} as Tarneeb.')
        self.bids[highest_bidder] = highest_bid

    def play_rounds(self):
        """Simulate the 13 rounds of the game"""
        for round_number in range(13):
            print(f'\nRound {round_number + 1}:')
            cards_played = []
            leading_suit = None

            for player in self.players:
                card = player.play_card(0)  # Simplified; player plays the first card
                cards_played.append((player, card))

                if leading_suit is None:
                    leading_suit = card.suit
                print(f'{player} plays {card}')

            # Determine winner of the trick
            winning_card = self.determine_winning_card(cards_played, leading_suit)
            winner = next(player for player, card in cards_played if card == winning_card)
            winner.tricks_won += 1
            print(f'{winner} wins the round with {winning_card}')

        self.calculate_scores()

    def determine_winning_card(self, cards_played, leading_suit):
        trump_cards = [card for player, card in cards_played if card.suit == self.trump_suit]
        leading_cards = [card for player, card in cards_played if card.suit == leading_suit]

        if trump_cards:
            return max(trump_cards, key=lambda card: card.value)
        else:
            return max(leading_cards, key=lambda card: card.value)

    def calculate_scores(self):
        print("\nGame Over. Scores:")
        for player in self.players:
            print(f'{player}: {player.tricks_won} tricks won.')

        # Further scoring logic can be added based on the bids and rules

# Initialize players
players = [Player('Alice'), Player('Bob'), Player('Charlie'), Player('David')]

# Start the game

# c = DeckOfCards()
# print(c)
game = TarneebGame(players)
game.start_game()