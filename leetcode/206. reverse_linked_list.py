def reverseList(head):
    prev = None
    current = head

    while current:
        next = current.next
        current.next = prev
        prev = current
        current = next

    return prev


print(reverseList([1,2]))
print(reverseList([1,2, 3, 4, 5]))
print(reverseList([]))