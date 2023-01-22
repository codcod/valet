"""Tools for JSON encoding."""

import functools
import json
from datetime import datetime as dt

from sqlalchemy import Row


__all__ = ['dumps']


class EnhancedJSONEncoder(json.JSONEncoder):
    """Enhanced JSONEncoder is able to encode datetimes and sqlalchemy.Rows."""

    def default(self, obj):
        if isinstance(obj, dt):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, Row):
            return dict([x for x in zip(obj._fields, obj)])
        return json.JSONEncoder.default(self, obj)


dumps = functools.partial(json.dumps, cls=EnhancedJSONEncoder)
