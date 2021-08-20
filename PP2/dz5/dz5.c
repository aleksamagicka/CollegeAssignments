#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <stdarg.h>

typedef struct Kontakt {
    char *kolone[40];
} Kontakt;

typedef struct Cvor {
    struct Cvor *sledeci, *prosli;
    Kontakt *kontakt;
} Cvor;


Kontakt *ucitajKontakt(FILE *ulaz) {
    if (ulaz == NULL) {
        printf("DAT_GRESKA");
        exit(1);
    }

    char *line_buf = NULL;
    size_t line_buf_size = 0;

    if (getline(&line_buf, &line_buf_size, ulaz) < 0)
    {
      free(line_buf);
      return NULL;
    }

    Kontakt *kontakt = malloc(sizeof(Kontakt));

    int i = 0;

    char *p = line_buf;
    while (1) {
        char *p2 = strchr(p, '\t');
        if (p2 != NULL)
            *p2 = '\0';

        kontakt->kolone[i] = malloc(strlen(p) * sizeof(char) + 1);
        strcpy(kontakt->kolone[i], p);

        if (p2 == NULL)
            break;
        p = p2 + 1;

        i++;
    }

    free(line_buf);

    return kontakt;
}

Cvor *ucitajSveKontakte(char* ulazniFajl) {
    FILE *ulaz = fopen(ulazniFajl, "r");
    if (ulaz == NULL)
        return NULL;

    Cvor *glava = malloc(sizeof(Cvor));
    if (glava == NULL)
        return NULL;

    char *line_buf = NULL;
    size_t line_buf_size = 0;

    // Guta heder sa kolonama
    if (getline(&line_buf, &line_buf_size, ulaz) < 0)
        return NULL;

    free(line_buf);

    Cvor *t = glava, *prethodni = NULL;

    while (1) {
        Kontakt *kontakt = ucitajKontakt(ulaz);
        if (kontakt == NULL)
            break;

        t->kontakt = kontakt;
        t->prosli = prethodni;

        t->sledeci = malloc(sizeof(Cvor));
        if (t->sledeci == NULL)
            return NULL;

        prethodni = t;
        t = t->sledeci;
    }

    free(prethodni->sledeci);
    prethodni->sledeci = NULL;

    fclose(ulaz);

    return glava;
}

// Laksi pristup koloni
char *k(Cvor *cvor, int i) {
    return cvor->kontakt->kolone[i];
}

void sortirajListuPoMejlAdresi(Cvor *lista) {
    for (Cvor *i = lista; i != NULL; i = i->sledeci) {
        for (Cvor *j = i->sledeci; j != NULL; j = j->sledeci) {
            if (strcmp(k(i, 4), k(j, 4)) >= 0) {
                Kontakt *tmp = i->kontakt;
                i->kontakt = j->kontakt;
                j->kontakt = tmp;
            }
        }
    }
}

bool popunjen(Kontakt *k, int count, ...) {
    va_list list;
    bool jedanPopunjen = false;

    va_start(list, count);
    for (int j = 0; j < count; j++) {
        char *polje = k->kolone[va_arg(list, int)];
        if (polje == NULL)
          continue;
        if (strcmp(polje, "") != 0) {
            jedanPopunjen = true;
            break;
        }
    }

    va_end(list);

    return jedanPopunjen;
}

void ispisiDatoteku(char *izlazniFajl, Cvor *lista) {
    FILE *izlaz = fopen(izlazniFajl, "w");
    if (izlaz == NULL) {
        printf("DAT_GRESKA");
        exit(1);
    }

    Cvor *t = lista;
    while (t != NULL) {
        /*
  "First Name","Last Name","Display Name","Nickname","Primary Email","Secondary Email","Screen Name","Work Phone"7,"Home Phone","Fax Number","Pager Number","Mobile Number","Home Address","Home Address 2","Home City","Home State","Home ZipCode","Home Country","Work Address"18,"Work Address 2","Work City","Work State","Work ZipCode"22,"Work Country","Job Title"24,"Department","Organization","Web Page 1","Web Page 2","Birth Year","Birth Month","Birth Day","Custom 1","Custom 2","Custom 3","Custom 4","Notes"
  */

        fprintf(izlaz, "begin:vcard\n");
        if (popunjen(t->kontakt, 2, 0, 1))
            fprintf(izlaz, "fn:%s %s\n", k(t, 0), k(t, 1));
        if (popunjen(t->kontakt, 2, 1, 0))
            fprintf(izlaz, "n:%s;%s\n", k(t, 1), k(t, 0));


        if (popunjen(t->kontakt, 1, 26))
        {
          fprintf(izlaz, "org:%s", k(t, 26));
          if (popunjen(t->kontakt, 1, 25))
          {
            fprintf(izlaz, ";%s", k(t, 25));
          }

          fprintf(izlaz, "\n");
        }

        if (popunjen(t->kontakt, 4, 18, 20, 21, 22))
        {
          fprintf(izlaz, "adr:;;%s;%s;%s;%s", k(t, 18), k(t, 20), k(t, 21), k(t, 22));

          if (popunjen(t->kontakt, 1, 23))
          fprintf(izlaz, ";%s", k(t, 23));
          fprintf(izlaz, "\n");
        }

        if (popunjen(t->kontakt, 1, 4))
            fprintf(izlaz, "email;internet:%s\n", k(t, 4));
        if (popunjen(t->kontakt, 1, 24))
            fprintf(izlaz, "title:%s\n", k(t, 24));

        if (popunjen(t->kontakt, 1, 7))
            fprintf(izlaz, "tel;work:%s\n", k(t, 7));
        if (popunjen(t->kontakt, 1, 9))
            fprintf(izlaz, "tel;fax:%s\n", k(t, 9));
        if (popunjen(t->kontakt, 1, 10))
            fprintf(izlaz, "tel;pager:%s\n", k(t, 10));
        if (popunjen(t->kontakt, 1, 8))
            fprintf(izlaz, "tel;home:%s\n", k(t, 8));
        if (popunjen(t->kontakt, 1, 11))
            fprintf(izlaz, "tel;cell:%s\n", k(t, 11));

        if (popunjen(t->kontakt, 1, 36))
            fprintf(izlaz, "note:%s\n", k(t, 36));

        if (popunjen(t->kontakt, 1, 27))
            fprintf(izlaz, "url:%s\n", k(t, 27));

        fprintf(izlaz, "version:2.1\n");
        fprintf(izlaz, "end:vcard\n");

        if (t->sledeci != NULL)
            fprintf(izlaz, "\n");

        t = t->sledeci;
    }

    fclose(izlaz);
}

void oslobodiListu(Cvor *kontakti)
{
  Cvor *t = kontakti;
  while (t != NULL)
  {
    //free(t->kontakt->kolone);
    for (int i =0; i<40; i++)
      free(t->kontakt->kolone[i]);
    free(t->kontakt);
    
    Cvor *t1 = t->sledeci;
    free(t);
    t = t1;
  }
}

int main(int argc, char* argv[]) {
    if (argc <= 2 || argc > 4) {
        printf("ARG_GRESKA");
        exit(0);
    }

    char *ulazniFajl = argv[1], *izlazniFajl = argv[2];
    bool sortiraj = false;

    if (argv[3] != NULL && strcmp(argv[3], "-sort") >= 0)
        sortiraj = true;

    Cvor *kontakti = ucitajSveKontakte(ulazniFajl);
    Cvor *t = kontakti;

    if (sortiraj)
        sortirajListuPoMejlAdresi(kontakti);

    ispisiDatoteku(izlazniFajl, kontakti);

    oslobodiListu(kontakti);

    return 0;
}
