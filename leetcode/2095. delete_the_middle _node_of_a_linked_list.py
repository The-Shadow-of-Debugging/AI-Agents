def deleteMiddle(head):
    if not head.next:
        return head.next

    slow = ListNode(-1, head)
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    if slow.next:
        slow.next = slow.next.next

    return head