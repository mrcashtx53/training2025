"""Simple command-line Blackjack game.

Controls:
- Type `h` or `hit` to take another card.
- Type `s` or `stand` to stop and let the dealer play.
- Type `q` or `quit` to exit the game.

Run: `python blackjack.py`
"""

import random
import sys


RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['♠', '♥', '♦', '♣']


def create_deck(num_decks=1):
	deck = []
	for _ in range(num_decks):
		for s in SUITS:
			for r in RANKS:
				deck.append((r, s))
	random.shuffle(deck)
	return deck


def value_of_card(card):
	rank, _ = card
	if rank in ['J', 'Q', 'K']:
		return 10
	if rank == 'A':
		return 11
	return int(rank)


def hand_value(hand):
	total = 0
	aces = 0
	for c in hand:
		v = value_of_card(c)
		total += v
		if c[0] == 'A':
			aces += 1
	# Downgrade aces from 11 to 1 as needed
	while total > 21 and aces:
		total -= 10
		aces -= 1
	return total


def pretty_hand(hand, hide_first=False):
	if hide_first and hand:
		return '[?, {}]'.format(', '.join(f"{r}{s}" for r, s in hand[1:]))
	return '[' + ', '.join(f"{r}{s}" for r, s in hand) + ']'


def deal_initial(deck):
	player = [deck.pop(), deck.pop()]
	dealer = [deck.pop(), deck.pop()]
	return player, dealer


def player_turn(deck, player_hand, dealer_hand, bankroll, bet, allow_double=True):
	"""Play one hand for the player. Returns (final_hand, bet_change)
	bet_change is how bankroll should be adjusted (negative means additional bet placed for doubling)."""
	doubled = False
	while True:
		print(f"Your hand: {pretty_hand(player_hand)}  (value: {hand_value(player_hand)})")
		print(f"Dealer: {pretty_hand(dealer_hand, hide_first=True)}")
		if hand_value(player_hand) == 21:
			print("Blackjack!")
			break
		if hand_value(player_hand) > 21:
			print("You busted!")
			break
		options = "(h/s"
		if allow_double and len(player_hand) == 2 and bankroll >= bet:
			options += "/d"
		options += "/q): "
		choice = input(f"Hit, stand{', double' if 'd' in options else ''}? {options}").strip().lower()
		if choice in ('h', 'hit'):
			player_hand.append(deck.pop())
			continue
		if choice in ('s', 'stand'):
			break
		if choice in ('d', 'double') and allow_double and len(player_hand) == 2 and bankroll >= bet:
			# double: take one card and stand, and match the bet
			player_hand.append(deck.pop())
			doubled = True
			print('You doubled down.')
			break
		if choice in ('q', 'quit'):
			print('Quitting...')
			sys.exit(0)
		print("Invalid input. Type 'h' to hit, 's' to stand, 'd' to double (if available), or 'q' to quit.")
	return player_hand, (bet if doubled else 0.0)


def dealer_turn(deck, dealer_hand):
	while hand_value(dealer_hand) < 17:
		dealer_hand.append(deck.pop())


def compare_hands(player_hand, dealer_hand):
	pv = hand_value(player_hand)
	dv = hand_value(dealer_hand)
	print(f"Final hands -> You: {pretty_hand(player_hand)} ({pv})  Dealer: {pretty_hand(dealer_hand)} ({dv})")
	if pv > 21:
		return 'lose'
	if dv > 21:
		return 'win'
	if pv > dv:
		return 'win'
	if pv < dv:
		return 'lose'
	return 'push'


def collect_bet(bankroll):
	while True:
		try:
			bet = input(f'Bankroll: ${bankroll} — place your bet: ')
			if bet.strip().lower() in ('q', 'quit'):
				print('Quitting...')
				sys.exit(0)
			bet = float(bet)
			if bet <= 0:
				print('Bet must be positive.')
				continue
			if bet > bankroll:
				print("You don't have enough funds for that bet.")
				continue
			return bet
		except ValueError:
			print('Please enter a valid number.')


