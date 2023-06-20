import pickle

import rsa
import sympy
import Crypto
from Crypto import Util
from Crypto.Cipher import CAST, AES
from Crypto.Hash import SHA1
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Util.number import inverse


class Kljuc:
    def __init__(self, ime, mejl, algoritam, velicina, tip, sadrzaj, svrha):
        self.tag = None
        self.nonce = None
        self.ime = ime
        self.interno_ime = ime + "-" + tip
        self.mejl = mejl
        self.algoritam = algoritam
        self.velicina = velicina
        self.tip = tip  # public, private, session
        if tip == "private":
            self.vezan_sa = (
                ime + "-" + ("public" if self.tip == "private" else "private")
            )
        self.sadrzaj = sadrzaj
        self.svrha = svrha  # sign, enc

    def id(self, lozinka=None):
        if self.tip == "private":
            otkljucan_sadrzaj = self.otkljucaj_sadrzaj(lozinka)
        else:
            otkljucan_sadrzaj = self.sadrzaj

        if self.algoritam == "RSA":
            return otkljucan_sadrzaj.save_pkcs1()[-64:].hex()
        elif self.algoritam == "elgamal":
            return hex(
                otkljucan_sadrzaj[0] * otkljucan_sadrzaj[1] * otkljucan_sadrzaj[2]
            )
        else:
            # DSA
            return hex(
                otkljucan_sadrzaj["y"] * otkljucan_sadrzaj["g"] * otkljucan_sadrzaj["p"]
            )

    def zakljucaj_sadrzaj(self, lozinka):
        lozinka = lozinka.encode("utf-8")
        sha1_hes = SHA1.new(lozinka).digest()[-16:]

        cipher = AES.new(sha1_hes, AES.MODE_EAX)
        self.nonce = cipher.nonce

        encrypted, tag = cipher.encrypt_and_digest(pickle.dumps(self.sadrzaj))
        self.tag = tag
        self.sadrzaj = encrypted

        #self.sadrzaj = CAST.new(sha1_hes, CAST.MODE_OPENPGP).encrypt(
        #    pickle.dumps(self.sadrzaj)
        #)

    def otkljucaj_sadrzaj(self, lozinka):
        lozinka = lozinka.encode("utf-8")
        sha1_hes = SHA1.new(lozinka).digest()[-16:]

        cipher = AES.new(sha1_hes, AES.MODE_EAX, nonce=self.nonce)
        decrypted = cipher.decrypt(self.sadrzaj)
        try:
            cipher.verify(self.tag)
        except ValueError:
            return None
        
        return pickle.loads(decrypted)

        """
        eiv = self.sadrzaj[: CAST.block_size + 2]
        podaci = self.sadrzaj[CAST.block_size + 2 :]
        try:
            return pickle.loads(
                CAST.new(sha1_hes, CAST.MODE_OPENPGP, eiv).decrypt(podaci)
            )
        except:
            # Lozinka ne valja
            return None
        """

    def potpisi(self, poruka, lozinka):
        if isinstance(poruka, str):
            poruka = poruka.encode("utf-8")

        if self.tip == "private":
            otkljucan_sadrzaj = self.otkljucaj_sadrzaj(lozinka)
            if otkljucan_sadrzaj is None:
                return None
        else:
            otkljucan_sadrzaj = self.sadrzaj

        if self.algoritam == "RSA":
            return rsa.sign(poruka, otkljucan_sadrzaj, "SHA-1")
        else:
            dsa_kljuc = DSA.construct(
                (
                    otkljucan_sadrzaj["y"],
                    otkljucan_sadrzaj["g"],
                    otkljucan_sadrzaj["p"],
                    otkljucan_sadrzaj["q"],
                    otkljucan_sadrzaj["x"],
                )
            )
            hash_obj = SHA1.new(poruka)
            return DSS.new(dsa_kljuc, "fips-186-3").sign(hash_obj)

    def proveri_potpis(self, podaci, potpis):
        if isinstance(podaci, str):
            podaci = podaci.encode("utf-8")

        if isinstance(potpis, str):
            potpis = potpis.encode("utf-8")

        if self.algoritam == "RSA":
            try:
                rsa.verify(podaci, potpis, self.sadrzaj)
                return True
            except (rsa.VerificationError, TypeError, ValueError):
                return False
        else:
            hashed_msg = SHA1.new(podaci)
            dsa_kljuc = DSA.construct(
                (
                    self.sadrzaj["y"],
                    self.sadrzaj["g"],
                    self.sadrzaj["p"],
                    self.sadrzaj["q"],
                )
            )
            verifier = DSS.new(dsa_kljuc, "fips-186-3")
            try:
                verifier.verify(hashed_msg, potpis)
                return True
            except ValueError:
                return False

    def sifruj(self, podaci, lozinka=None):
        if isinstance(podaci, str):
            podaci = podaci.encode("utf-8")

        if self.tip == "private":
            otkljucan_sadrzaj = self.otkljucaj_sadrzaj(lozinka)
            if otkljucan_sadrzaj is None:
                return None
        else:
            otkljucan_sadrzaj = self.sadrzaj

        if self.algoritam == "RSA":
            return rsa.encrypt(podaci, otkljucan_sadrzaj)
        else:
            # El Gamal
            m = int.from_bytes(podaci, byteorder="big")
            (p, g, y) = otkljucan_sadrzaj

            K = Crypto.Util.number.getRandomRange(2, p - 1)
            c1 = pow(g, K, p)
            c2 = (m * pow(y, K, p)) % p
            return c1, c2

    def desifruj(self, podaci, lozinka):
        if self.tip == "private":
            otkljucan_sadrzaj = self.otkljucaj_sadrzaj(lozinka)
            if otkljucan_sadrzaj is None:
                return None
        else:
            otkljucan_sadrzaj = self.sadrzaj

        if self.algoritam == "RSA":
            if isinstance(podaci, str):
                podaci = podaci.encode("utf-8")

            return rsa.decrypt(podaci, otkljucan_sadrzaj)
        else:
            # El Gamal
            p, g, y, x = otkljucan_sadrzaj
            c1, c2 = podaci
            s = pow(c1, x, p)
            inv_s = inverse(s, p)
            plaintext = (c2 * inv_s) % p
            return plaintext.to_bytes(
                (plaintext.bit_length() + 7) // 8, byteorder="big"
            )


