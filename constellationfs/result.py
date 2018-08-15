# v11AUG18
import datetime as dt
import json
import uuid as uuidlib


class C0JsonEncoder(json.JSONEncoder):
    """ v.12JAN18
    """
    def default(self, obj):
        if isinstance(obj, dt.datetime):
            return obj.isoformat().replace('T', ' ')
        elif isinstance(obj, dt.date):
            return obj.isoformat()
        elif isinstance(obj, uuidlib.UUID):
            return str(obj)
        elif hasattr(obj, 'json'):
            return obj.json
        else:
            return super().default(obj)


class Result:

    def __init__(self, ok=None, success_msg=None, error_msg=None, data=None, misc={}):
        self.ok = ok
        self.success_msg = success_msg
        self.error_msg = error_msg
        self.data = data
        self.misc = misc
        self.msg = None

    def load_from_dict(self, dict_result):
        for k, v in dict_result.items():
            setattr(self, k, v)
        return self

    def process(self):
        if self.ok is None:
            self.ok = 1 if (self.data or self.success_msg) else 0
        self.msg = self.success_msg if self.ok == 1 else self.error_msg
        return self

    @property
    def json(self):
        self.process()
        return json.dumps(self.__dict__, cls=C0JsonEncoder)
