import pytest

from valet.job.lottery import draw

PLAYERS = list('abcd')
WINNINGS = {
    'a': 10,
    'b': 10,
    'c': 5
}

def test_draw():
    c, winners = draw(PLAYERS, WINNINGS)

    assert c == ['d']
    assert winners == {
        'a': 10,
        'b': 10,
        'c': 5,
        'd': 1
    }

