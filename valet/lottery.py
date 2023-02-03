from collections import Counter
from random import choices

# def merge(players: dict, winners: dict):
#     # for k, v in a.items():
#     #     if k in b:
#     #         a[k] = v + b[k]
#     # return a

#     # choose only those among winners that currently in play
#     c = [(k, v) for k, v in winners.items() if k in players]
#     # update players with winners in play
#     copy = players.copy()
#     copy.update(c)
#     return copy


def draws_won_by_players(
    players: list[str], all_winnings: list[tuple[int, int]]
) -> dict[str, int]:
    '''Calculate weights used in randomly choosing a winner to ensure a fair choice'''
    current_players = {name: 0 for name in players}  # change a list into a dict
    winnings = dict(all_winnings)
    keys = winnings.keys() & current_players.keys()
    wins = {k: v for k, v in winnings.items() if k in keys}
    current_players.update(wins)
    return current_players


# def draws_won_by_players_2(
#     players: list[str], all_winnings: list[tuple[int, int]]
# ) -> dict[str, int]:
#     '''Calculate weights used in randomly choosing a winner to ensure a fair choice'''
#     # choose only those among all winners that currently in play
#     winnings = dict(all_winnings)
#     winners_in_play = [(k, v) for k, v in winnings.items() if k in players]
#     # update players with winners in play
#     current_players: dict = {name: 0 for name in players}  # change a list into a dict
#     current_players.update(winners_in_play)
#     return current_players


def replace_win_with_weight(draws_won: dict[str, int]) -> dict[str, float]:
    s = sum(draws_won.values())
    return {k: (1 - (v / s)) for k, v in draws_won.items()}


def draw(players: list[str], all_winnings: list[tuple[int, int]]):
    wins = draws_won_by_players(players, all_winnings)
    wins = replace_win_with_weight(wins)
    winners = choices(list(wins.keys()), weights=list(wins.values()))
    return winners
