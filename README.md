# Training Workspace

Repository layout:

- `blackjack/` — simple Blackjack CLI and README. Run `python3 blackjack/blackjack.py` to play.
- `codefinity/` — Codefinity course materials (starter files included).
- `coursera/` — Coursera course materials (starter files included).

This repository contains small training projects and course materials.
<<<<<<< HEAD
# Simple Blackjack

This is a small command-line Blackjack game implemented in `blackjack.py`.

Run:

```bash
python3 blackjack.py
```

# Simple Blackjack

This is a small command-line Blackjack game implemented in `blackjack.py`.

Run:

```bash
python3 blackjack.py
```

Controls:

- `h` or `hit` — take another card
- `s` or `stand` — stop and let the dealer play
- `q` or `quit` — exit immediately

The dealer follows standard rules: hits until reaching 17 or more. Aces count as 11 or 1 to avoid busting when possible.

Betting and Bankroll:

- The game starts with a default bankroll of $100.
- Each round you are prompted to place a bet. Enter `q` to quit immediately.
- Blackjack pays 3:2. Regular wins pay 1:1. Push returns your bet.

Doubling and Splitting:

- Double down: When you have exactly two cards you may choose to double (`d`) if you have enough bankroll. Your bet is matched, you receive exactly one more card, and the hand then stands.
- Split: If your initial two cards are a pair (same rank) and you have enough bankroll for a second bet, you will be offered to split into two separate hands. Each hand receives another card and is played independently; the second bet is placed immediately.

# training2025

This repository contains the simple Blackjack CLI used for training.
