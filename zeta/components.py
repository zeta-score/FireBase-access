import logging
import json


# Constants
TX_TYPES = ['recieve', 'send']
ZETA_MIN = 0.0
ZETA_MAX = 1.0
ZETA_SCORE_INIT = (ZETA_MIN + ZETA_MAX)/2

# Configurations
logging.basicConfig(level=logging.DEBUG)

#package
__all__ = ['TX_TYPES', 'ZETA_MAX', 'ZETA_MIN', 'ZETA_SCORE_INIT', 'Node', 'Tx']

class Node:
    def __init__(self, id, zeta_score = ZETA_SCORE_INIT, balance = 0, transactions = None):
        """
        id: address of the node
        zeta_score: float between (0,1)
        balance: float >0
        transactions: {
            'send': [Tx],
            'recieve': [Tx]
        }
        """
        self.id = id
        self.__zeta_score = ZETA_SCORE_INIT
        self.__balance = 0
        self.tx = {
            "recieve":{

            },
            "send":{

            }
        }
        self.set_zscore(zeta_score)
        self.set_balance(balance)
        if transactions is not None:
            for type in transactions:
                if type in TX_TYPES:
                    for txs in transactions[type]:
                        self.add_tx(txs,type)

    @classmethod
    def from_dict(cls, node_as_dict):
        """
        creates an instance from a dictionary
        """
        transactions = {
            type: [Tx(**tx) for tx in txs.values()]
            for type, txs in node_as_dict['tx'].items()
            if type in TX_TYPES
        }
        node = cls(node_as_dict['id'], node_as_dict['zeta_score'], node_as_dict['balance'], transactions)
        '''
        for type in node_as_dict['tx']:
            if type in TX_TYPES:
                node.tx[type] = {
                    tx_id: Tx(**transaction)
                    for tx_id, transaction in node_as_dict['tx'][type].items()
                }
        '''
        return node

    def set_zscore(self, zeta_score):
        if zeta_score >= 0 and zeta_score <= 1:
            self.__zeta_score = zeta_score
            return True
        else:
            logging.critical(
                "{zeta_score} out of range [{z_min},{z_max}]"
                .format(zeta_score=zeta_score, z_min=ZETA_MIN, z_max=ZETA_MAX)
            )
            return False
    def get_zscore(self):
        return self.__zeta_score


    def set_balance(self, balance):
        if balance >= 0:
            self.__balance = balance
            return True
        else:
            logging.critical(
                "{balance} cannot be less than zero"
                .format(balance=balance)
            )
            return False
    def get_balance(self):
        return self.__balance


    def add_tx(self, transaction, type):
        """
        adds a transaction for the node
        transaction: Tx instance
        type: ['recieve', 'send']
        """
        if type in TX_TYPES:
            tx_id = transaction.id
            self.tx[type][tx_id] = transaction
        else:
            logging.critical("{type} not found in {tx_types}".format(type=type, tx_types=TX_TYPES))

    def jsonify(self):
        """
        returns: a json of the instance
        """
        data = {
            'id': self.id,
            'zeta_score': self.__zeta_score,
            'balance': self.__balance,
            'tx': {
                type: {
                    timestamp:transaction.jsonify()
                    for timestamp,transaction in self.tx[type].items()
                }
                for type in  self.tx
            }
        }
        return data

    def __repr__(self):
        return str(self.jsonify())


class Tx:
    def __init__(self, id, timestamp, source, target, value):
        """
        id: transaction id (str)
        timestamp: timestamp (str)
        source: address of the source (str)
        target: address of the target (str)
        value: value of the transaction (str)
        """
        self.id = id
        self.timestamp = timestamp
        self.source = source
        self.target = target
        self.value = min(0,value)
        if value < 0:
            logging.critical("{value} cannot be less than zero, value set to zero")

    def jsonify(self):
        data = {
            'id':self.id,
            'timestamp': self.timestamp,
            'source': self.source,
            'target': self.target,
            'value': self.value
        }
        return data

    def __repr__(self):
        return str(self.jsonify())
