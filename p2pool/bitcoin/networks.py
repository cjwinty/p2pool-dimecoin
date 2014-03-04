import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack

nets = dict(
    ###CJWinty: code clean
    dimecoin=math.Object(
        P2P_PREFIX='fea503dd'.decode('hex'),
        P2P_PORT=11931,
        ADDRESS_VERSION=58,
        RPC_PORT=11930,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'dimecoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 2048*100000000 >> (height + 1)//60480,
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        BLOCK_PERIOD=30, # s
        SYMBOL='DIM',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Dimecoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Dimecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.dimecoin'), 'dimecoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://http://107.150.11.146:333//block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://http://107.150.11.146:333//address/',
        ### CJWinty: Code clear 
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1), 
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),
    dimecoin_testnet=math.Object(
        P2P_PREFIX='011a39f7'.decode('hex'),
        P2P_PORT=18331,
        ADDRESS_VERSION=119,
        RPC_PORT=18332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'dimecoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 2048*100000000 >> (height + 1)//60480,
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        BLOCK_PERIOD=30, # s
        SYMBOL='tQRK',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Quarkcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Quarkcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.quarkcoin'), 'quarkcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://none.yet/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://none.yet/address/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**24 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),
    ### CJWinty: code clear

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
