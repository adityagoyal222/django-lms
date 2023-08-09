from cbor2 import dumps, loads
import json
from multibase import encode, decode
from .mappings import *


class MerkleProof2019:
    def __init__(self):
        proof_value = None
        json = None

    def decode(self, proof_value):
        # decode the multibase encoding
        multibase_decoded = decode(proof_value)

        # decode cbor map to readable json
        decoded_map = loads(multibase_decoded)
        self.proof_value = self.__decode_map(decoded_map)

        return self.proof_value

    def encode(self, proof_json):
        if type(proof_json) == str:
            self.json = json.loads(proof_json)
        else:
            self.json = proof_json

        # map json to cbor-efficient values
        mapped_values = self.__map_json()

        # cbor encode map
        cbor_encoding = dumps(mapped_values)

        # multibase encode to base58btc
        self.proof_value = encode('base58btc', cbor_encoding)
        return self.proof_value

    def __map_json(self):
        mapped_list = []

        for key in self.json:
            if key == 'path':
                path_list = self.__map_path(key)
                mapped_list.append([root[key], path_list])
            elif key == 'anchors':
                anchor_list = self.__map_anchors(key)
                mapped_list.append([root[key], anchor_list])
            else:
                mapped_list.append([root[key], dumps(self.json[key])])

        return mapped_list

    def __map_anchors(self, key):
        anchor_list = []
        for anchor_item in self.json[key]:
            anchor_item_list = []
            anchor_items = anchor_item.split(':')
            for i, anchor_partial in enumerate(anchor_items):
                if i == 0:
                    continue
                elif i == 1:
                    anchor_item_list.append([0, chain[anchor_partial]['id']])
                elif i == 2 and 'networks' in chain[anchor_items[i - 1]]:
                    anchor_item_list.append([1, chain[anchor_items[i - 1]]['networks'][anchor_partial]])
                else:
                    anchor_item_list.append([i - 1, dumps(anchor_partial)])
            anchor_list.append(anchor_item_list)
        return anchor_list

    def __map_path(self, key):
        path_list = []
        for path_item in self.json[key]:
            if 'right' in path_item:
                path_list.append([path['right'], dumps(path_item['right'])])
            if 'left' in path_item:
                path_list.append([path['left'], dumps(path_item['left'])])
        return path_list

    def __decode_map(self, map):
        # inverse mapping
        inv_root = {v: k for k, v in root.items()}

        decoded_json = {}

        for map_item in map:
            print(root)

            if map_item[0] == 2:
                decoded_json[inv_root[map_item[0]]] = self.__decode_anchor_map(map_item)
            elif map_item[0] == 3:
                decoded_json[inv_root[map_item[0]]] = self.__decode_path_map(map_item)
            else:
                decoded_json[inv_root[map_item[0]]] = loads(map_item[1])

        return decoded_json

    def __decode_path_map(self, map_item):
        # inverse mapping
        inv_path = {v: k for k, v in path.items()}

        path_list = []
        for path_item in map_item[1]:
            path_item_obj = {}
            direction = inv_path[path_item[0]]
            path_item_obj[direction] = loads(path_item[1])
            path_list.append(path_item_obj)
        return path_list

    def __decode_anchor_map(self, map_item):
        anchor_string_list = []
        for anchor in map_item[1]:
            anchor_string = 'blink:'
            anchored_chain = findChainById(anchor[0][1])
            anchor_string += anchored_chain + ':'
            anchor_string += findNetworkById(anchored_chain, anchor[1][1]) + ':'
            anchor_string += loads(anchor[2][1])

            anchor_string_list.append(anchor_string)
        return anchor_string_list
