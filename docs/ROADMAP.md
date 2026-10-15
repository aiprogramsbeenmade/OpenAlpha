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

## Fase 6 — Operazioni matematiche 🚧

Obiettivo: portare OpenAlpha a copertura CAS completa, in blocchi
tematici. Le operazioni sono elencate nell'**Inventario operazioni**
(sotto). T6.3 (linguaggio naturale) e T6.4 (AI locale) sono rimandate
a una versione 2.0.

### Blocco 1 — Fondamentali mancanti ✅

- **T6.1** ✅ `evaluate` — calcolo numerico diretto
- **T6.2** ✅ `series` — sviluppo in serie
- **T6.6** ✅ `dsolve` — equazioni differenziali
- **T6.7** ✅ Blocco algebra: `apart`, `together`, `cancel`, `collect`
- **T6.8** ✅ Blocco teoria dei numeri: `factorint`, `isprime`, `divisors`, `totient`, `prime`

### Blocco 2 — Aritmetica di base ✅

- **T6.9** ✅ `gcd` / `lcm`
- **T6.10** ✅ `factorial`
- **T6.11** ✅ `combinations` / `permutations`
- **T6.12** ✅ `mod_inverse`
- **T6.13** ✅ `round` / `floor` / `ceil`

### Blocco 3 — Sommatorie, serie avanzate, trasformate ⬜

- **T6.14** ⬜ `sum` / `product` (richiede estensione parser per range)
- **T6.15** ⬜ `roots`
- **T6.16** ⬜ `laplace_transform` / `inverse_laplace`
- **T6.17** ⬜ `fourier_transform`

### Blocco 4 — Statistica e probabilità ⬜

- **T6.18** ⬜ `mean`, `median`, `std`, `var` (richiede liste)
- **T6.19** ⬜ `crt` — teorema cinese

### Blocco 5 — Calcolo avanzato ⬜

- **T6.20** ⬜ `diff_partial`, `gradient`, `hessian`, `critical_points`
- **T6.21** ⬜ `integrate_multiple`
- **T6.22** ⬜ `limit_sequence`
- **T6.23** ⬜ `convergence`

### Blocco 6 — Equazioni avanzate ⬜

- **T6.24** ⬜ `solve_inequality`
- **T6.25** ⬜ `solve_system_nonlinear`
- **T6.26** ⬜ `dsolve_system`

### Blocco 7 — Algebra e polinomi (rifinitura) ⬜

- **T6.27** ⬜ `degree`, `coeff`
- **T6.28** ⬜ `gcd_poly`, `lcm_poly`, `div_poly`, `rem_poly`

### Blocco 8 — Algebra lineare ⬜ (richiede parser matrici)

- **T6.29** ⬜ Parser matrici (`[[1, 2], [3, 4]]`)
- **T6.30** ⬜ `det`, `inv`, `transpose`, `rank`, `rref`, `trace`
- **T6.31** ⬜ `eigenvalues`, `eigenvectors`
- **T6.32** ⬜ `lu`, `qr`, `svd`

### Blocco 9 — Geometria analitica (opzionale) ⬜

- **T6.33** ⬜ `distance`, `line_equation`, `intersection`

### Rimandate a v2.0

- Linguaggio naturale (parsing di richieste in italiano/inglese)
- Integrazione AI locale
- API REST pubblica

---

## Stato attuale

**Fase:** 6 — in corso.
**Ultimo task chiuso:** T6.13 (blocco aritmetica di base)
**Prossimo task:** Blocco 3 (sommatorie, serie avanzate, trasformate)

**Numeri:**
- 664 test verdi.
- 24 operazioni implementate.
- 2 interfacce: CLI (`python -m openalpha`) e web UI (`python -m openalpha.web`).
- Bundle `.app` funzionante.

---

