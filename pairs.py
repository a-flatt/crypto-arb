




class Pair:

    def __init__(
        self, 
        addr: str,
        token0addr: str,
        token0sym: str,
        token1addr: str,
        token1sym: str,
        reserve0: int,
        reserve1: int,
    ) -> None:

        self.addr = addr
        self.token0addr = token0addr
        self.token0sym = token0sym
        self.token1addr = token1addr
        self.token1sym = token1sym
        self.reserve0 = reserve0
        self.reserve1 = reserve1
        
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
