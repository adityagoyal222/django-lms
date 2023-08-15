root = {
    'merkleRoot': 0,
    'targetHash': 1,
    'anchors': 2,
    'path': 3
}

path = {
    'left': 0,
    'right': 1
}

chain = {
  'btc': {
    'id': 0,
    'networks': {
      'mainnet': 1,
      'regtest': 2,
      'testnet': 3
    }
  },
  'eth': {
    'id': 1,
    'networks': {
      'mainnet': 1,
      'ropsten': 3,
      'rinkeby': 4,
      'goerli': 5,
      'sepolia': 11155111
    }
  },
  'mocknet': {
      'id': -1
  }
}

def findChainById(id):
    for i, dic in chain.items():
        if chain[i]['id'] == id:
            return i
    return ''



def findNetworkById(blockchain, id):
    networks = chain[blockchain]['networks']
    for i, dic in networks.items():
        if networks[i] == id:
            return i
    return ''