import numpy as np

abc = """абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,?!:;+-_—*"<>«»=()0123456789abcdefghijklmnopqrstuvwxyz"""
# abc = """abcdefghijklmnopqrstuvwxyz"""
# abc = """абвгдеёжзийклмнопрстуфхцчшщъыьэюя., ?"""

def input_key(n):# функция для ввода ключевой матрицы
    # A = np.zeros((n, n))
    # A = np.array([[3, 1, 7], [2, 0, 2], [4, 6, 5]], dtype=int)
    # # A = np.array([[0, 12, 29], [16, 9, 14], [9, 8, 13]], dtype=int)
    while True:
        print('Введите ключевую матрицу')
        A = np.zeros((n, n), dtype=int)
        for i in range(0, n):
            for j in range(0, n):
                while True:
                    print('Введите', i + 1, j + 1, 'элемент    ')
                    a = input()
                    if a.isdigit():
                        break
                    else:
                        print('Некооректный ввод')
                A[i][j] = int(a) % len(abc)
        if np.linalg.det(A) % len(abc) == 0:
            print('Ошибка: Определитель матрицы равен 0')
        else:
            break
    return A

def input_text():# функция для ввода текста; возвращает список с номерами букв текста в алфавите
    print('Введите текст')
    text = input()
    x = []
    for i in text.lower():
        try:    #если символа нет в алфавите, то он удаляется
            x.append(abc.index(i))
        except ValueError:
            continue
    return x

def input_block():# функция для ввода длины блока
    while True:
        a = input('Введите длину блока    ')
        if a == '1':
            print('Ошибка: При блоках длины 1 шифрование поэлементное, а не поблочное')
        elif int(a) <= 0:
            print('Ошибка: Размер блока должен быть натуральным числом')
        elif a.isdigit():
            return int(a)
        else:
            print('Ошибка: Некорректный ввод')
    # return 3

def save_key(A):
    while True:
        a = input('Сохранить ключевую матрицу (только в этом сеансе)? y/n  ')
        if a == 'y':
            return A
        elif a == 'n':
            A = np.zeros((1, 1), dtype=int)
            return A
        else:
            print('Ошибка: Некорректный ввод')

def make_abc(y):
    yabc = []
    for i in y:
        i = i % len(abc)
        yabc.append(abc[i])
    return(yabc)

def enc_hill(A):
    text = input_text()
    A = check_ecxist_mat(A, 1)
    print('Ключевая матрица:\n', A)
    n = A.shape[0]
    text = add_text(text, n)
    y = []
    for i in range(0, len(text), n):
        t = np.array(text[i: i + n:])
        y = y + np.dot(t, A).tolist()
    k = ''.join(make_abc(y))
    print('Шифртекст: ', k)
    return save_key(A)

def find_inverse_element(a):
    for i in range(1, len(abc)):
        k = a * i
        while True:
            k = k - len(abc)
            if k == 1:
                return i
            elif k < 1:
                break

def dec_hill(A):
    text = input_text()
    A = check_ecxist_mat(A, 1)
    print('Ключевая матрица:\n', A)
    n = A.shape[0]
    text = add_text(text, n)
    y = []
    B = np.zeros((n, n), dtype=int)
    inv_det = find_inverse_element(round(np.linalg.det(A)) % len(abc))
    for i in range(0, n):
        for j in range(0, n):
            B[i][j] = round(np.linalg.inv(A)[i][j] * round(np.linalg.det(A)))
            B[i][j] = B[i][j] * inv_det % len(abc)
    for i in range(0, len(text), n):
        t = np.array(text[i: i + n:])
        y = y + np.dot(t, B).tolist()
    k = ''.join(make_abc(y))
    print('Открытый текст: ', k)
    return save_key(A)

def check_ecxist_mat(A, n):
    if np.all(A == 0):
        if n == 1:
            n = input_block()
        A = input_key(n)
    return A

