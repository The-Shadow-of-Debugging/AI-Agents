def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    hash_char = {}

    for char in s:
        if char in hash_char:
            hash_char[char] = hash_char[char] + 1
        else:
            hash_char[char] = 1

    for char in t:
        if char in hash_char:
            hash_char[char] = hash_char[char] - 1

            if hash_char[char] < 0:
                return False
        else:
            return False

    return True

print(isAnagram(s = "anagram", t = "nagaram"))
print(isAnagram(s = "rat", t = "car"))
