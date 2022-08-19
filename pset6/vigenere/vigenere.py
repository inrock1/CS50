# условие задачи, 6ая неделя, Шифрование сообщения шифром Vigenere. https://courses.prometheus.org.ua/courses/course-v1:Prometheus+CS50+2019_T1/courseware/c0265c89598e4cb5aefc9f4d98bb05f4/e87556b3528245e58c38691c468d3003/?activate_block_id=block-v1%3APrometheus%2BCS50%2B2019_T1%2Btype%40sequential%2Bblock%40e87556b3528245e58c38691c468d3003
from cs50 import get_string
import sys

# transfer key to variable
k = sys.argv[1]

# проверка, если с консоли был введен 0 или более одного входного числа - то выход с программы.
# isalpha проверка, действительно ли там только буквы
if len(sys.argv) != 2 or not k.isalpha():
    print("Usage: python vigenere.py k")
    sys.exit(1)

p = get_string("plaintext: ")
j = 0

print("ciphertext: ", end="")

for ch in p:
        if not ch.isalpha(): # проверяем каждый символ, если не буква пропускаем шифровку
            print(ch, end="")
            continue
        # задаем смещение по таблице АСКИ
        ascii_offset = 65 if ch.isupper() else 97
            # ord() Возвращает числовой номер ASCII для указанного символа.
            # chr() Возвращает символ для указанного числового номера ASCII
        # приводим текущий символ исходного сообщения, в формат А/а = 0, Z/z = 25
        pi = ord(ch) - ascii_offset

        # приводим для каждого текущего символа соответсвующий символ ключа, в формат А/а = 0, Z/z = 25
        # upper() - Возвращает копию исходной строки с символами приведёнными к верхнему регистру
        kj = ord(k[j % len(k)].upper()) - 65
        j += 1
        # вычисляем сдвинутый символ и делаем перенос символ + ключ если превышает длину алфавита 26.
        ci = (pi + kj) % 26
        print(chr(ci + ascii_offset), end="")
print()





