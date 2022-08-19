# условие задачи, 6ая неделя, "Cash". https://courses.prometheus.org.ua/courses/course-v1:Prometheus+CS50+2019_T1/course/

from cs50 import get_float
import sys

# проверка, если с консоли был введен 0 или более одного входного числа - то выход с программы.
if len(sys.argv) != 2:
    sys.exit(1)

# transfer key to variable
k = int(sys.argv[1])
k = k % 26
p = input("plaintext: ")

print("ciphertext: ", end="")
for i in p:
    temp = int(ord(i))  #ord() Возвращает числовой номер ASCII для указанного символа.
    if temp >= 65 and temp <= 90:
        if temp + k > 90:
            temp = temp + k - 26
        else:
            temp = temp + k
    elif temp >= 97 and temp <= 122:
        if temp + k > 122:
            temp = temp + k - 26
        else:
            temp = temp + k
    else:
        temp = temp
    i = chr(temp)  # #Возвращает символ для указанного числового номера ASCII
    print(i, end="")
print()