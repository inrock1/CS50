#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    bool Success = false;
    int key = 0;
    int text_length = 0;
    string text = "";
    do
    {
        // проверка, если с консоли был введен 0 или более одного входного числа - то выход с программы.
        // argc - argument count - это количество аргументов командной строки.
        if(argc != 2)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        // argv[] - argument vector - массив значений этих аргументов
        // strlen() - возвращает длину строки
        for (int j = 0, n = strlen(argv[1]); j < n; j++)
        {

        // isdigit() возвращает ненулевое значение, если аргумент ch является цифрой от 0 до 9, в противном случае возвращается 0.
        if (! isdigit(argv[1][j]))
            {
                printf("Usage: ./caesar key\n");
            return 1;
            }
        }

        // atoi() конвертирует строку, на которую указывает параметр str, в величину типа int.
        key = atoi(argv[1]);
        if (key < 0)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        	else
        	{
        	Success = true;
        	printf("plaintext: ");
        	}
    }
    while(!Success);

    text = get_string("");
    printf("ciphertext: ");
    text_length = strlen(text);
    for(int i = 0; i < text_length; i++)
    {
        // isalpha() возвращает ненулевое значение, если его аргумент является буквой алфавита
        if(isalpha(text[i]))
        {
            // islower() возвращает ненулевое значение, если аргумент ch является буквой нижнего регистра (от «а» до «z»); в противном случае возвращается 0.
            if(islower(text[i]))
            {
                printf("%c", ((((text[i] - 97)+key)%26)+97));
            }
            else
            {
                printf("%c", ((((text[i] - 65)+key)%26)+65));
            }
        }
        else
        {
            printf("%c", text[i]);
        }
    }
printf("\n");
return 0;
}