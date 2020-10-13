from decimal import Decimal
import datetime
import json


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 != 0:
                return float(o)
            else:
                return int(o)
        elif isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d")
        elif isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        return json.JSONEncoder.default(self, o)