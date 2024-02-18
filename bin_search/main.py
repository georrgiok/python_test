
import bisect


def bi_find(list_, target):
    result = bisect.bisect_left(list_, target)
    if result < len(list_) and list_[result] == target:
        return result
    else:
        return -1


my_list = [20, 30, 40, 50, 60, 70, 80, 90]

target = 50
result = bi_find(my_list, target)
print(result)
# result = 3

target = 61
result = bi_find(my_list, target)
print(result)
# result = -1

target = 90
result = bi_find(my_list, target)
print(result)
# result = 7
