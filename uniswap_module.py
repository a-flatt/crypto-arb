import json
import asyncio
import base64

import sys
sys.path.append('..')
from uniswap_python_port.uniswap import *

import requests
from requests.auth import HTTPBasicAuth

import web3
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from pairs import Pair

# Pair abi info; to move later
pair_abi = json.load(open("files/abi/pairs.abi"))['abi']

# Setup GraphQL to query pairs; tidy
transport = AIOHTTPTransport(url="https://bsc.streamingfast.io/subgraphs/name/pancakeswap/exchange-v2")
client = Client(transport=transport, fetch_schema_from_transport=True)
    
# Bunch of config; again, tidy
BSC_NODE = "https://bsc-dataseed.binance.org/"
BSC_PROVIDER = web3.Web3.HTTPProvider(BSC_NODE)
w3 = web3.Web3(BSC_PROVIDER)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Create Uniswap instance; move to a config file
address = None        
private_key = None 
version = 2                       
web3 = w3
factory_contract_addr = w3.toChecksumAddress("0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73")
router_contract_addr = w3.toChecksumAddress("0x10ED43C718714eb63d5aA57B78B54704E256024E")

uniswap = Uniswap(address=address, 
                  private_key=private_key, 
                  version=version, 
                  web3=web3, 
                  factory_contract_addr=factory_contract_addr, router_contract_addr=router_contract_addr)

def buildPairs(w3):

    pairList = []

    cake_pairs = json.load(open("./files/50_pairs_pancake.json"))["data"]["pairs"]
    
    for i in range(len(cake_pairs)):
        pair_addr = cake_pairs[i]['id']
        pair_contract = util._load_pair_contract(w3, pair_abi, pair_addr)
        token0addr = pair_contract.functions.token0().call()
        token0sym = cake_pairs[i]['token0']['symbol']
        token1addr = pair_contract.functions.token1().call()
        token1sym = cake_pairs[i]['token1']['symbol']

        reserves = pair_contract.functions.getReserves().call()
        reserve0 = reserves[0]
        reserve1 = reserves[1]

        pair = Pair(w3,
                    pair_addr,
                    token0addr,
                    token0sym,
                    token1addr,
                    token1sym,
                    reserve0,
                    reserve1)

        pairList.append(pair)

    return pairList

def test():

    """
    # pair_address = uniswap.factory_contract.functions.allPairs(1).call()
    # pair_contract = util._load_pair_contract(w3, pair_abi, pair_address)
    
    # Info to build pair:
    token0addr = pair_contract.functions.token0().call()
    token0sym = "ABC"
    token1addr = pair_contract.functions.token1().call()
    token1sym = "XYZ"
    reserve0 = pair_contract.functions.getReserves().call()[0]
    reserve1 = pair_contract.functions.getReserves().call()[1]

    pair = Pair(w3,
                pair_address,
                token0addr,
                token0sym,
                token1addr,
                token1sym,
                reserve0,
                reserve1)
    
    pair.monitorPair()
    
    """
    pairList = buildPairs(w3)
    print(pairList[0].pairStruct)
