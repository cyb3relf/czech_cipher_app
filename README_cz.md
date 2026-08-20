#  Czech Cipher App

Grafické rozhraní pro pokročilé šifrování a dešifrování textu s plnou podporou české diakritiky. Program je navržen v retro-hakerském stylu a je optimalizován pro bezproblémový běh na všech hlavních systémech.

##  Hlavní vlastnosti
- **100% podpora češtiny**: Algoritmy správně zpracovávají `ěščřžýáíéóňďť`.
- **12 unikátních modulů**: Od klasických historických šifer až po moderní kódování dat.
- **Multiplatformní**: Testováno na Windows, macOS a Linux (Arch Linux).
- **Hakerský design**: UI inspirované terminály s 3D efekty a plynulou interakcí.
- **Linux Fix**: Integrovaná automatická korekce pro psaní s "mrtvými klávesami".

##  Seznam šifer
1.  **Písmena pozpátku** - Převrácení pořadí znaků.
2.  **Slova pozpátku** - Převrácení pořadí celých slov.
3.  **Caesarova šifra** - Posun v české abecedě (41 znaků).
4.  **Čísla** - Převod písmen na jejich pozici v české abecedě.
5.  **Atbash** - Zrcadlové obrácení abecedy.
6.  **Binární kód** - Převod textu na nuly a jedničky (UTF-8).
7.  **Hexadecimální kód** - Převod na šestnáctkovou soustavu.
8.  **Base64** - Standardní kódování pro bezpečný přenos dat.
9.  **Leet Speak** - Hakerská substituce písmen za číslice.
10. **Gronsfeldova šifra** - Polyalfabetická šifra využívající číselný klíč.
11. **Unicode Shift** - Totální posun všech Unicode znaků.
12. **Morseova šifra** - Radiová komunikace (automaticky čistí diakritiku při šifrování).

##  Instalace a spuštění

K instalaci potřebujete mít v systému **Git** a **Python 3.x**.

```bash
# 1. Klonování repozitáře z GitHubu
git clone https://github.com/susjantux/czech_cipher_app.git

# 2. Přechod do složky projektu
cd czech_cipher_app

# 3. Spuštění aplikace
python czech_cipher_app.py
