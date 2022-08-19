# при вызове программы, аргументом командного рядка надо передать хэш для подбора пароля, например 51v3Nh6ZWGHOQ
# второй варинт решения задачи. Через комбинаторную перестановку.
# условие задачи, 6ая неделя, "Crack". https://courses.prometheus.org.ua/courses/course-v1:Prometheus+CS50+2019_T1/course/
import crypt
import sys
import itertools

# проверка, если с консоли был введен 0 или более одного входного числа - то выход с программы.
if len(sys.argv) != 2:
    print("Need only password <hash>")
    sys.exit(1)

# transfer hash to variable
hash_1 = sys.argv[1]
st = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
salt = hash_1[0:2]
k = 0
for x in itertools.permutations(st,5):
    a = ''.join(x)
    print(x,a)
    if crypt.crypt(a, salt) == hash_1:
        print("password = ", crypt.crypt(a, salt))
        sys.exit(0)
    k+=1
print(k)





