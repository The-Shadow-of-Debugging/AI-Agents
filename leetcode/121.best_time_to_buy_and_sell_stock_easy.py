from typing import List


def maxProfit(prices: List[int]) -> int:
    profit = 0
    minCost = prices[0]

    for i, value in enumerate(prices):
        future_profit = value - minCost

        if future_profit > profit:
            profit = future_profit

        if value < minCost:
            minCost = value

    return profit


print(maxProfit([7,1,5,3,6,4]))
print(maxProfit([7,6,4,3,1]))