import tkinter as tk
import base64
import unicodedata

okno = tk.Tk()
okno.title("Šifrovací a dešifrovací aplikace (Česká edice)")
okno.geometry("1080x1000")
okno.attributes("-alpha", 0.9)
okno.configure(bg="#000000")

ZELENA = "#00FF00"      
TMAVA_ZELENA = "#002200"      
CERNA_ZELENA = "#000a00"     
ZELENA_NAJETI = "#003300"      
STIN = "#003300"      
RAMECEK = "#00FF00"      

HLAVNI_PISMO = ("Consolas", 12, "bold")

CESKA_ABECEDA = "aábcčdďeéěfghiíjklmnňoópqrřsštťuúůvwxyýzž"
CESKA_ABECEDA_VELKA = CESKA_ABECEDA.upper()

MORSE_SLOVNIK = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', 
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', 
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', 
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', 
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', 
    '--..': 'Z', '----': 'CH', 
    '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', 
    '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0'
}
OBRACENY_MORSE_SLOVNIK = {h: k for k, h in MORSE_SLOVNIK.items()}

def vymaz_pole():
    if 'vstupni_pole' in globals() and 'vystupni_pole' in globals():
        vstupni_pole.delete("1.0", tk.END)
        vystupni_pole.delete("1.0", tk.END)

def odstran_diakritiku(text):
    return "".join(z for z in unicodedata.normalize('NFD', text) if unicodedata.category(z) != 'Mn').upper()

def oprav_diakritiku(udalost):
    
    if udalost.keysym in ('Up', 'Down', 'Left', 'Right', 'BackSpace', 'Delete'):
        return
        
    textove_pole = udalost.widget
    
    try:
        kurzor = textove_pole.index(tk.INSERT)
        radek, sloupec = map(int, kurzor.split('.'))
        
        
        start_sloupec = max(0, sloupec - 5)
        start_index = f"{radek}.{start_sloupec}"
        
        text_k_oprave = textove_pole.get(start_index, kurzor)
        
        
        opraveny_text = unicodedata.normalize('NFC', text_k_oprave)
        
        
        slovnik_oprav = {
            "ˇc": "č", "ˇC": "Č", "ˇd": "ď", "ˇD": "Ď", "ˇe": "ě", "ˇE": "Ě",
            "ˇn": "ň", "ˇN": "Ň", "ˇr": "ř", "ˇR": "Ř", "ˇs": "š", "ˇS": "Š",
            "ˇt": "ť", "ˇT": "Ť", "ˇz": "ž", "ˇZ": "Ž",
            "´a": "á", "´A": "Á", "´e": "é", "´E": "É", "´i": "í", "´I": "Í",
            "´o": "ó", "´O": "Ó", "´u": "ú", "´U": "Ú", "´y": "ý", "´Y": "Ý",
            "°u": "ů", "°U": "Ů"
        }
        
        for klic, hodnota in slovnik_oprav.items():
            opraveny_text = opraveny_text.replace(klic, hodnota)
            
        
        if opraveny_text != text_k_oprave:
            textove_pole.delete(start_index, kurzor)
            textove_pole.insert(start_index, opraveny_text)
            
    except Exception:
        pass

