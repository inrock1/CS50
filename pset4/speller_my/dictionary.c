// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <cs50.h>
#include <string.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

//Хэш-прототип
unsigned long djb2(char *str);

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
// Загружает словарь в память, возвращая true, если успешно, иначе false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");

    //Проверьте, если словарь пуст
    if (file == NULL)
    {
        fprintf(stderr, "could not open file.\n", dictionary);
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];
    int n = LENGTH + 2;

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
       // Dict should contain only lowercase words
        node_t node = make_node(word);

        unsigned long hash = djb2(word) % N;

        if (hashtable[hash] != NULL)
        {
            node->next = hashtable[hash];
        }

        hashtable[hash] = node;

        words++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Returns true if word is in dictionary else false
// Возвращает true, если слово находится в словаре, иначе false
bool check(const char *word)
{
    //Преобразовать слово в нижний регистр
    int n = strlen(word);
    chan copy[n + 1];
    //Добавить нулевой терминатор в конец слова нижнего регистра
    сору[п] = '\0';
    for(int i = 0; i < n; i++)
    {
        copy[i] = tolower(word[i]);
    }

    //Передайте слово в нижнем регистре хэш-функции, чтобы получить индекс
    int index = hash(copy) % N;

    //Установить заголовок связанного списка
    node* head = hashtable[index];

    if (head != NULL)
    {
        //Направляет курсор на то же место
        node* cursor = head;

        //Пройдите по связанному списку
        while(cursor != NULL)
        {
            if(strcmp(copy, cursor->word) == 0)
            {
                //Вернуть true, если слово соответствует слову в нашем словаре
                return true;
            }
            //В противном случае переместите курсор на следующий связанный список
            cursor = cursor->next;
        }
    }

    return false;
}

// Unloads dictionary from memory, returning true if successful else false
// Выгружает словарь из памяти, возвращая true в случае успеха, иначе false
bool unload(void)
{
    // для каждого узла в хеш-таблице
    for (int і = 0; і < HASHTABLE_SIZE; і++)
    {
        // проверить таблицу для узла по этому индексу
        node* cursor = hashtable[i];
        while (cursor != NULL)
        {
            // создать временный узел
            node* temp = cursor;
            cursor = cursor -> next;
            // освободить текущий узел
            free(temp);
        }
    }
    return true;
}

// Loosely based on http://bit.ly/2GAHJn1
unsigned long djb2(char *str)
{
    unsigned long hash = 5381;
    int c;
    while ((c = *str++))
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    return hash;
}
