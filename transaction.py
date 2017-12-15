import json


class Transaction(object):
    def __init__(self, send='', recv='', amount='', deserialize=None):
        assert isinstance(send, str)
        assert isinstance(recv, str)
        assert isinstance(amount, int)
        assert isinstance(deserialize, str) or deserialize is None

        if deserialize is None:
            self.send = send
            self.recv = recv
            self.amount = self.amount
        else:
            deserialized = json.loads(deserialize)
            self.send = deserialized['send']
            self.recv = deserialized['recv']
            self.amount = deserialized['amount']

    def serialize(self):
        return json.dumps(self.toDict())

    def toDict(self):
        return {
            'send': self.send,
            'recv': self.recv,
            'amount': self.amount
        }
