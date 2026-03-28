### Snippets Assembleur x86 (16-bit) - ABALONE.EXE (1999)

Voici les sections critiques du code désassemblées lors de l'analyse de l'IA.

#### 1. Initialisation de la Matrice de Poids (Segment 4)
Ce code itère sur les 61 positions du plateau et assigne les poids (1, 4, 6, 7, 8) selon l'index de la case.

```nasm
; --- Assignation du Poids 6 (Rayon 2) ---
0xb37b: mov bx, dx          ; dx contient l'index de la case (0-60)
0xb37d: shl bx, 4           ; Multiplication par 16 (taille de la structure cell)
0xb380: mov word ptr [bx + 0x2668], 6  ; Stocke le poids 6 à l'offset 0x2668 (poids positionnel)

; --- Assignation du Poids 7 (Rayon 1) ---
0xb3a6: mov bx, dx
0xb3a8: shl bx, 4
0xb3ab: mov word ptr [bx + 0x2668], 7

; --- Assignation du Poids 8 (Centre) ---
0xb3b8: mov bx, dx
0xb3ba: shl bx, 4
0xb3bd: mov word ptr [bx + 0x2668], 8
```

#### 2. Cœur de la Fonction d'Évaluation (Calcul du Score)
Extrait du calcul de la différence matérielle et pondération positionnelle.

```nasm
; --- Calcul Différence Matérielle ---
0x97bc: cmp word ptr [0x2640], 0x3e8 ; Compare avec 1000 (Valeur d'une bille)
0x97c2: jg  0x97da                  ; Si > 1000, avantage significatif

; --- Boucle d'Evaluation ---
0xa869: mov bx, dx                  ; bx = index case
0xa86b: shl bx, 4                   ; bx = offset structure
0xa86e: mov ax, word ptr [bx + 0x265a] ; ax = état de la case (Joueur 0/1/-1)
0xa872: cmp ax, word ptr [0x2650]   ; Est-ce le joueur actuel ?
0xa876: jne 0xa896
0xa878: mov bx, word ptr [bp - 8]   ; bp-8 contient l'index de la bille
0xa87b: shl bx, 4
0xa87e: mov ax, word ptr [bx + 0x2668] ; ax = Poids de la case (8, 7, 6...)
0xa882: mov bx, dx
0xa884: shl bx, 4
0xa887: sub ax, word ptr [bx + 0x2668]
0xa88b: imul word ptr [bp + 6]      ; Multiplication par multiplicateur de groupe
0xa88e: add ax, word ptr [bp - 4]    ; Ajout au score total
0xa891: mov word ptr [bp - 4], ax
```

#### 3. Paramètres Alpha-Beta (Constants)
```nasm
0x1291: mov si, 0x2710 ; Valeur 10000 (Bonus Victoire / Capture de la 6ème bille)
0x1294: div si         ; Normalisation du score
```
