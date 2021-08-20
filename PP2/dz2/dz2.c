#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct cvor {
    int brojReda;
    struct cvor *sledeci;
    struct cvor *prosli;

    bool zaglavlje;
} cvor_t;

cvor_t *glava = NULL;
cvor_t *trenutni = NULL;

void dodajNaSpisak(int brojReda) {
    cvor_t *novi = (cvor_t *) malloc(sizeof(cvor_t));
    novi->brojReda = brojReda;

    novi->prosli = trenutni;
    novi->sledeci = NULL;
    novi->zaglavlje = false;

    trenutni->sledeci = novi;
    trenutni = novi;
}

void freeListu(cvor_t *glava) {
    cvor_t *tmp;

    while (glava != NULL) {
        tmp = glava;
        glava = glava->sledeci;
        free(tmp);
    }
}

void ispisiNizZaMoodle(int *niz, int n) {
    for (int i = 0; i < n; i++) {
        if (i == n - 1)
            printf("%d", niz[i]);
        else
            printf("%d ", niz[i]);
    }
}

int main() {
    // Alokacija spiska indeksa neopadajucih redova
    glava = (cvor_t *) malloc(sizeof(cvor_t));
    if (glava == NULL) {
        return 0;
    }

    glava->zaglavlje = true;

    trenutni = glava;

    int m, n; // vrsta, kolona
    scanf("%d %d\n", &m, &n);

    if (m <= 0 || n <= 0) {
        return 0;
    }

    int **matrica = (int **) malloc(m * sizeof(int *));

    // U ekstremnom slucaju su iste
    int **matrica2 = (int **) malloc(m * sizeof(int *));
    if (matrica == NULL || matrica2 == NULL) {
        return 0;
    }

    for (int i = 0; i < m; i++) {
        matrica[i] = (int *) malloc(n * sizeof(int));
        if (matrica[i] == NULL) {
            return 0;
        }
    }

    bool rastuciRed = true;
    int brojac = 0;

    for (int i = 0; i < m; i++) {
        rastuciRed = true;

        for (int j = 0; j < n; j++) {
            scanf("%d", &matrica[i][j]);
            if (j > 0 && rastuciRed && matrica[i][j] <= matrica[i][j - 1])
                rastuciRed = false;
        }

        if (rastuciRed) {
            matrica2[brojac] = (int *) malloc(n * sizeof(int));
            if (matrica2[brojac] == NULL)
                return 0;

            for (int j = 0; j < n; j++) {
                matrica2[brojac][j] = matrica[i][j];
            }

            brojac++;
            dodajNaSpisak(i);
        }
    }

    for (int i = 0; i < m; i++) {
        ispisiNizZaMoodle(matrica[i], n);
        printf("\n");
    }

    cvor_t *t = glava->sledeci;
    cvor_t *t2 = NULL;

    while (t != NULL) {
        printf("%d\n", t->brojReda);

        if (t->sledeci == NULL)
            t2 = t;

        t = t->sledeci;
    }

    for (int i = brojac - 1; i >= 0; i--) {
        ispisiNizZaMoodle(matrica2[i], n);
        printf("\n"); // if (i != m-1)
    }

    freeListu(glava);
    for (int i = 0; i < m; i++)
        free(matrica[i]);
    for (int i = 0; i < brojac; i++)
        free(matrica2[i]);
    free(matrica);
    free(matrica2);

    return 0;
}