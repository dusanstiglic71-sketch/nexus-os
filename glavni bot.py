import os
import time
import sys
import random

# Komanda za napredne RGB boje u Windows terminalu
os.system('color')

def animacija_kucanja(tekst, brzina=0.03):
    """Pravi onaj hakerski efekat kucanja slovo po slovo"""
    for slovo in tekst:
        sys.stdout.write(slovo)
        sys.stdout.flush()
        time.sleep(brzina)
    print()

def boot_sekvenca():
    """Filmsko učitavanje sistema pri paljenju bota"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\033[90m[SYS] POKRETANJE NEXUS KERNELA...\033[0m\n")
    time.sleep(0.5)
    
    moduli = [
        "Inicijalizacija AI modula za obradu slika",
        "Uspostavljanje bezbedne konekcije sa serverom",
        "Učitavanje baze klijenata i ključeva",
        "Kalibracija vizuelnog interfejsa"
    ]
    
    for modul in moduli:
        sys.stdout.write(f"\033[38;2;0;255;204m[*]\033[0m \033[97m{modul}...\033[0m")
        sys.stdout.flush()
        time.sleep(random.uniform(0.3, 0.8))
        print(" \033[32m[OK]\033[0m")
        
    print("\n\033[90mKompajliranje radnog okruženja:\033[0m")
    for i in range(1, 101, 2):
        bar = "█" * (i // 5) + "░" * (20 - (i // 5))
        sys.stdout.write(f"\r\033[38;2;255;0;127m[{bar}] {i}%\033[0m")
        sys.stdout.flush()
        time.sleep(0.015)
        
    print("\n\n\033[38;2;0;255;204m[USPEH] NEXUS OS JE SPREMAN ZA RAD.\033[0m")
    time.sleep(1)

def prikazi_interfejs():
    """Generiše podeljeni ekran sa menijem i metrikama sistema"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Generisanje uverljivih sistemskih metrika
    cpu = f"{random.randint(12, 45)}%"
    ram = f"{random.randint(30, 65)}%"
    ping = f"{random.randint(8, 24)}ms"
    
    print("\033[38;2;0;255;204m")
    print(" ╔════════════════════════════════════════════════════════════════════════════╗")
    print(" ║  ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗     ██████╗ ███████╗          ║")
    print(" ║  ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝    ██╔═══██╗██╔════╝          ║")
    print(" ║  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗    ██║   ██║███████╗          ║")
    print(" ║  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║    ██║   ██║╚════██║          ║")
    print(" ║  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║    ╚██████╔╝███████║          ║")
    print(" ║  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝     ╚═════╝ ╚══════╝          ║")
    print(" ╠════════════════════════════════════════════╦═══════════════════════════════╣")
    print(" ║  \033[97mKONTROLNI MENI:\033[38;2;0;255;204m                           ║  \033[97mSISTEMSKE METRIKE:\033[38;2;0;255;204m           ║")
    print(" ║                                            ║                               ║")
    print(f" ║  \033[38;2;0;255;204m[1]\033[0m \033[97mPokreni Elite AI Foto Modul\033[38;2;0;255;204m           ║  \033[90mCPU Upotreba:\033[0m \033[97m{cpu.ljust(5)}\033[38;2;0;255;204m           ║")
    print(f" ║  \033[38;2;0;255;204m[2]\033[0m \033[97mEvidentiraj prodaju na sajtu\033[38;2;0;255;204m          ║  \033[90mRAM Memorija:\033[0m \033[97m{ram.ljust(5)}\033[38;2;0;255;204m           ║")
    print(f" ║  \033[38;2;0;255;204m[3]\033[0m \033[97mKonekcija sa bazom klijenata\033[38;2;0;255;204m          ║  \033[90mServer Ping:\033[0m  \033[97m{ping.ljust(5)}\033[38;2;0;255;204m           ║")
    print(" ║                                            ║  \033[90mNet Status:\033[0m   \033[32mSECURE\033[38;2;0;255;204m         ║")
    print(" ║  \033[38;2;255;0;127m[4]\033[0m \033[90mIsključi i dekriptuj sistem\033[38;2;0;255;204m           ║  \033[90mAutor:\033[0m        \033[97mDušan Štiglic\033[38;2;0;255;204m  ║")
    print(" ╚════════════════════════════════════════════╩═══════════════════════════════╝\033[0m")

def glavni_meni():
    # Pokrećemo boot sekvencu samo jednom pri paljenju
    boot_sekvenca()
    
    while True:
        prikazi_interfejs()
        
        # Oštra, profesionalna komandna linija
        izbor = input("\n\033[90m  sys@nexus\033[0m:\033[38;2;0;255;204m~\033[0m$ ")
        
        if izbor == '4':
            animacija_kucanja("\n\033[90m  Zatvaranje sigurnosnih protokola i gašenje sistema...\033[0m", 0.04)
            time.sleep(1)
            break
        elif izbor in ['1', '2', '3']:
            print(f"\n\033[38;2;0;255;204m  [OK] Inicijalizacija modula '{izbor}'...\033[0m")
            time.sleep(1.5)
        else:
            print("\n\033[38;2;255;0;127m  [!] Komanda nije prepoznata. Odbijeno.\033[0m")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        glavni_meni()
    except KeyboardInterrupt:
        # Sakriva ružne greške ako slučajno ugasiš bot preko Ctrl+C
        print("\n\n\033[38;2;255;0;127m  [!] Nasilno gašenje detektovano. Terminal isključen.\033[0m")
        sys.exit()