# Функция-генератор для чтения слов (токенов) из входного потока
def get_tokens():
    while True:
        try:
            line = input()
            if not line:
                break
            for word in line.split():
                yield word
        except EOFError:
            break


tokens = get_tokens()

# Читаем n и m
try:
    line_n = next(tokens)
    line_m = next(tokens)
    n = int(line_n)
    m = int(line_m)
except StopIteration:
    n = 0

if n > 0:
    epochs = []
    for _ in range(n):
        row = []
        for _ in range(m):
            row.append(int(next(tokens)))
        row.sort()  # Сортируем артефакты внутри эпохи
        epochs.append(row)

    # --- Ручная реализация Min-Heap (минимальной кучи) ---
    heap = []


    def heap_push(val, ep_idx, val_idx):
        heap.append((val, ep_idx, val_idx))
        curr = len(heap) - 1
        while curr > 0:
            parent = (curr - 1) // 2
            if heap[curr][0] < heap[parent][0]:
                heap[curr], heap[parent] = heap[parent], heap[curr]
                curr = parent
            else:
                break


    def heap_pop():
        if len(heap) == 1:
            return heap.pop()
        top = heap[0]
        heap[0] = heap.pop()
        curr = 0
        while True:
            left = 2 * curr + 1
            right = 2 * curr + 2
            smallest = curr
            if left < len(heap) and heap[left][0] < heap[smallest][0]:
                smallest = left
            if right < len(heap) and heap[right][0] < heap[smallest][0]:
                smallest = right
            if smallest != curr:
                heap[curr], heap[smallest] = heap[smallest], heap[curr]
                curr = smallest
            else:
                break
        return top


    # --- Инициализация ---
    current_max = -1
    current_sum = 0
    for i in range(n):
        val = epochs[i][0]
        heap_push(val, i, 0)
        if val > current_max:
            current_max = val
        current_sum += val

    best_range = 2 * (10 ** 18)  # Очень большое число
    best_sum = 2 * (10 ** 18)
    best_min_val = -1

    # --- Основной цикл алгоритма ---
    while True:
        min_val, ep_idx, val_idx = heap_pop()

        curr_range = current_max - min_val

        # Проверка на лучший результат
        if curr_range < best_range:
            best_range = curr_range
            best_sum = current_sum
            best_min_val = min_val
        elif curr_range == best_range:
            if current_sum < best_sum:
                best_sum = current_sum
                best_min_val = min_val

        # Переходим к следующему элементу в той же эпохе
        if val_idx + 1 < m:
            next_val = epochs[ep_idx][val_idx + 1]
            current_sum = current_sum - min_val + next_val
            if next_val > current_max:
                current_max = next_val
            heap_push(next_val, ep_idx, val_idx + 1)
        else:
            # Если в какой-то эпохе элементы кончились, размах больше не уменьшить
            break

    # --- Восстановление ответа ---
    ans = []
    for i in range(n):
        # Ручной бинарный поиск для нахождения первого элемента >= best_min_val
        arr = epochs[i]
        low = 0
        high = m - 1
        found = arr[-1]
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] >= best_min_val:
                found = arr[mid]
                high = mid - 1
            else:
                low = mid + 1
        ans.append(found)

    # Сортируем и выводим итоговую последовательность
    ans.sort()
    print(*(ans))