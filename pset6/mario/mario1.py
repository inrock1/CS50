# условие задачи, 6ая неделя, "Credit". https://courses.prometheus.org.ua/courses/course-v1:Prometheus+CS50+2019_T1/course/

from cs50 import get_int

while True:
    n = get_int("Height: ")
    if n > 0:
        if n <= 8:
            break

for i in range(n):
        print(" "*(n-i-1), end='')
        print("#"*(i+1), end='')
        print()