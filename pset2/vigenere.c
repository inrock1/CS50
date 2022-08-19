#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    else
    {
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            // проверка чтоб были только буквы
            if (!isalpha(argv[1][i]))
            {
                printf("Usage: ./vigenere keyword\n");
                return 1;
            }
        }
    }
       printf("plaintext: ");

    string key = argv[1];
    int keyLength = strlen(key);
    char temp, temp2;
    string text = get_string("");
    printf("ciphertext: ");
    for (int i = 0, j = 0, n = strlen(text); i < n; i++)
    {
        // Функция tolower выполняет преобразование прописных букв в строчные.
        // letterKey текущее значение на сколько сдвигать текущщую букву
        int letterKey = tolower(key[j % keyLength]) -'a';
        if (isupper(text[i]))
        {
            printf("%c", 'A' + (text[i] -'A' + letterKey) % 26);
           j++;
        }
        else if (islower(text[i]))
        {
            temp = text[i] - 'a';
            temp2 = 'a' + (temp + letterKey) % 26;
            printf("%c", temp2);
            j++;
        }
        else
        {
           printf("%c", text[i]);
        }
    }
      printf("\n");
    return 0;
}
