# Tecnologie dei Sistemi Informatici 26/27

Materiale dei laboratori. Segui le istruzioni in ordine la **prima volta**; le volte successive basta il punto 4.

---

## 1. Installa Git

Serve per scaricare e aggiornare il materiale.

| Sistema | Istruzioni |
|---------|-----------|
| **Windows** | Scarica e installa [git-scm.com](https://git-scm.com/download/win) (lascia tutte le opzioni predefinite) |
| **macOS** | Apri il Terminale e scrivi `git --version` — se non è installato, ti chiede di installarlo automaticamente |
| **Linux** | `sudo apt install git` (Debian/Ubuntu) oppure `sudo dnf install git` (Fedora) |

---

## 2. Installa uv

`uv` gestisce Python e le librerie al posto tuo — non serve installare Python separatamente.

Apri il terminale (su Windows usa **PowerShell**) e incolla il comando per il tuo sistema:

**macOS / Linux**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Chiudi e riapri il terminale dopo l'installazione.

---

## 3. Scarica il repo (solo la prima volta)

```bash
git clone https://github.com/stortolini/tecnologie_sistemi_informatici_2627.git
cd tecnologie_sistemi_informatici_2627
```

---

## 4. Aggiorna il materiale (ogni lezione)

Entra nella cartella del repo ed esegui:

```bash
git pull
```

---

## 5. Prima di eseguire gli script del Lab 2

1. Vai nella cartella `lab_2/`
2. Copia `costanti.example.py` e rinominala `costanti.py`
3. Apri `costanti.py` e compila:
   - **API_KEY** → la tua chiave da [app.pinecone.io](https://app.pinecone.io)
   - **NOME** → il tuo nome (es. `"mario"`)
   - **MIE_FRASI** → le frasi che vuoi caricare

---

## 6. Esegui uno script

Dalla cartella `lab_2/`:

```bash
uv run 4_upsert.py
uv run 5_query.py
```

La prima volta `uv` scarica Python e le librerie necessarie automaticamente — può richiedere qualche minuto.
