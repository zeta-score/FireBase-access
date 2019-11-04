import logging
import firebase_admin
from firebase_admin import db
import json

from zeta.components import *

#configurations
firebase_admin.initialize_app(options={
    'databaseURL': 'https://master-isotope-233310.firebaseio.com/'
})
logging.basicConfig(level=logging.DEBUG)

#package
__all__ = ['create', 'read', 'update', 'delete', 'exists']


NODES = db.reference('nodes')

def create(node):
    """
    creates a node in FireBase
    Args:
        node: zeta.components.Node
    returns:
        Boolean on the status of the creation at FireBase
    """
    node = node.jsonify()
    id = node['id']
    NODES.child(id).set(node)
    logging.debug("{id} is Created".format(id=id))
    return exists(id)

def read(id):
    """
    returns a node in FireBase with a particular id
    Args:
        id: str
    returns:
        zeta.components.Node
    """
    node = NODES.child(id).get()
    if node is None:
        logging.critical("{id} cannot be read".format(id=id))
    else:
        node = Node.from_dict(node)
        logging.debug("{id} is Found".format(id=id))
    return node

def update(node):
    """
    updates a node in FireBase with a particular id
    Args:
        node: zeta.components.Node
    returns:
        Boolean on the status of the updation at FireBase
    """
    node = node.jsonify()
    id = node['id']
    if exists(id):
        NODES.child(id).set(node)
        logging.debug("{id} is Updated".format(id=id))
        return True
    logging.debug("{id} is not changed".format(id=id))
    return False

def delete(id):
    """
    deletes a node in FireBase with a particular id
    Args:
        id: str
    returns:
        Boolean on the status of the deletion at FireBase
    """
    if exists(id):
        NODES.child(id).delete()
        logging.debug("{id} is deleted".format(id=id))
        return True
    return False

def exists(id):
    """
    helper function to check if an id exists in FireBase
    Args:
        id: str
    returns:
        Boolean: if the id exists in FireBase
    """
    if not NODES.child(id).get():
        logging.critical("{id} Not Found".format(id=id))
        return False
    logging.debug("{id} is Found".format(id=id))
    return True

if __name__ == "__main__":
    with open('../json_files/sample.json') as f:
        node = Node.from_dict(json.load(f))
        create(node)
        id = node.id
        node = read(id)
        node.set_balance(999)
        node.set_zscore(0.6)
        update(node)
