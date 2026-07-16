from typing import List


def maxProfit(prices: List[int]) -> int:
    profit = 0
    minCost = prices[0]
    minCostIndex = 0

    for i, value in enumerate(prices):
        future_profit = value - minCost

        if i > minCostIndex and value > minCost and future_profit > profit:
            profit = future_profit

        if value < minCost:
            minCost = value
            minCostIndex = i

    return profit


print(maxProfit([7,1,5,3,6,4]))
print(maxProfit([7,6,4,3,1]))