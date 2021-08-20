# 2. Приказује рад са строго горње троугаоном матрицом линеаризованом по колонама

from os import system
import gc

podrazumevana_vrednost = 0
debug = False

# N - dimenzija
niz, N = None, None


def ispisi_repl():
    print("izbor> ", end="")
    return


def ocisti_konzolu():
    _ = system('cls')
    return


def izracunaj_pomeraj(i, j):
    # Pocetni A11 je 0
    broj = int((j-1) * j / 2 + i)

    if debug:
        print("Pomeraj: " + str(broj))
        print("i, j: " + str(i) + ", " + str(j))
        print()

    return broj


def inicijalizacija_matrice():
    global N, niz, prvi_put

    N = int(input("N: "))

    niz = [None] * int(N*(N-1)/2)

    prikazi_uputstvo()

    prvi_put = False

    return


def postavljanje_podrazumevane_vrednosti():
    global podrazumevana_vrednost

    podrazumevana_vrednost = float(input("Podrazumevana vrednost: "))
    return


def dohvatanje_elementa():
    i = int(input("Red: "))
    j = int(input("Kolona: "))

    if i > N or j > N or i < 1 or j < 1:
        print("Ne postoji takav element")
    else:
        pomeraj = izracunaj_pomeraj(i-1, j-1)
        element = niz[pomeraj]

        if element is None:
            element = podrazumevana_vrednost

        print("Element je: " + str(element))

    return


def postavljanje_vrednosti_elementa():
    i = int(input("Red: "))
    j = int(input("Kolona: "))
    vrednost = float(input("Vrednost: "))

    if i > N or j > N or i < 1 or j < 1:
        print("Izvan dimenzija matrice je")
    else:
        niz[izracunaj_pomeraj(i-1, j-1)] = vrednost

    return


def broj_podrazumevanih(ispis):
    broj = N*(N+1)/2

    if ispis:
        print("Podrazumevanih: " + str(int(broj)))
    return broj


def broj_nepodrazumevanih(ispis=True):
    broj = len(niz)

    if ispis:
        print("Nepodrazumevanih: " + str(int(broj)))
    return broj


def ispis_matrice():
    for i in range(0, N):
        red = ""
        for j in range(0, N):
            if j > i:
                red += str(niz[izracunaj_pomeraj(i, j)]) + " "
            else:
                red += str(podrazumevana_vrednost) + " "

        print(red)

    if debug:
        print(niz)
    return


def procenat_ustede():
    broj = broj_nepodrazumevanih(False)/(N*N) * 100
    print("Procenat uštede: " + str(broj))
    return


def brisanje_matrice():
    global niz, N, podrazumevana_vrednost

    niz = M = N = podrazumevana_vrednost = None

    gc.collect()

    print("Obrisana")


uputstvo = "1. Inicijalizacija retke trougaone matrice\n"
uputstvo2 = "2. Podrazumevana vrednost\n" \
           "3. Dohvatanje elementa\n" \
           "4. Postavljanje vrednosti elementa\n" \
           "5. Broj nepodrazumevanih elemenata\n" \
           "6. Ispis matrice\n" \
           "7. Procenat uštede\n" \
           "8. Brisanje matrice\n" \
           "9. Izlaz\n"


def prikazi_uputstvo():
    if N is None:
        print(uputstvo)
    else:
        ocisti_konzolu()
        print(uputstvo + uputstvo2)
    return


prikazi_uputstvo()

menjac = {
    0: prikazi_uputstvo,
    1: inicijalizacija_matrice,
    2: postavljanje_podrazumevane_vrednosti,
    3: dohvatanje_elementa,
    4: postavljanje_vrednosti_elementa,
    5: broj_nepodrazumevanih,
    6: ispis_matrice,
    7: procenat_ustede,
    8: brisanje_matrice,
}


def pokreni_stavku(broj):
    funkcija = menjac.get(broj, None)
    if funkcija is None:
        print("Ta stavka ne postoji")
        return

    funkcija()

    return


ispisi_repl()

ulaz = None
while ulaz != 9:
    ulaz = input().strip()
    if ulaz == "":
        ulaz = None
        ispisi_repl()
        continue

    try:
        ulaz = int(ulaz)
        pokreni_stavku(ulaz)
    except:
        print("Los unos")
        continue

    ispisi_repl()

exit(0)
