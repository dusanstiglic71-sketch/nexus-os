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
    alert.geometry("500x350")
    alert.configure(fg_color=BG_COLOR)
    alert.attributes("-topmost", True)
    
    ctk.CTkLabel(alert, text=naslov, font=ctk.CTkFont(size=20, weight="bold"), text_color=ACCENT_COLOR).pack(pady=(20, 10))
    t_box = ctk.CTkTextbox(alert, width=450, height=200, fg_color=CARD_COLOR, text_color=TEXT_MAIN, font=ctk.CTkFont(size=14))
    t_box.pack(padx=20, pady=5)
    t_box.insert("0.0", tekst)
    t_box.configure(state="disabled")
    ctk.CTkButton(alert, text="Zatvori", width=150, height=35, fg_color=ACCENT_COLOR, hover_color=HOVER_COLOR, command=alert.destroy).pack(pady=10)

def moderni_unos(naslov, tekst):
    dialog = ctk.CTkInputDialog(text=tekst, title=naslov)
    return dialog.get_input()

# --- LOGIN SISTEM ---
korisnik_ime = "Dušan"
korisnik_pin = "1234"

try:
    with open(CONFIG_FAJL, "r") as f:
        podaci = json.load(f)
        korisnik_ime = podaci.get("ime", "Dušan")
        korisnik_pin = podaci.get("pin", "1234")
except: pass

pin_odobren = False
login_app = ctk.CTk()
login_app.title("NEXUS OS - Autentifikacija")
login_app.geometry("380x450")
login_app.configure(fg_color=BG_COLOR)

ctk.CTkLabel(login_app, text=f"Sistem spreman, {korisnik_ime}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(60, 5))
ctk.CTkLabel(login_app, text="Unesite Master PIN", text_color=TEXT_MUTED).pack(pady=(0, 40))

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
root.title("NEXUS OS - V5.0 Expansion")
root.geometry("900x750")
root.configure(fg_color=BG_COLOR)

def pozovi_u_pozadini(funkcija, *args):
    threading.Thread(target=funkcija, args=args, daemon=True).start()

def opcija_kalistenika():
    zgibovi = moderni_unos("Trening", "Broj zgibova:")
    if not zgibovi: return
    propadanja = moderni_unos("Trening", "Broj propadanja:")
    sklekovi = moderni_unos("Trening", "Broj sklekova:")
    moderni_alert("Trening Upisan", f"Uspisano:\nZgibovi: {zgibovi}\nPropadanja: {propadanja}\nSklekovi: {sklekovi}\n\nMišići su napumpani. Vreme je za šejk!")

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
header_frame.pack(fill="x", padx=40, pady=(30, 10))
vreme_tekst = datetime.datetime.now().strftime("%d. %b %Y.")
ctk.CTkLabel(header_frame, text=f"Komandni Centar V5", font=ctk.CTkFont(size=32, weight="bold")).pack(anchor="w")
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
napravi_karticu(grid_frame, "🏋️", "Trening", "Snimi zgibove, propadanja, sklekove.", opcija_kalistenika, 0, 1)
napravi_karticu(grid_frame, "📱", "Mreže", "Pregledi i skokovi na TikToku.", opcija_mreze, 0, 2)

# Red 2
napravi_karticu(grid_frame, "⚽", "Partizan", "Crno-beli radar za uživo vesti.", opcija_vesti, 1, 0)
napravi_karticu(grid_frame, "🔐", "Sef", "Kriptovane šifre u bazi.", otvori_sef, 1, 1)
napravi_karticu(grid_frame, "💰", "Berza", "Skeniraj tržište kriptovaluta.", opcija_kurs, 1, 2)

# Red 3 (Sistemski alati)
napravi_karticu(grid_frame, "🧹", "Boost OS", "Očisti đubre i ubrzaj laptop.", optimizuj_laptop, 2, 0)

root.mainloop()