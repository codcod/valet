"""Basic types."""

import typing as tp

ValetConfig: tp.TypeAlias = dict[str, tp.Any]
Winnings: tp.TypeAlias = dict[int, int]
WeightedWinnings: tp.TypeAlias = dict[int, float]
