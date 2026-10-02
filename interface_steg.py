import customtkinter as ctk
from tkinter import filedialog
import os
import steganographie as steg 
import polybe as poly
import vigenere as vige
import playfair as plf

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Projet ISEC - Cryptographie & Stéganographie")
        self.geometry("1100x700")
        ctk.set_appearance_mode("light")
        
        self.purple_main = "#5a32fa"
        self.selected_algo = "Polybe"
        self.image_path = None

        # --- NAVIGATION ---
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=50, pady=(20, 10))
        self.btn_stegano = ctk.CTkButton(self.nav_frame, text="📷 Stéganographie", command=self.show_stegano_view)
        self.btn_stegano.pack(side="left", expand=True, fill="x", padx=5)
        self.btn_crypto = ctk.CTkButton(self.nav_frame, text="🔒 Chiffrements", command=self.show_crypto_view)
        self.btn_crypto.pack(side="left", expand=True, fill="x", padx=5)

        self.stegano_view = ctk.CTkFrame(self, fg_color="transparent")
        self.crypto_view = ctk.CTkFrame(self, fg_color="transparent")
        self.setup_stegano_ui()
        self.setup_crypto_ui()
        self.show_stegano_view()

    def show_stegano_view(self):
        self.crypto_view.pack_forget()
        self.stegano_view.pack(fill="both", expand=True)
        self.btn_stegano.configure(fg_color=self.purple_main)
        self.btn_crypto.configure(fg_color="white", text_color="black")

    def show_crypto_view(self):
        self.stegano_view.pack_forget()
        self.crypto_view.pack(fill="both", expand=True)
        self.btn_crypto.configure(fg_color=self.purple_main)
        self.btn_stegano.configure(fg_color="white", text_color="black")

    def setup_stegano_ui(self):
        container = ctk.CTkFrame(self.stegano_view, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=20)
        left = ctk.CTkFrame(container); left.pack(side="left", expand=True, fill="both", padx=10)
        self.label_img_status = ctk.CTkLabel(left, text="Aucune image sélectionnée")
        self.label_img_status.pack(pady=10)
        ctk.CTkButton(left, text="Sélectionner une image", command=self.choisir_image).pack(expand=True)

        right = ctk.CTkFrame(container); right.pack(side="left", expand=True, fill="both", padx=10)
        self.stegano_text = ctk.CTkTextbox(right, height=150); self.stegano_text.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(right, text="🔒 Cacher", command=self.action_cacher).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(right, text="🔓 Extraire", command=self.action_extraire).pack(fill="x", padx=15, pady=5)

    def setup_crypto_ui(self):
        self.cards_frame = ctk.CTkFrame(self.crypto_view, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=40, pady=10)
        for algo in ["Polybe", "Playfair", "Vigenère"]:
            ctk.CTkButton(self.cards_frame, text=algo, fg_color="white", text_color="black", command=lambda a=algo: self.select_algo(a)).pack(side="left", expand=True, fill="both", padx=10)

        self.box = ctk.CTkFrame(self.crypto_view, fg_color="white", corner_radius=15)
        self.box.pack(fill="both", expand=True, padx=50, pady=20)
        self.algo_title = ctk.CTkLabel(self.box, text="Chiffrement de Polybe", font=("bold", 18))
        self.algo_title.pack(pady=10)
        self.crypto_input = ctk.CTkTextbox(self.box, height=200); self.crypto_input.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkButton(self.box, text="🔒 Exécuter", command=self.executer_chiffrement).pack(pady=15)

    def select_algo(self, algo):
        self.selected_algo = algo
        self.algo_title.configure(text=f"Chiffrement de {algo}")

    def choisir_image(self):
        path = filedialog.askopenfilename(filetypes=[("PNG", "*.png")])
        if path:
            self.image_path = path
            self.label_img_status.configure(text=os.path.basename(path))

    def action_cacher(self):
        msg = self.stegano_text.get("0.0", "end").strip()
        save_path = filedialog.asksaveasfilename(defaultextension=".png")
        if self.image_path and msg and save_path:
            steg.cacher_message(self.image_path, msg, save_path)
            self.stegano_text.delete("0.0", "end")
            self.stegano_text.insert("0.0", "Message caché !")

    def action_extraire(self):
        if self.image_path:
            res = steg.extraire_message(self.image_path)
            self.stegano_text.delete("0.0", "end")
            self.stegano_text.insert("0.0", res if res else "Aucun message trouvé.")

    def executer_chiffrement(self):
        txt = self.crypto_input.get("0.0", "end").strip()
        if self.selected_algo == "Polybe": res = poly.chiffre_polybe(txt)
        elif self.selected_algo == "Vigenère": res = vige.chiffre_vigenere(txt, 'project')
        else: res = plf.chiffre_playfair(txt, 'jeux')
        self.crypto_input.delete("0.0", "end"); self.crypto_input.insert("0.0", res)

if __name__ == "__main__":
    app = App(); app.mainloop()