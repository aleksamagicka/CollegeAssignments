! inicijalizacija simulacije
dc x.1, x.9996
dc x.0, x.9998
onkp false, x.1, x.1
onkp false, x.1, x.1
onkp true, x.1, x.1
ondma x.1, x.1
ondma x.1, x.1
ondma x.1, x.1
ondma x.1, x.1
kpreg 1.1, r0, x.1
kpreg 1.1, r1, x.2
kpreg 1.1, r2, x.3
kpreg 1.1, r3, x.4
kpreg 1.1, r4, x.5
kpreg 1.1, r5, x.6
kpreg 1.1, r6, x.7
kpreg 1.1, r7, x.8
kpreg 2.1, r0, x.9
kpreg 2.1, r1, x.a
kpreg 2.1, r2, x.b
kpreg 2.1, r3, x.c
kpreg 2.1, r4, x.d
kpreg 2.1, r5, x.e
kpreg 2.1, r6, x.f
kpreg 2.1, r7, x.10
reg pc, x.4000
reg ivtp, x.4000
reg sp, x.9000
! kraj inicijalizacije

org x.4000

! ----------------- INICIJALIZACIJA IVTP TABELE -----------------

! ivtp = 0100h
ldimm x.0100, r0
mvrir r0, ivtp 

! ivtp[0] = 3000h
ldimm x.3000, r0
stmem x.0100, r0

! ivtp[1] = 2500h
ldimm x.2500, r0
stmem x.0101, r0

! ivtp[2] = 1500h
ldimm x.1500, r0
stmem x.0102, r0

! ivtp[3] = 2000h
ldimm x.2000, r0
stmem x.0103, r0

! ivtp[4] = 1000h
ldimm x.1000, r0
stmem x.0104, r0

! ivtp[5] = 0500h
ldimm x.0500, r0
stmem x.0105, r0

! ----------------- Pokretanje KP1.1 - prekidi -----------------

ldimm x.5000, r4 ! Smestace pocev od 5000h
ldimm x.9, r5 ! r5 broji koliko je ostalo

ldimm x.0105, r2
stmem x.f102, r2 ! Unos u entry registar

ldimm x.f, r2 ! 1111 za aktivaciju

clr ra ! praznjenje semafora

stmem x.f100, r2 ! aktiviranje KP1.1

! Pokretanje KP2.1 - bit spremnosti

ldimm x.6000, r0 ! Smestace pocev od 6000h
ldimm x.9, r1 ! r1 broji koliko je ostalo
ldimm x.5, r2 ! 101 za aktivaciju
stmem x.f200, r2 ! Aktiviranje KP2.1

! Ispitivanje bita spremnosti KP2.1

loop: ldimm x.1, r2
      ldmem x.f201, r3
      and r3, r3, r2
      beql loop

      !! Bit spremnosti je sad postavljen
      ldmem x.f203, r2
      stri [r0], r2
      inc r0
      dec r1
      bneq loop

! Ovde je zavrsio sa KP2.1
clr r0
stmem x.f200, r0 ! Iskljucuje se

! Cekamo da primimo niz B
ldimm x.1, r2
wait: and ra, ra, r2
      beql wait

! Postavljanje parametara za xorArr(int* a, int* b, int n)
ldimm x.8, r2
push r2
ldimm x.6000, r2
push r2
ldimm x.5000, r2
push r2

jsr xorArr

pop r2
pop r2
pop r2
clr r2


! Deo V - treci deo
 ! Slanje niza A u DMA1.1 paketski

ldimm x.8, r0 ! koliko treba preneti
stmem x.f004, r0 !  upis u count registar DMA1.1

ldimm x.5000, r0 ! odakle se uzima (gde je izvor)
stmem x.f005, r0 ! upis u izvorisni registar

clr rc ! semafor za DMA1.1
stmem x.7000, rc

ldimm x.0103, r0
stmem x.f002, r0 ! upis lokacije prekidne rutine u entry

ldimm x.8e, r0 ! 1000 1110 - control bitovi za DMA1.1
stmem x.f000, r0 ! upis control bitova i aktivacija DMA1.1

