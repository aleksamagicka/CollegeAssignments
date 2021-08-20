#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

char *readLine() {
    char *l = NULL;
    size_t duzina = 0;
    size_t status = getline(&l, &duzina, stdin);

    if (status != -1)
        return l;
    else
        return NULL;
}

char **readLines(int *n) {
    int i = 0, delic = 16, brojElemenata = delic;

    char **niz = NULL, **tmp = NULL;
    niz = malloc(brojElemenata * sizeof(char *));
    if (niz == NULL)
        return NULL;

    while (1) {
        char *linija = readLine();
        if (!linija)
            return NULL;

        if (linija[0] == '\n')
            break;

        linija[strlen(linija) - 1] = '\0';

        if (i >= brojElemenata) {
            brojElemenata += delic;
            tmp = realloc(niz, brojElemenata * sizeof(char *));
            if (!tmp) {
                free(niz);
                return NULL;
            }
            niz = tmp;
        }

        niz[i++] = linija;
    }

    tmp = realloc(niz, i * sizeof(char *));
    if (!tmp)
        return NULL;

    *n = i;

    return tmp;
}

bool areClose(char *string0, char *string1) {
    int duzina1 = strlen(string0), duzina2 = strlen(string1);
    if (duzina1 != duzina2)
        return false;

    int broj = 0, prvi = -1, drugi = -1;

    for (int i = 0; i < duzina1; i++) {
        if (string0[i] != string1[i]) {
            broj++;
            if (broj > 2)
                break;
            prvi = drugi;
            drugi = i;
        }
    }

    return broj == 2 && string0[prvi] == string1[drugi] && string0[drugi] == string1[prvi];
}

int main() {
    int n = -1;
    char **linije = readLines(&n);

    if (n == -1) {
        printf("GRESKA\n");
        return 0;
    }
    // Proveriti
    else if (linije == NULL) {
        printf("MEM_GRESKA\n");
        return 0;
    }

    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
             if (areClose(linije[i], linije[j]))
                printf("%s:%s\n", linije[i], linije[j]);

    for (int i = 0; i < n; i++)
        free(linije[i]);
    free(linije);
    return 0;
}
