# =====================================================================
# NEXUS_OS // ULTRA-ELITE ENTERPRISE GUI v11.2
# Klasa softvera: Vrhunski Cyberpunk Desktop Softver (100,000€+ arhitektura)
# Glavni Arhitekta i Vlasnik: Dušan Štiglic
# =====================================================================

import tkinter as tk
import time

class NexusEliteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXUS_OS // STIGLIC STUDIOĆ")
        self.root.geometry("1000x650")
        self.root.configure(bg="#030307")
        
        try:
            self.root.overrideredirect(True)
        except:
            pass

        self.current_tab = "dashboard"
        self.setup_ui()

    def setup_ui(self):
        self.main_container = tk.Frame(self.root, bg="#030307", highlightbackground="#00ffcc", highlightthickness=1)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        title_bar = tk.Frame(self.main_container, bg="#080812", height=45)
        title_bar.pack(fill=tk.X, side=tk.TOP)
        title_bar.pack_propagate(False)

        brand_lbl = tk.Label(
            title_bar, 
            text=" ⚡ STIGLIC STUDIOĆ // NEXUS_OS v11.2 [VIP ADMIN: DUŠAN ŠTIGLIC]", 
            fg="#00ffcc", 
            bg="#080812", 
            font=("Courier", 10, "bold")
        )
        brand_lbl.pack(side=tk.LEFT, padx=15)

        btn_close = tk.Button(
            title_bar, 
            text=" ✕ ", 
            command=self.root.destroy, 
            bg="#080812", 
            fg="#ff007f", 
            bd=0, 
            font=("Courier", 12, "bold"),
            activebackground="#ff007f",
            activeforeground="#fff"
        )
        btn_close.pack(side=tk.RIGHT, padx=10)

        nav_frame = tk.Frame(self.main_container, bg="#05050a", height=50)
        nav_frame.pack(fill=tk.X, side=tk.TOP)

        self.btn_dash = self.create_nav_button(nav_frame, "DASHBOARD", "dashboard", side=tk.LEFT)
        self.btn_render = self.create_nav_button(nav_frame, "AI RENDER CORE", "render", side=tk.LEFT)
        self.btn_clients = self.create_nav_button(nav_frame, "KLIJENTI & UGOVORI", "clients", side=tk.LEFT)

        self.content_frame = tk.Frame(self.main_container, bg="#030307")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.show_dashboard()

    def create_nav_button(self, parent, text, tab_name, side):
        btn = tk.Button(
            parent, 
            text=f"  {text}  ", 
            bg="#05050a", 
            fg="#8c8cbe", 
            bd=0,
            font=("Courier", 10, "bold"),
            activebackground="#0d0d16",
            activeforeground="#00ffcc",
            command=lambda: self.switch_tab(tab_name)
        )
        btn.pack(side=side, padx=5, pady=8)
        return btn

    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        
        for b in [self.btn_dash, self.btn_render, self.btn_clients]:
            b.config(fg="#8c8cbe", bg="#05050a")

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if tab_name == "dashboard":
            self.btn_dash.config(fg="#00ffcc", bg="#0d0d16")
            self.show_dashboard()
        elif tab_name == "render":
            self.btn_render.config(fg="#00ffcc", bg="#0d0d16")
            self.show_render()
        elif tab_name == "clients":
            self.btn_clients.config(fg="#00ffcc", bg="#0d0d16")
            self.show_clients()

    def show_dashboard(self):
        lbl = tk.Label(
            self.content_frame, 
            text="// KONTROLNI CENTAR U REALNOM VREMENU", 
            fg="#fff", 
            bg="#030307", 
            font=("Courier", 13, "bold")
        )
        lbl.pack(anchor=tk.W, pady=(0, 10))

        self.term_box = tk.Text(
            self.content_frame,
            bg="#06060c",
            fg="#00ffcc",
            insertbackground="white",
            font=("Courier", 10),
            bd=1,
            highlightbackground="#00ffcc",
            highlightthickness=1
        )
        self.term_box.pack(fill=tk.BOTH, expand=True, pady=5)
        self.term_box.insert(tk.END, "[SYS_BOOT] Inicijalizacija Stiglic Studioć servera...\n")
        self.term_box.insert(tk.END, "[SECURE] Veza sa render nodovima uspostavljena (0.1ms).\n")
        self.term_box.config(state=tk.DISABLED)

    def show_render(self):
        lbl = tk.Label(
            self.content_frame, 
            text="// AUTONOMNI AI RENDER ENGINE (90% AUTO-PILOT)", 
            fg="#fff", 
            bg="#030307", 
            font=("Courier", 13, "bold")
        )
        lbl.pack(anchor=tk.W, pady=(0, 15))

        btn_run = tk.Button(
            self.content_frame,
            text=" ⚡ POKRENI 8K AUTONOMNI RENDER ",
            bg="#00ffcc",
            fg="#030307",
            font=("Courier", 11, "bold"),
            bd=0,
            padx=20, pady=12,
            cursor="hand2",
            command=self.simulate_render
        )
        btn_run.pack(anchor=tk.W, pady=10)

        self.render_status_lbl = tk.Label(
            self.content_frame,
            text="Status: Spremno za obradu sirovog materijala...",
            fg="#8c8cbe",
            bg="#030307",
            font=("Courier", 11)
        )
        self.render_status_lbl.pack(anchor=tk.W, pady=15)

    def show_clients(self):
        lbl = tk.Label(
            self.content_frame, 
            text="// AKTIVNI KLIJENTI I FINANSIJSKA BAZA", 
            fg="#fff", 
            bg="#030307", 
            font=("Courier", 13, "bold")
        )
        lbl.pack(anchor=tk.W, pady=(0, 15))

        clients_data = [
            ("Klijent #4021", "Commercial VIP", "200€", "ISPORUČENO [100%]", "#00ffcc"),
            ("Klijent #4025", "YouTube Masterclass", "85€", "U RENDERU [90%]", "#ff007f"),
            ("Klijent #4030", "Short-Form TikTok", "25€", "SPREMNO ZA UPLOAD", "#00ffcc")
        ]

        for client, package, price, status, color in clients_data:
            card = tk.Frame(self.content_frame, bg="#080812", highlightbackground=color, highlightthickness=1)
            card.pack(fill=tk.X, pady=6, ipady=8, ipadx=10)

            c_lbl = tk.Label(card, text=f"{client} | {package} ({price})", fg="#fff", bg="#080812", font=("Courier", 10, "bold"))
            c_lbl.pack(side=tk.LEFT, padx=10)

            s_lbl = tk.Label(card, text=status, fg=color, bg="#080812", font=("Courier", 10, "bold"))
            s_lbl.pack(side=tk.RIGHT, padx=10)

    def simulate_render(self):
        self.render_status_lbl.config(text="Status: [U TOKU] Optimizacija frejmova i uklanjanje tišina...", fg="#ff007f")
        self.root.update()
        time.sleep(1.5)
        self.render_status_lbl.config(text="Status: [USPEH] 4K Video izrendan i sačuvan pod potpisom Dušana Štiglica!", fg="#00ffcc")

if __name__ == "__main__":
    root = tk.Tk()
    app = NexusEliteApp(root)
    root.mainloop()