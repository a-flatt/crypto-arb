# from helper import *
import asyncio
from web3 import Web3
from uniswap_python_port.uniswap import *
import json
import time

pair_abi = json.load(open("files/abi/pairs.abi"))['abi']

class Pair:

    def __init__(
        self, 
        w3,
        addr: str,
        token0addr: str,
        token0sym: str,
        token1addr: str,
        token1sym: str,
        reserve0: int,
        reserve1: int,
    ) -> None:

        self.w3 = w3
        self.addr = addr
        self.token0addr = token0addr
        self.token0sym = token0sym
        self.token1addr = token1addr
        self.token1sym = token1sym
        self.reserve0 = reserve0
        self.reserve1 = reserve1
        
        # Generate a dict for easier referencing
        self.pairStruct = self.pairToDict()
    
    def pairToDict(self):
        pairDict = {"address": self.addr, 
                    "token0": {
                        "address": self.token0addr, 
                        "symbol": self.token0sym
                    },
                    "token1": {
                        "address": self.token1addr, 
                        "symbol": self.token1sym
                    },
                    "reserve0": self.reserve0,
                    "reserve1": self.reserve1
                }
        return pairDict

# ------ asyncio stuff -----------------------------------------------------------------------------
    """
    Still to flesh out, currently just running a small loop    
    """
    async def getReserve(self, contract):
        self.reserve0 = contract.functions.getReserves().call()[0]
        self.reserve1 = contract.functions.getReserves().call()[1]
        print(self.pairStruct)

    async def updateReserves(self, contract):
        while True:
            await asyncio.gather(self.getReserve(contract))
    
    def monitorPair(self):
        
        for i in range(10):
            pair_contract = util._load_pair_contract(self.w3, pair_abi, self.addr)
            print(pair_contract.functions.getReserves().call()[0])
            time.sleep(5)


