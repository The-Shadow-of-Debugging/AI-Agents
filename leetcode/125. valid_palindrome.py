def isPalindrome(s: str) -> bool:
    prepared_str = "".join([char for char in s if char.isalnum()]).lower()

    return prepared_str == prepared_str[::-1]

print(isPalindrome("A man, a plan, a canal: Panama"))
print(isPalindrome("race a car"))
print(isPalindrome(" "))
print(isPalindrome("0P"))