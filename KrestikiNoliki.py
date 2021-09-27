import random
#import time


def greet():
    print("-------------------")
    print("  Приветсвуем вас  ")
    print("      в игре       ")
    print("  крестики-нолики  ")
    print("-------------------")
    print(" формат ввода: x y ")
    print(" x - номер столбца ")
    print(" y - номер строки  ")
    print()
    print("   Играют два ИИ   ")


def creat_field(_field=None, _x=3, _y=3, _empty='-'):
    if _field is None:
        _field = []
    _field = [[_empty for i in range(_x)] for i in range(_y)]
    return _field


def draw_field(_field, _makr=True):
    if _makr:  # пеать номеров
        print('\t  ', end='')
        for x in range(len(_field[0])):
            print(' '+str(x), end='')
        print()
    for y in range(len(_field)):  # Печать поля
        print('\t', end='')
        if _makr:
            print(str(y)+' ', end='')
        for x in range(len(_field[y])):
            print(' '+str(_field[y][x]), end='')
        print()


def check_point(_field, _x, _y, _empty):
    if _field[_y][_x] == _empty:
        return True
    return False


# поиск второй вражеской точки на линии
def search_second_enemy(_field, _x, _y, _enemy):
    res = []
    if _x < 2 and _y < 2:
        if _field[_y+1][_x+1] == _enemy:
            res.append([(_x+1), (_y+1)])
    if _x < 2:
        if _field[_y][_x+1] == _enemy:
            res.append([(_x+1), (_y)])
    if _y < 2:
        if _field[_y+1][_x] == _enemy:
            res.append([(_x), (_y+1)])
    if not _x and not _y:
        if _field[2][2] == _enemy:
            res.append([(2), (2)])
    if not _x:
        if _field[_y][2] == _enemy:
            res.append([(2), (_y)])
    if not _y:
        if _field[2][_x] == _enemy:
            res.append([(_x), (2)])

    if res == []:
        res = None
    # print('search_second_enemy',res)
    return res


def sap(q1, q2):  # Поиск координаты между двумя точками
    z = abs(q1-q2)
    if z == 0:
        return q1
    if z == 1 and min(q1, q2) == 0:
        return 2
    if z == 1 and min(q1, q2) == 1:
        return 0
    if z == 2:
        return 1


def search_empty_point(_field, _x, _y, _enemy, _second_enemy, _empty):
    res = []
    for x, y in _second_enemy:
        ry = sap(y, _y)  # Поиск координаты между двумя точками
        rx = sap(x, _x)
        if _field[ry][rx] == _empty:
            res.append([rx, ry])
    if res == []:
        res = None
    # print('search_empty_point',res)
    return res


def search_two_points(_field, _enemy, _empty):
    res = []
    for y in range(3):
        for x in range(3):
            if _field[y][x] == _enemy:  # нашли вражескую точку
                # поиск второй вражеской точки на линии
                second_enemy = search_second_enemy(_field, x, y, _enemy)
                # Найдены в линию две вражеские точки
                if second_enemy is not None:
                    # поиск пустой точки между ними
                    empty_point = search_empty_point(
                        _field, x, y, _enemy, second_enemy, _empty)
                    # если нашли пустую точку между двумя вражескими
                    if empty_point is not None:
                        # print('empty_point',empty_point)
                        # передаём координаты для установки точки
                        res = empty_point[0]
    if res == []:
        res = None
    # print('search_two_enemys',res)
    return res


def search_enemys(_field, _empty):  # Поиск пустой точки
    if check_point(_field, 1, 1, _empty):
        return [1, 1]
    points = [[0, 0], [0, 2], [2, 0], [2, 2]]  # угловые точки
    for i in range(10):
        x, y = random.choice(points)
        if check_point(_field, x, y, _empty):
            return [x, y]
    points = [[1, 0], [0, 1], [2, 1], [1, 2]]  # боковые точки
    for i in range(10):
        x, y = random.choice(points)
        if check_point(_field, x, y, _empty):
            return [x, y]

    # поиск последней оставшейся
    for y in range(3):
        for x in range(3):
            if check_point(_field, x, y, _empty):
                return [x, y]
    print('нет свободных точек, крит ошибка')
    raise