def play_round(deck, bankroll):
	if len(deck) < 15:
		print('Reshuffling deck...')
		deck[:] = create_deck(4)
	bet = collect_bet(bankroll)
	player, dealer = deal_initial(deck)
	print(f'You bet ${bet:.2f}')
	# remember bankroll before placing bets so we can compute net change
	initial_bankroll = bankroll
	# Deduct the initial bet from bankroll immediately (place the bet)
	bankroll -= bet

	# Handle splitting
	player_hands = [player]
	bets = [bet]
	# If initial two cards are a pair, offer split
	if player[0][0] == player[1][0] and bankroll >= bet * 1:  # need funds for second bet
		cards_str = f"{player[0][0]}{player[0][1]} and {player[1][0]}{player[1][1]}"
		val = hand_value(player)
		choice = input(f'You have a pair ({cards_str}, value {val}) — split? (y/n): ').strip().lower()
		if choice in ('y', 'yes'):
			# create two hands
			h1 = [player[0], deck.pop()]
			h2 = [player[1], deck.pop()]
			player_hands = [h1, h2]
			bets = [bet, bet]
			# Deduct the second bet now (place the split bet)
			bankroll -= bet
			print('Hand split into two hands.')
	# Play each hand (allow doubling on each initial hand)
	total_delta = 0.0
	final_hands = []
	for i, ph in enumerate(player_hands):
		print(f"Playing hand #{i+1}")
		ph, extra_bet = player_turn(deck, ph, dealer, bankroll, bets[i], allow_double=True)
		bets[i] += extra_bet
		# If player doubled and returned an extra bet, deduct it now (place the additional bet)
		if extra_bet:
			bankroll -= extra_bet
		final_hands.append(ph)
	# natural blackjack checks per hand
	dealer_val = hand_value(dealer)
	# If any player hand is a natural blackjack and dealer also, handle per-hand
	# Dealer plays once if any player hand survives
	need_dealer = any(hand_value(h) <= 21 for h in final_hands)
	if need_dealer:
		dealer_turn(deck, dealer)

	round_change = 0.0
	for i, ph in enumerate(final_hands):
		pv = hand_value(ph)
		dv = hand_value(dealer)
		print(f"--- Result for hand #{i+1} ---")
		print(f'Your hand: {pretty_hand(ph)} ({pv})  Dealer: {pretty_hand(dealer)} ({dv})')
		# natural blackjack: player receives original bet + 1.5x bet = 2.5x total
		if len(ph) == 2 and pv == 21:
			if dv == 21 and len(dealer) == 2:
				print('Push (both blackjack). Bet returned.')
				round_change += bets[i]  # return original bet
			else:
				payout = bets[i] * 2.5
				print(f'Blackjack! You receive ${payout:.2f} (includes original bet) on hand #{i+1}')
				round_change += payout
			continue
		if pv > 21:
			print(f'Hand #{i+1} busted, you lose the bet of ${bets[i]:.2f}.')
			# lost bet already deducted
			continue
		if dv > 21:
			payout = bets[i] * 2.0
			print(f'Dealer busted. You receive ${payout:.2f} (includes original bet) on hand #{i+1}!')
			round_change += payout
			continue
		if pv > dv:
			payout = bets[i] * 2.0
			print(f'You win ${bets[i]:.2f} (profit) — receiving ${payout:.2f} total on hand #{i+1}!')
			round_change += payout
		elif pv < dv:
			print(f'You lose ${bets[i]:.2f} on hand #{i+1}.')
			# lost bet already deducted
		else:
			print(f'Push on hand #{i+1}. Bet returned.')
			round_change += bets[i]

	final_bankroll = bankroll + round_change
	delta = final_bankroll - initial_bankroll
	return final_bankroll, delta


def main():
	print('Welcome to simple Blackjack with betting!')
	deck = create_deck(4)
	bankroll = 100.0
	while True:
		bankroll, delta = play_round(deck, bankroll)
		print(f'Bankroll now: ${bankroll:.2f} (change: {delta:+.2f})')
		if bankroll <= 0:
			print('You are out of money. Game over.')
			break
		# Ask to play again and validate input strictly
		while True:
			again = input('Play another hand? (y/n): ').strip().lower()
			if again in ('y', 'yes'):
				break
			if again in ('n', 'no'):
				print('Thanks for playing.')
				return
			print("Please answer 'y' or 'n'.")


if __name__ == '__main__':
	main()

