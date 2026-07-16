from typing import List


def twoSum(nums: List[int], target: int) -> List[int]:
    seen = dict()

    for i in range(len(nums)):
        search_num = target - nums[i]

        if search_num in seen:
            return [seen[search_num], i]
        else:
            seen[nums[i]] = i


print(twoSum([2,7,11,15], 9))
print(twoSum([3,2,4], 6))
print(twoSum([3, 3], 6))