import math
from collections import deque

'''
OPŠTE INFORMACIJE

- tg se moze diferencirati samo jednom
- za konstante koje nisu cifre, zameniti ih simbolom i posle mu dodeliti vrednost
'''


class CvorBinarnogStabla:
    def __init__(self, sadrzaj, levo=None, desno=None):
        if str(sadrzaj).isdecimal():
            self.sadrzaj = float(sadrzaj)
        else:
            self.sadrzaj = sadrzaj

        self.levo = levo
        self.desno = desno
        self.operator = sadrzaj in prioriteti_operatora
        self.unarni = unarni_operator(sadrzaj)


prioriteti_operatora = {'+': (2, 2), '-': (2, 2), '*': (3, 3), '/': (3, 3), '^': (5, 4), 'm': (7, 6),
                        '(': (100, 0), ')': (1, None),
                        '~': (10, 9), 'l': (12, 11), 't': (14, 13), 'c': (16, 15), 's': (18, 17)}

stablo = None
vrednosti_operanada = dict()
unesene_vrednosti = False
uneto_stablo = False


def zamena_funkcija(infix_izraz):
    izraz = infix_izraz.replace("(-)", "~").replace("(-", "~(")
    izraz = izraz.replace("ln", "l")
    izraz = izraz.replace("tg", "t")
    izraz = izraz.replace("min", "m")
    return izraz


def unarni_operator(karakter):
    return karakter == '~' or karakter == 'l' or karakter == 't' or karakter == 'c' or karakter == 's'


def ispisi_cvor(cvor):
    if cvor is not None and cvor.sadrzaj is not None:
        print(f"cvor: {cvor.sadrzaj}, ", end="")
        if cvor.levo is not None:
            print(f"levo: {cvor.levo.sadrzaj} ", end="")
        if cvor.desno is not None:
            print(f"desno: {cvor.desno.sadrzaj}", end="")
        print()


def unos_izraza():
    global stablo, vrednosti_operanada, uneto_stablo, unesene_vrednosti

    vrednosti_operanada = dict()

    infix_izraz = zamena_funkcija(input("Unesi izraz: "))

    postfix_izraz = list()

    stek = deque()

    i = 0
    while i < len(infix_izraz):
        karakter = infix_izraz[i]

        if karakter == ',' or karakter == ' ':
            i += 1
            continue

        if karakter not in prioriteti_operatora:
            postfix_izraz.append(karakter)

            if karakter.isdecimal():
                vrednosti_operanada[float(karakter)] = float(karakter)
            else:
                vrednosti_operanada[karakter] = karakter
        else:
            while len(stek) != 0 and prioriteti_operatora[karakter][0] <= prioriteti_operatora[stek[0]][1]:
                postfix_izraz.append(stek.popleft())
            if karakter != ')':
                stek.appendleft(karakter)
            else:
                stek.popleft()

        i += 1

    while len(stek) > 0:
        postfix_izraz.append(stek.popleft())

    spojeno = ''.join(postfix_izraz)

    # print(f"Postfiks izraz je: {spojeno}")

    stablo = napravi_stablo(spojeno)

    uneto_stablo = True
    unesene_vrednosti = False


# Pravi stablo od datog postfiksnog izraza
def napravi_stablo(postfiks):
    stek = deque()

    for karakter in postfiks:
        cvor = CvorBinarnogStabla(karakter)
        if karakter in prioriteti_operatora:
            # Operator
            cvor.levo = stek.popleft()
            cvor.levo.otac = cvor

            if not unarni_operator(karakter):
                cvor.desno = stek.popleft()
                cvor.desno.otac = cvor
            else:
                cvor.unarni = True

            cvor.operator = True

            stek.appendleft(cvor)
        else:
            # Operand
            stek.appendleft(cvor)

    return stek.popleft()


def odstampaj_stablo():
    if not uneto_stablo:
        print("Stablo još nije uneto!")
        return

    stek = deque()
    stek.appendleft((stablo, "", True))

    while len(stek) > 0:
        skinuto = stek.popleft()

        cvor = skinuto[0]
        prefix = skinuto[1]
        je_li_desni = skinuto[2]

        if cvor is not None:
            print(f"{prefix}{'~-' if je_li_desni else '|-'} {cvor.sadrzaj}", sep="")
            prefix += "   "

            broj_sinova = 0
            if cvor.levo is not None:
                broj_sinova += 1
            if cvor.desno is not None:
                broj_sinova += 1

            sinovi = [cvor.levo, cvor.desno]
            for i, sin in enumerate(sinovi):
                je_li_desni = i != (broj_sinova - 1)
                stek.appendleft((sin, prefix, je_li_desni))


