import os
from datetime import datetime
from playwright.sync_api import sync_playwright

HTML_FAJL = "sajt.html"

def proveri_sajt():
    print(f"\n[AGENT // STATUS] Proveravam sistem: {HTML_FAJL}")
    if not os.path.exists(HTML_FAJL):
        print(f"[GREŠKA] Fajl {HTML_FAJL} nije pronađen!")
        return False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file:///{os.path.join(os.getcwd(), HTML_FAJL)}")
        naslov = page.title()
        print(f"[USPEH] Sajt je aktivan. Naslov: '{naslov}'")
        browser.close()
    return True

def auto_upgrade_sajta(novi_modul_naslov, opis_modula):
    """Ova funkcija omogućava botu da samostalno modifikuje HTML i doda novu sekciju na sajt!"""
    if not os.path.exists(HTML_FAJL):
        print("[GREŠKA] Ne mogu da izvršim upgrade, fajl ne postoji.")
        return

    print(f"\n[AUTO-UPGRADE] Pokrećem nadogradnju sajta sa modulom: '{novi_modul_naslov}'...")

    with open(HTML_FAJL, "r", encoding="utf-8") as f:
        sadrzaj = f.read()

    # HTML kod novog modula koji bot sam generiše i ubacuje u grid kartica
    timestamp = datetime.now().strftime("%d.%m.%Y. u %H:%M")
    novi_kod_kartice = f"""
            <div class="card" style="border-color: #a855f7; box-shadow: 0 0 20px rgba(168, 85, 247, 0.3);">
                <div class="icon">🚀</div>
                <h3>{novi_modul_naslov}</h3>
                <p>{opis_modula}</p>
                <div style="margin-top: 15px; font-size: 0.8rem; color: #a855f7; font-weight: bold;">[AUTO-GENERISANO OD STRANE AGENTA: {timestamp}]</div>
            </div>
    """

    # Tražimo gde se završava grid kartica i ubacujemo naš novi auto-upgrade modul
    # Bot automatski lepi novu karticu u postojeći dizajn sajta
    if "</div>" in sadrzaj:
        # Ubacujemo pre poslednjeg dela stranice ili unutar grid-a
        sadrzaj_izmenjen = sadrzaj.replace('</div>\n\n        <!-- TABELA', f'{novi_kod_kartice}\n        </div>\n\n        <!-- TABELA')
        
        with open(HTML_FAJL, "w", encoding="utf-8") as f:
            f.write(sadrzaj_izmenjen)
            
        print(f"[USPEH] Sajt je uspešno nadograđen! Novi modul je dodat i sačuvan u {HTML_FAJL}.")
    else:
        print("[GREŠKA] Struktura HTML-a nije prepoznala mesto za ubacivanje.")

if __name__ == "__main__":
    # 1. Prvo proveravamo da li je sajt zdrav
    if proveri_sajt():
        # 2. Bot samostalno vrši upgrade i ubacuje novu moćnu funkciju u hodu!
        auto_upgrade_sajta(
            "AI Autonomous Core V2", 
            "Modul dodat automatski od strane agenta. Prati performanse u realnom vremenu, optimizuje resurse i automatski osvežava sistem."
        )
        
        # 3. Ponovo proveravamo sajt nakon izmena
        print("\n[AGENT // RE-TEST] Testiram sajt nakon izvršenog upgrade-a...")
        proveri_sajt()