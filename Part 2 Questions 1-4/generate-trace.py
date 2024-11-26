#! /usr/bin/env python3
import random
from operator import itemgetter

random.seed(0)  # Ensure consistent results with a fixed random seed
numaddrs = 10
maxpage = 10
count = {}
addrList = []

while True:  # Loop until the condition is met
    for i in range(numaddrs):
        n = int(maxpage * random.random())
        addrList.append(n)
        count[n] = count.get(n, 0) + 1  # Increment count or initialize to 1

    # Sort addresses by their frequency in descending order
    sortedCount = sorted(count.items(), key=itemgetter(1), reverse=True)
    
    # Calculate the total frequency of the top 20% most common addresses
    countSum = sum(sortedCount[k][1] for k in range(int(0.2 * numaddrs)))

    # Check if top 20% addresses contribute at least 80% of total
    if countSum / numaddrs >= 0.8:
        break  # Exit loop if condition is satisfied
    else:
        # Reset for the next iteration
        count = {}
        addrList = []

print(addrList)