def add_text(text, n): #дополняет текст до целоко количества блоков
    while len(text) % n != 0:
        text.append(abc.index(' '))
    return text

def dec_rec_hill(A, B):
    text = input_text()
    Key = []
    n = A.shape[0]
    Key.append(check_ecxist_mat(A, n))
    n = Key[0].shape[0]
    Key.append(check_ecxist_mat(B, n))
    A = Key[0]
    B = Key[1]
    print('Первая ключевая матрица:\n', Key[0])
    print('Вторая ключевая матрица:\n', Key[1])
    text = add_text(text, n)
    for k in [0, 1]:
        inv_det = find_inverse_element(round(np.linalg.det(Key[k])) % len(abc))
        InverseMat = np.zeros((n, n), dtype=int)
        for i in range(0, n):
            for j in range(0, n):
                InverseMat[i][j] = round(np.linalg.inv(Key[k])[i][j] * round(np.linalg.det(Key[k])))
                InverseMat[i][j] = InverseMat[i][j] * inv_det % len(abc)
        del Key[k]
        Key.insert(k, InverseMat)
    for i in range(2, round(len(text) / n)):
        Key.append(np.dot(Key[i-2], Key[i-1]) % len(abc))
    for i in range(0, round(len(text) / n)):
        print('key', i, Key[i])
    k = -1
    y = []
    for i in range(0, len(text), n):
        k += 1
        t = np.array(text[i: i + n:])
        y = y + np.dot(t, Key[i - (n - 1) * k]).tolist()
    k = ''.join(make_abc(y))
    print('Открытый текст: ', k)
    return save_key(A), save_key(B)

def enc_rec_hill(A, B):
    text = input_text()
    Key = []
    n = A.shape[0]
    Key.append(check_ecxist_mat(A, n))
    n = Key[0].shape[0]
    Key.append(check_ecxist_mat(B, n))
    # if np.all(B == 0):
    #     Key.append(check_ecxist_mat(A, 0))
    #     n = A.shape[0]
    #     Key.append(check_ecxist_mat(B, n))
    # else:
    #     n = B.shape[0]
    #     Key.append(check_ecxist_mat(A, n))
    print('Первая ключевая матрица:\n', Key[0])
    print('Вторая ключевая матрица:\n', Key[1])
    text = add_text(text, n)
    for i in range(2, round(len(text) / n)):
        Key.append(np.dot(Key[i-1], Key[i-2]) % len(abc))
        # print('key', i, Key[i])
    k = -1
    y = []
    for i in range(0, len(text), n):
        k += 1
        t = np.array(text[i: i + n:])
        y = y + np.dot(t, Key[i - (n - 1) * k]).tolist()
        # print('t', t)
        # print('k', Key[i - (n - 1) * k])
    k = ''.join(make_abc(y))
    print('Шифртекст: ', k)
    return save_key(Key[0]), save_key(Key[1])


# b = 'n'
# A = np.zeros((1, 1), dtype=int)
# B = np.zeros((1, 1), dtype=int)
# while b == 'n':
#     while True:
#         print(
#             """Что вы хотите сделать?\n1 - зашифровать шифром Хилла\n2 - расшифровать шифр Хилла\n3 - зашифровать реккурентным шифром Хилла\n4 - расшифровать реккурентный шифр Хилла""")
#         a = input()
#         a = a.replace(' ', '')
#         if a == '1':
#             A = enc_hill(A)
#             break
#         elif a == '2':
#             A = dec_hill(A)
#             break
#         elif a == '3':
#             A, B = enc_rec_hill(A, B)
#             break
#         elif a == '4':
#             A, B = dec_rec_hill(A, B)
#             break
#         else:
#             print('Ошибка: Некорректный выбор действия')
#     while True:
#         print('Завершить работу программы? y/n')
#         b = input()
#         b = b.replace(' ', '')
#         if b == 'y' or b == 'n':
#             break
#         else:
#             print('Ошибка: Некорректный ввод')