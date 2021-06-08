import json
from decimal import Decimal

startToken = {
        "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "symbol": "WETH",
        "decimal": 18,
    }

tradingPairs = json.load(open('100_pairs.json'))

baseToken = exitToken = startToken
currentPairs = []
tradePath = [baseToken]
trades = []
maxTurns = 100
count = 0
d997 = Decimal(997)
d1000 = Decimal(1000)

def getAmountOut(amountIn, reserveIn, reserveOut):
    assert amountIn > 0
    assert reserveIn > 0 and reserveOut > 0
    if not isinstance(amountIn, Decimal):
        amountIn = Decimal(amountIn)
    if not isinstance(reserveIn, Decimal):
        reserveIn = Decimal(reserveIn)
    if not isinstance(reserveOut, Decimal):
        reserveOut = Decimal(reserveOut)
    return d997*amountIn*reserveOut/(d1000*reserveIn+d997*amountIn)

def getOptimalAmount(Ea, Eb):
    if Ea > Eb:
        return None
    if not isinstance(Ea, Decimal):
        Ea = Decimal(Ea)
    if not isinstance(Eb, Decimal):
        Eb = Decimal(Eb)
    return Decimal(int((Decimal.sqrt(Ea*Eb*d997*d1000)-Ea*d1000)/d997))

def adjustReserve(token, amount):
    # res = Decimal(amount)*Decimal(pow(10, 18-token['decimal']))
    # return Decimal(int(res))
    return amount

def toInt(n):
    return Decimal(int(n))

def getEaEb(tokenIn, pairs):
    Ea = None
    Eb = None
    idx = 0
    tokenOut = tokenIn.copy()
    for pair in pairs:
        if idx == 0:
            if tokenIn['address'] == pair['token0']['address']:
                tokenOut = pair['token1']
            else:
                tokenOut = pair['token0']
        if idx == 1:
            Ra = adjustReserve(pairs[0]['token0'], pairs[0]['reserve0'])
            Rb = adjustReserve(pairs[0]['token1'], pairs[0]['reserve1'])
            if tokenIn['address'] == pairs[0]['token1']['address']:
                temp = Ra
                Ra = Rb
                Rb = temp
            Rb1 = adjustReserve(pair['token0'], pair['reserve0'])
            Rc = adjustReserve(pair['token1'], pair['reserve1'])
            if tokenOut['address'] == pair['token1']['address']:
                temp = Rb1
                Rb1 = Rc
                Rc = temp
                tokenOut = pair['token0']
            else:
                tokenOut = pair['token1']
            Ea = toInt(d1000*Ra*Rb1/(d1000*Rb1+d997*Rb))
            Eb = toInt(d997*Rb*Rc/(d1000*Rb1+d997*Rb))
        if idx > 1:
            Ra = Ea
            Rb = Eb
            Rb1 = adjustReserve(pair['token0'], pair['reserve0'])
            Rc = adjustReserve(pair['token1'], pair['reserve1'])
            if tokenOut['address'] == pair['token1']['address']:
                temp = Rb1
                Rb1 = Rc
                Rc = temp
                tokenOut = pair['token0']
            else:
                tokenOut = pair['token1']
            Ea = toInt(d1000*Ra*Rb1/(d1000*Rb1+d997*Rb))
            Eb = toInt(d997*Rb*Rc/(d1000*Rb1+d997*Rb))
        idx += 1
    return Ea, Eb

def findTradePaths(tradingPairs, baseToken, exitToken, tradePath, trades, currentPairs):
    """
    Pending. 
    """    
    for i in range(len(tradingPairs)):
        newTradePath = tradePath.copy()
        pair = tradingPairs[i]
        if not pair['token0']['address'] == baseToken['address'] and not pair['token1']['address'] == baseToken['address']:
            continue
        if baseToken['address'] == pair['token0']['address']:
            poolToken = pair['token1']
        else:
            poolToken = pair['token0']

        newTradePath.append(poolToken)
        
        if poolToken['address'] == exitToken['address'] and len(tradePath) > 2:
            # trades.append(newTradePath)
            Ea, Eb = getEaEb(exitToken, currentPairs + [pair])
            newTrade = {'route': currentPairs + [pair], 'path': newTradePath, 'Ea': Ea, 'Eb': Eb }
            if Ea and Eb: print('True')
            print(Ea)
            print(Eb)
            
            if Ea < Eb: 
                print('True')
            else: 
                print('False')
            
            
            if Ea and Eb and Ea < Eb:
                newTrade['optimalAmount'] = getOptimalAmount(Ea, Eb)
                print('optimal amount:', newTrade['optimalAmount'])
                if newTrade['optimalAmount'] > 0:
                    newTrade['outputAmount'] = getAmountOut(newTrade['optimalAmount'], Ea, Eb)
                    newTrade['profit'] = newTrade['outputAmount']-newTrade['optimalAmount']
                    newTrade['p'] = int(newTrade['profit'])/pow(10, exitToken['decimal'])
                else:
                    continue
                trades.append(newTrade)
                print(newTrade)
            
        elif maxTurns < 1:
            break
        else:
            _tradingPairs = tradingPairs[:i] + tradingPairs[i+1:]
            findTradePaths(_tradingPairs, poolToken, exitToken, newTradePath, trades, currentPairs + [pair])
    return trades

def main():

    tradeset = findTradePaths(tradingPairs, baseToken, exitToken, tradePath, trades, currentPairs)
    for trade in tradeset:
        print(trade)


main()