# OpenAlpha — Roadmap

Questo documento è il punto di ingresso operativo al progetto. Va
aggiornato **alla fine di ogni task**, non "quando c'è tempo".

Legenda stato: ✅ completato · 🚧 in corso · ⬜ da fare · ⏸️ sospeso · ❌ abbandonato

---

## Fase 0 — Setup ✅

- **T0.1** ✅ Struttura cartelle
- **T0.2** ✅ `requirements.txt` e `requirements-dev.txt`
- **T0.3** ✅ `pyproject.toml` con configurazione pytest
- **T0.4** ✅ `.gitignore`
- **T0.5** ✅ `README.md` con istruzioni minime

---

## Fase 1 — Fondamenta ✅

- **T1.1** ✅ Modello di stato (`core/status.py`)
- **T1.2** ✅ Eccezioni del progetto (`core/exceptions.py`)
- **T1.3** ✅ Modello di risultato (`core/result.py`)
- **T1.4** ✅ Test del modello di risultato
- **T1.5** ✅ Registro operazioni (`core/registry.py`)
- **T1.6** ✅ Prima operazione: `simplify`
- **T1.7** ✅ CLI minima

---

## Fase 2 — Parser e algebra elementare ✅

- **T2.1** ✅ Tokenizer
- **T2.2** ✅ Parser (AST proprio)
- **T2.3** ✅ Conversione AST → SymPy
- **T2.4** ✅ Validatore
- **T2.5** ✅ Integrazione: `simplify` usa il parser proprio
- **T2.6** ✅ Suite di sicurezza minima
- **T2.7** ✅ Operazione `expand`
- **T2.8** ✅ Operazione `factor` + `apply_sympy_operation`

---

## Fase 3 — Equazioni, dominio, spiegazioni ✅

- **T3.1** ✅ Modello `Step`
- **T3.2** ✅ Modello `Rule`
- **T3.3** ✅ Formatter e integrazione di `Step` in `Result`
- **T3.4** ✅ Dominio e condizioni di validità
- **T3.5** ✅ Operazione `solve`
- **T3.7** ✅ Motore delle spiegazioni (prima versione)
- **T3.7-bis** ✅ Redesign di `Rule` (pattern + function-based)
- **T3.8** ✅ Politica delle spiegazioni (`docs/EXPLANATIONS.md`)

---

## Fase 4 — Analisi, numerica, grafici ✅

- **T4.1** ✅ Operazione `limit`
- **T4.2** ✅ Operazione `diff`
- **T4.3** ✅ Operazione `integrate`
- **T4.4** ✅ Approssimazioni (`approximate` in `Result`)
- **T4.5** ✅ Operazioni `nsolve` e `nintegrate`
- **T4.6** ✅ Operazione `plot` (grafici 2D statici)
- **T4.7** ✅ Operazione `plot3d` (grafici 3D statici)
- **T4.8** ✅ Operazione `solve_system` (sistemi lineari)

---

## Fase 5 — Web UI ✅

Web app locale in stile Wolfram Alpha, con rendering MathJax,
grafici interattivi (Plotly), tastiera matematica, cronologia,
esportazione, e bundle `.app`.

- **T5.1** ✅ Server Flask + pagina HTML base
- **T5.2** ✅ API esecuzione (`/api/execute`, `/api/operations`)
- **T5.3** ✅ Rendering MathJax (formule + passaggi)
- **T5.5a** ✅ API con parametri extra (`var`, `point`, `order`, ...)
- **T5.5b** ✅ Tastiera matematica + parsing di alto livello
- **T5.6** ✅ Cronologia (`localStorage`, 50 voci, click per ri-eseguire)
- **T5.7** ✅ Grafici 2D inline (base64, file temporaneo cancellato)
- **T5.8** ✅ Copia/esportazione (LaTeX, testo, PNG, JSON)
- **T5.9** ✅ Grafici 3D interattivi (Plotly, rotazione/zoom/pan)
- **T5.9-bis** ✅ Grafici 2D interattivi (Plotly, zoom/pan/hover)
- **T5.10** ✅ Bundle PyInstaller + launcher (`OpenAlpha.app`)

**Risultato:** 520 test verdi. Webapp completa, funzionante,
distribuita come applicazione standalone.

---

## Fase 5-bis — Rifiniture UI (in corso)

- **T5.11** ⬜ Input visuale (barra che renderizza formule come WA)
- **T5.12** 🚧 Rifinitura estetica

