import os
import time
from PIL import Image, ImageEnhance, ImageDraw, ImageFont

class NexusProFotoEditor:
    def __init__(self, autor="Dušan Štiglic"):
        self.autor = autor
        print(f"==========================================")
        print(f" NEXUS PRO FOTO STUDIO // Autor: {self.autor}")
        print(f"==========================================")

    def obradi_sliku(self, putanja_do_slike):
        if not os.path.exists(putanja_do_slike):
            print(f"[GREŠKA] Slika '{putanja_do_slike}' ne postoji u folderu! Ubaci neku sliku (npr. slika.jpg).")
            return

        id_transakcije = int(time.time()) % 9000 + 1000
        print(f"\n[INFO] Učitavam sliku: {putanja_do_slike}")
        
        try:
            img = Image.open(putanja_do_slike).convert("RGB")
            
            # 1. Ozbiljna profesionalna obrada (Kontrast, Oštrina, Boje)
            print(f"[INFO] Primenjujem AI korekciju oštrine i boja...")
            
            # Pojačavanje kontrasta
            enhancer_c = ImageEnhance.Contrast(img)
            img = enhancer_c.enhance(1.25)
            
            # Pojačavanje oštrine detalja
            enhancer_s = ImageEnhance.Sharpness(img)
            img = enhancer_s.enhance(1.5)
            
            # Pojačavanje živosti boja
            enhancer_col = ImageEnhance.Color(img)
            img = enhancer_col.enhance(1.2)

            # 2. Profesionalni Autorski Vodeni Žig (Veliki i uočljiv)
            draw = ImageDraw.Draw(img)
            sirina, visina = img.size
            
            tekst_potpisa = f"© {self.autor} | NEXUS PRO"
            
            # Pozicija u donjem desnom uglu sa automatskim skaliranjem prema veličini slike
            x_poz = sirina - int(sirina * 0.25)
            y_poz = visina - int(visina * 0.08)
            
            draw.text((x_poz, y_poz), tekst_potpisa, fill=(0, 255, 204))

            # 3. Čuvanje u maksimalnom kvalitetu
            izlazni_fajl = f"PRO_Obradjena_ID_{id_transakcije}.jpg"
            img.save(izlazni_fajl, quality=100)
            
            print(f"[USPEH] Slika uspešno obrađena i sačuvana kao: {izlazna_fajl}")

        except Exception as e:
            print(f"[GREŠKA] Neuspešna obrada slike: {e}")

if __name__ == "__main__":
    editor = NexusProFotoEditor()
    # Ovde upiši ime svoje slike koju hoćeš da obradiš, npr. "slika1.jpg"
    editor.obradi_sliku("slika1.jpg")