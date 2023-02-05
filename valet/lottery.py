"""
Randomly choose from the population in a fair way.

Use past winnings to influence future choices. The more a user won in the past
the less he or she is going to win in the future to allow others to use a parking
spot too.
"""

from random import choices

from .types_ import Winnings, WeightedWinnings

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


def restrict_winnings_to_requestors(
    requestors: list[str], all_winnings: Winnings
) -> Winnings:
    """
    From all winnings take out only those ones the requestors had.

    In other words from the dictionary that collects all users and the count
    how many times they won take only those 'rows' that refer to current
    requestors. Take the dictionary with all winnings and return the dictionary
    containing winnings of the requestors only.
    """
    current_players = {name: 0 for name in requestors}  # change a list into a dict
    winnings = dict(all_winnings)
    keys = winnings.keys() & current_players.keys()
    wins = {k: v for k, v in winnings.items() if k in keys}
    current_players.update(wins)
    return current_players


def replace_wins_with_weight(winnings: Winnings) -> WeightedWinnings:
    """
    In the winnings dictionary replace the count of wins with a weight.

    A weight represents the likelihood of a future win. The more you win the
    probability is lower.
    """
    s = sum(winnings.values())
    return {k: (1 - (v / s)) for k, v in winnings.items()}


def draw(requestors: list[str], winnings: Winnings, k: int = 1):
    """
    Randomly draw `k` `winners` out of `requestors` based on their `winnings`
    so far.
    """
    if not requestors:
        return []

    restricted_winnings = restrict_winnings_to_requestors(requestors, winnings)
    weighted_winnings = replace_wins_with_weight(restricted_winnings)
    winners = choices(
        list(weighted_winnings.keys()), weights=list(weighted_winnings.values()), k=k
    )
    return winners
