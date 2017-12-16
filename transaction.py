import json


class Transaction(object):
    def __init__(self, send='', recv='', amount=0, deserialize=None):
        assert isinstance(send, str)
        assert isinstance(recv, str)
        assert isinstance(amount, int)
        assert isinstance(deserialize, dict) or deserialize is None

        if deserialize is None:
            self.send = send
            self.recv = recv
            self.amount = amount
        else:
            self.send = deserialize['send']
            self.recv = deserialize['recv']
            self.amount = deserialize['amount']

    def serialize(self):
        return json.dumps(self.toDict())

    def toDict(self):
        return {
            'send': self.send,
            'recv': self.recv,
            'amount': self.amount
        }
