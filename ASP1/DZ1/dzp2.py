class ListNode:
    def __init__(self, info=None):
        self.info = info
        self.next = None


class ListHeader:
    def __init__(self):
        self.head = None
        self.tail = None
        self.numElem = None


glava = ListHeader()


def stek_prazan():
    return glava is None


def push(info):
    global glava

    novi = ListNode()
    novi.info = info

    if glava.head is None:
        glava.head = glava.tail = novi
        glava.numElem = 1
    else:
        novi.next = glava.head
        glava.head = novi

    glava.numElem += 1
    return


def pop():
    global glava

    glava.numElem -= 1

    if stek_prazan():
        return None

    sledeci = glava.head
    glava.head = glava.head.next

    return sledeci.info


def ispisi_listu():
    global glava

    p = glava.head

    while p:
        print(str(p.info))
        p = p.next

    return


izraz, mapa = None, None

uputstvo = "1. Unos i provera izraza\n" \
           "2. Unos operanada\n" \
           "3. Izračunavanje izraza\n" \
           "4. Izlaz\n" \
           "5. Testiraj listu\n"


def ispisi_repl():
    print("izbor> ", end="")
    return


def prikazi_uputstvo():
    print(uputstvo)
    return


def unos_i_provera_izraza():
    global izraz, mapa

    mapa = dict()

    izraz = input("Izraz: ")

    brojac = 0
    neuspelo = False

    for i in izraz:
        if i.isalpha():
            brojac += 1

            # Podrazumevana vrednost
            mapa[i] = 0
        elif i == '+' or i == '-' or i == '*' or i == '/':
            brojac -= 2

            if brojac < 0:
                neuspelo = True
                break

            brojac += 1

    if brojac != 1 or neuspelo:
        print("Ulaz nije validan")
        izraz = None

    return


def unos_operanada():
    global mapa

    for slovo in mapa:
        mapa[slovo] = float(input(str(slovo) + ": "))

    return


def izracunavanje_izraza():
    for i in izraz:
        if i.isalpha():
            push(mapa[i])
        else:
            v1, v2 = pop(), pop()

            if i == '+':
                push(v2 + v1)
            if i == '-':
                push(v2 - v1)
            if i == '*':
                push(v2 * v1)
            if i == '/':
                if v1 != 0:
                    push(v2 / v1)
                else:
                    print(v1 + " je 0 pri deljenju!")
                    break

    print("Rezultat: " + str(pop()))


def testiraj_listu():
    print("Ubacujem 5, 4, 3...")

    push(5)
    push(4)
    push(3)

    ispisi_listu()

    print("Pop-ujem tri puta...")

    for i in range(0, 3):
        print(pop())

    return


prikazi_uputstvo()

menjac = {
    0: prikazi_uputstvo,
    1: unos_i_provera_izraza,
    2: unos_operanada,
    3: izracunavanje_izraza,
    5: testiraj_listu
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
while ulaz != 4:
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
