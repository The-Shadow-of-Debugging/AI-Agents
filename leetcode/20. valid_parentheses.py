def isValid(s: str) -> bool:
    bracket_hash = {
        ']': '[',
        '}': '{',
        ')': '('
    }

    bracket_stack = []

    for char in s:
        if char not in bracket_hash:
            bracket_stack.append(char)
        elif len(bracket_stack) and bracket_hash[char] == bracket_stack[-1]:
            bracket_stack.pop()
        else:
            return False

    return len(bracket_stack) == 0


print(isValid(s = "()"))
print(isValid(s = "()[]{}"))
print(isValid(s = "(]"))
print(isValid(s = "([])"))
print(isValid(s = "([)]"))
print(isValid(s = "["))
print(isValid(s = "]"))