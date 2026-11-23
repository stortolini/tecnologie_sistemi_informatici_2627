"""Lab 2 · Blocco 5: Interroga l'indice Pinecone con una frase.

    uv run 5_query.py

Dipendenze:
    uv add pinecone
    uv add sentence-transformers
"""

from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# =============================================================================
# MODIFICA QUESTA SEZIONE
# =============================================================================

API_KEY = "pcsk_2ViYYa_BQ74kPM5tDYMcLdRd9trgoWsG9uRuWzQ5diJz9bQWsdbzzCCCHBDjFyNZuPTwLZ"   # la stessa chiave usata in 4_upsert.py

MIA_QUERY = "allenamento in palestra"   # scrivi qui la frase che vuoi cercare

QUANTI_RISULTATI = 5   # quanti documenti simili restituire

# =============================================================================

INDEX_NAME = "laboratorio"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# Connessione all'indice
pc = Pinecone(api_key=API_KEY)
index = pc.Index(INDEX_NAME)

# Codifica la query con lo stesso modello usato durante l'upsert
# (fondamentale: vettore query e vettori documento devono vivere nello stesso spazio)
model = SentenceTransformer(MODEL_NAME)
vettore_query = model.encode(MIA_QUERY, normalize_embeddings=True)

# Ricerca per similarità coseno nell'indice.
# score_by descrive come calcolare la similarità:
#   "type": "dense_vector"  → usa il campo vettoriale (non embedding integrato)
#   "fields": ["embedding"] → nome del campo vettoriale definito nello schema
#   "values": [...]         → il vettore della query (deve avere le stesse dimensioni: 384)
# include_fields: quali campi aggiuntivi restituire insieme al risultato
risultati = index.documents.search(
    namespace="__default__",
    top_k=QUANTI_RISULTATI,
    score_by=[{
        "type":   "dense_vector",
        "fields": ["embedding"],
        "values": vettore_query.tolist()
    }],
    include_fields=["testo", "autore"]
)

# Pinecone restituisce i risultati già ordinati dal più simile al meno simile
print(f"\nQuery: {MIA_QUERY!r}")
print(f"Trovati {len(risultati.matches)} risultati:\n")

for match in risultati.matches:
    # match.score: similarità coseno (1.0 = identico, 0.0 = non correlato)
    # match.testo, match.autore: i campi richiesti in include_fields
    print(f"  score: {match.score:.3f}  [{match.autore}]  {match.testo}")
