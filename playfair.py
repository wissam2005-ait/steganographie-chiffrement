def generer_matrice(cle):
    cle = cle.upper().replace("J", "I")
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # Pas de J
    matrice = []
    used = []
    
    # Ajouter la clé d'abord
    for char in cle:
        if char not in used and char in alphabet:
            used.append(char)
    # Compléter avec le reste de l'alphabet
    for char in alphabet:
        if char not in used:
            used.append(char)
            
    # Transformer en grille 5x5
    return [used[i:i+5] for i in range(0, 25, 5)]

def trouver_position(matrice, char):
    for r, row in enumerate(matrice):
        if char in row:
            return r, row.index(char)
    return None

def chiffre_playfair(texte, cle):
    matrice = generer_matrice(cle)
    texte = texte.upper().replace("J", "I").replace(" ", "")
    
    # les paires
    i = 0
    paires = []
    while i < len(texte):
        a = texte[i]
        b = ""
        if i + 1 < len(texte):
            if a == texte[i+1]:
                b = "X"
                i += 1
            else:
                b = texte[i+1]
                i += 2
        else:
            b = "X"
            i += 1
        paires.append((a, b))

    resultat = ""
    for a, b in paires:
        r1, c1 = trouver_position(matrice, a)
        r2, c2 = trouver_position(matrice, b)

        if r1 == r2: # Même ligne -> décalage à droite
            resultat += matrice[r1][(c1 + 1) % 5] + matrice[r2][(c2 + 1) % 5]
        elif c1 == c2: # Même colonne -> décalage en bas
            resultat += matrice[(r1 + 1) % 5][c1] + matrice[(r2 + 1) % 5][c2]
        else: # Rectangle -> inversion des colonnes
            resultat += matrice[r1][c2] + matrice[r2][c1]
            
    return resultat