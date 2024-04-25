from abc import ABC, abstractmethod
import datetime


class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def ar_szamitas(self):
        pass


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=10000, szobaszam=szobaszam)

    def ar_szamitas(self):
        return self.ar


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=15000, szobaszam=szobaszam)

    def ar_szamitas(self):
        return self.ar


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szoba, datum):
        foglalas = Foglalas(szoba, datum)
        self.foglalasok.append(foglalas)
        return foglalas.ar_szamitas()

    def foglalas_by_szobaszam_and_datum(self, szobaszam, datum):
        today = datetime.date.today()
        if datum < today:
            return "A foglalás nem sikeres, mert a megadott dátum a múltban van."
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                return "A foglalás nem sikeres, mert a szoba már foglalt."
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas = Foglalas(szoba, datum)
                self.foglalasok.append(foglalas)
                return foglalas.ar_szamitas()
        return "A foglalás nem sikeres, mert érvénytelen szobaszám."

    def lemondas_by_szobaszam_and_datum(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return True
        return False

    def listaz_foglalasok(self):
        for foglalas in self.foglalasok:
            print(f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}")


class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

    def ar_szamitas(self):
        return self.szoba.ar_szamitas()


def main():
    # Szálloda, szobák és foglalások inicializálása
    szalloda = Szalloda(nev="Szállj-oda Szálloda")
    egyagyas_szoba1 = EgyagyasSzoba(szobaszam=101)
    ketagyas_szoba1 = KetagyasSzoba(szobaszam=102)
    ketagyas_szoba2 = KetagyasSzoba(szobaszam=103)
    szalloda.add_szoba(egyagyas_szoba1)
    szalloda.add_szoba(ketagyas_szoba1)
    szalloda.add_szoba(ketagyas_szoba2)
    szalloda.foglalas(egyagyas_szoba1, datetime.date(2024, 5, 15))
    szalloda.foglalas(egyagyas_szoba1, datetime.date(2024, 5, 16))
    szalloda.foglalas(ketagyas_szoba1, datetime.date(2024, 5, 15))
    szalloda.foglalas(ketagyas_szoba1, datetime.date(2024, 5, 17))
    szalloda.foglalas(ketagyas_szoba2, datetime.date(2024, 5, 18))

    # Felhasználói interfész
    print(f"Üdvözöl a {szalloda.nev}!")
    print("\nVálaszható szobák:")
    print("101-es szoba: Egyágyas szoba 1")
    print("102-es szoba: Kétágyas szoba 1")
    print("103-as szoba: Kétágyas szoba 2")

    while True:
        print("\nVálassz egy műveletet:")
        print("1. Foglalás")
        print("2. Lemondás")
        print("3. Foglalások listázása")
        print("4. Kilépés")

        valasztas = input("Művelet kiválasztása (1/2/3/4): ")

        if valasztas == "1":
            szobaszam = int(input("Add meg a foglalandó szoba számát: "))
            datum_str = input("Add meg a foglalás dátumát (éééé-hh-nn): ")
            datum = datetime.datetime.strptime(datum_str, "%Y-%m-%d").date()
            foglalas_ar = szalloda.foglalas_by_szobaszam_and_datum(szobaszam, datum)
            if isinstance(foglalas_ar, str):
                print(foglalas_ar)
            else:
                print(f"Foglalás sikeres! Ár: {foglalas_ar} Ft")

        elif valasztas == "2":
            szobaszam = int(input("Add meg a lemondandó foglalás szoba számát: "))
            datum_str = input("Add meg a lemondandó foglalás dátumát (éééé-hh-nn): ")
            datum = datetime.datetime.strptime(datum_str, "%Y-%m-%d").date()
            sikeres = szalloda.lemondas_by_szobaszam_and_datum(szobaszam, datum)
            if sikeres:
                print("A foglalás lemondása sikeres.")
            else:
                print("Nem sikerült a lemondás. Ilyen szobaszámmal és időponttal nem létezik foglalás a rendszerben.")

        elif valasztas == "3":
            print("Foglalások listázása:")
            szalloda.listaz_foglalasok()

        elif valasztas == "4":
            print("Kilépés...")
            break

        else:
            print("Érvénytelen választás. Kérlek válasszon egy érvényes műveletet.")


if __name__ == "__main__":
    main()
