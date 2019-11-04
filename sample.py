from zeta.zbase import *
from zeta.components import *
import json
if __name__ == "__main__":
    with open('./json_files/sample.json') as f:
        node = Node.from_dict(json.load(f))
        create(node)
        id = node.id
        node = read(id)
        node.set_balance(999)
        node.set_zscore(0.6)
        update(node)
        print(node)