! provera da li je DMA1.1 gotov
ldimm x.1, r0
dma11Loop: ldmem x.7000, rc
           cmp rc, r0
           bneq dma11Loop


 ! Slanje memorijske lokacija 9999h u DMA1.2 ciklus po ciklus

ldimm x.1, r0 ! koliko treba preneti
stmem x.f044, r0 !  upis u count registar DMA1.2

ldimm x.9999, r0 ! odakle se uzima (gde je izvor)
stmem x.f045, r0 ! upis u izvorisni registar

clr rd ! semafor za DMA1.1
stmem x.7008, rd

ldimm x.0101, r0
stmem x.f042, r0 ! upis lokacije prekidne rutine u entry

ldimm x.0e, r0 ! 0000 1110 - control bitovi za DMA1.2
stmem x.f040, r0 ! upis control bitova i aktivacija DMA1.2

! provera da li je DMA1.2 gotov
ldimm x.1, r0
dma12Loop: ldmem x.7008, rd
           cmp rd, r0
           bneq dma12Loop

halt


! ----------------- XOR_ARR RUTINA -----------------
xorArr:

push rf ! rf je bazni registar gde ce biti SP
mvrpl rf, sp ! rf = SP sada

! Stek pocev od rf nagore izgleda ovako:
! rf, retPC, A, B, n

! Sad se svi ovi pushuju jer se koriste
push r0
push r1
push r2
push r3
push r4
push r5
push r6
push r7
push ra
push rb

ldrid [rf]x.2, r0
ldrid [rf]x.3, r1
ldrid [rf]x.4, r3

mvrrl r2, r0

loop2:

ldrid [r0]x.0, r5
ldrid [r1]x.0, r6
xor r7, r5, r6
stri [r2], r7
inc r0
inc r1
inc r2
dec r3
bneq loop2

ldimm x.9999, r2
ldmem x.5000, r3 ! Ucitava se prvi element niza A
stri [r2], r3 ! Smesta se na adresu 9999h

! Kopiranje A[0] 8h puta pocev od 5100h na DMA1.4 paketski

ldimm x.8, r0 ! koliko treba preneti
stmem x.f0c4, r0 !  upis u count registar DMA1.4

ldimm x.0100, r0
stmem x.f0c2, r0

ldimm x.5000, r0 ! odakle se uzima (gde je izvor)
stmem x.f0c5, r0 ! upis u izvorisni registar

ldimm x.5100, r0 ! adresa gde se salje
stmem x.f0c6, r0 ! upis u odredisni registar

clr rb ! semafor za DMA1.4
ldimm x.9e, r0 ! 1001 1110 - control bitovi za DMA1.4
stmem x.f0c0, r0 ! upis control bitova i aktivacija DMA1.4

! provera da li je DMA1.4 gotov
ldimm x.1, r2
dma14Loop: and rb, rb, r2
           beql dma14Loop

! Kad dodjemo ovde, DMA1.4 je zavrsio
pop rb
pop ra
pop r7
pop r6
pop r5
pop r4
pop r3
pop r2
pop r1
pop r0

pop rf
rts

! ----------------- PREKIDNE RUTINE -----------------
 ! Prekidna rutina za KP1.1
org x.0500

dec r5
bneq prenos
stmem x.f100, r5
ldimm x.1, ra ! semafor
jmp back

prenos: ldmem x.f103, r6
        stri [r4], r6 ! mem[r4] = r6
        inc r4

back: rti

 ! Prekidna rutina za DMA1.4
org x.3000

push r8

ldimm x.1, rb ! aktiviranje semafora

clr r8
stmem x.f0c0, r8 ! gasenje DMA1.4

pop r8
rti



 ! Prekidna rutina za DMA1.1
org x.2000

push r8

ldimm x.1, rc ! aktiviranje semafora
stmem x.7000, rc

clr r8
stmem x.f000, r8 ! gasenje DMA1.1

pop r8
rti



 ! Prekidna rutina za DMA1.2
org x.2500

push r8

ldimm x.1, rd ! aktiviranje semafora
stmem x.7008, rd

clr r8
stmem x.f040, r8 ! gasenje DMA1.1

pop r8
rti
