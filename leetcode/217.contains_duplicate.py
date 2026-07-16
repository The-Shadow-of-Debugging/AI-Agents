from typing import List


def containsDuplicate(nums: List[int]) -> bool:
    seen = {}

    for i, num in enumerate(nums):
        if num in seen:
            return True
        else:
            seen[num] = 1

    return False

print(containsDuplicate([1,2,3,1]))
print(containsDuplicate([1,2,3,4]))
print(containsDuplicate([1,1,1,3,3,4,3,2,4,2]))