def ispisi_prefiksni_obilazak():
    if not uneto_stablo:
        print("Stablo još nije uneto!")
        return

    print("Prefiksni obilazak je: ", end="")

    stek = deque()
    stek.appendleft(stablo)

    while len(stek) > 0:
        cvor = stek.popleft()
        print(cvor.sadrzaj, end='')

        if cvor.desno is not None:
            stek.appendleft(cvor.desno)

        if cvor.levo is not None:
            stek.appendleft(cvor.levo)

    print()


def unos_vrednosti_operanada():
    global vrednosti_operanada, unesene_vrednosti

    if not uneto_stablo:
        print("Stablo još nije uneto!")
        return

    try:
        for i in vrednosti_operanada:
            if i == 'e':
                vrednosti_operanada[i] = math.e
            if not type(i) is float:
                vrednosti_operanada[i] = float(input(f"Vrednost za {i}: "))
    except:
        print("Unesena je nekorektna vrednost, koja nije broj.")
        return

    unesene_vrednosti = True


def izracunaj_osnovne_funkcije(parametar, v1, v2):
    rezultat = 0
    v1 = float(v1)
    if v2 is not None:
        v2 = float(v2)

    if parametar == '+':
        rezultat = v1 + v2
    elif parametar == '-':
        rezultat = v1 - v2
    elif parametar == '*':
        rezultat = v1 * v2
    elif parametar == '/':
        if v2 != 0:
            rezultat = v1 / v2
        else:
            print(f"Operand je 0 pri deljenju!")
    elif parametar == '^':
        rezultat = math.pow(v1, v2)
    elif parametar == 'm':
        rezultat = min(v1, v2)
    elif parametar == 'l':
        if v1 <= 0:
            print("Prirodni logaritam ne prima vrednosti manje od 0!")
            return
        rezultat = math.log2(v1) / math.log2(math.e)
    elif parametar == 't':
        if math.cos(v1) != 0:
            rezultat = math.sin(v1) / math.cos(v1)
    elif parametar == 'c':
        rezultat = math.cos(v1)
    elif parametar == 's':
        rezultat = math.sin(v1)
    elif parametar == '~':
        rezultat = -v1

    return rezultat


def vrednost_stabla(pocetni_cvor):
    if pocetni_cvor is None:
        print("Stablo još nije uneto!")
        return

    if not unesene_vrednosti:
        print("Vrednosti operanada nisu unesene!")
        return

    stek = deque()
    stek_vrednosti = deque()

    t = pocetni_cvor

    while True:
        while t is not None:
            if t.desno is not None:
                stek.appendleft(t.desno)
            stek.appendleft(t)

            t = t.levo

        t = stek.popleft()

        if t.desno is not None and len(stek) > 0 and stek[0] == t.desno:
            stek.popleft()
            stek.appendleft(t)
            t = t.desno
        else:
            # Realan broj
            if type(t.sadrzaj) is float:
                stek_vrednosti.appendleft(t.sadrzaj)
            elif t.sadrzaj in vrednosti_operanada:
                # Operand
                stek_vrednosti.appendleft(vrednosti_operanada[t.sadrzaj])
            elif t.operator:
                # Operator
                if t.unarni:
                    stek_vrednosti.appendleft(
                        izracunaj_osnovne_funkcije(t.sadrzaj, stek_vrednosti.popleft(), None))
                else:
                    stek_vrednosti.appendleft(
                        izracunaj_osnovne_funkcije(t.sadrzaj, stek_vrednosti.popleft(), stek_vrednosti.popleft()))

            t = None

        if len(stek) == 0:
            break

    return float(stek_vrednosti.popleft())


def racunanje_vrednosti_izraza():
    if not uneto_stablo:
        print("Stablo još nije uneto!")
        return

    rezultat = vrednost_stabla(stablo)
    print(f"Rezultat izraza je: {rezultat}")


def napravi_list(cvor, sadrzaj):
    cvor.operator = False
    cvor.sadrzaj = sadrzaj
    cvor.levo = cvor.desno = None


