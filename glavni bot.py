import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from plyer import notification
import requests
from bs4 import BeautifulSoup
import warnings
import subprocess
import tkinter as tk
import json
from cryptography.fernet import Fernet
import ctypes
import keyboard
import customtkinter as ctk
import threading

warnings.filterwarnings("ignore")

# --- PODEŠAVANJA MODERNOG DIZAJNA ---
ctk.set_appearance_mode("dark")
BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
ACCENT_COLOR = "#3b82f6"
HOVER_COLOR = "#2563eb"
TEXT_MAIN = "#f8fafc"
TEXT_MUTED = "#94a3b8"

FAJL_KLJUCA = "kljuc.key"
FAJL_SEFA = "tajni_sef.xlsx"
CONFIG_FAJL = "config.json"
FAJL_PRODAJE = "nexus_prodaja.xlsx"
FAJL_ZA_SAJT = "prodaja.json"

# --- INICIJALIZACIJA SIGURNOSTI ---
def ucitaj_ili_kreiraj_kljuc():
    if not os.path.exists(FAJL_KLJUCA):
        kljuc = Fernet.generate_key()
        with open(FAJL_KLJUCA, "wb") as f_kljuc: f_kljuc.write(kljuc)
    else:
        with open(FAJL_KLJUCA, "rb") as f_kljuc: kljuc = f_kljuc.read()
    return kljuc

KLJUC = ucitaj_ili_kreiraj_kljuc()
CIPHER = Fernet(KLJUC)

