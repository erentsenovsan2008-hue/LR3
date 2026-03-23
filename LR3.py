import numpy as np
from fractions import Fraction


def create_ahp_matrix(n):  # Создаётся матрица попарных сравнений для критериев
    """Создание матрицы парных сравнений"""
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            if i == j:
                matrix[i][j] = 1  # На главной диагонали все значения равны 1
            else:
                value = round(float(Fraction(input(f"Сравнение критерия {i + 1} с {j + 1}: "))),
                              3)  # Выше главной диагонали вводятся значения в виде: 1, 1/2, 3...; Значения в виде 1/2 переводятся в float и округляются до тысячных
                matrix[i][j] = value
                matrix[j][i] = round(1 / value,
                                     3)  # Значения ниже главной диагонали являются обратными к значениям, симметричным относительно главной диагонали
    return matrix


def create_ahp_matrix_alternative(
        n):  # Создаётся матрица попарных сравнений для альтернатив (далее то же самое, что и в предыдущей фукнции)
    """Создание матрицы парных сравнений"""
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            if i == j:
                matrix[i][j] = 1
            else:
                value = round(float(Fraction(input(f"Сравнение альтернативы {i + 1} с {j + 1}: "))), 3)
                matrix[i][j] = value
                matrix[j][i] = round(1 / value, 3)
    return matrix


array_criterion = ['стоимость', 'репутация', 'местоположение', 'программы', 'трудоустройство']  # критерии для сравнения
print('критерии:')
for i in range(len(array_criterion)):
    print(f'{i + 1}) {array_criterion[i]}')  # Выводятся критерии по номерам
matrix_criterion = create_ahp_matrix(5)  # Создана матрица попарных сравнений критериев
print(f'Матрица попарных сравнений для критериев:\n{matrix_criterion}')
print()


def weight_matrix(matrix):  # Вычисляется матрица веса (весовой столбец)
    '''Вычисление весового столбца'''
    normal_matrix = np.round(matrix / np.sum(matrix, axis=0), 3)  # Сначала нормализируется матрица попарных сравнений
    print(f'Нормализация матрицы попарных сранений:\n{normal_matrix}')
    weight_array = np.round(np.mean(normal_matrix, axis=1),
                            4)  # И вычисялется среднее значение в каждой строке (итоговой столбец = весовой столбец)
    print(f'Весовой столбец: {weight_array}')
    return weight_array


weight_array_criterion = weight_matrix(matrix_criterion)  # Весовой столбец выводится в виде 1 строки
weight_matrix_criterion = np.array([weight_array_criterion]).reshape(-1,
                                                                     1)  # Весовой столбец выводится в виде матрицы (1 столбец)

matrix_alternatives_all = []  # Список, в к-ом будут храниться 5 матриц попарных сравнений альтернатив (каждая матрица по 1 из критериев)
array_university = ['МАИ', 'МГУ', 'МФТИ']  # вузы для сравнения
for crit in range(len(array_criterion)):  # Цикл для создания каждой из 5 матриц
    print(f'критерий {crit + 1}) {array_criterion[crit]}')
    print('ВУЗы:')
    for i in range(len(array_university)):
        print(f'{i + 1}) {array_university[i]}')  # Вывод каждого вуза по номерам
    matrix_alternative = create_ahp_matrix_alternative(
        len(array_university))  # Создаётся матрица попарных сравнений альтернатив
    print(matrix_alternative)
    matrix_alternatives_all.append(matrix_alternative)

weight_alternatives = []  # Матрица для хранения весовых столбцов (в виде строк) для матриц попарных сравнений альтернатив
for matrix in matrix_alternatives_all:  # Цикл перебирает матрицы попарных сравнений альтернатив
    weight_array = weight_matrix(matrix)  # Весовой столбец (в виде строки) матрицы попарных сравнений альтернатив
    weight_alternatives.append(weight_array)

weight_matrix_alternatives = np.array(
    weight_alternatives).T  # Транспонирование матрицы, содержащей весовые строки (чтобы получились весовые столбцы)
print(weight_matrix_alternatives)

print('Итоговая матрица веса альтернатив с точки зрения достижения цели (учёт критериев):')
total_matrix = np.dot(weight_matrix_alternatives,
                      weight_matrix_criterion)  # Умножение матрицы, содержащей весовые столбцы для матриц попарных сравнений альтернатив, на матрицу, содержащую весовой столбец для матрицы попарных сравнений критериев
print(total_matrix)
print()
for i in range(len(total_matrix)):
    print(
        f'{array_university[i]}: {(total_matrix[i]) * 100}%')  # Выводятся значения каждой ячейки итоговой матрицы веса, соответсвующие ВУЗу, в виде: ВУЗ: ...%
