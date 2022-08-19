#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover filename.xxx \n");
        exit(1);
    }

    // open input file
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    FILE *outptr = NULL;  // объявляем что
    unsigned char buffer[512];
    char jpg_name[8];
    int counter = 0;
    bool flag = false;

    while (fread(buffer, 512, 1, inptr) == 1)
    {
        // check if we found a JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (flag == true)
            {
                fclose(outptr);
            }
            else
            {
                flag = true;
            }

            sprintf(jpg_name, "%03i.jpg", counter);
            outptr = fopen(jpg_name, "w");
            counter++;
        }

        if (flag == true)
            {
                fwrite(&buffer, 512, 1, outptr);
            }
    }

    fclose(inptr);
    fclose(outptr);
    return 0;
}
