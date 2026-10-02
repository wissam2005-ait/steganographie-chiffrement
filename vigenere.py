def chiffre_vigenere(texte, cle):
    res = ""
    cle = cle.upper()
    texte = texte.upper()
    cle_index = 0
    for char in texte:
        if char.isalpha():
            shift = ord(cle[cle_index % len(cle)]) - 65
            res += chr((ord(char) - 65 + shift) % 26 + 65)
            cle_index += 1
        else:
            res += char
    return res