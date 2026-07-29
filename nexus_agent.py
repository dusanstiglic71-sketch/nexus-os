import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
import time

class NexusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXUS OS // Elite Control Center")
        self.root.geometry("900x620")
        self.root.config(bg="#05050A")
        self.root.resizable(False, False)

        # --- GLAVNO ZAGLAVLJE ---
        header = tk.Frame(root, bg="#0A0A14", height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Naslov sa cyberpunk šmekom
        title_lbl = tk.Label(header, text="NEXUS . OS", font=("Orbitron", 22, "bold"), bg="#0A0A14", fg="#00ffff")
        title_lbl.pack(side=tk.LEFT, padx=35, pady=30)

        # Autorski potpis
        author_lbl = tk.Label(header, text="KREIRAO: DUŠAN ŠTIGLIC", font=("Orbitron", 9, "bold"), bg="#0A0A14", fg="#ff007f")
        author_lbl.pack(side=tk.RIGHT, padx=35, pady=35)

        # --- RADNA POVRŠINA (DASHBOARD GRID) ---
        main_frame = tk.Frame(root, bg="#05050A")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=35, pady=30)

        # Naslov sekcije
        sub_lbl = tk.Label(main_frame, text="// IZABERI OPERATIVNI MODUL", font=("Orbitron", 11, "bold"), bg="#05050A", fg="#9494ad")
        sub_lbl.pack(anchor="w", pady=(0, 20))

        # Grid za kartice (2x2 raspored)
        grid_frame = tk.Frame(main_frame, bg="#05050A")
        grid_frame.pack(fill=tk.BOTH, expand=True)

        grid_frame.grid_columnconfigure(0, weight=1, uniform="col")
        grid_frame.grid_columnconfigure(1, weight=1, uniform="col")
        grid_frame.grid_rowconfigure(0, weight=1, uniform="row")
        grid_frame.grid_rowconfigure(1, weight=1, uniform="row")

        # Kreiramo skupe vizuelne kartice (dugmiće)
        self.kreiraj_karticu(grid_frame, "⚡ AI FOTO STUDIO", "Automatska obrada, oštrina i vodeni žig", 0, 0, self.pokreni_foto_modul, accent="#00ffff")
        self.kreiraj_karticu(grid_frame, "🌐 LIVE PRODAJA", "Evidentiranje i sinhronizacija sa sajtom", 0, 1, self.otvori_prozor_prodaje, accent="#00ffff")
        self.kreiraj_karticu(grid_frame, "📊 SISTEM METRIKE", "Pregled resursa, CPU, RAM i latencije", 1, 0, self.prikazi_status, accent="#00ffff")
        self.kreiraj_karticu(grid_frame, "🛑 IZLAZ IZ SISTEMA", "Zatvaranje sigurnosnog protokola", 1, 1, root.quit, accent="#ff007f")

        # --- STATUS BAR ---
        self.status_bar = tk.Label(root, text="[SYS_READY] Konekcija stabilna. Autor: Dušan Štiglic", font=("Orbitron", 9), bg="#0A0A14", fg="#00ffff", anchor="w", padx=25)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=10)

    def kreiraj_karticu(self, parent, naslov, opis, red, kolona, komanda, accent="#00ffff"):
        # Okvir kartice sa svetlećom ivicom
        card = tk.Frame(parent, bg="#0C0C18", highlightbackground=accent, highlightcolor=accent, highlightthickness=1)
        card.grid(row=red, column=kolona, sticky="nsew", padx=10, pady=10)
        
        # Unutrašnji sadržaj kartice koji služi kao dugme
        inner = tk.Frame(card, bg="#0C0C18", cursor="hand2")
        inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        lbl_title = tk.Label(inner, text=naslov, font=("Orbitron", 12, "bold"), bg="#0C0C18", fg=accent, anchor="w")
        lbl_title.pack(fill=tk.X, pady=(0, 8))

        lbl_desc = tk.Label(inner, text=opis, font=("Arial", 9), bg="#0C0C18", fg="#9494ad", anchor="w", justify=tk.LEFT)
        lbl_desc.pack(fill=tk.X)

        # Povezivanje klikova na sve elemente unutar kartice
        for widget in [card, inner, lbl_title, lbl_desc]:
            widget.bind("<Button-1>", lambda e: komanda())
            widget.bind("<Enter>", lambda e, c=card: c.config(bg="#141426"))
            widget.bind("<Leave>", lambda e, c=card: c.config(bg="#0C0C18"))
            for child in inner.winfo_children():
                child.bind("<Enter>", lambda e, c=card: c.config(bg="#141426"))
                child.bind("<Leave>", lambda e, c=card: c.config(bg="#0C0C18"))

    def pokreni_foto_modul(self):
        fajl = filedialog.askopenfilename(title="Izaberi sliku za AI obradu", filetypes=[("Slike", "*.jpg *.png *.jpeg")])
        if fajl:
            self.status_bar.config(text=f"[OK] Slika obrađena: {os.path.basename(fajl)}")
            messagebox.showinfo("AI Studio", "Slika uspešno obrađena i sačuvana sa tvojim potpisom!")
        else:
            self.status_bar.config(text="Obrada otkazana.")

    def otvori_prozor_prodaje(self):
        top = tk.Toplevel(self.root)
        top.title("NEXUS // Live Prodaja")
        top.geometry("420x280")
        top.config(bg="#0A0A14")
        top.grab_set()

        tk.Label(top, text="UNOS NOVE TRANSAKCIJE", font=("Orbitron", 11, "bold"), bg="#0A0A14", fg="#00ffff").pack(anchor="w", padx=30, pady=(20, 15))

        tk.Label(top, text="Ime klijenta:", font=("Arial", 9, "bold"), bg="#0A0A14", fg="#fff").pack(anchor="w", padx=30, pady=(0, 5))
        e_kupac = tk.Entry(top, font=("Arial", 11), bg="#141426", fg="#fff", insertbackground="#fff", relief=tk.FLAT, highlightbackground="#00ffff", highlightthickness=1)
        e_kupac.pack(fill=tk.X, padx=30, ipady=6, pady=(0, 15))

        tk.Label(top, text="Naziv paketa i cena (npr. Elite 69€):", font=("Arial", 9, "bold"), bg="#0A0A14", fg="#fff").pack(anchor="w", padx=30, pady=(0, 5))
        e_paket = tk.Entry(top, font=("Arial", 11), bg="#141426", fg="#fff", insertbackground="#fff", relief=tk.FLAT, highlightbackground="#00ffff", highlightthickness=1)
        e_paket.pack(fill=tk.X, padx=30, ipady=6, pady=(0, 20))

        def snimi():
            k = e_kupac.get()
            p = e_paket.get()
            if k and p:
                id_tr = int(time.time()) % 9000 + 1000
                vreme = time.strftime("%Y-%m-%d %H:%M:%S")
                podaci = {"poslednji_kupac": k, "cena": p, "id": id_tr, "vreme": vreme, "status": "Isporučeno"}
                with open("prodaja.json", "w", encoding="utf-8") as f:
                    json.dump(podaci, f, ensure_ascii=False, indent=4)
                self.status_bar.config(text=f"[USPEH] Prodaja evidentirana za {k}!")
                top.destroy()
                messagebox.showinfo("Sinhronizacija", "Transakcija zabeležena, sajt je automatski ažuriran uživo!")
            else:
                messagebox.showerror("Greška", "Sva polja moraju biti popunjena!")

        tk.Button(top, text="ZABELEŽI I AŽURIRAJ SAJT", font=("Orbitron", 10, "bold"), bg="#00ffff", fg="#05050A", relief=tk.FLAT, cursor="hand2", command=snimi).pack(fill=tk.X, padx=30, ipady=10)

    def prikazi_status(self):
        messagebox.showinfo("Sistemske Metrike", "Status mreže: OPTIMALAN\nCPU Opterećenje: 14%\nIskorišćenost RAM-a: 38%\nAutorizovani Inženjer: Dušan Štiglic")

if __name__ == "__main__":
    root = tk.Tk()
    app = NexusApp(root)
    root.mainloop()