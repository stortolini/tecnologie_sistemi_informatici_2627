"""Lab 2 · Blocco 4: Carica le tue frasi su Pinecone.

Prima di eseguire questo script:
    1. Vai su app.pinecone.io e crea un indice con questi parametri:
         Nome:        try
         Schema:      campo "embedding", tipo Dense vector, 384 dim, cosine
    2. Scrivi le tue frasi nella lista MIE_FRASI
    3. Scegli un nome univoco (il tuo nome) in NOME

    uv run 4_upsert.py

Dipendenze:
    uv add pinecone
    uv add sentence-transformers
"""

from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# =============================================================================
# MODIFICA QUESTA SEZIONE
# =============================================================================

API_KEY = "pcsk_2ViYYa_BQ74kPM5tDYMcLdRd9trgoWsG9uRuWzQ5diJz9bQWsdbzzCCCHBDjFyNZuPTwLZ"   # copia la tua API key da app.pinecone.io

NOME = "sofia"               # il tuo nome: diventa il prefisso degli ID e il campo "autore"

MIE_FRASI = [
    "vorrei il nuovo GTA VI",
    "Avrei davvero bisogno di un nuovo PC",
    "I miei studenti usano Baldur's Gate e nomi assurdi come nickname!"
]

# =============================================================================

INDEX_NAME = "laboratorio"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# Connessione all'indice Pinecone
pc = Pinecone(api_key=API_KEY)
index = pc.Index(INDEX_NAME)

# Codifica le frasi in vettori numerici (dimensione 384)
print(f"Codifico {len(MIE_FRASI)} frasi...")
model = SentenceTransformer(MODEL_NAME)
vettori = model.encode(MIE_FRASI, normalize_embeddings=True)

# Costruisce la lista di documenti da caricare.
# Ogni documento è un dizionario con:
#   "_id"       → identificatore univoco (nome + numero)
#   "embedding" → il vettore numerico (lista di 384 float); il nome deve coincidere con il campo dello schema
#   "testo"     → il testo originale, conservato come campo aggiuntivo (utile per mostrarlo nei risultati)
#   "autore"    → il tuo nome, utile per capire chi ha inserito quale frase
documents = []
for i, (frase, vettore) in enumerate(zip(MIE_FRASI, vettori)):
    documento = {
        "_id":       f"{NOME}_{i}",
        "embedding": vettore.tolist(),   # da array numpy a lista Python
        "testo":     frase,
        "autore":    NOME
    }
    documents.append(documento)

# Upsert: "insert or update" — se un _id esiste già, sovrascrive; altrimenti inserisce
# index.documents è la nuova Documents API di Pinecone (richiesta dagli indici con schema)
index.documents.upsert(
    namespace="__default__",   # namespace vuoto = namespace di default
    documents=documents
)

print(f"Caricati {len(documents)} documenti con prefisso ID '{NOME}_'.")
print("Puoi verificare su app.pinecone.io → il tuo indice → Browse Records.")
