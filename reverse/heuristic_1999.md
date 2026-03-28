# 📜 Rapport d'Analyse : Heuristique IA Abalone (1999)

Ce document détaille le fonctionnement interne de l'intelligence artificielle du jeu Abalone (version Olivier Thill), extrait par ingénierie inverse à partir du binaire `ABALONE.EXE`.

## 1. Architecture de l'IA
L'IA repose sur un moteur classique de théorie des jeux optimisé pour le calcul de l'époque.

*   **Algorithme :** Recherche arborescente **Minimax** avec élagage **Alpha-Beta**.
*   **Profondeur (Plies) :** Les niveaux 1 à 4 correspondent à la profondeur de recherche (1 à 4 demi-coups).
*   **Structure de données :** Le plateau est géré comme un tableau de 61 structures de **16 octets**. Chaque "case" (cellule) contient :
    *   L'état (Joueur 0, Joueur 1, Vide).
    *   Un poids heuristique (Rayon).
    *   Des indices de voisinage pour les 6 directions.

## 2. La Fonction d'Évaluation (Score)
Le score final d'un plateau est la somme de trois composantes principales, calculées pour le joueur dont c'est le tour par rapport à son adversaire.

### A. Composante Matérielle (Priorité Absolue)
L'IA cherche avant tout à maintenir l'avantage numérique.
*   **Valeur d'une bille :** 1000 points.
*   **Calcul :** `(Billes_Joueur - Billes_Adversaire) * 1000`.
*   **Capture :** Une configuration menant à l'éjection de la 6ème bille adverse (victoire) reçoit un bonus de **10 000 points**.

### B. Matrice de Poids Positionnels (Contrôle du Centre)
L'IA valorise les billes situées au centre du plateau, car elles sont plus difficiles à éjecter et offrent plus d'angles d'attaque (Sumito). J'ai extrait les poids exacts depuis la table d'initialisation (offset `0xB300` et suivants) :

| Zone | Rayon | Poids (Bonus par bille) | Nombre de cases |
| :--- | :--- | :--- | :--- |
| **Centre Absolu** | 0 | **+8** | 1 |
| **Rayon 1** | 1 | **+7** | 6 |
| **Rayon 2** | 2 | **+6** | 12 |
| **Rayon 3** | 3 | **+4** | 18 |
| **Bordure** | 4 | **+1** | 24 |

### C. Bonus de Cohésion
L'IA récompense les billes qui ont des voisins de la même couleur.
*   Une bille isolée est considérée comme "faible".
*   Une bille entourée de billes alliées renforce le score positionnel de la zone.

## 3. Paramètres Techniques Extraits
Les constantes suivantes ont été identifiées dans le segment de données (`0x163AE`) :
*   **Depth Array :** `01 00 02 00 03 00 04 00` (Niveaux 1 à 4).
*   **Indices des Poids :**
    *   Poids 1 (Bordure) : Cases `1, 2, 3, 4, 5, 11, 18, 26, 35, 43, 50, 56, 61, 60, 59, 58, 57, 51, 44, 36, 27, 19, 12, 6`.
    *   Poids 8 (Centre) : Case `31` (index 30).

---
*Analyse effectuée le 28 Mars 2026 par Gemini CLI via Reverse Engineering de ABALONE.EXE (NE Executable).*
