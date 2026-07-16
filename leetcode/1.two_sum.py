from typing import List


def twoSum(nums: List[int], target: int) -> List[int]:
    sorted_pairs = sorted(enumerate(nums), key=lambda x: x[1])

    first_idx, last_idx = 0, len(nums) - 1

    while sorted_pairs[first_idx][1] + sorted_pairs[last_idx][1] != target:
        sum = sorted_pairs[first_idx][1] + sorted_pairs[last_idx][1]

        if sum > target:
            last_idx -= 1

        if sum < target:
            first_idx += 1

    return [sorted_pairs[first_idx][0], sorted_pairs[last_idx][0]]


print(twoSum([2,7,11,15], 9))
print(twoSum([3,2,4], 6))
print(twoSum([3, 3], 6))