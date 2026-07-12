def solve():
    n, k = map(int, input().split())
    platforms = list(map(int, input().split()))

    # Отмечаем надежные платформы
    safe = [False] * (n + 1)
    for x in platforms:
        safe[x] = True
    safe[0] = True
    safe[n] = True

    # Проверяем возможность добраться
    points = [0] + platforms
    if n not in points:
        points.append(n)
    points.sort()

    for i in range(1, len(points)):
        if points[i] - points[i - 1] > 2:
            print(-1)
            return

    # DP от конца к началу
    INF = 10 ** 9
    dp = [INF] * (n + 1)
    dp[n] = 0

    for i in range(n - 1, -1, -1):
        if not safe[i]:
            continue

        # Смотрим, куда можно прыгнуть
        for jump_len in (1, 2):
            nxt = i + jump_len
            if nxt <= n and safe[nxt]:
                if dp[nxt] + 1 < dp[i]:
                    dp[i] = dp[nxt] + 1

    if dp[0] == INF:
        print(-1)
        return

    # Восстанавливаем путь, выбирая лексикографически минимальный
    path = []
    curr = 0

    while curr < n:
        # Пробуем прыжок на 1
        if curr + 1 <= n and safe[curr + 1] and dp[curr + 1] == dp[curr] - 1:
            # Проверяем, можно ли отсюда добраться до конца
            path.append(1)
            curr += 1
        # Пробуем прыжок на 2
        elif curr + 2 <= n and safe[curr + 2] and dp[curr + 2] == dp[curr] - 1:
            path.append(2)
            curr += 2
        else:
            # Этого не должно случиться, если путь существует
            break

    print(len(path))
    print(''.join(map(str, path)))


solve()