class TeloPoruke:
    def __init__(
        self, plaintext, potpisana, potpis=None, id_kljuca=None, timestamp=None
    ):
        self.plaintext = plaintext
        self.potpisana = potpisana
        self.potpis = potpis
        self.id_kljuca = id_kljuca
        self.timestamp = timestamp


class Poruka:
    def __init__(
        self,
        telo_poruke,
        sifruj,
        kompresuj,
        sifruj_algoritam,
        javni_kljuc_id,
        sifrovan_sesijski_kljuc,
    ):
        self.telo_poruke = telo_poruke
        self.sifruj = sifruj
        self.kompresuj = kompresuj
        self.sifruj_algoritam = sifruj_algoritam
        self.javni_kljuc_id = javni_kljuc_id
        self.sifrovan_sesijski_kljuc = sifrovan_sesijski_kljuc


class PrstenKljuceva:
    def __init__(self):
        self.kljucevi = list()
        self.broj_privatnih = 0
        self.broj_javnih = 0

    def generisi(self, ime, mejl, algoritam, velicina, lozinka, svrha):
        if algoritam == "RSA":
            (public_key, private_key) = rsa.newkeys(velicina)
            privatni_rsa = Kljuc(
                ime, mejl, algoritam, velicina, "private", private_key, 'Enkripcija'
            )
            privatni_rsa.zakljucaj_sadrzaj(lozinka)
            javni_rsa = Kljuc(
                ime, mejl, algoritam, velicina, "public", public_key, 'Enkripcija'
            )

            self.dodaj_kljuc(privatni_rsa)
            self.dodaj_kljuc(javni_rsa)
        else:
            # DSA i El Gamal

            # Stvaranje El Gamala
            p = sympy.randprime(2 ** (velicina - 1), 2**velicina)  # Prime p
            g = sympy.randprime(3, p)  # Generator
            x = Crypto.Util.number.getRandomRange(2, p - 1)  # Privatni kljuc
            y = pow(g, x, p)  # Javni kljuc

            privatni_el_gamal = Kljuc(
                ime, mejl, "elgamal", velicina, "private", (p, g, y, x), "Enkripcija"
            )
            privatni_el_gamal.zakljucaj_sadrzaj(lozinka)
            javni_el_gamal = Kljuc(
                ime, mejl, "elgamal", velicina, "public", (p, g, y), "Enkripcija"
            )

            self.dodaj_kljuc(privatni_el_gamal)
            self.dodaj_kljuc(javni_el_gamal)

            # Stvaranje DSS
            dsa_kljuc = DSA.generate(velicina)
            privatni_dsa = Kljuc(
                ime, mejl, "dsa", velicina, "private", dsa_kljuc._key, "Potpisivanje"
            )
            privatni_dsa.zakljucaj_sadrzaj(lozinka)
            javni_dsa = Kljuc(
                ime, mejl, "dsa", velicina, "public", dsa_kljuc._key, "Potpisivanje"
            )

            self.dodaj_kljuc(privatni_dsa)
            self.dodaj_kljuc(javni_dsa)

    def dodaj_kljuc(self, kljuc):
        self.kljucevi.append(kljuc)
        if kljuc.tip == "private":
            self.broj_privatnih += 1
        else:
            self.broj_javnih += 1

    def ukloni_kljuc(self, mejl, tip):
        for kljuc in self.kljucevi:
            if kljuc.mejl == mejl and kljuc.tip == tip:
                if kljuc.tip == "private":
                    self.broj_privatnih -= 1
                else:
                    self.broj_javnih -= 1
                self.kljucevi.remove(kljuc)
                break

    def izvoz(self, mejl, tip, algoritam, lozinka=None):
        for kljuc in self.kljucevi:
            if kljuc.mejl == mejl and kljuc.tip == tip and kljuc.algoritam == algoritam:
                if kljuc.tip == "private":
                    otkljucan_sadrzaj = kljuc.otkljucaj_sadrzaj(lozinka)
                    if otkljucan_sadrzaj is None:
                        return None
                else:
                    otkljucan_sadrzaj = kljuc.sadrzaj

                if kljuc.algoritam == "RSA":
                    return otkljucan_sadrzaj.save_pkcs1().decode("utf8")
                elif kljuc.algoritam == "DSA":
                    return otkljucan_sadrzaj.export_key(passphrase=lozinka)
                else:
                    return pickle.dumps(otkljucan_sadrzaj)
        return None

    # Samo za javne
    def nadji_po_id(self, id, tip):
        for kljuc in self.kljucevi:
            if kljuc.tip == "private":
                continue
            if kljuc.id() == id and kljuc.tip == tip:
                return kljuc
        return None

    def nadji_po_mejlu(self, mejl, tip, algoritam):
        for kljuc in self.kljucevi:
            if kljuc.mejl == mejl and kljuc.tip == tip and kljuc.algoritam == algoritam:
                return kljuc
        return None
