"""
Tools for JSON encoding.
"""

import json
import typing as tp
from datetime import datetime as dt
from functools import partial

from sqlalchemy import Row

__all__ = ['dumps']


class EnhancedJSONEncoder(json.JSONEncoder):
    """
    Enhanced JSONEncoder is able to encode datetimes and sqlalchemy.Rows.
    """

    def default(self, obj: tp.Any) -> tp.Any:
        """
        Method to be implemented in a subclass such that it returns a serializable object.
        """
        if isinstance(obj, dt):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, Row):
            return dict([x for x in zip(obj._fields, obj)])
        return json.JSONEncoder.default(self, obj)


dumps = partial(json.dumps, cls=EnhancedJSONEncoder)