def ai_move(_field, _mark, _enemy, _empty):
    res = search_two_points(_field, _mark, _empty)  # Поиск 2 всоих точек рядом
    if res is not None:
        return [res[0], res[1]]

    # Поиск 2 точек противника рядом
    res = search_two_points(_field, _enemy, _empty)
    if res is not None:
        return [res[0], res[1]]
    # print('Проверка двух точет противника, крит ошибка')
    # res.append(empty_point[0])

    res = search_enemys(_field, _empty)  # Поиск пустой точки
    if res is not None:
        return [res[0], res[1]]
    # print('Проверка двух точет противника, крит ошибка')
    # res.append(empty_point[0])


def check_game(_field, _mark, _empty):
    win = False
    global p1

    if (check_point(_field, 0, 0, _mark)
            and check_point(_field, 0, 1, _mark)
            and check_point(_field, 0, 2, _mark)):
        win = True

    if (check_point(_field, 1, 0, _mark)
            and check_point(_field, 1, 1, _mark)
            and check_point(_field, 1, 2, _mark)):
        win = True

    if (check_point(_field, 2, 0, _mark)
            and check_point(_field, 2, 1, _mark)
            and check_point(_field, 2, 2, _mark)):
        win = True

    if (check_point(_field, 0, 0, _mark)
            and check_point(_field, 1, 0, _mark)
            and check_point(_field, 2, 0, _mark)):
        win = True

    if (check_point(_field, 0, 1, _mark)
            and check_point(_field, 1, 1, _mark)
            and check_point(_field, 2, 1, _mark)):
        win = True

    if (check_point(_field, 0, 2, _mark)
            and check_point(_field, 1, 2, _mark)
            and check_point(_field, 2, 2, _mark)):
        win = True

    if (check_point(_field, 0, 2, _mark)
            and check_point(_field, 1, 1, _mark)
            and check_point(_field, 2, 0, _mark)):
        win = True

    if (check_point(_field, 0, 0, _mark)
            and check_point(_field, 1, 1, _mark)
            and check_point(_field, 2, 2, _mark)):
        win = True

    if win:
        if _mark == p1:
            print('\tПобедил первый игрок!!!')
        else:
            print('\tПобедил второй игрок!!!')
        return True

    for y in range(3):
        for x in range(3):
            if (check_point(_field, x, y, _empty)):
                return False

    print('\tНичья !!!!')
    return True

#    print( check_point(_field, 0, 0, _mark))
#    print( check_point(_field, 0, 1, _mark))
#    print( check_point(_field, 0, 2, _mark) )

def user_move(_field, _mark, _enemy, _empty):
    while True:
        ss = input('Ваш ход: ').split()
        if len(ss) != 2:
            print('Введите 2 координаты!')
            continue
        x, y = ss
        
        if not(x.isdigit()) or not(y.isdigit()):
            print('Введите два числа')
            continue
        
        x, y = int(x), int(y)
        
        if not((0<= x < 3) and (0<= y < 3)):
            print('За пределами поля')
            continue
            
        if _field[y][x] == _empty:
            return [x, y]
        print('В эту точку уже ходили')
            

def action(_field, _mark, _enemy, _empty, _who='ai'):
    res = []
    global p1
    # print(win_game(_field, _mark))

    if _who == 'ai':
        res = ai_move(_field, _mark, _enemy, _empty)
    else:
        res = user_move(_field, _mark, _enemy, _empty)
    # print(res)

    if res == []:
        print('не нашел куда пойти, крит ошибка')
        raise

    # Установка точки
    if check_point(_field, res[0], res[1], _empty):  # Проверка пустой точки
        print('--------------------------------------')
        if _mark == p1:
            print('Ход первого игрока Х:', end='')
        else:
            print('Ход воторого игрока Х:', end='')
        print(str(res[0])+', Y:' + str(res[1]) + '   '+_mark)

        _field[res[1]][res[0]] = _mark
    else:
        print('Проверка Хода, нет пустой клетки, крит ошибка')
        raise


# %%

greet()


empty = '-'  # заполнитель поля
p1 = 'X'      # метка первого игрока
p2 = 'O'      # второго игрока
desk_y = 3    # размер поля, кол строк
desk_x = 3    # размер поля, кол колонок
# создание пустого поля
field = creat_field(_x=desk_x, _y=desk_y, _empty=empty)

draw_field(field, _makr=True)
while True:
    action(field, p1, p2, empty, 'us')
    draw_field(field, _makr=True)
    if check_game(field, p1, empty):
        break

    #time.sleep(3)
    action(field, p2, p1, empty)
    draw_field(field, _makr=True)
    if check_game(field, p2, empty):
        break
    #time.sleep(3)


# draw_field(field, _makr=False)

# print(field)
# print(len(field))
