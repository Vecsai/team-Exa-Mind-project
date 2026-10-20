x = float(input('Введите координату по x:'))
y = float(input('Введите координату по y:'))

if (x >= -2 and x <= 2) and (y >= 0 and y <= 2):
    print('Попадает')
else:
    if y >= -((1 - x ** 2)**1/2):
        print('НЕ попадает')
    else:
        if y >= -((4 - x ** 2)**1/2):
            print('Попадает')
        else:
            print('НЕ попадает')