def zpracuj_akci():
    vstupni_text = vstupni_pole.get("1.0", tk.END).strip()
    vybrana_sifra = promenna_sifry.get()
    je_sifrovani = (promenna_hlavniho_rezimu.get() == "sifrovat")
    hodnota_klice = vstup_klice.get()
    
    vystupni_pole.delete("1.0", tk.END)
    if not vstupni_text: 
        return

    if vybrana_sifra == "pismena_pozpatku":
        vystupni_pole.insert(tk.END, vstupni_text[::-1])
        
    elif vybrana_sifra == "slova_pozpatku":
        vystupni_pole.insert(tk.END, " ".join(vstupni_text.split()[::-1]))

    elif vybrana_sifra == "caesar":
        try: 
            posun = int(hodnota_klice)
        except ValueError: 
            vystupni_pole.insert(tk.END, "[CHYBA] Klíč musí být číslo!")
            return
            
        vysledek = ""
        for znak in vstupni_text:
            if znak in CESKA_ABECEDA:
                index = (CESKA_ABECEDA.index(znak) + posun if je_sifrovani else CESKA_ABECEDA.index(znak) - posun) % len(CESKA_ABECEDA)
                vysledek += CESKA_ABECEDA[index]
            elif znak in CESKA_ABECEDA_VELKA:
                index = (CESKA_ABECEDA_VELKA.index(znak) + posun if je_sifrovani else CESKA_ABECEDA_VELKA.index(znak) - posun) % len(CESKA_ABECEDA_VELKA)
                vysledek += CESKA_ABECEDA_VELKA[index]
            else: 
                vysledek += znak
        vystupni_pole.insert(tk.END, vysledek)

    elif vybrana_sifra == "cisla":
        if je_sifrovani:
            slova = vstupni_text.split()
            zpracovana_slova = []
            for slovo in slova:
                zpracovane_znaky = [str(CESKA_ABECEDA.index(z.lower()) + 1) if z.lower() in CESKA_ABECEDA else z for z in slovo]
                zpracovana_slova.append(" ".join(zpracovane_znaky))
            vystupni_pole.insert(tk.END, " / ".join(zpracovana_slova))
        else:
            slova = [s.strip() for s in vstupni_text.replace("/", "  ").split("  ") if s.strip()]
            zpracovana_slova = []
            for slovo in slova:
                znaky = slovo.split()
                zpracovane_znaky = [CESKA_ABECEDA_VELKA[int(c)-1] if c.isdigit() and 1 <= int(c) <= len(CESKA_ABECEDA) else c for c in znaky]
                zpracovana_slova.append("".join(zpracovane_znaky))
            vystupni_pole.insert(tk.END, " ".join(zpracovana_slova))

    elif vybrana_sifra == "atbash":
        vysledek = ""
        for znak in vstupni_text:
            if znak in CESKA_ABECEDA: 
                vysledek += CESKA_ABECEDA[::-1][CESKA_ABECEDA.index(znak)]
            elif znak in CESKA_ABECEDA_VELKA: 
                vysledek += CESKA_ABECEDA_VELKA[::-1][CESKA_ABECEDA_VELKA.index(znak)]
            else: 
                vysledek += znak
        vystupni_pole.insert(tk.END, vysledek)

    elif vybrana_sifra == "binarni":
        if je_sifrovani: 
            vystupni_pole.insert(tk.END, " ".join(format(b, '08b') for b in vstupni_text.encode('utf-8')))
        else:
            try: 
                vystupni_pole.insert(tk.END, bytes(int(b, 2) for b in vstupni_text.split()).decode('utf-8'))
            except Exception: 
                vystupni_pole.insert(tk.END, "[CHYBA] Neplatný binární kód!")

    elif vybrana_sifra == "hex":
        if je_sifrovani: 
            vystupni_pole.insert(tk.END, vstupni_text.encode('utf-8').hex(' '))
        else:
            try: 
                vystupni_pole.insert(tk.END, bytes.fromhex(vstupni_text.replace(" ", "")).decode('utf-8'))
            except Exception: 
                vystupni_pole.insert(tk.END, "[CHYBA] Neplatný HEX kód!")

    elif vybrana_sifra == "base64":
        try:
            if je_sifrovani: 
                vystupni_pole.insert(tk.END, base64.b64encode(vstupni_text.encode('utf-8')).decode('utf-8'))
            else: 
                vystupni_pole.insert(tk.END, base64.b64decode(vstupni_text.encode('utf-8')).decode('utf-8'))
        except Exception: 
            vystupni_pole.insert(tk.END, "[CHYBA] Neplatný Base64 řetězec!")

    elif vybrana_sifra == "leet":
        slovnik_leet = {'a':'4', 'A':'4', 'e':'3', 'E':'3', 'i':'1', 'I':'1', 'o':'0', 'O':'0', 's':'5', 'S':'5', 't':'7', 'T':'7'}
        vystupni_pole.insert(tk.END, "".join([slovnik_leet.get(z, z) for z in vstupni_text]))

    elif vybrana_sifra == "gronsfeld":
        if not hodnota_klice.isdigit(): 
            vystupni_pole.insert(tk.END, "[CHYBA] Klíč musí být číselná řada (např. 123)!")
            return
            
        vysledek = ""
        for i, znak in enumerate(vstupni_text):
            posun = int(hodnota_klice[i % len(hodnota_klice)])
            if znak in CESKA_ABECEDA:
                index = (CESKA_ABECEDA.index(znak) + posun if je_sifrovani else CESKA_ABECEDA.index(znak) - posun) % len(CESKA_ABECEDA)
                vysledek += CESKA_ABECEDA[index]
            elif znak in CESKA_ABECEDA_VELKA:
                index = (CESKA_ABECEDA_VELKA.index(znak) + posun if je_sifrovani else CESKA_ABECEDA_VELKA.index(znak) - posun) % len(CESKA_ABECEDA_VELKA)
                vysledek += CESKA_ABECEDA_VELKA[index]
            else: 
                vysledek += znak
        vystupni_pole.insert(tk.END, vysledek)

    elif vybrana_sifra == "ushift":
        try: 
            posun = int(hodnota_klice)
        except ValueError: 
            posun = 1
            
        vysledek = ""
        for z in vstupni_text:
            novy_kod = (ord(z) + posun if je_sifrovani else ord(z) - posun) % 0x110000
            vysledek += chr(novy_kod)
        vystupni_pole.insert(tk.END, vysledek)

    elif vybrana_sifra == "morse":
        if je_sifrovani:
            slova = vstupni_text.split()
            zpracovana_slova = []
            for slovo in slova:
                zpracovane_znaky = [OBRACENY_MORSE_SLOVNIK.get(z, z) for z in odstran_diakritiku(slovo)]
                zpracovana_slova.append(" ".join(zpracovane_znaky))
            vystupni_pole.insert(tk.END, " / ".join(zpracovana_slova))
        else:
            slova = [s.strip() for s in vstupni_text.replace("/", "  ").split("  ") if s.strip()]
            zpracovana_slova = []
            for slovo in slova:
                znaky = slovo.split()
                zpracovane_znaky = [MORSE_SLOVNIK.get(z, z) for z in znaky]
                zpracovana_slova.append("".join(zpracovane_znaky))
            vystupni_pole.insert(tk.END, " ".join(zpracovana_slova))

