"""
Constant values.
"""

STATUS_REQUESTED = 100
STATUS_LOTTERY = 201
STATUS_CANCELLED = 210
STATUS_WON = 301
STATUS_LOST = 310
STATUS_USED = 401
STATUS_UNCONFIRMED = 402
STATUS_UNUSED = 405
STATUS_RESIGNED = 410

# populate the module with Statuses and their respective values
_GLOBALS = globals()
_RESPONSES = [
    ('STATUS_{}'.format(k), v) for k, v in _GLOBALS.items() if k.startswith('STATUS_')
]
_GLOBALS.update(_RESPONSES)
