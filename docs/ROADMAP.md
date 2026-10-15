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

## Fase 5-bis — Rifiniture UI ✅

- **T5.11** ✅ Input visuale (barra che renderizza formule come WA)
  - **T5.11a** ✅ Toggle testo/visuale + fallback (infrastruttura)
  - **T5.11b** ✅ Setup MathLive (file statici, include, boot)
  - **T5.11c** ✅ Sostituzione `<input>` con `<math-field>` in modalità visuale
  - **T5.11d** ✅ Tastiera matematica nell'editor visuale
  - **T5.11e** ✅ Adattamento `analizzaInput` / cronologia
  - **T5.11f** ✅ Test manuali, pulizia, documentazione
- **T5.12** ✅ Rifinitura estetica
  - **T5.12a** ✅ Palette e tipografia
  - **T5.12b** ✅ Layout e responsive
  - **T5.12c** ✅ Animazioni e stati
  - **T5.12d** ✅ Iconografia (Lucide)
---

## Fase 5-ter — Miglioramenti UI futuri ⬜

- **T5.13** ⬜ Plot 2D con dominio dinamico (zoom/pan rilancia il calcolo)
  - **T5.13a** ⬜ Listener `plotly_relayout` + debounce
  - **T5.13b** ⬜ Adattamento dinamico di `n_points`
  - **T5.13c** ⬜ Reset del range al rifare il calcolo
  - **T5.13d** ⬜ Gestione asintoti e casi limite
  - **T5.13e** ⬜ Test manuali
- **T5.14** ⬜ Plot 2D/3D con range configurabile dall'utente
  (`plot(f, xmin, xmax)`, `plot3d(f, xmin, xmax, ymin, ymax)`)
- **T5.15** ⬜ UI dedicata per i parametri di plot (campi xmin, xmax, ecc.)
---

## Fase 6 — Operazioni matematiche ⬜

Obiettivo: portare OpenAlpha a copertura CAS completa, in blocchi
tematici. Le operazioni sono elencate nell'**Inventario operazioni**
(sopra). T6.3 (linguaggio naturale) e T6.4 (AI locale) sono rimandate
a una versione 2.0.

### Blocco 1 — Fondamentali mancanti (priorità alta)

- **T6.1** ✅ `evaluate` — calcolo numerico diretto
- **T6.1a** ✅ Versione base
- **T6.2** ✅ `series` — sviluppo in serie
- **T6.3** ⬜ `roots` — radici di polinomi
- **T6.4** ⬜ `sum` / `product` — sommatorie e produttorie
- **T6.5** ⬜ `taylor` (alias di `series`? — da decidere)
- **T6.6** ⬜ `dsolve` — equazioni differenziali (primo ordine)
- **T6.7** ⬜ `dsolve` — equazioni differenziali (secondo ordine)
- **T6.8** ⬜ `apart` — frazioni parziali

### Blocco 2 — Algebra lineare

- **T6.8** ⬜ Parser matrici (`[[1, 2], [3, 4]]`)
- **T6.9** ⬜ `det`, `inv`, `transpose`, `rank`, `rref`
- **T6.10** ⬜ `eigenvalues`, `eigenvectors`, `trace`

### Blocco 3 — Teoria dei numeri

- **T6.11** ⬜ `factorint`, `isprime`, `divisors`, `totient`, `prime`
- **T6.12** ⬜ `gcd`, `lcm`, `mod_inverse`, `crt`

### Blocco 4 — Statistica

- **T6.13** ⬜ `mean`, `median`, `std`, `var`
- **T6.14** ⬜ `combinations`, `permutations`, `factorial`

### Blocco 5 — Calcolo avanzato

- **T6.15** ⬜ `diff_partial`, `gradient`, `hessian`, `critical_points`
- **T6.16** ⬜ `integrate_multiple`
- **T6.17** ⬜ `laplace_transform`, `inverse_laplace`, `fourier_transform`

