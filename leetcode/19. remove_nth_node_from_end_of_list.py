def removeNthFromEnd(self, head, n: int):
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy

    for i in range(n + 1):
        fast = fast.next

    while fast:
        slow = slow.next
        fast = fast.next

    if slow.next:
        slow.next = slow.next.next

    return dummy.next