def vytvor_retro_box(rodic, text_nadpisu):
    kontejner = tk.Frame(rodic, bg="#000000", height=200)
    kontejner.pack(fill="x", padx=40, pady=20)
    kontejner.pack_propagate(False)

    stin = tk.Frame(kontejner, bg=STIN)
    stin.place(x=12, y=12, relwidth=1.0, width=-12, relheight=1.0, height=-12)

    hlavni_ramec = tk.Frame(kontejner, bg=CERNA_ZELENA, highlightbackground=RAMECEK, highlightcolor=RAMECEK, highlightthickness=2, bd=0)
    hlavni_ramec.place(x=0, y=0, relwidth=1.0, width=-12, relheight=1.0, height=-12)

    horni_panel = tk.Frame(hlavni_ramec, bg=TMAVA_ZELENA, height=40)
    horni_panel.pack(fill="x")
    horni_panel.pack_propagate(False)

    popisek = tk.Label(horni_panel, text=text_nadpisu, bg=TMAVA_ZELENA, fg=ZELENA, font=("Consolas", 14, "bold"), anchor="w")
    popisek.pack(fill="both", expand=True, padx=15)

    tk.Frame(hlavni_ramec, bg=RAMECEK, height=2).pack(fill="x")

    textove_pole = tk.Text(hlavni_ramec, bg=CERNA_ZELENA, fg=ZELENA, font=HLAVNI_PISMO, borderwidth=0, highlightthickness=0, insertbackground=ZELENA, padx=15, pady=10)
    textove_pole.pack(fill="both", expand=True)
    
    # ZDE VÁŽEME NAŠI FUNKCI NA KAŽDÉ ZMÁČKNUTÍ KLÁVESY
    textove_pole.bind("<KeyRelease>", oprav_diakritiku)

    return textove_pole

def pri_najeti(udalost):
    udalost.widget.config(bg=ZELENA_NAJETI)

def pri_odjeti(udalost):
    if not getattr(udalost.widget, 'je_aktivni', False):
        udalost.widget.config(bg="#000000")

def vytvor_tlacitko(rodic, text_tlacitka, sirka=18, styl_pisma=HLAVNI_PISMO):
    tlacitko = tk.Button(rodic, text=text_tlacitka, bg="#000000", fg=ZELENA, font=styl_pisma, activebackground=ZELENA_NAJETI, activeforeground=ZELENA, relief="flat", borderwidth=0, highlightbackground=RAMECEK, highlightcolor=RAMECEK, highlightthickness=1, width=sirka, cursor="hand2")
    tlacitko.je_aktivni = False
    tlacitko.bind("<Enter>", pri_najeti)
    tlacitko.bind("<Leave>", pri_odjeti)
    return tlacitko

tlacitka_hlavniho_rezimu = {}
def nastav_hlavni_rezim(rezim):
    promenna_hlavniho_rezimu.set(rezim)
    for klic, tlacitko in tlacitka_hlavniho_rezimu.items():
        if klic == rezim:
            tlacitko.je_aktivni = True
            tlacitko.config(bg=ZELENA_NAJETI)
        else:
            tlacitko.je_aktivni = False
            tlacitko.config(bg="#000000")
            
    if 'hlavni_tlacitko' in globals():
        if rezim == "sifrovat":
            hlavni_tlacitko.config(text="Šifrovat")
        else:
            hlavni_tlacitko.config(text="Dešifrovat")
            
    vymaz_pole()

