def mergeTwoLists(list1, list2):
    merged_list = new ListNode(-1)
    current = merged_list

    while list1 or list2:
        if list1.val > list2.val:
            merged_list.next = list1
            list1 = list1.next
        else:
            merged_list.next = list2
            list2 = list2.next

        merged_list = merged_list.next

    if list1:
        merged_list.next = list1

    if list2:
        merged_list.next = list2

    return current.next
