"""
Randomly choose from the population in a fair way.

Use past winnings to influence future choices. The more a user won in the past
the less he or she is going to win in the future to allow others to use a parking
spot too.
"""

from random import choices

from ..types import Winnings, WeightedWinnings


def filter_out_winnings(requestors: list[str], winnings: Winnings) -> Winnings:
    """
    How many times the requestors won a parking spot.

    In other words from the dictionary that collects all users and the count
    how many times they won take only those 'rows' that refer to current
    requestors. Take the dictionary with all winnings and return the dictionary
    containing winnings of the requestors only.
    """
    reqs_dict = {name: 0 for name in requestors}  # change a list into a dict
    keys = winnings.keys() & reqs_dict.keys()
    wins = {k: v for k, v in winnings.items() if k in keys}
    reqs_dict.update(wins)
    return reqs_dict


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

    wins = filter_out_winnings(requestors, winnings)
    weighted_wins = replace_wins_with_weight(wins)
    winners = choices(
        list(weighted_wins.keys()), weights=list(weighted_wins.values()), k=k
    )
    return winners
