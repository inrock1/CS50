#include <stdio.h>
#include <cs50.h>

int main()
{
    long long number = get_long_long("Number: ");
    int x1 = 0, x2 = 0, character_count = 0, sum3 = 0, sum = 0, first_two_dig,  sum6;
	bool valide;

    while (number > 0)
    {
        x2 = x1;   // предпоследний знак
        x1 = number % 10;   // последний знак

        if (character_count % 2 == 0)   // для четных знаков
        {
            sum += x1;
        }
        else  // для не четных знаков
        {
            sum6 = 2 * x1;
            sum3 += (sum6 / 10) + (sum6 % 10);
        }

        number /= 10;
        character_count++;
//        printf("%lld\n", i);
    }

    valide = (sum + sum3) % 10 == 0;
    first_two_dig = (x1 * 10) + x2; //первые 2 цифры

    if (x1 == 4 && character_count >= 13 && character_count <= 16 && valide)
    {
        printf("VISA\n");
    }
    else if (first_two_dig >= 51 && first_two_dig <= 55 && character_count == 16 && valide)
    {
        printf("MASTERCARD\n");
    }
    else if ((first_two_dig == 34 || first_two_dig == 37) && character_count == 15 && valide)
    {
        printf("AMEX\n");
    }
    else
    {
        printf("INVALID\n");
    }
}