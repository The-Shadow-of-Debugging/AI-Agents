n, q = map(int, input().split())

count = [0] * n
diff = [0] * (n + 1)
max = 0

a = list(map(int, input().split()))
a.sort(reverse=True)


for _ in range(q):
    l, r = map(int, input().split())
    diff[l - 1] += 1
    diff[r] -= 1

current_sum = 0

for i in range(n):
    current_sum += diff[i]
    count[i] = current_sum

count.sort(reverse=True)

for i in range(n):
    max += a[i] * count[i]

print(max)