## Problemi noti / decisioni rimandate

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
- [2026-10-13] **Posizionamento cursore MathLive**: approssimativo
  (`executeCommand("moveToPreviousChar")` in loop). Funziona per i
  casi comuni, non preciso al carattere.

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
- **2026-10-13**: T5.11a (toggle testo/visuale) completato. 526 test verdi.
- **2026-10-13**: T5.11b (setup MathLive) completato. 526 test verdi.
- **2026-10-13**: T5.11c (integrazione `<math-field>` in modalità visuale) completato. 526 test verdi.
- **2026-10-13**: T5.11d (tastiera in editor visuale) e T5.11e (round-trip testo/visuale stabile) completati. 526 test verdi.
- **2026-10-13**: T5.12d (iconografia Lucide) completato. Fase 5-bis chiusa. 526 test verdi.
- **2026-10-13**: T6.1a (`evaluate`) completato. 554 test verdi.
- **2026-10-14**: T6.2 (`series`) completato. 571 test verdi.
- **2026-10-15**: T6.6 (`dsolve`) completato. 594 test verdi.
- **2026-10-15**: T6.7 (algebra) e T6.8 (teoria dei numeri) completati. 664 test verdi.
- **2026-10-15**: T6.9–T6.13 (blocco aritmetica di base: `gcd`, `lcm`, `factorial`, `combinations`, `permutations`, `mod_inverse`, `round`, `floor`, `ceil`) completati. 742 test verdi.
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
  le operazioni SymPy. Accetta `**func_kwargs` per passare argomenti
  extra alla funzione SymPy.
- **Numerica**: `nsolve` e `nintegrate` restituiscono `APPROXIMATE`.
- **Web UI**: il backend Flask fa da adattatore. Le operazioni restano
  "pure" (producono `Result`), il layer web le adatta al contesto
  (base64 per i grafici, LaTeX per il rendering).
- **Bundle**: PyInstaller include Python, dipendenze, e file statici.
  Il bundle è self-contained (~200 MB).

### Input visuale (T5.11)

**Scelta:** MathLive 0.101.2 (MIT, ~1 MB), editor matematico WYSIWYG.
L'editor **convive** con la barra testuale: toggle "Testo / Visuale".
La tastiera matematica OpenAlpha funziona in entrambe le modalità.
Fallback obbligatorio: se MathLive non carica, resta la modalità Testo.

La tastiera virtuale nativa di MathLive è **disabilitata**
(`mathVirtualKeyboard.mode = "off"`): OpenAlpha usa la propria.
I suoni di MathLive non sono inclusi.

**Conversione tra formati:**
- `convertOpenAlphaToMathLive(str)` — da sintassi OpenAlpha a LaTeX
  per l'inserimento in MathLive.
- `convertMathLiveToOpenAlpha(str)` — da `getValue("ascii-math")`
  di MathLive a sintassi OpenAlpha.

Le due funzioni sono inverse l'una dell'altra per i casi base
(potenze, sqrt, pi, funzioni trigonometriche, chiamate di operazione,
derivate con apici e prime unicode). I frammenti complessi
(`integrate`, `diff`, `solve`, `dsolve`, ...) sono trattati come
testo: MathLive li renderizza in modo funzionale e
`getValue("ascii-math")` li restituisce identici.

### Visualizzazione 3D interattiva

Approccio scelto: **Plotly.js** locale (MIT, ~3 MB), invece di
Three.js o QtWebEngine. Plotly supporta superfici 3D e grafici 2D
interattivi nativamente.

### Rendering dei risultati

Alcune operazioni (es. `factorint`, `divisors`, `isprime`) restituiscono
stringhe formattate che **non** sono espressioni matematiche valide
(es. `"2^2 * 5^2"` verrebbe rivalutato a `100` da SymPy).

Per queste operazioni, il `Result` include `metadata["latex_exact"]` con
il LaTeX già pronto. `app.py` lo usa direttamente, senza passare da
`_try_latex`. Se `latex_exact` è assente, si tenta la conversione
automatica con `_try_latex`.

Questo evita di rivalutare espressioni che perderebbero informazione.
### Ombra delle built-in

Alcune operazioni hanno nomi che coincidono con built-in Python
(`round`, `sum`, `min`, `max`, `abs`). All'interno del modulo, va
usato `builtins.<nome>` per riferirsi alla built-in, altrimenti si
crea ricorsione infinita (es. `round.py` chiamava `round()` che
chiamava se stessa). Questo è il motivo per cui `round.py` importa
`builtins` e usa `builtins.round(...)`.

