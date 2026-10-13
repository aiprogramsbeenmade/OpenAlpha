# OpenAlpha

Calcolatore matematico locale, open source e modulare.
Obiettivo: fornire risultati corretti con spiegazioni verificate,
funzionamento offline, e nessun costo.

## Stato

Progetto in sviluppo attivo. **Fasi 0–5 completate.**

- 520 test automatici verdi.
- 12 operazioni disponibili.
- Due interfacce: CLI e web UI.
- Bundle `.app` funzionante (doppio click su macOS).
- Parser proprio, senza `eval`/`exec`.
- Spiegazioni verificate per algebra elementare.
- Grafici 2D e 3D interattivi nella web UI.

## Requisiti

- Python 3.10+ (per uso da sorgente)
- macOS, Linux o Windows
- Nessuna connessione Internet richiesta

## Installazione

Assumendo che la virtualenv sia già attiva:

    pip install -r requirements-dev.txt

## Uso

### CLI

Semplificare un'espressione:

    python -m openalpha "sin(x)**2 + cos(x)**2"

Sviluppare, fattorizzare, risolvere:

    python -m openalpha --operation expand "(x + 1)**2"
    python -m openalpha --operation factor "x**2 + 2*x + 1"
    python -m openalpha --operation solve "x**2 - 1 = 0"

Calcolo:

    python -m openalpha --operation limit "sin(x)/x"
    python -m openalpha --operation diff "sin(x)"
    python -m openalpha --operation integrate "x**2"

Numerica:

    python -m openalpha --operation nsolve "x**5 - x + 1" --initial -1
    python -m openalpha --operation nintegrate --from 0 --to 1 "exp(-x**2)"

Grafici:

    python -m openalpha --operation plot "sin(x)"
    python -m openalpha --operation plot3d "x**2 + y**2"

Elenco e aiuto:

    python -m openalpha --list
    python -m openalpha --help

### Web UI

    python -m openalpha.web

Il browser si apre automaticamente su `http://127.0.0.1:5000`.
La web UI include:

- Barra di input con anteprima renderizzata.
- Tastiera matematica (Basic, Calculus, Algebra, Trig, Plot).
- Risultati renderizzati con MathJax.
- Grafici 2D e 3D interattivi (Plotly).
- Cronologia persistente.
- Copia/esportazione (LaTeX, testo, PNG, JSON).

### App desktop

Se hai costruito il bundle (`pyinstaller openalpha.spec`):

- **macOS**: `open dist/OpenAlpha.app`
- **Windows**: `dist\OpenAlpha.exe`
- **Linux**: `./dist/OpenAlpha`

## Operazioni disponibili

| Operazione | Descrizione |
|-----------|-------------|
| `simplify` | Semplifica un'espressione algebrica |
| `expand` | Sviluppa prodotti e potenze |
| `factor` | Fattorizza un'espressione |
| `solve` | Risolve un'equazione in una variabile |
| `solve_system` | Risolve un sistema di equazioni lineari |
| `limit` | Calcola il limite di un'espressione |
| `diff` | Calcola la derivata |
| `integrate` | Calcola l'integrale indefinito o definito |
| `nsolve` | Trova numericamente una radice |
| `nintegrate` | Calcola numericamente un integrale definito |
| `plot` | Genera un grafico 2D |
| `plot3d` | Genera un grafico 3D |

## Sintassi supportata

