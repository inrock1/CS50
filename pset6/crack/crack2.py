# при вызове программы, аргументом командного рядка надо передать хэш для подбора пароля, например 51v3Nh6ZWGHOQ  (ответ: ROFL)
# условие задачи, 6ая неделя, "Crack". https://courses.prometheus.org.ua/courses/course-v1:Prometheus+CS50+2019_T1/course/

import sys
import crypt

def main():
    if len(sys.argv) != 2:
        print("Need only password <hash>")
        sys.exit(1)

entered_hash = sys.argv[1]
#entered_hash = "51.xJagtPnb6s"
salt = entered_hash[0:2]
available_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

for fifth in available_letters:
    for fourth in available_letters:
        for third in available_letters:
            for second in available_letters:
                for first in available_letters:
                    passw = f"{first}{second}{third}{fourth}{fifth}".strip()
                    if crypt.crypt(passw, salt) == entered_hash:
	                    print(passw)
	                    sys.exit(0)
if __name__ ==	"__main__":
    main()