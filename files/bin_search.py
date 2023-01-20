array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
n = len(array)
x = 9

left = 0
right = n
# Пока левый индекс меньше, чем правый
while left < right:
    mid = (left + right) // 2  # находим средний
    # Если элемент равен искомому, то выводим его и выходим из цикла
    if array[mid] == x:
        print(mid)
        break
    # если меньше, то сдвигаем левую границу к середине
    elif array[mid] < x:
        left = mid + 1
    else:
        # иначе правую
        right = mid
else:
    # если элемент не найден в массиве
    print(-1)