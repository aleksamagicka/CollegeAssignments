#include <stdio.h>
#include <stdlib.h>

typedef struct cvor {
    int pocetniIndeks, duzina;
    struct cvor *sledeci;
} cvor_t;

cvor_t *glava = NULL;
cvor_t *trenutni = NULL;

void dodajNaSpisak(int pocetak, int duzina) {
    cvor_t *novi = (cvor_t *) malloc(sizeof(cvor_t));
    novi->pocetniIndeks = pocetak;
    novi->duzina = duzina;
    novi->sledeci = NULL;

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

int main() {
    // Alokacija spiska neopadajucih sekvenci i njihovih duzina
    glava = (cvor_t *) malloc(sizeof(cvor_t));
    if (glava == NULL) {
        return 1;
    }

    trenutni = glava;

    // Unos brojeva
    int n;
    scanf("%d\n", &n);

    if (n < 0)
        return 1;

    int *niz = (int *) malloc(n * sizeof(int));
    for (int i = 0; i < n; ++i) {
        scanf("%d", &niz[i]);
    }

    // Ispis brojeva
    for (int i = 0; i < n; printf("%d ", niz[i++]));

    printf("\n");

    int trenutniPocetak = 0, duzina = 0, ukupnaDuzina = 0;

    // Trazenje rastucih podnizova
    for (int i = 0; i < n; ++i) {
        if (i == n - 1) {
            if (niz[i - 1] <= niz[i]) {
                dodajNaSpisak(trenutniPocetak, duzina + 1);
                ukupnaDuzina += duzina + 1;
            }

            break;
        }

        if (niz[i] > niz[i + 1]) {
            // Ne moze, prekida se
            if (duzina != 0) {
                dodajNaSpisak(trenutniPocetak, duzina + 1);
                ukupnaDuzina += duzina + 1;
            }

            duzina = 0;
            trenutniPocetak = -1;
        } else {
            // Dobro je
            if (trenutniPocetak == -1)
                trenutniPocetak = i;

            duzina++;
        }
    }

    int *nizIzdvojenih = (int *) malloc(ukupnaDuzina * sizeof(int));
    int i = 0;

    // Ispis takvih podnizova i dodavanje u drugi niz
    cvor_t *p = glava->sledeci;
    while (p != NULL) {
        printf("%d %d \n", p->pocetniIndeks, p->duzina);

        for (int j = p->pocetniIndeks; j < p->pocetniIndeks + p->duzina; ++j) {
            nizIzdvojenih[i++] = niz[j];
        }

        p = p->sledeci;
    }

    if (ukupnaDuzina == 0)
        printf("NIZ JE PRAZAN");
    else
        for (int i = 0; i < ukupnaDuzina; ++i)
            printf("%d ", nizIzdvojenih[i]);

    free(niz);
    free(nizIzdvojenih);
    freeListu(glava);

    getchar();
    return 0;
}