---

## Fase 6 — Estensioni future ⬜

- **T6.1** ⬜ Equazioni differenziali
- **T6.2** ⬜ Serie e successioni
- **T6.3** ⬜ Linguaggio naturale (parsing di richieste in italiano/inglese)
- **T6.4** ⬜ Integrazione AI locale (opzionale)
- **T6.5** ⬜ API REST pubblica
- **T6.6** ⬜ Altre operazioni (matrici, statistica, teoria dei numeri)

---

## Stato attuale

**Fase:** 5 — chiusa. In corso: rifiniture UI (T5.12).
**Ultimo task chiuso:** T5.10
**Prossimo task:** T5.12 (rifinitura estetica)

**Numeri:**
- 520 test verdi.
- 12 operazioni disponibili.
- 2 interfacce: CLI (`python -m openalpha`) e web UI (`python -m openalpha.web`).
- Bundle `.app` funzionante.

---

## Problemi noti / decisioni rimandate

- [2026-10-13] **Input visuale (T5.11)**: barra renderizzata come WA.
  Opzionale, complesso. Da valutare dopo T5.12.
- [2026-10-13] **Rifinitura estetica (T5.12)**: layout, tipografia,
  colori, spaziature. Non aggiunge funzionalità.
- [2026-10-13] **Commit Git**: rimandato.
- [2026-10-13] **Firma del codice**: il bundle `.app` non è firmato.
  Gatekeeper lo blocca al primo avvio. L'utente deve autorizzare
  con `xattr -cr` o dalle impostazioni di sistema.
- [2026-10-13] **Build multi-architettura**: il bundle è x86_64.
  Per Apple Silicon servirà una build separata.
- [2026-10-13] **`nsolve` dipende dal punto iniziale**: con
  `initial="1"`, alcune equazioni non convergono. L'utente può
  specificare `--initial`.
- [2026-10-13] **`solve_system`**: solo sistemi lineari con soluzione
  unica. Sistemi non lineari, inconsistenti, indeterminati → `UNSUPPORTED`.
- [2026-10-13] **Nome definitivo del progetto**: ancora "OpenAlpha".
- [2026-10-13] **Venv nella root**: funziona, ma un domani si può
  migrare a `.venv/`.

---

## Diario sintetico

- **2026-10-12**: Fasi 0–1 completate. 52 test verdi.
- **2026-10-12**: Fase 2 completata. 211 test verdi.
- **2026-10-12/13**: Fase 3 completata. Spiegazioni verificate,
  dominio, equazioni. 325 test verdi.
- **2026-10-13**: Fase 4 completata. Analisi, numerica, grafici,
  sistemi lineari. 447 test verdi.
- **2026-10-13**: Fase 5 completata. Web app locale in stile WA.
  MathJax, Plotly, tastiera matematica, cronologia, esportazione,
  bundle `.app`. 520 test verdi.
- **2026-10-13**: inizio rifiniture UI (T5.12).

---

## Note architetturali

- **`core/` indipendente da SymPy**: `Result`, `Step`, `Status`,
  eccezioni non importano SymPy.
- **Parser a strati**: tokenizer → parser → validatore → to_sympy.
- **Regole pattern-based vs function-based**: le prime per pattern
  specifici, le seconde per pattern generici.
  Vedi `docs/EXPLANATIONS.md`.
- **`apply_sympy_operation`** centralizza il pattern comune a tutte
  le operazioni SymPy.
- **Numerica**: `nsolve` e `nintegrate` restituiscono `APPROXIMATE`.
- **Web UI**: il backend Flask fa da adattatore. Le operazioni restano
  "pure" (producono `Result`), il layer web le adatta al contesto
  (base64 per i grafici, LaTeX per il rendering).
- **Bundle**: PyInstaller include Python, dipendenze, e file statici.
  Il bundle è self-contained (~200 MB).

### Visualizzazione 3D interattiva

Approccio scelto: **Plotly.js** locale (MIT, ~3 MB), invece di
Three.js o QtWebEngine. Plotly supporta superfici 3D e grafici 2D
interattivi nativamente.

### Input visuale (T5.11, opzionale)

Per l'input visuale stile WA, tre possibili approcci:
- **A.** QtWebEngine + MathJax (150 MB, due linguaggi).
- **B.** Widget custom con editor contenteditable.
- **C.** Editor LaTeX visuale.

Scelta rimandata. Raccomandazione preliminare: **B** (contenteditable).