- **Numeri**: `2`, `3.14`, `1e-3`
- **Variabili**: `x`, `y`, `alpha`
- **Operatori**: `+`, `-`, `*`, `/`, `**`, `^`
- **Parentesi**: `(`, `)`
- **Moltiplicazione implicita**: `2x`, `2(x+1)`, `(x+1)(x-1)`
- **Funzioni**: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`,
  `cosh`, `tanh`, `exp`, `log`, `sqrt`, `abs`
- **Costanti**: `pi`, `e`

Nella web UI, funzioni di alto livello come `integrate(x**2, x)`,
`diff(sin(x), x)`, `plot(sin(x))` sono riconosciute automaticamente.

## Condizioni e dominio

Le operazioni restituiscono `status=partial` quando il risultato ha
condizioni di validità. Esempio:

    python -m openalpha "1/x"

Output:

    status:      partial
    exact:       1/x
    conditions:  x != 0

## Spiegazioni

Quando possibile, OpenAlpha mostra i **passaggi verificati** del
procedimento. Ogni passo è prodotto da una regola esplicita, mai
inventato. Se il software non ha un procedimento verificato, lo
dichiara.

La politica completa è in [`docs/EXPLANATIONS.md`](docs/EXPLANATIONS.md).

## Test

    python -m pytest tests/ -v

**Nota:** usare `python -m pytest`, non `pytest`, per garantire
l'uso dell'interprete della virtualenv.

## Struttura

    openalpha/
      core/            # modello di risultato, stato, eccezioni, registro, Step
      parser/          # tokenizer, parser, AST, validatore, to_sympy
      operations/      # operazioni, divise per dominio
        algebra/       # simplify, expand, factor
        equations/     # solve, solve_system
        calculus/      # limit, diff, integrate
        numeric/       # nsolve, nintegrate
        visualization/ # plot, plot3d
      explanations/    # regole, motore, formatter, dominio
      cli/             # interfaccia a riga di comando
      web/             # web UI locale
        app.py         # server Flask
        launcher.py    # launcher con porta libera
        templates/     # HTML
        static/        # CSS, JS, MathJax, Plotly
    tests/             # test automatici
    docs/              # documentazione e roadmap
    examples/          # script d'uso

## Come costruire l'app desktop

OpenAlpha può essere impacchettato come applicazione standalone
(non richiede Python né dipendenze installate).

### Requisiti

- PyInstaller: `pip install pyinstaller`
- macOS, Linux o Windows

### Costruzione

Dalla root del progetto:

    pyinstaller openalpha.spec

Output:

- **macOS**: `dist/OpenAlpha.app`
- **Windows**: `dist/OpenAlpha.exe`
- **Linux**: `dist/OpenAlpha`
### Scaricare MathJax e Plotly

Dalla root del progetto:

    # MathJax (per il rendering delle formule)
    mkdir -p openalpha/web/static/mathjax
    curl -L -o openalpha/web/static/mathjax/tex-svg.js \
      https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js

    # Plotly (per i grafici interattivi)
    mkdir -p openalpha/web/static/plotly
    curl -L -o openalpha/web/static/plotly/plotly.min.js \
      https://cdn.plot.ly/plotly-2.35.2.min.js
### Note

- **macOS**: al primo avvio, Gatekeeper potrebbe bloccare l'app.
  Vai in *Impostazioni di Sistema → Privacy e Sicurezza* e autorizza.
  Oppure, da terminale: `xattr -cr dist/OpenAlpha.app`
- Il bundle è **grande** (~200 MB) perché include Python e tutte
  le dipendenze (SymPy, NumPy, Matplotlib, Flask, Plotly, ...).
- Il bundle è **self-contained**: funziona su qualsiasi Mac con
  la stessa architettura, senza installare nulla.

### Modalità di input

L'interfaccia web supporta due modalità di input, commutabili con il
toggle **Testo / Visuale** nella barra:

- **Testo**: si scrive l'espressione in sintassi OpenAlpha
  (`(x+1)**2`, `integrate(x**2, x)`, `solve(x**2 - 1 = 0)`).
  È la modalità di default e funziona sempre.
- **Visuale**: si scrive l'espressione in un editor matematico
  interattivo (MathLive). L'editor produce la stessa sintassi
  OpenAlpha internamente, quindi tutte le operazioni funzionano
  in entrambe le modalità.

La tastiera matematica (Basic, Calculus, Algebra, Trig, Plot)
funziona in entrambe le modalità.

Se MathLive non è disponibile, la modalità Visuale non si attiva
e resta solo quella Testuale (fallback automatico).

## Filosofia

- Il motore matematico non dipende dall'interfaccia.
- Non si dichiara un risultato esatto se è solo un'approssimazione.
- Non si inventano passaggi matematici.
- L'input non viene mai valutato con `eval` o `exec`.
- Il parser accetta una sintassi esplicita e rifiuta il resto.
- Funziona offline, senza costi, su hardware modesto.

## Documentazione

- [`docs/ROADMAP.md`](docs/ROADMAP.md) — stato e prossimi passi.
- [`docs/EXPLANATIONS.md`](docs/EXPLANATIONS.md) — politica delle spiegazioni.

## Licenza

Open source. Licenza da definire (probabilmente MIT).