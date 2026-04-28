# Czech Cipher App

Graphical interface for advanced encrypting and decrypting of text with full support for Czech diacritics. The program is designed in a retro-hacker style and is optimized to run smoothly on all major systems.

## Main Features
- **100% Czech language support**: Algorithms correctly process `ěščřžýáíéóňďť`.
- **12 unique modules**: From classic historical ciphers to modern data encoding.
- **Multiplatform**: Tested on Windows, macOS, and Linux (Arch Linux).
- **Hacker design**: Terminal-inspired UI with 3D effects and smooth interaction.
- **Linux Fix**: Integrated automatic correction for typing with "dead keys".

## List of Ciphers
1. **Letters backwards** - Reversing the order of characters.
2. **Words backwards** - Reversing the order of whole words.
3. **Caesar Cipher** - Shift in the Czech alphabet (41 characters).
4. **Numbers** - Conversion of letters to their position in the Czech alphabet.
5. **Atbash** - Mirror reflection of the alphabet.
6. **Binary Code** - Conversion of text into zeros and ones (UTF-8).
7. **Hexadecimal Code** - Conversion to the base-16 numbering system.
8. **Base64** - Standard encoding for secure data transmission.
9. **Leet Speak** - Hacker substitution of letters with digits.
10. **Gronsfeld Cipher** - Polyalphabetic cipher using a numeric key.
11. **Unicode Shift** - Total shift of all Unicode characters.
12. **Morse Code** - Radio communication (automatically cleans diacritics when encrypting).

## Installation and execution

To install, you need **Git** and **Python 3.x** on your system.

```bash
# 1. Cloning the repository from GitHub
git clone [https://github.com/susjantux/czech_cipher_app.git](https://github.com/susjantux/czech_cipher_app.git)

# 2. Navigating to the project folder
cd czech_cipher_app

# 3. Running the application
python czech_cipher_app.py
