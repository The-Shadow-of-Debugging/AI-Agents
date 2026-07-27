def isAnagram(s: str, t: str) -> bool:
    sorted_s = "".join(sorted(s))
    sorted_t = "".join(sorted(t))

    return sorted_s == sorted_t

print(isAnagram(s = "anagram", t = "nagaram"))
print(isAnagram(s = "rat", t = "car"))