### Blocco 6 — Equazioni avanzate

- **T6.18** ⬜ `solve_inequality`
- **T6.19** ⬜ `solve_system_nonlinear`

### Blocco 7 — Algebra e polinomi (rifinitura)

- **T6.20** ⬜ `together`, `cancel`, `collect`, `degree`, `coeff`
- **T6.21** ⬜ `gcd_poly`, `lcm_poly`, `div_poly`, `rem_poly`

### Blocco 8 — Geometria analitica (opzionale)

- **T6.22** ⬜ `distance`, `line_equation`, `intersection`

### Rimandate a v2.0

- Linguaggio naturale (parsing di richieste in italiano/inglese)
- Integrazione AI locale
- API REST pubblica
---

## Stato attuale

**Fase:** 6 — in corso (Blocco 1: fondamentali mancanti).
**Ultimo task chiuso:** T6.2
**Prossimo task:** T6.3 (`roots`) o quello che decidiamo

---

## Problemi noti / decisioni rimandate

- [2026-10-13] **Input visuale (T5.11)**: barra renderizzata come WA.
  Opzionale, complesso. Da valutare dopo T5.12.
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
- - **2026-10-13**: T5.11a (toggle testo/visuale) completato. 526 test verdi.
- - **2026-10-13**: T5.11b (setup MathLive) completato. 526 test verdi.
- **2026-10-13**: T5.11c (integrazione `<math-field>` in modalità visuale) completato. 526 test verdi.
- **2026-10-13**: T5.11d (tastiera nell'editor visuale) completato. 526 test verdi.
- **2026-10-13**: T5.11d (tastiera in editor visuale) e T5.11e (round-trip testo/visuale stabile) completati. 526 test verdi.
- **2026-10-13**: T5.12d (iconografia Lucide) completato. Fase 5-bis chiusa. 526 test verdi.
- **2026-10-13**: T6.1a (`evaluate`) completato. 554 test verdi.
- **2026-10-14**: T6.2 (`series`) completato. 571 test verdi.
- 

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
- **Input visuale (T5.11)**: Scelta: **MathLive** (MIT, ~500 KB), editor strutturato WYSIWYG
(math-field). L'editor **convive** con la barra testuale: toggle
"Testo / Visuale". La tastiera matematica resta, ma inserisce
nell'editor attivo. Fallback obbligatorio: se MathLive non carica,
la modalità testo resta disponibile. MathLive 0.101.2 scaricato localmente in `static/mathlive/`
(~1 MB, MIT). La tastiera virtuale nativa di MathLive è
**disabilitata**: OpenAlpha usa la propria tastiera matematica.
I suoni di MathLive non sono inclusi.

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

---

## Inventario operazioni

Stato: ✅ implementata · 🚧 in corso · ⬜ da fare · ⏸️ sospesa

**Contatori:** 14 implementate · 52 pianificate · 66 totali

### Algebra e polinomi

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 1 | `simplify` | ✅ | |
| 2 | `expand` | ✅ | |
| 3 | `factor` | ✅ | |
| 4 | `apart` | ⬜ | Frazioni parziali |
| 5 | `together` | ⬜ | Denominatore comune |
| 6 | `cancel` | ⬜ | Semplifica razionali |
| 7 | `collect` | ⬜ | Raccogli per variabile |
| 8 | `roots` | ⬜ | Radici di polinomi |
| 9 | `gcd_poly` | ⬜ | MCD di polinomi |
| 10 | `lcm_poly` | ⬜ | mcm di polinomi |
| 11 | `div_poly` | ⬜ | Divisione polinomiale |
| 12 | `rem_poly` | ⬜ | Resto polinomiale |
| 13 | `degree` | ⬜ | Grado di un polinomio |
| 14 | `coeff` | ⬜ | Coefficienti |

### Equazioni e sistemi

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 15 | `solve` | ✅ | Polinomiali, grado ≤ 4 |
| 16 | `solve_system` | ✅ | Solo lineari, soluzione unica |
| 17 | `solve_system_nonlinear` | ⬜ | |
| 18 | `solve_inequality` | ⬜ | Disequazioni |

### Calcolo differenziale

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 19 | `diff` | ✅ | |
| 20 | `diff_partial` | ⬜ | Derivate parziali |
| 21 | `gradient` | ⬜ | |
| 22 | `hessian` | ⬜ | |
| 23 | `taylor` | ⬜ | Sviluppo di Taylor |
| 24 | `series` | ✅ | Sviluppo in serie (Taylor, Maclaurin) |
| 25 | `critical_points` | ⬜ | Punti critici |

### Calcolo integrale

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 26 | `integrate` | ✅ | Indefinito e definito |
| 27 | `integrate_multiple` | ⬜ | Integrali doppi/tripli |

### Limiti

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 28 | `limit` | ✅ | |
| 29 | `limit_sequence` | ⬜ | Limite di successione |

### Equazioni differenziali

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 30 | `dsolve` | ⬜ | ODE primo/secondo ordine |
| 31 | `dsolve_system` | ⬜ | Sistemi di ODE |

### Trasformate

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 32 | `laplace_transform` | ⬜ | |
| 33 | `inverse_laplace` | ⬜ | |
| 34 | `fourier_transform` | ⬜ | |

### Serie e successioni

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 35 | `sum` | ⬜ | Sommatorie |
| 36 | `product` | ⬜ | Produttorie |
| 37 | `convergence` | ⬜ | Criteri di convergenza |

### Algebra lineare

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 38 | `det` | ⬜ | Richiede parser matrici |
| 39 | `inv` | ⬜ | Richiede parser matrici |
| 40 | `transpose` | ⬜ | Richiede parser matrici |
| 41 | `rank` | ⬜ | Richiede parser matrici |
| 42 | `rref` | ⬜ | Richiede parser matrici |
| 43 | `eigenvalues` | ⬜ | Richiede parser matrici |
| 44 | `eigenvectors` | ⬜ | Richiede parser matrici |
| 45 | `trace` | ⬜ | Richiede parser matrici |
| 46 | `lu` | ⬜ | Richiede parser matrici |
| 47 | `qr` | ⬜ | Richiede parser matrici |
| 48 | `svd` | ⬜ | Richiede parser matrici |

### Teoria dei numeri

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 49 | `factorint` | ⬜ | Fattorizzazione in primi |
| 50 | `isprime` | ⬜ | Test di primalità |
| 51 | `prime` | ⬜ | n-esimo primo |
| 52 | `totient` | ⬜ | φ di Eulero |
| 53 | `divisors` | ⬜ | Divisori |
| 54 | `gcd` | ⬜ | MCD interi |
| 55 | `lcm` | ⬜ | mcm interi |
| 56 | `mod_inverse` | ⬜ | Inverso modulare |
| 57 | `crt` | ⬜ | Teorema cinese |

### Statistica e probabilità

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 58 | `mean` | ⬜ | |
| 59 | `median` | ⬜ | |
| 20 | `std` | ⬜ | Deviazione standard |
| 61 | `var` | ⬜ | Varianza |
| 62 | `combinations` | ⬜ | Coefficienti binomiali |
| 63 | `permutations` | ⬜ | |
| 64 | `factorial` | ⬜ | |

### Aritmetica di base

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 65 | `evaluate` | ✅ | Calcolo numerico diretto |
| 66 | `round` / `floor` / `ceil` | ⬜ | Arrotondamenti |

---

**Nota:** alcuni numeri sono indicativi. Le operazioni raggruppate
(es. `round`/`floor`/`ceil`) contano come una voce di catalogo ma
potrebbero diventare più operazioni distinte.

**Prossimo blocco pianificato:** Blocco 1 — Fondamentali mancanti.