---

## Inventario operazioni

Stato: ✅ implementata · 🚧 in corso · ⬜ da fare · ⏸️ sospesa

**Contatori:** 33 implementate · 32 pianificate · 65 totali

**Nota:** `taylor` è coperto da `series` (stessa operazione SymPy).
Non è contato separatamente.

### Algebra e polinomi

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 1 | `simplify` | ✅ | |
| 2 | `expand` | ✅ | |
| 3 | `factor` | ✅ | |
| 4 | `apart` | ✅ | Frazioni parziali |
| 5 | `together` | ✅ | Denominatore comune |
| 6 | `cancel` | ✅ | Semplifica razionali |
| 7 | `collect` | ✅ | Raccogli per variabile |
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
| 23 | `series` | ✅ | Sviluppo in serie (Taylor, Maclaurin) |
| 24 | `critical_points` | ⬜ | Punti critici |

### Calcolo integrale

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 25 | `integrate` | ✅ | Indefinito e definito |
| 26 | `integrate_multiple` | ⬜ | Integrali doppi/tripli |

### Limiti

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 27 | `limit` | ✅ | |
| 28 | `limit_sequence` | ⬜ | Limite di successione |

### Equazioni differenziali

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 29 | `dsolve` | ✅ | ODE primo/secondo ordine, con condizioni iniziali |
| 30 | `dsolve_system` | ⬜ | Sistemi di ODE |

### Trasformate

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 31 | `laplace_transform` | ⬜ | |
| 32 | `inverse_laplace` | ⬜ | |
| 33 | `fourier_transform` | ⬜ | |

### Serie e successioni

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 34 | `sum` | ⬜ | Sommatorie |
| 35 | `product` | ⬜ | Produttorie |
| 36 | `convergence` | ⬜ | Criteri di convergenza |

### Algebra lineare

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 37 | `det` | ⬜ | Richiede parser matrici |
| 38 | `inv` | ⬜ | Richiede parser matrici |
| 39 | `transpose` | ⬜ | Richiede parser matrici |
| 40 | `rank` | ⬜ | Richiede parser matrici |
| 41 | `rref` | ⬜ | Richiede parser matrici |
| 42 | `eigenvalues` | ⬜ | Richiede parser matrici |
| 43 | `eigenvectors` | ⬜ | Richiede parser matrici |
| 44 | `trace` | ⬜ | Richiede parser matrici |
| 45 | `lu` | ⬜ | Richiede parser matrici |
| 46 | `qr` | ⬜ | Richiede parser matrici |
| 47 | `svd` | ⬜ | Richiede parser matrici |

### Teoria dei numeri

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 48 | `factorint` | ✅ | Fattorizzazione in primi |
| 49 | `isprime` | ✅ | Test di primalità |
| 50 | `prime` | ✅ | n-esimo primo |
| 51 | `totient` | ✅ | φ di Eulero |
| 52 | `divisors` | ✅ | Divisori |
| 53 | `gcd` | ✅ | MCD interi |
| 54 | `lcm` | ✅ | mcm interi |
| 55 | `mod_inverse` | ✅ | Inverso modulare |
| 56 | `crt` | ⬜ | Teorema cinese |

### Statistica e probabilità

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 57 | `mean` | ⬜ | |
| 58 | `median` | ⬜ | |
| 59 | `std` | ⬜ | Deviazione standard |
| 60 | `var` | ⬜ | Varianza |
| 61 | `combinations` | ✅ | Coefficienti binomiali |
| 62 | `permutations` | ✅ | |
| 63 | `factorial` | ✅ | |

### Aritmetica di base

| # | Operazione | Stato | Note |
|---|-----------|-------|------|
| 64 | `evaluate` | ✅ | Calcolo numerico diretto |
| 65 | `round` / `floor` / `ceil` | ✅ | Arrotondamenti |

---

**Nota:** alcuni numeri sono indicativi. Le operazioni raggruppate
(es. `round`/`floor`/`ceil`) contano come una voce di catalogo ma
potrebbero diventare più operazioni distinte.

**Prossimo blocco pianificato:** Blocco 2 — Aritmetica di base.