from typing import List


def moveZeroes(nums: List[int]) -> None:
    """
    Do not return anything, modify nums in-place instead.
    """
    pos = 0

    for i, value in enumerate(nums):
        if value != 0:
            nums[pos], nums[i] = nums[i], nums[pos]
            pos += 1


nums = [0,1,0,3,12]
moveZeroes(nums)
print(nums)