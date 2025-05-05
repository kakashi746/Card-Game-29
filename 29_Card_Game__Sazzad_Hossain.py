import random
from enum import Enum
from typing import List, Tuple

# Define suits and ranks
class Suit(Enum):
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"

class Rank(Enum):
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

# Card class
class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank.name} of {self.suit.value}"

    def value(self, trump_suit: Suit, lead_suit: Suit) -> int:
        # Trump cards rank higher; within suit, rank determines value
        if self.suit == trump_suit:
            return self.rank.value + 100  # Trump bonus
        if self.suit == lead_suit:
            return self.rank.value
        return 0  # Non-lead, non-trump cards have no value in trick

# Player class
class Player:
    def __init__(self, name: str, is_human: bool = False):
        self.name = name
        self.is_human = is_human
        self.hand: List[Card] = []
        self.tricks_won = 0

    def play_card(self, lead_card: Card, trump_suit: Suit, played_cards: List[Card]) -> Card:
        valid_cards = [card for card in self.hand if self.can_play(card, lead_card, trump_suit)]
        if not valid_cards:
            valid_cards = self.hand  # Play any card if no valid ones

        if self.is_human:
            print(f"\nYour hand: {[str(card) for card in self.hand]}")
            if lead_card:
                print(f"Lead card: {lead_card}, Trump suit: {trump_suit.value}")
            print(f"Played cards: {[str(card) for card in played_cards]}")
            while True:
                try:
                    idx = int(input(f"Choose card to play (0-{len(self.hand)-1}): "))
                    if 0 <= idx < len(self.hand) and self.hand[idx] in valid_cards:
                        card = self.hand.pop(idx)
                        return card
                    print("Invalid choice or card. Try again.")
                except ValueError:
                    print("Enter a number.")
        else:
            # Simple AI: Play highest valid card
            card = max(valid_cards, key=lambda c: c.value(trump_suit, lead_card.suit if lead_card else trump_suit))
            self.hand.remove(card)
            print(f"{self.name} plays {card}")
            return card

    def can_play(self, card: Card, lead_card: Card, trump_suit: Suit) -> bool:
        if not lead_card:
            return True  # Can play any card if leading
        lead_suit = lead_card.suit
        # Must follow suit if possible
        has_lead_suit = any(c.suit == lead_suit for c in self.hand)
        return card.suit == lead_suit if has_lead_suit else True

# Game class
class TwentyNineCardGame:
    def __init__(self):
        self.deck: List[Card] = [Card(suit, rank) for suit in Suit for rank in Rank]
        self.players = [
            Player("You", is_human=True),
            Player("AI North"),
            Player("AI East"),
            Player("AI West")
        ]
        self.trump_suit = random.choice(list(Suit))
        self.team_tricks = {"You & East": 0, "North & West": 0}

    def deal_cards(self):
        random.shuffle(self.deck)
        for i, card in enumerate(self.deck):
            self.players[i % 4].hand.append(card)
        for player in self.players:
            player.hand.sort(key=lambda c: (c.suit.value, c.rank.value))

    def play_trick(self) -> int:
        played_cards: List[Card] = []
        lead_card: Card = None
        for i, player in enumerate(self.players):
            card = player.play_card(lead_card, self.trump_suit, played_cards)
            played_cards.append(card)
            if i == 0:
                lead_card = card

        # Determine trick winner
        winner_card = max(played_cards, key=lambda c: c.value(self.trump_suit, lead_card.suit))
        winner_idx = played_cards.index(winner_card)
        self.players[winner_idx].tricks_won += 1
        print(f"\n{self.players[winner_idx].name} wins the trick with {winner_card}\n")
        return winner_idx

    def play_round(self):
        self.deal_cards()
        print(f"\nTrump suit: {self.trump_suit.value}")
        current_player = 0
        for _ in range(8):  # Each player has 8 cards
            print(f"\n--- Trick {_+1} ---")
            winner_idx = self.play_trick()
            current_player = winner_idx
            # Rotate players so winner leads next trick
            self.players = self.players[winner_idx:] + self.players[:winner_idx]

        # Update team scores
        team1_tricks = self.players[0].tricks_won + self.players[2].tricks_won
        team2_tricks = self.players[1].tricks_won + self.players[3].tricks_won
        self.team_tricks["You & East"] += team1_tricks
        self.team_tricks["North & West"] += team2_tricks

        print("\n--- Round Summary ---")
        for player in self.players:
            print(f"{player.name}: {player.tricks_won} tricks")
        print(f"You & East: {team1_tricks} tricks, North & West: {team2_tricks} tricks")
        print(f"Total Score - You & East: {self.team_tricks['You & East']}, North & West: {self.team_tricks['North & West']}")

    def play(self):
        print("Welcome to 29 Card Game!")
        self.play_round()
        winner = "You & East" if self.team_tricks["You & East"] > self.team_tricks["North & West"] else "North & West"
        print(f"\nGame Over! Winner: {winner}")

if __name__ == "__main__":
    game = TwentyNineCardGame()
    game.play()