def bot_kaze(tekst):
    def govor():
        try:
            t = str(tekst).replace('"', '').replace("'", "")
            cmd = f"Add-Type -AssemblyName System.speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{t}')"
            subprocess.run(["powershell", "-Command", cmd], creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass
    threading.Thread(target=govor, daemon=True).start()

def moderni_alert(naslov, tekst):
    alert = ctk.CTkToplevel()
    alert.title(naslov)
    alert.geometry("540x400")
    alert.configure(fg_color=BG_COLOR)
    alert.attributes("-topmost", True)
    
    ctk.CTkLabel(alert, text=naslov, font=ctk.CTkFont(size=20, weight="bold"), text_color=ACCENT_COLOR).pack(pady=(20, 10))
    t_box = ctk.CTkTextbox(alert, width=480, height=230, fg_color=CARD_COLOR, text_color=TEXT_MAIN, font=ctk.CTkFont(size=13))
    t_box.pack(padx=20, pady=5)
    t_box.insert("0.0", tekst)
    t_box.configure(state="disabled")
    ctk.CTkButton(alert, text="Zatvori", width=150, height=35, fg_color=ACCENT_COLOR, hover_color=HOVER_COLOR, command=alert.destroy).pack(pady=10)

def moderni_unos(naslov, tekst):
    dialog = ctk.CTkInputDialog(text=tekst, title=naslov)
    return dialog.get_input()

# --- LOGIN SISTEM ---
korisnik_ime = "Dušan Štiglic"
korisnik_pin = "1234"

try:
    with open(CONFIG_FAJL, "r") as f:
        podaci = json.load(f)
        korisnik_ime = podaci.get("ime", "Dušan Štiglic")
        korisnik_pin = podaci.get("pin", "1234")
except: pass

pin_odobren = False
login_app = ctk.CTk()
login_app.title("NEXUS OS - Autentifikacija")
login_app.geometry("380x450")
login_app.configure(fg_color=BG_COLOR)

ctk.CTkLabel(login_app, text=f"Sistem spreman,\n{korisnik_ime}", font=ctk.CTkFont(size=20, weight="bold"), justify="center").pack(pady=(50, 5))
ctk.CTkLabel(login_app, text="Unesite Master PIN", text_color=TEXT_MUTED).pack(pady=(0, 30))

unos_pin = ctk.CTkEntry(login_app, placeholder_text="••••", show="*", width=220, height=50, font=ctk.CTkFont(size=24, weight="bold"), justify="center", fg_color=CARD_COLOR, border_width=0)
unos_pin.pack(pady=20)
greska_label = ctk.CTkLabel(login_app, text="", text_color="#ef4444")
greska_label.pack(pady=5)

def proveri_pin(event=None):
    global pin_odobren
    if unos_pin.get() == korisnik_pin:
        pin_odobren = True
        login_app.destroy()
    else:
        unos_pin.delete(0, tk.END)
        greska_label.configure(text="Pristup odbijen.")

unos_pin.bind('<Return>', proveri_pin)
ctk.CTkButton(login_app, text="Pristupi", width=220, height=45, fg_color=ACCENT_COLOR, hover_color=HOVER_COLOR, command=proveri_pin).pack(pady=10)
login_app.mainloop()

if not pin_odobren: exit()

# --- GLAVNI SISTEM ---
root = ctk.CTk()
root.title("NEXUS OS - V5.0 Enterprise Core")
root.geometry("950x780")
root.configure(fg_color=BG_COLOR)

def pozovi_u_pozadini(funkcija, *args):
    threading.Thread(target=funkcija, args=args, daemon=True).start()

def opcija_kalistenika():
    zgibovi = moderni_unos("Trening", "Broj zgibova:")
    if not zgibovi: return
    propadanja = moderni_unos("Trening", "Broj propadanja:")
    sklekovi = moderni_unos("Trening", "Broj sklekova:")
    moderni_alert("Trening Upisan", f"Upisano:\nZgibovi: {zgibovi}\nPropadanja: {propadanja}\nSklekovi: {sklekovi}\n\nMišići su napumpani. Vreme je za šejk!")

# SEZONA I BAKŠIŠ
def opcija_sezona():
    danas = datetime.date.today()
    oktobar = datetime.date(2026, 10, 1)
    dani_do_kraja = (oktobar - danas).days
    
    baksis = moderni_unos("Bife Smene", "Koliko si evra bakšiša uzeo danas?")
    if not baksis: return
    
    datum = datetime.datetime.now().strftime("%Y-%m-%d")
    df_novi = pd.DataFrame([{"Datum": datum, "Bakšiš (€)": float(baksis)}])
    putanja = "Sezona_Baksis.xlsx"
    baza = pd.concat([pd.read_excel(putanja), df_novi], ignore_index=True) if os.path.exists(putanja) else df_novi
    baza.to_excel(putanja, index=False)
    
    ukupno = baza['Bakšiš (€)'].sum()
    
    izvestaj = f"⏳ DANA DO POVRATKA U SRBIJU: {dani_do_kraja} dana!\n\n"
    izvestaj += f"💵 Današnji bakšiš: {baksis} €\n"
    izvestaj += f"💰 UKUPNO ZARAĐENO NA BIFEU: {ukupno} €\n\nSamo jako, sezona se bliži kraju!"
    moderni_alert("Sezonski Trezor", izvestaj)

# --- SISTEM NAPLATE, AUTOMATSKE ISPORUKE I POVEZIVANJA SA SAJTOM ---
def opcija_paketi():
    prozor_paketi = ctk.CTkToplevel(root)
    prozor_paketi.title("NEXUS OS - Modul za Naplatu i Sajt Sinhronizaciju")
    prozor_paketi.geometry("520x550")
    prozor_paketi.configure(fg_color=BG_COLOR)
    prozor_paketi.attributes("-topmost", True)
    
    ctk.CTkLabel(prozor_paketi, text="🛒 NAPLATA I WEB SINHRONIZACIJA", font=ctk.CTkFont(size=20, weight="bold"), text_color=ACCENT_COLOR).pack(pady=(20, 5))
    ctk.CTkLabel(prozor_paketi, text="Autor: Dušan Štiglic | Automatski šalje podatke na sajt", text_color=TEXT_MUTED).pack(pady=(0, 15))
    
    info_tekst = (
        "[1] CORE MODUL (29€)\n"
        "    -> Osnovna optimizacija i Git repo.\n\n"
        "[2] ELITE SYSTEM (69€) [PREPORUČENO]\n"
        "    -> Cyberpunk dizajn, metrike i AI bot.\n\n"
        "[3] ENTERPRISE VIP (149€)\n"
        "    -> Custom kod, baze i 24/7 VIP podrška."
    )
    
    t_box = ctk.CTkTextbox(prozor_paketi, width=460, height=200, fg_color=CARD_COLOR, text_color=TEXT_MAIN, font=ctk.CTkFont(size=13))
    t_box.pack(padx=20, pady=5)
    t_box.insert("0.0", info_tekst)
    t_box.configure(state="disabled")
    
    ctk.CTkLabel(prozor_paketi, text="Unesi broj paketa za naplatu (1, 2 ili 3):", text_color=TEXT_MAIN).pack(pady=(15, 5))
    unos_izbora = ctk.CTkEntry(prozor_paketi, placeholder_text="npr. 2", width=200, height=35, justify="center", fg_color=CARD_COLOR, border_width=0)
    unos_izbora.pack(pady=5)
    
    def izvrsi_naplatu_i_sinhronizaciju():
        izbor = unos_izbora.get().strip()
        paketi_info = {
            "1": {"naziv": "Core Modul", "cena": 29, "isporuka": "Generisan Core ZIP paket sa čistom web arhitekturom."},
            "2": {"naziv": "Elite System", "cena": 69, "isporuka": "Generisan Elite sistem sa staklenim efektima i AI botom."},
            "3": {"naziv": "Enterprise VIP", "cena": 149, "isporuka": "Aktiviran VIP pristup bazama i custom skriptama."}
        }
        
        if izbor in paketi_info:
            p = paketi_info[izbor]
            datum = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # 1. Upis u Excel evidenciju prodaje
            df_novi = pd.DataFrame([{"Datum": datum, "Paket": p["naziv"], "Cena (€)": p["cena"], "Status": "Plaćeno & Ioručeno"}])
            baza = pd.concat([pd.read_excel(FAJL_PRODAJE), df_novi], ignore_index=True) if os.path.exists(FAJL_PRODAJE) else df_novi
            baza.to_excel(FAJL_PRODAJE, index=False)
            
            # 2. Generisanje JSON fajla za automatsko čitanje na web sajtu
            podaci_za_sajt = {
                "poslednji_kupac": p["naziv"],
                "cena": f"{p['cena']}€",
                "status": "Aktivirano & Ioručeno",
                "autor": "Dušan Štiglic",
                "vreme": datum
            }
            with open(FAJL_ZA_SAJT, "w", encoding="utf-8") as f_json:
                json.dump(podaci_za_sajt, f_json, ensure_ascii=False, indent=4)
            
            rezultat_poruka = (
                f"✅ UPLATA USPEŠNO OBRADJENA!\n\n"
                f"📦 Paket: {p['naziv']} ({p['cena']}€)\n"
                f"🌐 Status: Podaci automatski poslati na sajt (prodaja.json)\n\n"
                f"🚀 ISPORUKA:\n{p['isporuka']}\n\n"
                f"Sistem registrovao pod nadzorom: Dušan Štiglic."
            )
            bot_kaze(f"Uplata za {p['naziv']} je uspešno izvršena i poslata na sajt.")
            moderni_alert("Uspešna Sinhronizacija", rezultat_poruka)
            prozor_paketi.destroy()
        else:
            moderni_alert("Greška", "Unesi validan broj paketa (1, 2 ili 3).")

    ctk.CTkButton(prozor_paketi, text="Naplati, isporuči i pošalji na sajt", width=260, height=40, fg_color="#10b981", hover_color="#059669", command=izvrsi_naplatu_i_sinhronizaciju).pack(pady=15)

# GROBARSKI RADAR
def task_vesti():
    try:
        url = "https://news.google.com/rss/search?q=FK+Partizan&hl=sr&gl=RS&ceid=RS:sr"
        odgovor = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(odgovor.content, "html.parser")
        tekst_vesti = "⬛⬜ AKTIVIRAN GROBARSKI RADAR ⬜⬛\n\n"
        for i, vest in enumerate(soup.find_all("title")[2:7], 1):
            tekst_vesti += f"{i}. {vest.text.replace(' - Google vesti', '')}\n\n"
        root.after(0, lambda: moderni_alert("Partizan Live", tekst_vesti))
    except: root.after(0, lambda: moderni_alert("Greška", "Satelit nije dostupan."))

def opcija_vesti():
    bot_kaze("Skeniram crno bele vesti.")
    pozovi_u_pozadini(task_vesti)

def opcija_mreze():
    platforma = moderni_unos("Mreže", "Gde kačiš? (TikTok/IG):")
    if not platforma: return
    pregledi = moderni_unos("Mreže", "Broj pregleda:")
    datum = datetime.datetime.now().strftime("%Y-%m-%d")
    df_novi = pd.DataFrame([{"Datum": datum, "Platforma": platforma, "Pregledi": int(pregledi) if pregledi.isdigit() else 0}])
    putanja = f"Statistika_{platforma}.xlsx"
    baza = pd.concat([pd.read_excel(putanja), df_novi], ignore_index=True) if os.path.exists(putanja) else df_novi
    baza.to_excel(putanja, index=False)
    
    plt.figure(figsize=(8, 4))
    plt.style.use('dark_background')
    plt.plot(baza['Datum'], baza['Pregledi'], marker='o', color='#bc13fe', linewidth=2)
    plt.title(f"TikTok/IG Analitika: {platforma}", fontsize=14, color="white")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def otvori_sef():
    prozor_sef = ctk.CTkToplevel(root)
    prozor_sef.title("Tajni Trezor")
    prozor_sef.geometry("400x420")
    prozor_sef.configure(fg_color=BG_COLOR)
    prozor_sef.attributes("-topmost", True)
    
    ctk.CTkLabel(prozor_sef, text="🔐 Privatni Trezor", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)
    e_nalog = ctk.CTkEntry(prozor_sef, placeholder_text="Aplikacija", width=280, height=40, fg_color=CARD_COLOR, border_width=0)
    e_nalog.pack(pady=8)
    e_korisnik = ctk.CTkEntry(prozor_sef, placeholder_text="Korisničko ime", width=280, height=40, fg_color=CARD_COLOR, border_width=0)
    e_korisnik.pack(pady=8)
    e_sifra = ctk.CTkEntry(prozor_sef, placeholder_text="Lozinka", show="*", width=280, height=40, fg_color=CARD_COLOR, border_width=0)
    e_sifra.pack(pady=8)
        
    def sacuvaj_u_bazu():
        if not e_nalog.get() or not e_sifra.get(): return
        enkriptovano = CIPHER.encrypt(e_sifra.get().encode()).decode()
        df_novi = pd.DataFrame([{"Nalog": e_nalog.get(), "Korisnik": e_korisnik.get(), "Lozinka": enkriptovano}])
        baza = pd.concat([pd.read_excel(FAJL_SEFA), df_novi], ignore_index=True) if os.path.exists(FAJL_SEFA) else df_novi
        baza.to_excel(FAJL_SEFA, index=False)
        moderni_alert("Uspeh", "Podaci kriptovani.")
        e_nalog.delete(0, tk.END); e_korisnik.delete(0, tk.END); e_sifra.delete(0, tk.END)
            
    def pregledaj_lozinke():
        if not os.path.exists(FAJL_SEFA): return
        baza = pd.read_excel(FAJL_SEFA)
        tekst = ""
        for _, red in baza.iterrows():
            try: des = CIPHER.decrypt(red['Lozinka'].encode()).decode()
            except: des = "[GREŠKA]"
            tekst += f"📍 {red['Nalog']}\n👤 {red['Korisnik']}\n🔑 {des}\n\n"
        moderni_alert("Dekriptovani Podaci", tekst)

    ctk.CTkButton(prozor_sef, text="Sačuvaj u bazu", width=280, height=40, fg_color="#10b981", hover_color="#059669", command=sacuvaj_u_bazu).pack(pady=(20, 10))
    ctk.CTkButton(prozor_sef, text="Prikaži Lozinke", width=280, height=40, fg_color="#475569", hover_color="#334155", command=pregledaj_lozinke).pack(pady=5)

def task_kripto():
    try:
        odgovor = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()
        cena = odgovor['bpi']['USD']['rate']
        root.after(0, lambda: moderni_alert("💰 Tržište", f"Cena Bitcoina:\n\n$ {cena} USD"))
    except: pass

def opcija_kurs(): pozovi_u_pozadini(task_kripto)

def task_optimizacija():
    subprocess.run(["powershell", "-Command", "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    try: ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
    except: pass
    subprocess.run(["powershell", "-Command", "[System.GC]::Collect()"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    root.after(0, lambda: moderni_alert("🧹 Optimizacija", "C Disk je oslobođen i sistem ubrzan."))

def optimizuj_laptop(): pozovi_u_pozadini(task_optimizacija)

def panik_mod():
    subprocess.run(["powershell", "-Command", "(New-Object -ComObject Shell.Application).MinimizeAll()"], creationflags=subprocess.CREATE_NO_WINDOW)
    subprocess.run(["powershell", "-Command", "Set-Volume -Mute $true"], creationflags=subprocess.CREATE_NO_WINDOW)

keyboard.add_hotkey('ctrl+shift+x', panik_mod)

# --- UI KREIRANJE ---
header_frame = ctk.CTkFrame(root, fg_color="transparent")
header_frame.pack(fill="x", padx=40, pady=(25, 10))
vreme_tekst = datetime.datetime.now().strftime("%d. %b %Y.")
ctk.CTkLabel(header_frame, text=f"Komandni Centar V5 // Dušan Štiglic", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w")
ctk.CTkLabel(header_frame, text=f"Sistem Online | {vreme_tekst} | Panik taster: Ctrl+Shift+X", text_color=TEXT_MUTED).pack(anchor="w")

grid_frame = ctk.CTkFrame(root, fg_color="transparent")
grid_frame.pack(fill="both", expand=True, padx=30, pady=10)

def napravi_karticu(roditelj, ikona, naslov, opis, komanda, r, c, naglaseno=False):
    boja_kartice = "#1e40af" if naglaseno else CARD_COLOR
    card = ctk.CTkFrame(roditelj, corner_radius=16, fg_color=boja_kartice)
    card.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")
    top_frame = ctk.CTkFrame(card, fg_color="transparent")
    top_frame.pack(fill="x", padx=20, pady=(20, 5))
    ctk.CTkLabel(top_frame, text=ikona, font=ctk.CTkFont(size=26)).pack(side="left")
    ctk.CTkLabel(top_frame, text=naslov, font=ctk.CTkFont(size=17, weight="bold")).pack(side="left", padx=10)
    ctk.CTkLabel(card, text=opis, text_color=TEXT_MUTED if not naglaseno else "#cbd5e1", justify="left", wraplength=200).pack(anchor="w", padx=20, pady=5)
    ctk.CTkButton(card, text="Iniciraj", width=120, height=35, fg_color="#334155" if not naglaseno else "#0f172a", hover_color=ACCENT_COLOR, command=komanda).pack(anchor="w", padx=20, pady=(15, 20))

grid_frame.grid_columnconfigure((0, 1, 2), weight=1)

# Red 1
napravi_karticu(grid_frame, "⏳", "Sezona", "Prati smene, bakšiš i dane do povratka.", opcija_sezona, 0, 0, naglaseno=True)
napravi_karticu(grid_frame, "🛒", "Naplata & Sajt", "Naplati paket i pošalji podatke na web sajt.", opcija_paketi, 0, 1, naglaseno=True)
napravi_karticu(grid_frame, "🏋️", "Trening", "Snimi zgibove, propadanja, sklekove.", opcija_kalistenika, 0, 2)

# Red 2
napravi_karticu(grid_frame, "📱", "Mreže", "Pregledi i skokovi na TikToku.", opcija_mreze, 1, 0)
napravi_karticu(grid_frame, "⚽", "Partizan", "Crno-beli radar za uživo vesti.", opcija_vesti, 1, 1)
napravi_karticu(grid_frame, "🔐", "Sef", "Kriptovane šifre u bazi.", otvori_sef, 1, 2)

# Red 3 (Sistemski alati i berza)
napravi_karticu(grid_frame, "💰", "Berza", "Skeniraj tržište kriptovaluta.", opcija_kurs, 2, 0)
napravi_karticu(grid_frame, "🧹", "Boost OS", "Očisti đubre i ubrzaj laptop.", optimizuj_laptop, 2, 1)

root.mainloop()