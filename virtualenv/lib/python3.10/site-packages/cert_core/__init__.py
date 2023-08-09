from enum import Enum


# display value for chains, including specific network.
CHAIN_BITCOIN_MAINNET = 'bitcoinMainnet'
CHAIN_BITCOIN_REGTEST = 'bitcoinRegtest'
CHAIN_BITCOIN_TESTNET = 'bitcoinTestnet'
CHAIN_ETHEREUM_MAINNET = 'ethereumMainnet'
CHAIN_ETHEREUM_ROPSTEN = 'ethereumRopsten'
CHAIN_ETHEREUM_GOERLI = 'ethereumGoerli'
CHAIN_ETHEREUM_SEPOLIA = 'ethereumSepolia'
CHAIN_MOCKCHAIN = 'mockchain'

# system value for chains, including specific network. Used in config files for example
SYS_CHAIN_BITCOIN_MAINNET = 'bitcoin_mainnet'
SYS_CHAIN_BITCOIN_REGTEST = 'bitcoin_regtest'
SYS_CHAIN_BITCOIN_TESTNET = 'bitcoin_testnet'
SYS_CHAIN_ETHEREUM_MAINNET = 'ethereum_mainnet'
SYS_CHAIN_ETHEREUM_ROPSTEN = 'ethereum_ropsten'
SYS_CHAIN_ETHEREUM_GOERLI = 'ethereum_goerli'
SYS_CHAIN_ETHEREUM_SEPOLIA = 'ethereum_sepolia'
SYS_CHAIN_MOCKCHAIN = 'mockchain'

# signature type, part of signature suite standard
CHAIN_TYPE_BITCOIN = 'BTCOpReturn'
CHAIN_TYPE_ETHEREUM = 'ETHData'
CHAIN_TYPE_MOCK = 'Mock'

# system config values, used for pycoin
SYS_NETWORK_BITCOIN_REGTEST = 'regtest'
SYS_NETWORK_BITCOIN_TESTNET = 'testnet'
SYS_NETWORK_BITCOIN_MAINNET = 'mainnet'

PUBKEY_PREFIX = 'ecdsa-koblitz-pubkey:'
URN_UUID_PREFIX = 'urn:uuid:'


class BlockcertVersion(Enum):
    V1_1 = 0
    V1_2 = 1
    V2_ALPHA = -1
    V2 = 2


class BlockchainType(Enum):
    bitcoin = 0, CHAIN_TYPE_BITCOIN
    ethereum = 1, CHAIN_TYPE_ETHEREUM
    mock = 2, CHAIN_TYPE_MOCK

    def __new__(cls, enum_value, external_display_value):
        obj = object.__new__(cls)
        obj._value_ = enum_value
        obj.external_display_value = external_display_value
        return obj


class Chain(Enum):
    bitcoin_mainnet = 0, BlockchainType.bitcoin, CHAIN_BITCOIN_MAINNET
    bitcoin_testnet = 1, BlockchainType.bitcoin, CHAIN_BITCOIN_TESTNET
    bitcoin_regtest = 2, BlockchainType.bitcoin, CHAIN_BITCOIN_REGTEST
    mockchain = 3, BlockchainType.mock, CHAIN_MOCKCHAIN
    ethereum_mainnet = 4, BlockchainType.ethereum, CHAIN_ETHEREUM_MAINNET
    ethereum_ropsten = 5, BlockchainType.ethereum, CHAIN_ETHEREUM_ROPSTEN
    ethereum_goerli = 6, BlockchainType.ethereum, CHAIN_ETHEREUM_GOERLI
    ethereum_sepolia = 7, BlockchainType.ethereum, CHAIN_ETHEREUM_SEPOLIA

    def __new__(cls, enum_value, blockchain_type, external_display_value):
        obj = object.__new__(cls)
        obj._value_ = enum_value
        obj.blockchain_type = blockchain_type
        obj.external_display_value = external_display_value
        return obj

    @staticmethod
    def parse_from_chain(chain_string):
        if chain_string == SYS_CHAIN_BITCOIN_MAINNET:
            return Chain.bitcoin_mainnet
        elif chain_string == SYS_CHAIN_BITCOIN_TESTNET:
            return Chain.bitcoin_testnet
        elif chain_string == SYS_CHAIN_BITCOIN_REGTEST:
            return Chain.bitcoin_regtest
        elif chain_string == SYS_CHAIN_MOCKCHAIN:
            return Chain.mockchain
        elif chain_string == SYS_CHAIN_ETHEREUM_MAINNET:
            return Chain.ethereum_mainnet
        elif chain_string == SYS_CHAIN_ETHEREUM_ROPSTEN:
            return Chain.ethereum_ropsten
        elif chain_string == SYS_CHAIN_ETHEREUM_GOERLI:
            return Chain.ethereum_goerli
        elif chain_string == SYS_CHAIN_ETHEREUM_SEPOLIA:
            return Chain.ethereum_sepolia
        else:
            raise UnknownChainError(chain_string)

    @staticmethod
    def parse_from_external_display_value(external_display_value):
        if external_display_value == CHAIN_BITCOIN_MAINNET:
            return Chain.bitcoin_mainnet
        elif external_display_value == CHAIN_BITCOIN_TESTNET:
            return Chain.bitcoin_testnet
        elif external_display_value == CHAIN_BITCOIN_REGTEST:
            return Chain.bitcoin_regtest
        elif external_display_value == CHAIN_MOCKCHAIN:
            return Chain.mockchain
        elif external_display_value == CHAIN_ETHEREUM_MAINNET:
            return Chain.ethereum_mainnet
        elif external_display_value == CHAIN_ETHEREUM_ROPSTEN:
            return Chain.ethereum_ropsten
        elif external_display_value == CHAIN_ETHEREUM_GOERLI:
            return Chain.ethereum_goerli
        elif external_display_value == CHAIN_ETHEREUM_SEPOLIA:
            return Chain.ethereum_sepolia
        else:
            raise UnknownChainError(external_display_value)

    def is_bitcoin_type(self):
        return self.blockchain_type == BlockchainType.bitcoin

    def is_mock_type(self):
        return self.blockchain_type == BlockchainType.mock

    def is_ethereum_type(self):
        return self.blockchain_type == BlockchainType.ethereum


def chain_to_bitcoin_network(chain):
    """
    Used or bitcoin.SelectParams
    :param chain:
    :return:
    """
    if chain == Chain.bitcoin_mainnet:
        return SYS_NETWORK_BITCOIN_MAINNET
    elif chain == Chain.bitcoin_testnet:
        return SYS_NETWORK_BITCOIN_TESTNET
    elif chain == Chain.bitcoin_regtest:
        return SYS_NETWORK_BITCOIN_REGTEST
    else:
        message = 'This chain cannot be converted to a bitcoin netcode; chain='
        if chain:
            message += chain.name
        else:
            message += '<NULL>'
        raise UnknownChainError(message)


def is_bitcoin_mainnet_address(address):
    return address.startswith('1') or address.startswith(PUBKEY_PREFIX + '1')


class InvalidUrlError(Exception):
    pass


class InvalidCertificateError(Exception):
    """
    Certificate lacks fields required to parse for display
    """
    pass


class UnknownChainError(Exception):
    """
    Didn't recognize chain
    """
    pass


class UnknownBlockcertVersionException(Exception):
    """
    Didn't recognize blockcert version
    """
    pass


from cert_core.cert_model.model import to_certificate_model, BlockchainCertificate