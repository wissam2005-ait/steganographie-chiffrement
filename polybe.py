def chiffre_polybe(texte):
    texte = texte.upper().replace('J', 'I') # Standard : I et J partagent la même case
    table = {
        'A':'11', 'B':'12', 'C':'13', 'D':'14', 'E':'15',
        'F':'21', 'G':'22', 'H':'23', 'I':'24', 'K':'25',
        'L':'31', 'M':'32', 'N':'33', 'O':'34', 'P':'35',
        'Q':'41', 'R':'42', 'S':'43', 'T':'44', 'U':'45',
        'V':'51', 'W':'52', 'X':'53', 'Y':'54', 'Z':'55'
    }
    res = ""
    for char in texte:
        if char in table: res += table[char] + " "
    return res.strip()