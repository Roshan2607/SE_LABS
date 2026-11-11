"""
Unit & Integration Tests for Lab 4: Scenario 18 - Blackjack vs Dealer
Validates Tasks 1 through 4.
"""

import pytest
from cards import Deck, hand_value
from game import Blackjack


# ============================================================================
# Task 1: Correct Ace Scoring Tests
# ============================================================================

def test_task1_single_ace_soft_and_hard():
    # A + 9 = 20
    assert hand_value([("A", "S"), ("9", "H")]) == 20
    # A + 9 + 5 = 15 (Ace becomes 1 to prevent bust)
    assert hand_value([("A", "S"), ("9", "H"), ("5", "D")]) == 15
    # A + K = 21 (Blackjack)
    assert hand_value([("A", "S"), ("K", "H")]) == 21


def test_task1_multiple_aces():
    # A + A + 9 = 21 (11 + 1 + 9)
    assert hand_value([("A", "S"), ("A", "H"), ("9", "D")]) == 21
    # A + A + A + A = 14 (11 + 1 + 1 + 1)
    assert hand_value([("A", "S"), ("A", "H"), ("A", "D"), ("A", "C")]) == 14
    # A + A + A + A + 9 = 13 (1 + 1 + 1 + 1 + 9)
    assert hand_value([("A", "S"), ("A", "H"), ("A", "D"), ("A", "C"), ("9", "S")]) == 13


def test_task1_face_cards_and_numbers():
    assert hand_value([("10", "S"), ("J", "H")]) == 20
    assert hand_value([("Q", "S"), ("K", "H"), ("2", "D")]) == 22  # Bust


# ============================================================================
# Task 2 & 3: Game Mechanics & Bankroll Logic
# ============================================================================

def test_deck_draw_and_depletion():
    deck = Deck()
    assert len(deck.cards) == 52
    drawn = [deck.draw() for _ in range(52)]
    assert len(drawn) == 52
    # Next draw should return None
    assert deck.draw() is None


def test_blackjack_initial_bankroll():
    game = Blackjack()
    assert game.chips == 100


def test_game_round_push_settlement(monkeypatch):
    """Test simulated push: both player and dealer stand with identical totals."""
    game = Blackjack()
    initial_chips = game.chips

    # Inputs: Wager 20, Stand ("s")
    inputs = iter(["20", "s"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Fix deck so player has 18, dealer has 18
    # Dealer: (10, 'S'), (8, 'D') -> 18; Player: (10, 'H'), (8, 'C') -> 18
    class MockDeck:
        def __init__(self):
            # Drawn in order: player 1, player 2, dealer 1, dealer 2
            self.cards = [("8", "D"), ("10", "S"), ("8", "C"), ("10", "H")]

        def draw(self):
            return self.cards.pop() if self.cards else None

    monkeypatch.setattr("game.Deck", MockDeck)
    game.round()

    # Chips must be unchanged on push
    assert game.chips == initial_chips


def test_game_round_player_win(monkeypatch):
    """Test player winning: wager added to bankroll."""
    game = Blackjack()
    initial_chips = game.chips
    wager = 25

    inputs = iter([str(wager), "s"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Player gets 20 (10, 10), Dealer gets 18 (10, 8)
    class MockDeck:
        def __init__(self):
            self.cards = [("8", "D"), ("10", "S"), ("10", "D"), ("10", "H")]

        def draw(self):
            return self.cards.pop() if self.cards else None

    monkeypatch.setattr("game.Deck", MockDeck)
    game.round()

    assert game.chips == initial_chips + wager


def test_game_round_player_loss(monkeypatch):
    """Test dealer winning: wager deducted from bankroll."""
    game = Blackjack()
    initial_chips = game.chips
    wager = 30

    inputs = iter([str(wager), "s"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Player gets 17 (10, 7), Dealer gets 19 (10, 9)
    class MockDeck:
        def __init__(self):
            self.cards = [("9", "D"), ("10", "S"), ("7", "D"), ("10", "H")]

        def draw(self):
            return self.cards.pop() if self.cards else None

    monkeypatch.setattr("game.Deck", MockDeck)
    game.round()

    assert game.chips == initial_chips - wager


def test_task4_invalid_wager_retry(monkeypatch):
    """Invalid wagers (negative, text, exceeds chips) must be rejected and reprompted."""
    game = Blackjack()

    # Sequence: invalid negative "-5", invalid text "abc", invalid excessive "500", then valid "10", then stand "s"
    inputs = iter(["-5", "abc", "500", "10", "s"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Mock tie game
    class MockDeck:
        def __init__(self):
            self.cards = [("8", "D"), ("10", "S"), ("8", "C"), ("10", "H")]
        def draw(self):
            return self.cards.pop() if self.cards else None

    monkeypatch.setattr("game.Deck", MockDeck)
    game.round()
    # Ensure settled properly after retry
    assert game.chips == 100
