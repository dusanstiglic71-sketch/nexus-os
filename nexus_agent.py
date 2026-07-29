import os
import datetime

HTML_FAJL = "index.html"
LOG_FAJL = "nexus_agent.log"

def zapisi_log(poruka):
    vreme = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_tekst = f"[{vreme}] {poruka}\n"
    print(log_tekst.strip())
    with open(LOG_FAJL, "a", encoding="utf-8") as f:
        f.write(log_tekst)

def ucitaj_sajt():
    if not os.path.exists(HTML_FAJL):
        zapisi_log("Greška: index.html nije pronađen!")
        return ""
    with open(HTML_FAJL, "r", encoding="utf-8") as f:
        return f.read()

def sacuvaj_sajt(sadrzaj):
    with open(HTML_FAJL, "w", encoding="utf-8") as f:
        f.write(sadrzaj)
    zapisi_log("Sajt uspešno ažuriran i sačuvan.")

def dodaj_element_na_sajt(html_kod_elementa):
    sadrzaj = ucitaj_sajt()
    # Ubacujemo novi element pre zatvaranja body sekcije
    if "</body>" in sadrzaj:
        novi_sadrzaj = sadrzaj.replace("</body>", f"\n    {html_kod_elementa}\n</body>")
        sacuvaj_sajt(novi_sadrzaj)
        zapisi_log("Novi element uspešno ubačen u strukturu sajta.")
    else:
        zapisi_log("Greška: Nije pronađen </body> tag u HTML-u.")

if __name__ == "__main__":
    zapisi_log("NEXUS Agent pokrenut u modifikovanom režimu sa naprednim funkcijama.")
    # Primer automatske provere i logovanja
    sadrzaj = ucitaj_sajt()
    zapisi_log(f"Učitan index.html, veličina fajla: {len(sadrzaj)} karaktera.")