tlacitka_sifer = {}
def nastav_aktivni_sifru(rezim):
    promenna_sifry.set(rezim)
    for klic, tlacitko in tlacitka_sifer.items():
        if klic == rezim:
            tlacitko.je_aktivni = True
            tlacitko.config(bg=ZELENA_NAJETI) 
        else:
            tlacitko.je_aktivni = False
            tlacitko.config(bg="#000000") 
            
    if rezim in ["caesar", "gronsfeld", "ushift"]:
        ramec_klice.pack(after=ramec_tlacitek, pady=5)
    else:
        ramec_klice.pack_forget()
        
    vymaz_pole()

promenna_hlavniho_rezimu = tk.StringVar()
promenna_sifry = tk.StringVar()

horni_ramec_rezimu = tk.Frame(okno, bg="#000000")
horni_ramec_rezimu.pack(pady=(20, 10))

tlacitko_sifrovani = vytvor_tlacitko(horni_ramec_rezimu, "Šifrátor", sirka=20, styl_pisma=("Consolas", 14, "bold"))
tlacitko_sifrovani.config(command=lambda: nastav_hlavni_rezim("sifrovat"))
tlacitko_sifrovani.grid(row=0, column=0, padx=10)
tlacitka_hlavniho_rezimu["sifrovat"] = tlacitko_sifrovani

tlacitko_desifrovani = vytvor_tlacitko(horni_ramec_rezimu, "Dešifrátor", sirka=20, styl_pisma=("Consolas", 14, "bold"))
tlacitko_desifrovani.config(command=lambda: nastav_hlavni_rezim("desifrovat"))
tlacitko_desifrovani.grid(row=0, column=1, padx=10)
tlacitka_hlavniho_rezimu["desifrovat"] = tlacitko_desifrovani

tk.Label(okno, text="Vyber typ šifry:", bg="#000000", fg=ZELENA, font=HLAVNI_PISMO).pack(anchor="w", padx=40, pady=(10, 5))

ramec_tlacitek = tk.Frame(okno, bg="#000000")
ramec_tlacitek.pack(pady=5)

seznam_sifer = [
    ("Písmena pozpátku", "pismena_pozpatku", 0, 0), 
    ("Slova pozpátku", "slova_pozpatku", 0, 1), 
    ("Caesarova šifra", "caesar", 0, 2), 
    ("Čísla", "cisla", 0, 3),
    ("Atbash", "atbash", 1, 0), 
    ("Binární kód", "binarni", 1, 1), 
    ("Hexadecimální kód", "hex", 1, 2), 
    ("Base64", "base64", 1, 3),
    ("Leet Speak", "leet", 2, 0), 
    ("Gronsfeld", "gronsfeld", 2, 1), 
    ("Unicode Shift", "ushift", 2, 2), 
    ("Morseova", "morse", 2, 3)
]

for text_popisku, mod, radek, sloupec in seznam_sifer:
    nove_tlacitko = vytvor_tlacitko(ramec_tlacitek, text_popisku)
    nove_tlacitko.config(command=lambda m=mod: nastav_aktivni_sifru(m))
    nove_tlacitko.grid(row=radek, column=sloupec, padx=5, pady=5)
    tlacitka_sifer[mod] = nove_tlacitko

ramec_klice = tk.Frame(okno, bg="#000000")
tk.Label(ramec_klice, text="Klíč (číslo/řada):", bg="#000000", fg=ZELENA, font=HLAVNI_PISMO).pack(side=tk.LEFT, padx=5)
vstup_klice = tk.Entry(ramec_klice, bg=CERNA_ZELENA, fg=ZELENA, font=HLAVNI_PISMO, width=15, 
                       insertbackground=ZELENA, highlightthickness=1, 
                       highlightbackground=RAMECEK, highlightcolor=RAMECEK, relief="flat")
vstup_klice.pack(side=tk.LEFT, padx=5)
vstup_klice.insert(0, "1")

vstupni_pole = vytvor_retro_box(okno, "Vstup:")
vystupni_pole = vytvor_retro_box(okno, "Výstup:")

hlavni_tlacitko = vytvor_tlacitko(okno, "Dešifrovat", sirka=40, styl_pisma=("Consolas", 14, "bold"))
hlavni_tlacitko.config(command=zpracuj_akci)
hlavni_tlacitko.pack(pady=10)

nastav_hlavni_rezim("desifrovat")
nastav_aktivni_sifru("pismena_pozpatku")

okno.mainloop()
