#include <cs50.h>
#include <stdio.h>

int main(void)
{
   //Создаем переменные для высоты, пробелов и хэшей
    int height;
    int spaces;
    int hashes;
    int hashes2;

//делать пока не свершится то что в условии while
do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

//Создаем строки
for (int i = 1; i <= height; i++)
    {
     //Создаем столбцы пробелов
       for (spaces = (height - i); spaces > 0; spaces--)
        {
            printf(" ");
        }
     //Создаем столбцы хешей
        for (hashes = 1; hashes <= (i); hashes++)
        {
            printf("#");
        }
        printf("  ");
    //Создаем второй столбец хешей
        for (hashes2 = 1; hashes2 <= (i); hashes2++)
        {
            printf("#");
        }

        printf("\n");
    }
    return 0;
}