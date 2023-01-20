array = [1, 4, 0, 3, 2] # исходный массив
n = len(array) # его длина

for i in range(n - 1): # перебираем все элементы массива
    # flag = True
    for j in range(n - i - 1): # перебираем все элементы от нулевого элемента до уже отсортированных
        if array[j] > array[j + 1]: # если левый больше, чем правый
            array[j], array[j + 1] = array[j + 1], array[j] # меняем их местами
            # flag = False
    # if flag:
    #     break

print(array)