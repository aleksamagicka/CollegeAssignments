import base64
import datetime
import math
import os
import pickle
import sys
import time

import rsa
from Crypto.Cipher import DES3, CAST
from zlib_ng import zlib_ng

from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QFileDialog,
    QInputDialog,
)
from PyQt5.uic import loadUi

from generisi_kljuc_dialog import Ui_GenerisiKljucDialog
from main_window import Ui_MainWindow
from prsten_kljuceva import PrstenKljuceva, Kljuc, TeloPoruke, Poruka
from uvezi_kljuc import Ui_UveziKljucDialog

HEDERI_TABELA = ["Ime", "Mejl", "Algoritam", "Velicina", "Svrha", "Vezan sa"]


def upozori_greska(poruka):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(poruka)
    msg.setWindowTitle("Greska!")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_()

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

        self.prsten_kljuceva = None
        if os.path.exists("prsten_kljuceva.pickle"):
            with open("prsten_kljuceva.pickle", "rb") as infile:
                self.prsten_kljuceva = pickle.load(infile)
        else:
            self.prsten_kljuceva = PrstenKljuceva()

        self.azuriraj_tabele()

    def connectSignalsSlots(self):
        self.btnGenerisi.clicked.connect(self.generisi_kljuc)
        self.btnUveziJavni.clicked.connect(self.uvezi_javni)
        self.btnUveziPrivatni.clicked.connect(self.uvezi_privatni)
        self.btnIzveziJavni.clicked.connect(self.izvezi_javni)
        self.btnIzveziPrivatni.clicked.connect(self.izvezi_privatni)
        self.btnObrisiJavni.clicked.connect(self.obrisi_javni)
        self.btnObrisiPrivatni.clicked.connect(self.obrisi_privatni)
        self.btnUradi.clicked.connect(self.odradi_sifrovanje)
        self.btnVerifikuj.clicked.connect(self.odradi_desifrovanje)
        self.btnOdaberiFajl.clicked.connect(self.uvezi_fajl)
        self.btnSnimiRezultat.clicked.connect(self.snimi_rezultat)

    def snimi_rezultat(self):
        putanja = self.save_file_dialog()[0]
        if putanja != "":
            with open(putanja, "w") as izvozf:
                izvozf.write(self.tbDesifrovanaPoruka.toPlainText())

    def closeEvent(self, event):
        with open("prsten_kljuceva.pickle", "wb") as outfile:
            pickle.dump(self.prsten_kljuceva, outfile)

    def generisi_simetricni_kljuc(self, algoritam):
        if algoritam == "3DES":
            return os.urandom(24)
        return os.urandom(16)

    def sifruj_simetricnim_kljucem(self, algoritam, kljuc, podaci):
        if isinstance(podaci, str):
            podaci = podaci.encode("utf-8")

        if algoritam == "3DES":
            des = DES3.new(kljuc, DES3.MODE_CFB)
            return des.iv + des.encrypt(podaci)
        else:
            # CAST-128
            return CAST.new(kljuc, CAST.MODE_OPENPGP).encrypt(podaci)

    def desifruj_simetricnim_kljucem(self, algoritam, kljuc, podaci):
        if algoritam == "3DES":
            iv = podaci[:DES3.block_size]
            sifrovani_podaci = podaci[DES3.block_size:]
            tdes = DES3.new(kljuc, DES3.MODE_CFB, iv)
            desifrovano = tdes.decrypt(sifrovani_podaci)
            return desifrovano
        else:
            # CAST-128
            if isinstance(podaci, str):
                podaci = podaci.encode("utf-8")
            eiv = podaci[:CAST.block_size + 2]
            podaci = podaci[CAST.block_size + 2:]
            plaintext = CAST.new(kljuc, CAST.MODE_OPENPGP, eiv).decrypt(podaci)
            return plaintext

    def odradi_sifrovanje(self):
        plaintext = self.tbPoruka.toPlainText()
        privatni_kljuc_od: Kljuc = self.cbOd.currentData()
        javni_kljuc_ka: Kljuc = self.cbKa.currentData()
        sifruj = self.cbSifruj.isChecked()
        sifruj_algoritam = self.cbSifrujAlgoritam.currentText()  # Simetricni algoritam
        potpisi = self.cbPotpisi.isChecked()
        potpisi_lozinka = self.lePotpisiLozinka.text()
        kompresuj = self.cbKompresuj.isChecked()
        poremeti_potpis = self.cbPoremetiPotpis.isChecked()
        poremeti_sifrovanje = self.cbPoremetiSifrovanje.isChecked()
        radix64 = self.cbKonvertuj.isChecked()

        if radix64:
            plaintext = base64.b64encode(bytes(plaintext, "utf-8"))

        # Prvo potpisivanje poruke
        if potpisi:
            javni_kljuc_od: Kljuc = self.prsten_kljuceva.nadji_po_mejlu(
                privatni_kljuc_od.mejl, "public", privatni_kljuc_od.algoritam
            )
            if javni_kljuc_od is None:
                upozori_greska("Cudna situacija, nemamo javni kljuc posiljaoca (nas)?")
                return
            izracunat_hes = privatni_kljuc_od.potpisi(plaintext, potpisi_lozinka)
            if izracunat_hes is None:
                upozori_greska("Potpis poruke je prazan, lozinka za PK nije ispravna!")
                return
            telo_poruke = TeloPoruke(
                plaintext, potpisi, izracunat_hes, javni_kljuc_od.id(), time.time()
            )

            if poremeti_potpis:
                telo_poruke.potpis = telo_poruke.potpis[:-2] + b"\xaf\xaf"
        else:
            telo_poruke = TeloPoruke(plaintext, False, timestamp=time.time())

        # Kompresovanje
        kompresovani_bajtovi = pickle.dumps(telo_poruke)
        if kompresuj:
            kompresovani_bajtovi = zlib_ng.compress(kompresovani_bajtovi)

        sifrovan_sesijski_kljuc = None
        sifrovano_telo_poruke = kompresovani_bajtovi

        # Potom enkripcija
        if sifruj:
            sesijski_kljuc = self.generisi_simetricni_kljuc(sifruj_algoritam)
            if poremeti_sifrovanje:
                novi_sesijski_kljuc = self.generisi_simetricni_kljuc(sifruj_algoritam)
            else:
                novi_sesijski_kljuc = sesijski_kljuc

            # Sesijskim kljucem sifruj kompresovanu poruku
            sifrovano_telo_poruke = self.sifruj_simetricnim_kljucem(
                sifruj_algoritam, sesijski_kljuc, kompresovani_bajtovi
            )
            # Sifruj sesijski kljuc javnim kljucem primaoca
            sifrovan_sesijski_kljuc = javni_kljuc_ka.sifruj(novi_sesijski_kljuc)

        konacna_poruka = Poruka(
            sifrovano_telo_poruke,
            sifruj,
            kompresuj,
            sifruj_algoritam,
            javni_kljuc_ka.id(),
            sifrovan_sesijski_kljuc,
        )

        putanja = self.save_file_dialog()[0]
        if putanja != "":
            with open(putanja, "wb") as izvozf:
                izvozf.write(pickle.dumps(konacna_poruka))

    def odradi_desifrovanje(self):
        self.tbDesifrovanaPoruka.setText("")

        lokacija_fajla = self.leOdabranFajl.text()
        if lokacija_fajla == "":
            upozori_greska("Nije odabran fajl za otkljucavanje!")
            return

        self.teRezultati.setText("")

        lozinka = self.leLozinkaVerifikacija.text()
        self.cbUspesanPotpis.setChecked(True)
        self.cbUspesnoDesifrovao.setChecked(True)

        unradix64 = self.cbUnRadix64.isChecked()

        try:
            with open(lokacija_fajla, "rb") as uvozf:
                poruka = pickle.loads(uvozf.read())
        except:
            upozori_greska("Fajl je korumpiran!")
            return

        # Desifrovanje sesijskog kljuca
        if poruka.sifruj:
            javni_kljuc_primaoca: Kljuc = self.prsten_kljuceva.nadji_po_id(
                poruka.javni_kljuc_id, "public"
            )
            if javni_kljuc_primaoca is None:
                upozori_greska("Javni kljuc primaoca nije nadjen!")
                self.cbUspesnoDesifrovao.setChecked(False)
                return

            privatni_kljuc_primaoca: Kljuc = self.prsten_kljuceva.nadji_po_mejlu(
                javni_kljuc_primaoca.mejl, "private", javni_kljuc_primaoca.algoritam
            )
            if privatni_kljuc_primaoca is None:
                upozori_greska("Privatni kljuc primaoca (nas) nije nadjen!")
                self.cbUspesnoDesifrovao.setChecked(False)
                return

            desifrovan_sesijski_kljuc = privatni_kljuc_primaoca.desifruj(
                poruka.sifrovan_sesijski_kljuc, lozinka
            )
            if desifrovan_sesijski_kljuc is None:
                upozori_greska("Privatni kljuc nije uspesno desifrovan lozinkom!")
                self.cbUspesnoDesifrovao.setChecked(False)
                return

            desifrovano_telo_poruke = self.desifruj_simetricnim_kljucem(
                poruka.sifruj_algoritam, desifrovan_sesijski_kljuc, poruka.telo_poruke
            )
            self.teRezultati.append("Poruka uspesno desifrovana.\n")
        else:
            desifrovano_telo_poruke = poruka.telo_poruke
            self.teRezultati.append("Poruka nije sifrovana.\n")

        # Dekompresija
        if poruka.kompresuj:
            try:
                telo_poruke = zlib_ng.decompress(desifrovano_telo_poruke)
            except:
                upozori_greska("Poruka nije uspesno dekompresovana!")
                return
        else:
            telo_poruke = desifrovano_telo_poruke

        try:
            telo_poruke = pickle.loads(telo_poruke)
            self.teRezultati.append("Poruka uspesno dekompresovana.\n")
        except:
            upozori_greska("Telo poruke je korumpirano - neuspesno desifrovanje!")
            self.cbUspesanPotpis.setChecked(False)
            return

        # Provera hash-a poruke
        if telo_poruke.potpisana:
            javni_kljuc_posiljaoca: Kljuc = self.prsten_kljuceva.nadji_po_id(
                telo_poruke.id_kljuca, "public"
            )
            if javni_kljuc_posiljaoca is None:
                upozori_greska(
                    "Neuspela provera potpisa poruke! Nemamo javni kljuc posiljaoca u prstenu!"
                )
                self.cbUspesanPotpis.setChecked(False)
                return
            if not javni_kljuc_posiljaoca.proveri_potpis(
                telo_poruke.plaintext, telo_poruke.potpis
            ):
                upozori_greska("Neuspela provera potpisa poruke!")
                self.cbUspesanPotpis.setChecked(False)
                return

            self.teRezultati.append(
                f"Potpis poruke uspesno proveren. Mejl autora je {javni_kljuc_posiljaoca.mejl}.\n"
            )

        try:
            radix64_dekodovan = base64.b64decode(telo_poruke.plaintext).decode("utf-8")
            if unradix64:
                self.teRezultati.append("Radix64 uspesno dekodovan.\n")
                plaintext = radix64_dekodovan
            else:
                plaintext = telo_poruke.plaintext
        except:
            plaintext = telo_poruke.plaintext
            if unradix64:
                self.teRezultati.append("Radix64 nije prisutan.\n")

        self.tbDesifrovanaPoruka.setText(str(plaintext))
        self.teRezultati.append(
            f"Poruka uspesno parsirana. Timestamp: {datetime.datetime.fromtimestamp(telo_poruke.timestamp)}.\n"
        )

    def zatrazi_lozinku(self):
        text, ok = QInputDialog.getText(self, "Lozinka", "Unesite lozinku za PK:")

        if ok:
            return str(text)
        return None

    def uvezi_fajl(self):
        fajl = self.open_file_dialog()[0]
        self.leOdabranFajl.setText(fajl)

    def azuriraj_tabele(self):
        self.privatniKljuceviWidget.clear()
        self.javniKljuceviWidget.clear()

        self.privatniKljuceviWidget.setHorizontalHeaderLabels(HEDERI_TABELA)
        self.javniKljuceviWidget.setHorizontalHeaderLabels(HEDERI_TABELA[:-1])

        self.privatniKljuceviWidget.setRowCount(self.prsten_kljuceva.broj_privatnih)
        self.javniKljuceviWidget.setRowCount(self.prsten_kljuceva.broj_javnih)

        privateRow = 0
        publicRow = 0
        for kljuc in self.prsten_kljuceva.kljucevi:
            if kljuc.tip == "private":
                self.privatniKljuceviWidget.setItem(
                    privateRow, 0, QTableWidgetItem(kljuc.ime)
                )
                self.privatniKljuceviWidget.setItem(
                    privateRow, 1, QTableWidgetItem(kljuc.mejl)
                )
                self.privatniKljuceviWidget.setItem(
                    privateRow, 2, QTableWidgetItem(kljuc.algoritam)
                )
                self.privatniKljuceviWidget.setItem(
                    privateRow, 3, QTableWidgetItem(str(kljuc.velicina))
                )
                self.privatniKljuceviWidget.setItem(
                    privateRow, 4, QTableWidgetItem(kljuc.svrha)
                )
                self.privatniKljuceviWidget.setItem(
                    privateRow, 5, QTableWidgetItem(kljuc.vezan_sa)
                )
                privateRow += 1
            else:
                self.javniKljuceviWidget.setItem(
                    publicRow, 0, QTableWidgetItem(kljuc.ime)
                )
                self.javniKljuceviWidget.setItem(
                    publicRow, 1, QTableWidgetItem(kljuc.mejl)
                )
                self.javniKljuceviWidget.setItem(
                    publicRow, 2, QTableWidgetItem(kljuc.algoritam)
                )
                self.javniKljuceviWidget.setItem(
                    publicRow, 3, QTableWidgetItem(str(kljuc.velicina))
                )
                self.javniKljuceviWidget.setItem(
                    publicRow, 4, QTableWidgetItem(kljuc.svrha)
                )
                publicRow += 1

        # Azuriranje combo box-ova u drugom tabu
        self.cbKa.clear()
        self.cbOd.clear()
        for kljuc in self.prsten_kljuceva.kljucevi:
            if kljuc.tip == "private" and kljuc.algoritam != "elgamal":
                self.cbOd.addItem(
                    kljuc.mejl + ", " + kljuc.tip + ", " + kljuc.algoritam, kljuc
                )  # Nas je privatni kojim potvrdjujemo autenticnost
            else:
                if kljuc.tip == "public" and kljuc.algoritam != "dsa":
                    self.cbKa.addItem(
                        kljuc.mejl + ", " + kljuc.tip + ", " + kljuc.algoritam, kljuc
                    )

    def generisi_kljuc(self):
        def generisi_accepted():
            ime = self.generisi_kljuc_window_ui.lineIme.text()
            mejl = self.generisi_kljuc_window_ui.lineMejl.text()
            velicina = self.generisi_kljuc_window_ui.cbVelicinaKljuca.currentText()
            algoritam = self.generisi_kljuc_window_ui.cbAlgoritam.currentText()
            lozinka = self.generisi_kljuc_window_ui.lineSifra.text()

            self.prsten_kljuceva.generisi(
                ime, mejl, algoritam, int(velicina), lozinka
            )
            self.azuriraj_tabele()

        def generisi_rejected():
            self.generisi_kljuc_window.close()

        self.generisi_kljuc_window = QMainWindow()
        self.generisi_kljuc_window_ui = Ui_GenerisiKljucDialog()
        self.generisi_kljuc_window_ui.setupUi(self.generisi_kljuc_window)
        self.generisi_kljuc_window.show()

        self.generisi_kljuc_window_ui.buttonBox.accepted.connect(generisi_accepted)
        self.generisi_kljuc_window_ui.buttonBox.rejected.connect(generisi_rejected)

    def open_file_dialog(self):
        return QFileDialog.getOpenFileName(self, "Otvori", os.getcwd(), filter="*")

    def save_file_dialog(self):
        return QFileDialog.getSaveFileName(self, "Snimi", os.getcwd(), filter="*")

    def uvezi_javni(self):
        lokacija = self.open_file_dialog()[0]
        if lokacija == "":
            return

        with open(lokacija, "rb") as privatefile:
            sadrzaj = privatefile.read()

        def uvezi_accepted():
            ime = self.uvezi_kljuc_window_ui.leIme.text()
            mejl = self.uvezi_kljuc_window_ui.leMejl.text()

            if b"RSA" in sadrzaj:
                public_key = rsa.PublicKey.load_pkcs1(sadrzaj, "PEM")
                javni_rsa = Kljuc(
                    ime,
                    mejl,
                    "RSA",
                    math.floor(math.log2(public_key.n)) + 1,
                    "public",
                    public_key,
                    "Enkripcija",
                )
                self.prsten_kljuceva.dodaj_kljuc(javni_rsa)

            self.azuriraj_tabele()

        def uvezi_rejected():
            self.uvezi_kljuc_window.close()

        self.uvezi_kljuc_window = QMainWindow()
        self.uvezi_kljuc_window_ui = Ui_UveziKljucDialog()
        self.uvezi_kljuc_window_ui.setupUi(self.uvezi_kljuc_window)
        self.uvezi_kljuc_window.show()

        self.uvezi_kljuc_window_ui.buttonBox.accepted.connect(uvezi_accepted)
        self.uvezi_kljuc_window_ui.buttonBox.rejected.connect(uvezi_rejected)

    def uvezi_privatni(self):
        lokacija = self.open_file_dialog()[0]
        if lokacija == "":
            return

        with open(lokacija, "rb") as privatefile:
            sadrzaj = privatefile.read()

        def uvezi_accepted():
            ime = self.uvezi_kljuc_window_ui.leIme.text()
            mejl = self.uvezi_kljuc_window_ui.leMejl.text()
            lozinka = self.uvezi_kljuc_window_ui.leLozinka.text()

            if b"RSA" in sadrzaj:
                privkey = rsa.PrivateKey.load_pkcs1(sadrzaj, "PEM")
                privatni_rsa = Kljuc(
                    ime,
                    mejl,
                    "RSA",
                    math.floor(math.log2(privkey.n)) + 1,
                    "private",
                    privkey,
                    "Enkripcija",
                )
                privatni_rsa.zakljucaj_sadrzaj(lozinka)
                self.prsten_kljuceva.dodaj_kljuc(privatni_rsa)

            self.azuriraj_tabele()

        def uvezi_rejected():
            self.uvezi_kljuc_window.close()

        self.uvezi_kljuc_window = QMainWindow()
        self.uvezi_kljuc_window_ui = Ui_UveziKljucDialog()
        self.uvezi_kljuc_window_ui.setupUi(self.uvezi_kljuc_window)
        self.uvezi_kljuc_window.show()

        self.uvezi_kljuc_window_ui.buttonBox.accepted.connect(uvezi_accepted)
        self.uvezi_kljuc_window_ui.buttonBox.rejected.connect(uvezi_rejected)

    def izvezi_javni(self):
        redovi = self.javniKljuceviWidget.selectionModel().selectedRows()
        if len(redovi) == 0:
            upozori_greska("Nije odabran javni kljuc za izvoz!")
            return
        red = redovi[0].row()
        pem_za_izvoz = self.prsten_kljuceva.izvoz(
            self.javniKljuceviWidget.item(red, 1).text(),
            "public",
            self.javniKljuceviWidget.item(red, 2).text(),
        )

        izvoz = self.save_file_dialog()
        if izvoz[0] != "":
            with open(izvoz[0], "wb" if isinstance(pem_za_izvoz, bytes) else "w") as f:
                f.write(pem_za_izvoz)

    def izvezi_privatni(self):
        redovi = self.privatniKljuceviWidget.selectionModel().selectedRows()
        if len(redovi) == 0:
            upozori_greska("Nije odabran privatni kljuc za izvoz!")
            return
        red = redovi[0].row()

        lozinka = self.zatrazi_lozinku()
        pem_za_izvoz = self.prsten_kljuceva.izvoz(
            self.privatniKljuceviWidget.item(red, 1).text(),
            "private",
            self.privatniKljuceviWidget.item(red, 2).text(),
            lozinka,
        )
        if pem_za_izvoz is None:
            upozori_greska("Lozinka za PK nije tacna!")
            return

        izvoz = self.save_file_dialog()
        if izvoz[0] != "":
            with open(izvoz[0], "wb" if isinstance(pem_za_izvoz, bytes) else "w") as f:
                f.write(pem_za_izvoz)

    def obrisi_javni(self):
        redovi = self.javniKljuceviWidget.selectionModel().selectedRows()
        if len(redovi) == 0:
            upozori_greska("Nije odabran javni kljuc za brisanje!")
            return
        red = redovi[0].row()
        mejl_za_brisanje = self.javniKljuceviWidget.item(red, 1).text()
        self.prsten_kljuceva.ukloni_kljuc(mejl_za_brisanje, "public")
        self.azuriraj_tabele()

    def obrisi_privatni(self):
        redovi = self.privatniKljuceviWidget.selectionModel().selectedRows()
        if len(redovi) == 0:
            upozori_greska("Nije odabran privatni kljuc za brisanje!")
            return
        red = redovi[0].row()
        mejl_za_brisanje = self.privatniKljuceviWidget.item(red, 1).text()
        self.prsten_kljuceva.ukloni_kljuc(mejl_za_brisanje, "private")
        self.azuriraj_tabele()


class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
