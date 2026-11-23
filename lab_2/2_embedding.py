"""
uv run 2_embedding.py

Dipendenze:
    uv add numpy
    uv add sentence-transformers
"""

import numpy as np

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        print(f"Carico il modello {MODEL_NAME} ...")
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def coseno(x, y):
    return x @ y / (np.linalg.norm(x) * np.linalg.norm(y))


def euclidea(x, y):
    return np.linalg.norm(x - y)


def codici_caratteri():
    """I codici dei caratteri descrivono la scrittura, non il significato."""
    for parola in ["casa", "cosa", "corsa", "running"]:
        print(f"{parola!r:10} → {[ord(c) for c in parola]}")
        # !r applica repr() alla parola, quindi aggiunge le virgolette attorno: 'casa' invece di casa
        # :10 allinea il risultato in un campo di 10 caratteri (padding a destra)
    print("byte UTF-8 di 'perché':", list("perché".encode("utf-8")))


def embedding_illustrativi():
    """Valori illustrativi della slide: prime 2 componenti di corsa, running, pizza."""
    corsa = np.array([0.81, 0.12])
    running = np.array([0.79, 0.15])
    pizza = np.array([-0.30, 0.66])
    print("cos(corsa, running) =", round(coseno(corsa, running), 3))  # ≈ 0.999
    print("cos(corsa, pizza)   =", round(coseno(corsa, pizza), 3))    # ≈ -0.28


def primo_embedding():
    """[modello] In Python bastano poche righe per un embedding."""
    model = get_model()
    frasi = ["Allenamento cardio sul tapis roulant",
             "Cardio workout on a treadmill",
             "Ricetta della pizza margherita"]
    vettori = model.encode(frasi)

    print(f"Dimensione vettori: {vettori.shape}")  # (3, 384)
    print("Prime 10 componenti del primo vettore:", vettori[0][:10])

    for i in range(len(frasi)):
        for j in range(i + 1, len(frasi)):
            sim = round(float(coseno(vettori[i], vettori[j])), 3)
            print(f"cos({frasi[i]!r}, {frasi[j]!r}) = {sim}")


if __name__ == "__main__":
    # sezione("Codici dei caratteri")
    codici_caratteri()

    # sezione("Embedding illustrativi")
    embedding_illustrativi()

    # sezione("Primo embedding con sentence-transformers")
    primo_embedding()
