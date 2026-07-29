# ==========================================
# NEXUS OS // PRODAJNI TERMINAL V3.0
# Autor: Dušan Štiglic
# ==========================================

import os
import sys
import time
import json
import datetime

FAJL_ZA_SAJT = "prodaja.json"
FAJL_BAZA = "baza_kupaca.json"
DIR_FAKTURA = "fakture"

# Kreiranje foldera za fakture ako ne postoji
if not os.path.exists(DIR_FAKTURA):
    os.makedirs(DIR_FAKTURA)

PAKETI = {
    "1": {
        "naziv": "Core Modul",
        "cena_num": 29,
        "cena": "29€",
        "opis": "Osnovno rešenje za stabilan start sa čistom web arhitekturom i Git repo-om."
    },
    "2": {
        "naziv": "Elite System",
        "cena_num": 69,
        "cena": "69€",
        "opis": "Cyberpunk dizajn, stakleni efekti, napredne metrike i ugrađeni AI asistent."
    },
    "3": {
        "naziv": "Enterprise VIP",
        "cena_num": 149,
        "cena": "149€",
        "opis": "Potpuno prilagođen kod, baze podataka, enkripcija i 24/7 VIP podrška."
    }
}

def ucitaj_bazu():
    if os.path.exists(FAJL_BAZA):
        try:
            with open(FAJL_BAZA, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def sacuvaj_bazu(baza):
    with open(FAJL_BAZA, "w", encoding="utf-8") as f:
        json.dump(baza, f, ensure_ascii=False, indent=4)

def generisi_fakturu(transakcija):
    ime_fajla = f"{DIR_FAKTURA}/Faktura_ID_{transakcija['id']}.txt"
    sadrzaj = f"""==================================================
           NEXUS OS // POTVRDA O KUPOVINI
==================================================
 ID Transakcije: #{transakcija['id']}
 Datum i vreme:  {transakcija['vreme']}
 Kupljeni paket: {transakcija['poslednji_kupac']}
 Cena:           {transakcija['cena']}
 Status:         {transakcija['status']}
--------------------------------------------------
 Glavni Inženjer / Autor: Dušan Štiglic
 Podrška i kontakt: Službeni NEXUS Core Sistem
==================================================
 Hvala na poverenju! Vaš sistem je uspešno isporučen.
"""
    with open(ime_fajla, "w", encoding="utf-8") as f:
        f.write(sadrzaj)
    return ime_fajla

def prikazi_meni():
    print("\n" + "="*55)
    print(" ⚡ NEXUS OS // PRODAJNI TERMINAL (PRODUKCIJA)")
    print(" Autor: Dušan Štiglic")
    print("="*55)
    print("Izaberi opciju:")
    print(" [1] Katalog paketa i cena")
    print(" [2] Naplati, isporuči i sinhronizuj sajt")
    print(" [3] Pregled finansija i baze kupaca")
    print(" [4] Generisi izveštaj o prodaji")
    print(" [5] Izlaz iz sistema")
    print("="*55)

def main():
    print("\n[OK] Pokretanje produkcijskog sistema...")
    time.sleep(0.5)
    
    while True:
        prikazi_meni()
        izbor = input("\nUnesi komandu (1-5): ").strip()
        
        if izbor == "1":
            print("\n--- KATALOG PAKETA ZA PRODAJU ---")
            for kljuc, p in PAKETI.items():
                print(f"[{kljuc}] {p['naziv']} -> {p['cena']}")
                print(f"    Opis: {p['opis']}")
            print("-" * 40)
            
        elif izbor == "2":
            print("\n--- MODUL ZA NAPLATU I FAKTURISANJE ---")
            for kljuc, p in PAKETI.items():
                print(f" [{kljuc}] {p['naziv']} ({p['cena']})")
            
            paket_izbor = input("\nUnesi broj paketa koji klijent kupuje (1-3): ").strip()
            
            if paket_izbor in PAKETI:
                p = PAKETI[paket_izbor]
                vreme_sada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                baza = ucitaj_bazu()
                novi_id = len(baza) + 1
                
                transakcija = {
                    "id": novi_id,
                    "poslednji_kupac": p['naziv'],
                    "cena": p['cena'],
                    "cena_num": p['cena_num'],
                    "status": "Plaćeno & Automatski isporučeno",
                    "autor": "Dušan Štiglic",
                    "vreme": vreme_sada
                }
                
                # 1. Sinhronizacija sa sajtom
                with open(FAJL_ZA_SAJT, "w", encoding="utf-8") as f_json:
                    json.dump(transakcija, f_json, ensure_ascii=False, indent=4)
                
                # 2. Upis u trajnu bazu
                baza.append(transakcija)
                sacuvaj_bazu(baza)
                
                # 3. Generisanje zvanične fakture
                putanja_fakture = generisi_fakturu(transakcija)
                
                print(f"\n[USPEH] Transakcija #{novi_id} uspešno procesuirana!")
                print(f"[PROMET] Naplaćen paket: {p['naziv']} ({p['cena']})")
                print(f"[FAKTURA] Kreiran dokument: {putanja_fakture}")
                print(f"[SAJT] Status automatski prosleđen na web sajt.")
                print(f"Autor sistema: Dušan Štiglic.")
            else:
                print("\n[GREŠKA] Nepoznat paket. Izaberi opciju od 1 do 3.")
                
        elif izbor == "3":
            baza = ucitaj_bazu()
            print(f"\n--- FINANSIJSKI IZVEŠTAJ ---")
            if not baza:
                print("Nema zabeleženih prodaja.")
            else:
                ukupan_promet = sum(t['cena_num'] for t in baza)
                print(f"Ukupno prodatih paketa: {len(baza)}")
                print(f"Ukupan prihod: {ukupan_promet}€\n")
                print("Lista poslednjih transakcija:")
                for t in baza[-10:]:
                    print(f" ID #{t['id']} | {t['vreme']} | {t['poslednji_kupac']} - {t['cena']}")
            print("-" * 40)
            
        elif izbor == "4":
            baza = ucitaj_bazu()
            ime_izvestaja = "Izvestaj_Prodaje.txt"
            ukupan_promet = sum(t['cena_num'] for t in baza) if baza else 0
            
            with open(ime_izvestaja, "w", encoding="utf-8") as f:
                f.write(f"NEXUS OS - ZVANIČNI IZVEŠTAJ O PRODAJI\nAutor: Dušan Štiglic\n")
                f.write(f"Ukupan prihod: {ukupan_promet}€ | Ukupno prodaja: {len(baza)}\n\n")
                for t in baza:
                    f.write(f"ID: #{t['id']} | Paket: {t['poslednji_kupac']} | Cena: {t['cena']} | Vreme: {t['vreme']}\n")
            
            print(f"\n[USPEH] Izveštaj uspešno sačuvan u fajl '{ime_izvestaja}'!")
            
        elif izbor == "5":
            print("\nGašenje prodajnog terminala. Srećno sa prodajom, majstore!")
            sys.exit(0)
        else:
            print("\n[GREŠKA] Nepoznata komanda.")

if __name__ == "__main__":
    main()
    import zipfile

def pripremi_isporuku(transakcija):
    dir_isporuke = "isporuka_klijentima"
    if not os.path.exists(dir_isporuke):
        os.makedirs(dir_isporuke)
        
    naziv_zipa = f"{dir_isporuke}/NEXUS_Paket_ID_{transakcija['id']}.zip"
    
    # Kreiramo zip fajl i unutra ubacujemo podatke za klijenta
    with zipfile.ZipFile(naziv_zipa, 'w') as zf:
        # Možeš da upišeš u zip fajl šta god želiš (npr. uputstvo ili sam kod)
        Uputstvo_tekst = f"Hvala na kupovini paketa {transakcija['poslednji_kupac']}!\nAutor: Dušan Štiglic\nID: #{transakcija['id']}"
        zf.writestr("Uputstvo_za_instalaciju.txt", Uputstvo_tekst)
        
    print(f"[ISPORUKA] Kreiran paket za preuzimanje: {naziv_zipa}")
    return naziv_zipa