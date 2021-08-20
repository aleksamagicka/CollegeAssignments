#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct Ucenik {
    char *indeks, *ime;
    int bodovi;
} Ucenik;

typedef struct Cvor {
    struct Cvor *prethodni, *sledeci;
    Ucenik *sadrzaj;
} Cvor;

Ucenik *ucitajUcenika() {
    Ucenik *ucenik = malloc(sizeof(Ucenik));
    if (ucenik == NULL)
        return NULL; // mem_greska?

    size_t bufsize = 100;

    char *linija = malloc(bufsize * sizeof(char));
    if (linija == NULL)
        return NULL;

    getline(&linija, &bufsize, stdin);

    if (strlen(linija) == 1)
        return NULL;

    ucenik->indeks = strtok(linija, ",");
    ucenik->ime = strtok(NULL, ",");
    ucenik->bodovi = atoi(strtok(NULL, ","));

    return ucenik;
}

Cvor *ucitajUcenike() {
    Cvor *cvor = malloc(sizeof(Cvor)), *prosli = NULL;
    if (cvor == NULL)
        return NULL;

    Ucenik *ucenik = ucitajUcenika();
    //printf("uneseno: %s,%s, %d\n", ucenik->indeks, ucenik->ime, ucenik->bodovi);
    while (ucenik != NULL) {
        cvor->sadrzaj = ucenik;

        cvor->prethodni = malloc(sizeof(Cvor));
        cvor->sledeci = malloc(sizeof(Cvor));
        if (cvor->prethodni == NULL || cvor->sledeci == NULL)
            return NULL;

        cvor->sledeci = prosli;
        prosli = cvor;

        ucenik = ucitajUcenika();
        if (ucenik != NULL)
            cvor = cvor->prethodni;
    }

    return cvor;
}

int redniBrojZadatka(Ucenik *ucenik, int ukupnoZadataka) {
    char *token = strtok(ucenik->indeks, "/");
    int brojIndeksa = atoi(token);

    token = strtok(ucenik->indeks, "/");

    char dveCifre[2] = {token[2], token[3]};

    int skracenaGodina = atoi(dveCifre);

    return (brojIndeksa + skracenaGodina) % ukupnoZadataka;
}

Cvor *spisakDomacih(Cvor *lista, int brojDomaceg, int ukupnoZadataka) {
    Cvor *t = lista;

    Cvor *novaLista = malloc(sizeof(Cvor));
    if (novaLista == NULL)
        return NULL;

    while (t != NULL) {
        if (redniBrojZadatka(t->sadrzaj, ukupnoZadataka) == brojDomaceg) {
            novaLista->sadrzaj = t->sadrzaj;
            novaLista->sledeci = malloc(sizeof(Cvor));
            if (novaLista->sledeci == NULL)
                return NULL;
        }

        t = t->sledeci;
    }

    return novaLista;
}

void ispisiDomace(Cvor *lista, int ukupnoZadataka, bool prefiks) {
    Cvor *t = lista;
    while (t != NULL) {
        if (!prefiks)
            printf("%s,%s, %d\n", t->sadrzaj->indeks, t->sadrzaj->ime, t->sadrzaj->bodovi);
        else {
            int redniBroj = redniBrojZadatka(t->sadrzaj, ukupnoZadataka);

            printf("%d, %s,%s, %d\n", redniBroj, t->sadrzaj->indeks, t->sadrzaj->ime, t->sadrzaj->bodovi);
        }

        t = t->sledeci;
    }
}

void ispisSvega(Cvor *lista, int ukupnoZadataka) {
    for (int i = 0; i < ukupnoZadataka; ++i) {
        Cvor *nL = spisakDomacih(lista, i, ukupnoZadataka);
        ispisiDomace(nL, ukupnoZadataka, true);
    }
}

void oslobodiMemoriju() {

}

int main(void) {
    Cvor *ucenici = ucitajUcenike();
    int ukupnoZadataka;
    scanf("%d", &ukupnoZadataka);

    ispisiDomace(ucenici, ukupnoZadataka, false);

    return 0;
}