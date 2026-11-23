import math
import numpy as np


def coseno(x, y):
    return x @ y / (np.linalg.norm(x) * np.linalg.norm(y))


def euclidea(x, y):
    return np.linalg.norm(x - y)


def vettore():
    """Un vettore è un array: ogni casella contiene una componente, nello stesso ordine."""
    v = np.array([3, 4])
    print("v =", v)
    print("v[0] (componente v1, lungo x) =", v[0])
    print("v[1] (componente v2, lungo y) =", v[1])
    print("dimensione del vettore:", v.shape[0])

    # L'ordine conta: (3, 4) e (4, 3) sono vettori diversi
    w = np.array([4, 3])
    print("(3, 4) uguale a (4, 3)?", np.array_equal(v, w))

    # Da 2 a n dimensioni: un iscritto alla palestra come vettore a 4 dimensioni
    # (età, peso in kg, minuti di cardio a settimana, sedute a settimana)
    marco = np.array([25, 70, 90, 3])
    giulia = np.array([27, 62, 100, 3])
    print("marco =", marco, " giulia =", giulia)


def operazioni():
    """Somma, differenza e prodotto per un numero: componente per componente."""
    A = np.array([1, 2])
    B = np.array([3, 1])
    print("A + B   =", A + B)          # (4, 3)
    print("B - A   =", B - A)          # (2, -1): la freccia dalla punta di A alla punta di B
    print("2 * (3, 4) =", 2 * np.array([3, 4]))   # (6, 8): stessa direzione, lunghezza doppia


def norma():
    """Lunghezza (norma) con Pitagora e normalizzazione."""
    v = np.array([3, 4])
    print("‖(3, 4)‖    =", np.linalg.norm(v))                       # 5
    print("‖(2, 3, 6)‖ =", np.linalg.norm(np.array([2, 3, 6])))     # 7
    print("a mano: √(3² + 4²) =", math.sqrt(3**2 + 4**2))

    v_norm = v / np.linalg.norm(v)
    print("normalizzato:", v_norm)                                  # (0.6, 0.8)
    print("lunghezza dopo la normalizzazione:", np.linalg.norm(v_norm))   # 1


def prodotto_scalare():
    """Prodotto scalare: si moltiplica posizione per posizione, poi si somma."""
    A = np.array([3, 4])
    B = np.array([4, 3])
    print("2D: (3, 4) · (4, 3) =", A @ B)                           # 24
    print("    a mano: 3*4 + 4*3 =", 3 * 4 + 4 * 3)

    A3 = np.array([1, 2, 3])
    B3 = np.array([4, 0, -1])
    print("3D: (1, 2, 3) · (4, 0, -1) =", np.dot(A3, B3))           # 1

    # Errore tipico: A * B NON è il prodotto scalare, è un vettore
    print("A * B (componente per componente) =", A * B, "← questo è un vettore!")

    # Il segno dice se due frecce vanno d'accordo
    a = np.array([2, 0])
    for b in ([2, 1], [0, 2], [-2, 1]):
        print(f"(2, 0) · {tuple(b)} = {a @ np.array(b)}")           # 4, 0, -4


def coseno_esempio():
    """La formula del coseno passo per passo con A = (1, 2) e B = (2, 1)."""
    A = np.array([1, 2])
    B = np.array([2, 1])
    numeratore = A @ B                                              # 4
    denominatore = np.linalg.norm(A) * np.linalg.norm(B)            # √5 · √5 = 5
    cos = numeratore / denominatore                                 # 0.8
    print("numeratore   A · B       =", numeratore)
    print("denominatore ‖A‖ · ‖B‖   =", round(denominatore, 4))
    print("cos θ                    =", round(cos, 4))
    print("θ in gradi               =", round(math.degrees(math.acos(cos)), 1))   # ≈ 36.9

    # Il coseno ignora la lunghezza: raddoppio B e il coseno non cambia
    print("cos(A, 2B)               =", round(coseno(A, 2 * B), 4))


def confronto_metriche():
    """Euclidea e coseno possono dare classifiche diverse."""
    A = np.array([3, 4]); B = np.array([6, 8]); C = np.array([4, 3])

    print(euclidea(A, B), euclidea(A, C))   # 5.0  1.41  → per l'euclidea vince C
    print(coseno(A, B), coseno(A, C))       # 1.0  0.96  → per il coseno vince B


def normalizzazione_e_classifica():
    """Con vettori di lunghezza 1: ‖A − B‖² = 2 − 2·cos θ, quindi stessa classifica."""
    A = np.array([0.6, 0.8])
    B = np.array([0.8, 0.6])
    print("‖A‖ =", np.linalg.norm(A), " ‖B‖ =", np.linalg.norm(B))
    print("‖A − B‖²      =", round(euclidea(A, B) ** 2, 4))         # 0.08
    print("cos θ = A · B =", round(A @ B, 4))                       # 0.96
    print("2 − 2·cos θ   =", round(2 - 2 * (A @ B), 4))             # 0.08

    # Verifica su vettori casuali normalizzati: le due classifiche coincidono
    rng = np.random.default_rng(0)
    q = rng.normal(size=50); q /= np.linalg.norm(q)
    docs = rng.normal(size=(8, 50)); docs /= np.linalg.norm(docs, axis=1, keepdims=True)
    per_coseno = np.argsort(-(docs @ q))
    per_distanza = np.argsort(np.linalg.norm(docs - q, axis=1))
    print("classifica per coseno:  ", per_coseno)
    print("classifica per distanza:", per_distanza)


# =============================================================================

if __name__ == "__main__":
    # Cos'è un vettore e come si indicizza
    vettore()
    print("=" * 40)
    # Operazioni elementari: somma, differenza, scala
    operazioni()
    print("=" * 40)

    # Lunghezza di un vettore e normalizzazione
    # norma()
    # print("=" * 40)

    # Prodotto scalare e interpretazione geometrica del segno
    # prodotto_scalare()
    # print("=" * 40)

    # Similarità del coseno: formula e invarianza rispetto alla scala
    # coseno_esempio()
    # print("=" * 40)

    # Euclidea vs coseno: le classifiche possono divergere
    # confronto_metriche()
    # print("=" * 40)

    # Dopo la normalizzazione euclidea e coseno danno la stessa classifica
    # normalizzazione_e_classifica()
    # print("=" * 40)