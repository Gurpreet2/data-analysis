from utils.dateutils import get_date_format
from datetime import datetime as dt
import json


class DataCollection(object):
    """
    This object contains an arbitrary collection of data in this format
    {
        'fields': ['first field', 'second field', 'and so on'],
        'data': [
            {
                'first field': 'a value',
                'second field': 5,
                'and so on': datetime.datetime(2020, 1, 1, 12, 0, 0, 0)
            }
        ],
        'field_metadata': {
            'first field': 'str',
            'second field': 'number',
            'and so on': 'date'
        }
    }

    `fields` and `data` are passed in when the object is initialized.
    `field_metadata` is generated during object initialization.
    """

    def __init__(self, fields, data):
        self.fields = fields
        self.data = data
        self.field_metadata = {}
        # Generate field metadata, learn if data in the field are numbers or dates
        # Note: only checks first object, but converts the objects if first one is a number or a date
        # numbers get converted to floats, and dates get converted to datetime objects
        if len(self.data) > 0:
            for field in self.fields:
                # check if the field may be a number
                try:
                    float(self.data[0][field])
                    self.field_metadata[field] = 'number'
                    for data_obj in self.data:
                        data_obj[field] = float(data_obj[field])
                    continue
                except ValueError:
                    pass
                # check if the field may be a date
                date_format = get_date_format(self.data[0][field])
                if date_format is not None:
                    self.field_metadata[field] = 'date'
                    for data_obj in self.data:
                        data_obj[field] = dt.strptime(data_obj[field], date_format)
                    continue
                # default to string
                self.field_metadata[field] = 'string'

    def json(self):
        """
        Return this `DataCollection` as a json string
        """
        return json.dumps({
            "fields": self.fields,
            "data": self.data,
            "field_metadata": self.field_metadata,
        })