def primeni_pravila_izvoda(cvor, levi_izvod, desni_izvod):
    novi_cvor = CvorBinarnogStabla(cvor.sadrzaj)
    novi_cvor.operator = True

    if cvor.sadrzaj == '+' or cvor.sadrzaj == '-':
        novi_cvor.levo = levi_izvod
        novi_cvor.desno = desni_izvod
    if cvor.sadrzaj == '~':
        novi_cvor = CvorBinarnogStabla('~', levi_izvod, desni_izvod)
    if cvor.sadrzaj == '*':
        levo = CvorBinarnogStabla('*', cvor.levo, desni_izvod)
        desno = CvorBinarnogStabla('*', cvor.desno, levi_izvod)

        novi_cvor = CvorBinarnogStabla('+', levo, desno)
    if cvor.sadrzaj == '/':
        prvi_deo = CvorBinarnogStabla('*', cvor.desno, levi_izvod)
        drugi_deo = CvorBinarnogStabla('*', cvor.levo, desni_izvod)

        brojilac = CvorBinarnogStabla('-', drugi_deo, prvi_deo)
        imenilac = CvorBinarnogStabla('^', cvor.desno, 2)

        razlomak = CvorBinarnogStabla('/', brojilac, imenilac)

        novi_cvor = razlomak
    if cvor.sadrzaj == '^':
        oduzimanje = CvorBinarnogStabla('-', CvorBinarnogStabla(1), cvor.levo)
        nizi_stepen = CvorBinarnogStabla('^', cvor.desno, oduzimanje)
        koeficijent = CvorBinarnogStabla('*', cvor.levo, desni_izvod)

        novi_cvor = CvorBinarnogStabla('*', koeficijent, nizi_stepen)
    if cvor.sadrzaj == 'l':
        razlomak = CvorBinarnogStabla('/', cvor.levo, CvorBinarnogStabla(1))

        novi_cvor = CvorBinarnogStabla('*', razlomak, levi_izvod)
    if cvor.sadrzaj == 't':
        imenilac = CvorBinarnogStabla('^', CvorBinarnogStabla(2), CvorBinarnogStabla('c', cvor.levo))
        razlomak = CvorBinarnogStabla('/', imenilac, CvorBinarnogStabla(1))

        novi_cvor = CvorBinarnogStabla('*', razlomak, levi_izvod)
    if cvor.sadrzaj == 'c':
        sin_cvor = CvorBinarnogStabla('s', cvor.levo, None)
        minus_sin_cvor = CvorBinarnogStabla('~', sin_cvor, None)

        novi_cvor = CvorBinarnogStabla('*', minus_sin_cvor, levi_izvod)
    if cvor.sadrzaj == 's':
        cos_cvor = CvorBinarnogStabla('c', cvor.levo, None)

        novi_cvor = CvorBinarnogStabla('*', cos_cvor, levi_izvod)
    if cvor.sadrzaj == 'm':
        novi_cvor = CvorBinarnogStabla('m', levi_izvod, desni_izvod)
    return novi_cvor


# Na sve izvode se uvek primenjuje složena funkcija
# U prostijim slučajevima, ona će biti jednaka jedinici

def izracunaj_izvod(cvor, promenljiva):
    if not uneto_stablo:
        print("Stablo još nije uneto!")
        return

    novi_cvor = None
    if cvor is not None:
        if not cvor.operator:
            if str(cvor.sadrzaj) == promenljiva:
                novi_cvor = CvorBinarnogStabla(1)
            else:
                novi_cvor = CvorBinarnogStabla(0)
        else:
            levi_izvod = izracunaj_izvod(cvor.levo, promenljiva)
            desni_izvod = izracunaj_izvod(cvor.desno, promenljiva)

            novi_cvor = primeni_pravila_izvoda(cvor, levi_izvod, desni_izvod)

    return novi_cvor


def racunanje_izvoda():
    if not uneto_stablo:
        print("Stablo još nije uneto!")
        return

    global stablo
    promenljiva = input("Promenljiva: ")

    stablo = izracunaj_izvod(stablo, promenljiva)


# REPL
uputstvo = "1. Unos infiksnog izraza\n" \
           "2. Odštampaj stablo\n" \
           "3. Prefiksni obilazak\n" \
           "4. Unos vrednosti operanada\n" \
           "5. Izračunavanje vrednosti izraza\n" \
           "6. Izračunavanje izvoda\n" \
           "9. Izlaz\n"


def ispisi_repl():
    print("izbor> ", end="")
    return


def prikazi_uputstvo():
    print(uputstvo)
    return


prikazi_uputstvo()

menjac = {
    0: prikazi_uputstvo,
    1: unos_izraza,
    2: odstampaj_stablo,
    3: ispisi_prefiksni_obilazak,
    4: unos_vrednosti_operanada,
    5: racunanje_vrednosti_izraza,
    6: racunanje_izvoda
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
        print("Loš ulaz!")
        continue

    ispisi_repl()

exit(0)
