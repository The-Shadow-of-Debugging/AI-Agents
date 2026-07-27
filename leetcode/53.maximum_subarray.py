from typing import List


def maxSubArray(nums: List[int]) -> int:
    сurrent_sum = nums[0]
    global_sum = nums[0]

    for i, value in enumerate(nums[1:]):
        сurrent_sum = max(сurrent_sum + value, value)
        global_sum = max(global_sum, сurrent_sum)

    return global_sum


print(maxSubArray([-2,1,-3,4,-1,2,1,-5,4]))
print(maxSubArray([1]))
print(maxSubArray([5,4,-1,7,8]))
