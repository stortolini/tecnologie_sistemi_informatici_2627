"""Lab 2 · Blocco 3: Ricerca lessicale e semantica.

    uv run 3_ricerca.py

Dipendenze:
    uv add numpy
    uv add rank-bm25
    uv add sentence-transformers
"""

import math

import numpy as np

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_model = None

DOCS_ESERCIZIO = ["Tapis roulant con pendenza regolabile",
                  "Treadmill for home workouts",
                  "Cyclette per allenamento cardio",
                  "Ricette proteiche post-allenamento",
                  "Manuale Skillrun: manutenzione del nastro",
                  "Panca regolabile per esercizi di forza"]
QUERY_ESERCIZIO = ["macchina per correre in casa", "Skillrun",
                   "cosa mangiare dopo la palestra", "regolabile"]


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        print(f"Carico il modello {MODEL_NAME} ...")
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def _tokenizza(testo):
    """
    Una tokenizzazione vera dovrebbe gestire punteggiatura variabile, apostrofi, 
    numeri, parole composte, stopword, stemming/lemmatizzazione… Qui è 
    ridotta all'osso per non distrarsi dal punto principale (BM25 e ricerca 
    semantica).
    """
    return testo.lower().replace(":", " ").replace("-", " ").split()


def sezione(titolo):
    print(f"\n{'=' * 60}")
    print(f"  {titolo}")
    print('=' * 60)


# =============================================================================

def bm25_esercizio():
    """[rank-bm25] Esercizio: cosa trova BM25 per ogni query."""
    from rank_bm25 import BM25Okapi

    # Da notare: per Q1 BM25 "trova" D3 e D6 solo perché contengono "per",
    # la stessa parola della query. È il motivo per cui si tolgono le stopword.
    bm25 = BM25Okapi([_tokenizza(d) for d in DOCS_ESERCIZIO])

    for q in QUERY_ESERCIZIO:
        scores = bm25.get_scores(_tokenizza(q))

        # argsort restituisce gli indici ordinati dal punteggio più basso al più alto;
        # [::-1] inverte l'ordine (dal più alto), [:3] prende i primi 3
        indici_top3 = np.argsort(scores)[::-1][:3]

        print(f"\nquery: {q!r}")
        for i in indici_top3:
            print(f"  {scores[i]:5.2f}  D{i + 1}  {DOCS_ESERCIZIO[i]}")


def ricerca_semantica():
    """[modello] Una ricerca semantica completa in poche righe."""
    model = get_model()
    docs = DOCS_ESERCIZIO
    doc_vec = model.encode(docs, normalize_embeddings=True)

    for query in QUERY_ESERCIZIO:
        q_vec = model.encode(query, normalize_embeddings=True)

        # Prodotto scalare tra il vettore query e ogni vettore documento:
        # con vettori normalizzati equivale alla similarità coseno
        scores = doc_vec @ q_vec

        indici_top3 = np.argsort(scores)[::-1][:3]

        print(f"\nquery: {query!r}")
        for i in indici_top3:
            print(f"  {scores[i]:.2f}  D{i + 1}  {docs[i]}")


def lessicale_vs_semantica():
    """[modello + rank-bm25] «scarpe per correre»: BM25 contro ricerca semantica."""
    from rank_bm25 import BM25Okapi

    docs = ["Calzature da running leggere", "Scarpe eleganti in pelle"]
    query = "scarpe per correre"

    bm25 = BM25Okapi([_tokenizza(d) for d in docs])
    punteggi_bm25 = bm25.get_scores(_tokenizza(query))
    print("BM25:")
    for doc, punteggio in zip(docs, punteggi_bm25):
        print(f"  {punteggio:.3f}  {doc}")

    model = get_model()
    vettori_docs = model.encode(docs, normalize_embeddings=True)
    vettore_query = model.encode(query, normalize_embeddings=True)
    sim = vettori_docs @ vettore_query
    # Poiché i vettori sono stati normalizzati a lunghezza 1 (normalize_embeddings=True), 
    # il prodotto scalare coincide esattamente con la similarità coseno — 
    # quindi sim è un array di 6 score tra -1 e 1, uno per documento.
    print("Semantica:")
    for doc, punteggio in zip(docs, sim):
        print(f"  {punteggio:.3f}  {doc}")

# =============================================================================

if __name__ == "__main__":
    sezione("BM25 applicato all'esercizio")
    bm25_esercizio()

    sezione("Ricerca semantica con sentence-transformers")
    ricerca_semantica()

    sezione("Lessicale vs semantica: scarpe per correre")
    lessicale_vs_semantica()
