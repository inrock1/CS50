# Программа принмает с аргументом командного рядка имя файла .txt со списком слов которые надо забанить.
# Принимает строку, и выводит ее же но с цензурой.

from sys import argv

# проверка, если с консоли был введен 0 или более одного слова.
if len(argv) != 2:
    print("Usage: python bleep.py dictionary")
    exit(1)

name_banned_file = argv[1]
my_file = open(name_banned_file)
banned_word = my_file.read()

message = input("What message would you like to censor?\n")
split_message = message.split()

for i in split_message:
    i_l = i.lower()
    if i_l in banned_word:
        print(len(i_l)*"*", end=" ")
    else:
        print(i, end=" ")
print()
my_file.close()
