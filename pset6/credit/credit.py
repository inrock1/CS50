# условие задачи, 6ая неделя, "Credit". https://courses.prometheus.org.ua/courses/course-v1:Prometheus+CS50+2019_T1/course/

from cs50 import get_float
import sys
while True:
    number = input("Number:")
    character_count = number.count('')-1
# card validation
    if character_count == 13 or character_count == 15 or character_count == 16:
        break
    print("INVALID")
    sys.exit()

# проверка на четность номера карты
if character_count% 2 == 0:
    count_even = 'even'
else:
    count_even = 'odd'

sum1 = 0
sum2 = 0
sum3 = 0
sum4 = 0
sum5 = 0

# вариант с НЕЧЁТНЫМ кол-вом цифр в номере карты
for i in range(character_count):
    cur_fig = int(number[i])  # current figure
# считаем сумму ту что умножать на 2 (нечётные индексы)
    if count_even == 'odd' and i % 2 != 0:
        if cur_fig*2 < 10:
            sum1 = cur_fig*2+sum1
        else:
            sum2 = sum2 + (1+cur_fig*2 % 10)
        sum3 = sum1 + sum2
# считаем сумму ту что умножать на 1 (чётные индексы)
    if count_even == 'odd' and i % 2 == 0:
        sum4 = sum4 + cur_fig
    sum5 = sum3 + sum4

# вариант с ЧЁТНЫМ кол-вом цифр в номере карты
for i in range(character_count):
    cur_fig = int(number[i])  # current figure
# считаем сумму ту что умножать на 2 (нечётные индексы)
    if count_even == 'even' and i % 2 == 0:
        if cur_fig*2 < 10:
            sum1 = cur_fig*2+sum1
        else:
            sum2 = sum2 + (1+cur_fig*2 % 10)
        sum3 = sum1 + sum2
# считаем сумму ту что умножать на 1 (чётные индексы)
    if count_even == 'even' and i % 2 != 0:
        sum4 = sum4 + cur_fig
    sum5 = sum3 + sum4

if sum5 % 10 == 0:
    if character_count == 15:
        print("AMEX")
    elif character_count == 16 and number[0] == '5' and number[1] >= '1' and number[1] <= '5':
        print("MASTERCARD")
    elif character_count == 13 or character_count == 16 and number[0] == '4':
        print("VISA")
else:
    print("INVALID")


