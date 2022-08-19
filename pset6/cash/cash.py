# условие задачи, 6ая неделя, "". https://courses.prometheus.org.ua/courses/course-v1:Prometheus+CS50+2019_T1/course/
from cs50 import get_float

while True:
    dollars = get_float("Change owed: ")
    if dollars > 0:
        break

#convert $ to cents and round
cents=round(dollars*100)

co25=cents//25
residual=cents%25
co10=residual//10
residual=residual%10
co5=residual//5
residual=residual%5

coins=co25+co10+co5+residual
print(coins)