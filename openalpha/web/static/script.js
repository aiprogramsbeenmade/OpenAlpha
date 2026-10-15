/* Gestione dell'interazione utente per OpenAlpha web. */

const HISTORY_KEY = "openalpha_history";
const HISTORY_MAX = 50;

function initOpenAlpha() {

    // ---------------------------------------------------------------------
    // Icone (SVG inline, da Lucide — ISC license)
    // ---------------------------------------------------------------------

    const ICONS = {
        latex: '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon" aria-hidden="true"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M10 12a1 1 0 0 0-1 1v1a1 1 0 0 1-1 1 1 1 0 0 1 1 1v1a1 1 0 0 0 1 1"/><path d="M14 18a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1 1 1 0 0 1-1-1v-1a1 1 0 0 0-1-1"/></svg>',
        text: '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon" aria-hidden="true"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M8 4H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/><path d="M16 4h2a2 2 0 0 1 2 2v4"/><path d="M21 14H11"/><path d="m15 10-4 4 4 4"/></svg>',
        png: '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon" aria-hidden="true"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>',
        json: '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon" aria-hidden="true"><path d="M14 22h4a2 2 0 0 0 2-2V8a2.4 2.4 0 0 0-.706-1.706l-3.588-3.588A2.4 2.4 0 0 0 14 2H6a2 2 0 0 0-2 2v6"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M5 14a1 1 0 0 0-1 1v2a1 1 0 0 1-1 1 1 1 0 0 1 1 1v2a1 1 0 0 0 1 1"/><path d="M9 22a1 1 0 0 0 1-1v-2a1 1 0 0 1 1-1 1 1 0 0 1-1-1v-2a1 1 0 0 0-1-1"/></svg>',
        check: '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
        x: '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>',
        broom: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-lg" aria-hidden="true"><path d="M11 2v2"/><path d="M12 3h-2"/><path d="M13.5 10.5 22 2"/><path d="M14.734 13.841a2 2 0 00-.314-2.42L12.58 9.58a2 2 0 00-2.421-.314l-7.657 4.461A1 1 0 002.3 15.3l6.403 6.403a1 1 0 001.571-.204z"/><path d="M20 15v4"/><path d="M22 17h-4"/><path d="M4 4v4"/><path d="m5 18 2-2"/><path d="M6 6H2"/><path d="m7.699 10.7 5.602 5.601"/></svg>',
    };


    const inputField = document.getElementById("input-expression");
    const calculateButton = document.getElementById("calculate-button");
    const resultContent = document.getElementById("result-content");
    const operationSelect = document.getElementById("operation-select");
    const previewDiv = document.getElementById("preview");
    const historyList = document.getElementById("history-list");
    const clearHistoryButton = document.getElementById("clear-history");
    const resultArea = document.querySelector(".result-area");

    const modeTextBtn = document.getElementById("mode-text-btn");
    const modeVisualBtn = document.getElementById("mode-visual-btn");
    const inputSlotText = document.getElementById("input-slot-text");
    const inputSlotVisual = document.getElementById("input-slot-visual");

    const visualEditor = document.getElementById("visual-editor");

    // Disabilita la tastiera virtuale nativa di MathLive:
    // OpenAlpha usa la propria tastiera matematica.
    if (window.mathVirtualKeyboard) {
        window.mathVirtualKeyboard.mode = "off";
    }

    let previewTimer = null;

    // ---------------------------------------------------------------------
    // Modalità di input (testo / visuale)
    // ---------------------------------------------------------------------

    let currentExpression = "";

    let activeMode = "text"; // "text" | "visual"

    function getActiveMode() {
        return activeMode;
    }

    function getExpression() {
        if (activeMode === "text") {
            return inputField.value;
        }
        if (visualEditor) {
            // MathLive 0.101.2: "text" non è un formato valido.
            // "ascii-math" produce sintassi matematica informale
            // (es. "(x+1)^2", "sqrt(2)") che convertiamo in sintassi
            // OpenAlpha. "latex" produrrebbe "\frac{}{}", "\sqrt{}",
            // che il parser OpenAlpha non accetta.
            let raw = "";
            try {
                raw = visualEditor.getValue("ascii-math") || "";
            } catch (err) {
                console.warn("[OpenAlpha] getValue('ascii-math') fallito, fallback su 'latex':", err);
                try {
                    raw = visualEditor.getValue("latex") || "";
                } catch (err2) {
                    console.error("[OpenAlpha] getValue fallito del tutto:", err2);
                    raw = visualEditor.value || "";
                }
            }
            return convertMathLiveToOpenAlpha(raw);
        }
        return currentExpression;
    }

    function setExpression(value) {
        currentExpression = value ?? "";
        if (activeMode === "text") {
            inputField.value = currentExpression;
        } else if (visualEditor) {
            // Converte la sintassi OpenAlpha in LaTeX prima di
            // scrivere nell'editor MathLive. Altrimenti MathLive
            // interpreta `**` come due asterischi e rende male.
            const latex = convertOpenAlphaToMathLive(currentExpression).mathlive;
            visualEditor.value = latex;
        }
    }

    function setActiveMode(mode) {
        if (mode !== "text" && mode !== "visual") return;
        if (mode === activeMode) return;

        const previous = getExpression();

        activeMode = mode;
        currentExpression = previous;

        if (mode === "text") {
            inputSlotText.hidden = false;
            inputSlotVisual.hidden = true;
            modeTextBtn.classList.add("active");
            modeTextBtn.setAttribute("aria-selected", "true");
            modeVisualBtn.classList.remove("active");
            modeVisualBtn.setAttribute("aria-selected", "false");
            inputField.value = currentExpression;
            inputField.focus();
        } else {
            inputSlotText.hidden = true;
            inputSlotVisual.hidden = false;
            modeTextBtn.classList.remove("active");
            modeTextBtn.setAttribute("aria-selected", "false");
            modeVisualBtn.classList.add("active");
            modeVisualBtn.setAttribute("aria-selected", "true");
            if (visualEditor) {
                // Stessa conversione di setExpression: da OpenAlpha a LaTeX.
                const latex = convertOpenAlphaToMathLive(currentExpression).mathlive;
                visualEditor.value = latex;
                visualEditor.focus();
            }
        }

        if (previewTimer) clearTimeout(previewTimer);
        previewTimer = setTimeout(aggiornaAnteprima, 100);
    }

    modeTextBtn.addEventListener("click", () => setActiveMode("text"));
    modeVisualBtn.addEventListener("click", () => setActiveMode("visual"));

    // ---------------------------------------------------------------------
    // Conversione MathLive -> sintassi OpenAlpha
    // ---------------------------------------------------------------------

    function convertMathLiveToOpenAlpha(raw) {
        if (!raw) return "";
        let s = raw.trim();

        // Normalizza spazi unicode e simboli comuni.
        s = s.replace(/\u00A0/g, " ");
        s = s.replace(/×/g, "*");
        s = s.replace(/÷/g, "/");
        s = s.replace(/−/g, "-");

        // Residui LaTeX: \left( \right) \cdot \times \div
        s = s.replace(/\\left\s*\(/g, "(");
        s = s.replace(/\\right\s*\)/g, ")");
        s = s.replace(/\\left\s*\[/g, "(");
        s = s.replace(/\\right\s*\]/g, ")");
        s = s.replace(/\\cdot/g, "*");
        s = s.replace(/\\times/g, "*");
        s = s.replace(/\\div/g, "/");

        // Frazioni LaTeX: \frac{a}{b} -> (a)/(b)
        s = s.replace(/\\frac\s*\{([^}]*)\}\s*\{([^}]*)\}/g, "($1)/($2)");

        // Radici LaTeX: \sqrt{a} -> sqrt(a)
        s = s.replace(/\\sqrt\s*\{([^}]*)\}/g, "sqrt($1)");

        // Funzioni LaTeX: \sin -> sin, \cos -> cos, ecc.
        s = s.replace(/\\(sin|cos|tan|asin|acos|atan|log|ln|exp|abs)/g, "$1");

        // Simboli greci comuni.
        s = s.replace(/\\pi/g, "pi");
        s = s.replace(/\\alpha/g, "alpha");
        s = s.replace(/\\beta/g, "beta");
        s = s.replace(/\\theta/g, "theta");
        s = s.replace(/\\lambda/g, "lambda");

        // Derivate: MathLive esporta y' in vari formati, a seconda
        // del contesto:
        //   - y'           (apostrofo ASCII)
        //   - y^'          (apice + apostrofo ASCII)
        //   - y^{\prime}   (LaTeX)
        //   - y^′          (apice + U+2032 PRIME unicode)
        //   - y′           (U+2032 PRIME unicode)
        // Li normalizziamo tutti in y', y'', y'''.
        //
        // Triple prime (U+2034), doppio prime (U+2033), prime (U+2032).
        s = s.replace(/\^\{\\prime\\prime\\prime\}/g, "'''");
        s = s.replace(/\^\{\\prime\\prime\}/g, "''");
        s = s.replace(/\^\{\\prime\}/g, "'");
        s = s.replace(/\^\\prime\\prime\\prime/g, "'''");
        s = s.replace(/\^\\prime\\prime/g, "''");
        s = s.replace(/\^\\prime/g, "'");
        s = s.replace(/\^\u2034/g, "'''");   // ^‴
        s = s.replace(/\^\u2033/g, "''");    // ^″
        s = s.replace(/\^\u2032/g, "'");     // ^′
        s = s.replace(/\u2034/g, "'''");     // ‴
        s = s.replace(/\u2033/g, "''");      // ″
        s = s.replace(/\u2032/g, "'");       // ′
        s = s.replace(/\^'/g, "'");          // ^'
        s = s.replace(/\^"/g, "'");          // ^" (a volte MathLive usa doppio apice ASCII)

        // Potenza: `^` -> `**`. Va fatto dopo i replace LaTeX,
        // altrimenti si rischia di toccare `**` già presenti.
        s = s.replace(/\^\{([^}]*)\}/g, "**($1)");
        s = s.replace(/\^\(([^)]*)\)/g, "**($1)");
        s = s.replace(/\^([0-9a-zA-Z])/g, "**$1");

        // Radice unicode.
        s = s.replace(/√/g, "sqrt");

        // Pi greco unicode.
        s = s.replace(/π/g, "pi");

        // Pulizia spazi multipli.
        s = s.replace(/\s+/g, " ").trim();

        return s;
    }

    // ---------------------------------------------------------------------
    // Conversione OpenAlpha -> LaTeX (per inserimento in MathLive)
    // ---------------------------------------------------------------------
    //
    // I frammenti della tastiera sono in sintassi OpenAlpha. MathLive
    // si aspetta LaTeX per il rendering. Questa funzione converte i
    // frammenti semplici (potenze, sqrt, pi, sin, ecc.) in LaTeX, e
    // lascia invariati i frammenti "complessi" (integrate, diff, ecc.)
    // che MathLive renderizza come testo e riesporta identici.
    //
    // Restituisce { mathlive, openAlpha }:
    //   mathlive: stringa LaTeX (o testo) da passare a mathfield.insert()
    //   openAlpha: stringa OpenAlpha "equivalente" dopo l'inserimento
    //              (usata per aggiornare lo stato interno)
    function convertOpenAlphaToMathLive(text) {
        if (!text) return { mathlive: "", openAlpha: "" };

        let s = text;

        // Converti SEMPRE `**` -> `^`, anche dentro le chiamate
        // di operazione (integrate, diff, ecc.). MathLive interpreta
        // `^` come apice; `**` come doppio apice vuoto, che rompe
        // la formula e produce `****` al round-trip.
        s = s.replace(/\*\*/g, "^");

        // Radice quadrata: sqrt(x) -> \sqrt{x}.
        s = s.replace(/sqrt\(([^)]*)\)/g, "\\sqrt{$1}");

        // Pi greco.
        s = s.replace(/\bpi\b/g, "\\pi");

        // Funzioni trigonometriche e logaritmiche.
        s = s.replace(/\b(sin|cos|tan|asin|acos|atan|log|ln|exp|abs)\(/g, "\\$1(");

        // Simboli greci comuni.
        s = s.replace(/\balpha\b/g, "\\alpha");
        s = s.replace(/\bbeta\b/g, "\\beta");
        s = s.replace(/\btheta\b/g, "\\theta");
        s = s.replace(/\blambda\b/g, "\\lambda");

        return { mathlive: s, openAlpha: text };
    }

    // ---------------------------------------------------------------------
    // Caricamento operazioni
    // ---------------------------------------------------------------------

    async function caricaOperazioni() {
        try {
            const response = await fetch("/api/operations");
            const data = await response.json();
            operationSelect.innerHTML = "";
            for (const op of data.operations) {
                const option = document.createElement("option");
                option.value = op.name;
                option.textContent = op.name;
                option.title = op.description;
                operationSelect.appendChild(option);
            }
            operationSelect.value = "simplify";
        } catch (err) {
            console.error("Errore nel caricamento delle operazioni:", err);
        }
    }

    // ---------------------------------------------------------------------
    // Tastiera
    // ---------------------------------------------------------------------

    function setupTastiera() {
        document.querySelectorAll(".keyboard-tabs .tab").forEach((tab) => {
            tab.addEventListener("click", () => {
                document.querySelectorAll(".keyboard-tabs .tab").forEach((t) => t.classList.remove("active"));
                document.querySelectorAll(".keyboard-panel").forEach((p) => p.classList.remove("active"));
                tab.classList.add("active");
                const panel = document.querySelector(`.keyboard-panel[data-panel="${tab.dataset.tab}"]`);
                if (panel) panel.classList.add("active");
            });
        });

        document.querySelectorAll(".keyboard-panel button").forEach((button) => {
            button.addEventListener("click", () => {
                const insert = button.dataset.insert || "";
                const offset = parseInt(button.dataset.cursorOffset || "0", 10);
                inserisciFrammento(insert, offset);
            });
        });
    }

    function inserisciFrammento(text, cursorOffset) {
        if (activeMode === "text") {
            inserisciInTesto(text, cursorOffset);
        } else if (activeMode === "visual") {
            inserisciInVisuale(text, cursorOffset);
        }
    }

    function inserisciInTesto(text, cursorOffset) {
        const start = inputField.selectionStart ?? inputField.value.length;
        const end = inputField.selectionEnd ?? inputField.value.length;
        const before = inputField.value.substring(0, start);
        const after = inputField.value.substring(end);
        inputField.value = before + text + after;

        let newPos = start + text.length;
        if (cursorOffset < 0) {
            newPos = start + text.length + cursorOffset;
        } else if (cursorOffset > 0) {
            newPos = start + cursorOffset;
        }
        inputField.setSelectionRange(newPos, newPos);
        inputField.focus();

        if (previewTimer) clearTimeout(previewTimer);
        previewTimer = setTimeout(aggiornaAnteprima, 300);
    }

    function inserisciInVisuale(text, cursorOffset) {
        if (!visualEditor) return;

        // Converte il frammento OpenAlpha in LaTeX per MathLive.
        // Per frammenti "complessi" (integrate, diff, ecc.) la conversione
        // è identità: MathLive li renderizza come testo e li riesporta
        // identici con getValue("ascii-math").
        const latex = convertOpenAlphaToMathLive(text);
        const openAlphaAfter = latex.openAlpha;

        try {
            visualEditor.insert(latex.mathlive);
        } catch (err) {
            console.error("[OpenAlpha] insert MathLive fallito:", err);
            return;
        }

        // Posiziona il cursore se richiesto.
        if (cursorOffset !== 0) {
            // MathLive non espone un'API diretta per spostare il cursore
            // di N posizioni. Usiamo executeCommand("moveToMathfieldEnd")
            // come fallback per ora, e gestiamo il posizionamento fine
            // in T5.11e.
            try {
                if (cursorOffset < 0) {
                    // Sposta indietro il cursore di |cursorOffset| posizioni.
                    // MathLive non ha un comando diretto, quindi spostiamo
                    // a fine campo e poi muoviamo indietro.
                    for (let i = 0; i < Math.abs(cursorOffset); i++) {
                        visualEditor.executeCommand("moveToPreviousChar");
                    }
                }
            } catch (err) {
                console.warn("[OpenAlpha] posizionamento cursore fallito:", err);
            }
        }

        visualEditor.focus();

        // Aggiorna currentExpression e anteprima.
        currentExpression = getExpression();
        if (previewTimer) clearTimeout(previewTimer);
        previewTimer = setTimeout(aggiornaAnteprima, 300);
    }

    // ---------------------------------------------------------------------
    // Anteprima
    // ---------------------------------------------------------------------

    inputField.addEventListener("input", () => {
        if (activeMode !== "text") return;
        currentExpression = inputField.value;
        if (previewTimer) clearTimeout(previewTimer);
        previewTimer = setTimeout(aggiornaAnteprima, 300);
    });

    if (visualEditor) {
        visualEditor.addEventListener("input", () => {
            if (activeMode !== "visual") return;
            currentExpression = getExpression();
            if (previewTimer) clearTimeout(previewTimer);
            previewTimer = setTimeout(aggiornaAnteprima, 300);
        });
    }

    async function aggiornaAnteprima() {
        const expr = getExpression().trim();
        if (!expr) {
            previewDiv.innerHTML = "";
            return;
        }
        const parsed = analizzaInput(expr);
        const previewExpr = parsed ? parsed.expression : expr;

        try {
            const response = await fetch("/api/render", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ expr: previewExpr }),
            });
            const data = await response.json();
            if (data.latex) {
                previewDiv.innerHTML = `\\[${data.latex}\\]`;
                if (window.MathJax && window.MathJax.typesetPromise) {
                    window.MathJax.typesetPromise([previewDiv]);
                }
            } else {
                previewDiv.innerHTML = `<code>${escapeHtml(previewExpr)}</code>`;
            }
        } catch (err) {
            console.error("Errore anteprima:", err);
        }
    }

    // ---------------------------------------------------------------------
    // Parsing di alto livello
    // ---------------------------------------------------------------------

    function analizzaInput(expr) {
        const patterns = [
            // ---- Serie e calcolo ----
            {
                name: "series",
                regex: /^\s*series\s*\(\s*(.+?)\s*,\s*(\w+)\s*,\s*(.+?)\s*,\s*(\d+)\s*\)\s*$/,
                build: (m) => ({
                    expression: m[1],
                    params: { var: m[2], point: m[3], order: parseInt(m[4], 10) },
                }),
            },
            {
                name: "series",
                regex: /^\s*series\s*\(\s*(.+?)\s*,\s*(\w+)\s*,\s*(.+?)\s*\)\s*$/,
                build: (m) => ({
                    expression: m[1],
                    params: { var: m[2], point: m[3] },
                }),
            },
            {
                name: "series",
                regex: /^\s*series\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "integrate",
                regex: /^\s*integrate\s*\(\s*(.+?)\s*,\s*(\w+)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: { var: m[2] } }),
            },
            {
                name: "diff",
                regex: /^\s*diff\s*\(\s*(.+?)\s*,\s*(\w+)\s*(?:,\s*(\d+)\s*)?\)\s*$/,
                build: (m) => ({
                    expression: m[1],
                    params: { var: m[2], order: m[3] ? parseInt(m[3], 10) : 1 },
                }),
            },
            {
                name: "limit",
                regex: /^\s*limit\s*\(\s*(.+?)\s*,\s*(\w+)\s*,\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: { var: m[2], point: m[3] } }),
            },
            {
                name: "dsolve",
                regex: /^\s*dsolve\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },

            // ---- Equazioni ----
            {
                name: "nsolve",
                regex: /^\s*nsolve\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "solve_system",
                regex: /^\s*solve_system\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "solve",
                regex: /^\s*solve\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },

            // ---- Grafici ----
            {
                name: "plot3d",
                regex: /^\s*plot3d\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "plot",
                regex: /^\s*plot\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },

            // ---- Algebra ----
            {
                name: "collect",
                regex: /^\s*collect\s*\(\s*(.+?)\s*(?:,\s*(\w+)\s*)?\)\s*$/,
                build: (m) => ({
                    expression: m[1],
                    params: m[2] ? { var: m[2] } : {},
                }),
            },
            {
                name: "apart",
                regex: /^\s*apart\s*\(\s*(.+?)\s*(?:,\s*(\w+)\s*)?\)\s*$/,
                build: (m) => ({
                    expression: m[1],
                    params: m[2] ? { var: m[2] } : {},
                }),
            },
            {
                name: "together",
                regex: /^\s*together\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "cancel",
                regex: /^\s*cancel\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "roots",
                regex: /^\s*roots\s*\(\s*(.+?)\s*(?:,\s*(\w+)\s*)?\)\s*$/,
                build: (m) => ({
                    expression: m[1],
                    params: m[2] ? { var: m[2] } : {},
                }),
            },

            // ---- Teoria dei numeri ----
            {
                name: "factorint",
                regex: /^\s*factorint\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "isprime",
                regex: /^\s*isprime\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "divisors",
                regex: /^\s*divisors\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "totient",
                regex: /^\s*totient\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "prime",
                regex: /^\s*prime\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "gcd",
                regex: /^\s*gcd\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: { b: m[2] } }),
            },
            {
                name: "lcm",
                regex: /^\s*lcm\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: { b: m[2] } }),
            },
            {
                name: "mod_inverse",
                regex: /^\s*mod_inverse\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: { m: m[2] } }),
            },
            {
                name: "factorial",
                regex: /^\s*factorial\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "combinations",
                regex: /^\s*combinations\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: { k: m[2] } }),
            },
            {
                name: "permutations",
                regex: /^\s*permutations\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: { k: m[2] } }),
            },

            // ---- Aritmetica ----
            {
                name: "evaluate",
                regex: /^\s*evaluate\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "round",
                regex: /^\s*round\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "floor",
                regex: /^\s*floor\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
            {
                name: "ceil",
                regex: /^\s*ceil\s*\(\s*(.+?)\s*\)\s*$/,
                build: (m) => ({ expression: m[1], params: {} }),
            },
        ];

        for (const p of patterns) {
            const m = expr.match(p.regex);
            if (m) {
                const built = p.build(m);
                return { operation: p.name, expression: built.expression, params: built.params };
            }
        }
        return null;
    }
    // ---------------------------------------------------------------------
    // Esecuzione
    // ---------------------------------------------------------------------

    async function esegui() {
        const raw = getExpression().trim();
        if (!raw) return;

        resultContent.innerHTML = `
            <div class="loading-container">
                <span class="spinner"></span>
                <span>Calcolo in corso...</span>
            </div>
        `;

        let operation, expression, params;
        const parsed = analizzaInput(raw);
        if (parsed) {
            operation = parsed.operation;
            expression = parsed.expression;
            params = parsed.params;
        } else {
            operation = operationSelect.value;
            expression = raw;
            params = {};
        }

        if (operation === "plot3d") {
            await eseguiPlot3D(expression, params, raw);
            return;
        }
        if (operation === "plot") {
            await eseguiPlot2D(expression, params, raw);
            return;
        }

        await eseguiOperazione(operation, expression, params, raw);
    }

    async function eseguiOperazione(operation, expression, params, rawForHistory) {
        resultContent.innerHTML = `
            <div class="loading-container">
                <span class="spinner"></span>
                <span>Calcolo in corso...</span>
            </div>
        `;

        try {
            const response = await fetch("/api/execute", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ operation, expression, params }),
            });
            const data = await response.json();
            if (!response.ok) {
                mostraErrore(data.error || "Errore sconosciuto");
                return;
            }
            mostraRisultato(data);
            if (data.status !== "error") {
                aggiungiAllaCronologia({
                    operation,
                    expression,
                    params,
                    raw: rawForHistory || expression,
                    exact: data.exact,
                });
            }
        } catch (err) {
            mostraErrore("Errore di rete: " + err.message);
        }
    }

    // ---------------------------------------------------------------------
    // Plot 2D
    // ---------------------------------------------------------------------

    async function eseguiPlot2D(expression, params, rawForHistory) {
        try {
            const response = await fetch("/api/plot2d-data", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    expression,
                    var: params.var || "x",
                    xmin: params.xmin || "-10",
                    xmax: params.xmax || "10",
                }),
            });
            const data = await response.json();

            if (!response.ok) {
                mostraErrore(data.error || "Errore sconosciuto");
                return;
            }

            mostraPlot2D(data);

            aggiungiAllaCronologia({
                operation: "plot",
                expression,
                params,
                raw: rawForHistory || expression,
                exact: "(grafico 2D)",
            });
        } catch (err) {
            mostraErrore("Errore di rete: " + err.message);
        }
    }

    function mostraPlot2D(data) {
        resultContent.innerHTML = `
            <p><strong>Operazione:</strong> plot</p>
            <p><strong>Stato:</strong> exact</p>
            <div id="plot2d-container" class="plot-2d-container"></div>
        `;

        const container = document.getElementById("plot2d-container");

        const trace = {
            type: "scatter",
            mode: "lines",
            x: data.x_values,
            y: data.y_values,
            line: { color: "#d94b2b", width: 2 },
            name: data.title,
            hovertemplate: "x = %{x:.4g}<br>y = %{y:.4g}<extra></extra>",
        };

        const layout = {
            title: data.title,
            xaxis: { title: data.xvar, zeroline: true, zerolinecolor: "#d94b2b", zerolinewidth: 1 },
            yaxis: { title: "y", zeroline: true, zerolinecolor: "#d94b2b", zerolinewidth: 1 },
            margin: { l: 50, r: 20, t: 40, b: 40 },
            autosize: false,
            width: container.offsetWidth || 700,
            height: 400,
            hovermode: "closest",
        };

        const config = {
            responsive: true,
            displaylogo: false,
            scrollZoom: true,
        };

        Plotly.newPlot(container, [trace], layout, config);

        if (resultArea) {
            resultArea.classList.remove("fade-in");
            void resultArea.offsetWidth;
            resultArea.classList.add("fade-in");
        }
    }

    // ---------------------------------------------------------------------
    // Plot 3D
    // ---------------------------------------------------------------------

    async function eseguiPlot3D(expression, params, rawForHistory) {
        try {
            const response = await fetch("/api/plot3d-data", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    expression,
                    xvar: params.xvar || "x",
                    yvar: params.yvar || "y",
                    xmin: params.xmin || "-5",
                    xmax: params.xmax || "5",
                    ymin: params.ymin || "-5",
                    ymax: params.ymax || "5",
                }),
            });
            const data = await response.json();

            if (!response.ok) {
                mostraErrore(data.error || "Errore sconosciuto");
                return;
            }

            mostraPlot3D(data);

            aggiungiAllaCronologia({
                operation: "plot3d",
                expression,
                params,
                raw: rawForHistory || expression,
                exact: "(grafico 3D)",
            });
        } catch (err) {
            mostraErrore("Errore di rete: " + err.message);
        }
    }

    function mostraPlot3D(data) {
        resultContent.innerHTML = `
            <p><strong>Operazione:</strong> plot3d</p>
            <p><strong>Stato:</strong> exact</p>
            <div id="plot3d-container" class="plot-3d-container"></div>
        `;

        const container = document.getElementById("plot3d-container");

        const trace = {
            type: "surface",
            x: data.x_values,
            y: data.y_values,
            z: data.z_matrix,
            colorscale: "Viridis",
            showscale: true,
        };

        const layout = {
            title: data.title,
            scene: {
                xaxis: { title: data.xvar },
                yaxis: { title: data.yvar },
                zaxis: { title: "z" },
            },
            margin: { l: 0, r: 0, t: 40, b: 0 },
            autosize: false,
            width: container.offsetWidth || 700,
            height: 500,
        };

        const config = {
            responsive: true,
            displaylogo: false,
        };

        Plotly.newPlot(container, [trace], layout, config);

        if (resultArea) {
            resultArea.classList.remove("fade-in");
            void resultArea.offsetWidth;
            resultArea.classList.add("fade-in");
        }
    }

    // ---------------------------------------------------------------------
    // Rendering del risultato
    // ---------------------------------------------------------------------

    function mostraRisultato(data) {
        let html = "";
        html += `<p><strong>Operazione:</strong> ${escapeHtml(data.operation)}</p>`;
        html += `<p><strong>Stato:</strong> ${escapeHtml(data.status)}</p>`;

        if (data.plot_data) {
            html += `<div class="plot-container">`;
            html += `<img src="data:image/png;base64,${data.plot_data}" alt="Grafico" class="plot-image">`;
            html += `</div>`;
        } else if (data.exact) {
            html += `<p><strong>Risultato esatto:</strong></p>`;
            if (data.latex && data.latex.exact) {
                html += `<div class="math">\\[${data.latex.exact}\\]</div>`;
            } else {
                html += `<div><code>${escapeHtml(data.exact)}</code></div>`;
            }
        }
        if (data.approximate) {
            html += `<p><strong>Approssimazione:</strong> <code>${escapeHtml(data.approximate)}</code></p>`;
        }
        if (data.solutions && data.solutions.length > 0) {
            html += `<p><strong>Soluzioni:</strong></p><ul class="math-list">`;
            data.solutions.forEach((sol, i) => {
                const latexSol = data.latex && data.latex.solutions && data.latex.solutions[i];
                if (latexSol) {
                    html += `<li>\\[${latexSol}\\]</li>`;
                } else {
                    html += `<li><code>${escapeHtml(sol)}</code></li>`;
                }
            });
            html += `</ul>`;
        }
        if (data.conditions && data.conditions.length > 0) {
            html += `<p><strong>Condizioni:</strong> ${data.conditions.map(escapeHtml).join(", ")}</p>`;
        }
        if (data.steps && data.steps.length > 0) {
            const MAX_VISIBLE = 5;
            const totalSteps = data.steps.length;
            const showAll = totalSteps <= MAX_VISIBLE;

            html += `<p><strong>Procedimento:</strong></p>`;
            html += `<ol class="steps-list" id="steps-list">`;
            data.steps.forEach((step, i) => {
                const hidden = !showAll && i >= MAX_VISIBLE;
                const latexStep = data.latex && data.latex.steps && data.latex.steps[i];

                html += `<li class="step-item"${hidden ? ' style="display: none;"' : ""} data-step-index="${i}">`;
                html += `<div class="step-description">${escapeHtml(step.description)}</div>`;

                // Usa sempre step.before / step.after. Il LaTeX generato
                // dal backend (latexStep) può essere stato rivalutato
                // (es. "2^2 * 5^2" -> "100"), quindi lo ignoriamo.
                let before = null, after = null;
                if (isLatexLike(step.before) && isLatexLike(step.after)) {
                    before = step.before;
                    after = step.after;
                }

                if (before !== null && after !== null) {
                    html += `<div class="math-step">\\[${before} \\quad \\to \\quad ${after}\\]</div>`;
                } else {
                    html += `<div><code>${escapeHtml(step.before)}</code> → <code>${escapeHtml(step.after)}</code></div>`;
                }
                html += `</li>`;
            });
            html += `</ol>`;

            if (!showAll) {
                html += `<button class="show-all-steps" id="show-all-steps">Mostra tutti i ${totalSteps} passaggi</button>`;
            }
        }
        if (data.error) {
            html += `<p class="error"><strong>Errore:</strong> ${escapeHtml(data.error)}</p>`;
        }

        if (data.status !== "error") {
            html += `<div class="action-bar">`;
            if (data.latex && data.latex.exact) {
                html += `<button class="action-btn" data-action="copy-latex" title="Copia LaTeX">${ICONS.latex}<span>LaTeX</span></button>`;
            }
            if (data.exact) {
                html += `<button class="action-btn" data-action="copy-text" title="Copia come testo">${ICONS.text}<span>Testo</span></button>`;
            }
            if (data.plot_data) {
                html += `<button class="action-btn" data-action="export-png" title="Esporta come PNG">${ICONS.png}<span>PNG</span></button>`;
            }
            html += `<button class="action-btn" data-action="export-json" title="Esporta come JSON">${ICONS.json}<span>JSON</span></button>`;
            html += `</div>`;
        }

        resultContent.innerHTML = html;

        if (resultArea) {
            resultArea.classList.remove("fade-in");
            void resultArea.offsetWidth;
            resultArea.classList.add("fade-in");
        }

        resultContent.dataset.result = JSON.stringify(data);
        setupAzioni(data);

        // Listener per "Mostra tutti i passaggi"
        const showAllBtn = document.getElementById("show-all-steps");
        if (showAllBtn) {
            showAllBtn.addEventListener("click", () => {
                document.querySelectorAll(".step-item").forEach((el) => {
                    el.style.display = "";
                });
                showAllBtn.remove();
            });
        }

        if (window.MathJax && window.MathJax.typesetPromise) {
            window.MathJax.typesetPromise([resultContent]);
        }
    }

    function setupAzioni(data) {
        document.querySelectorAll(".action-btn").forEach((btn) => {
            btn.addEventListener("click", () => {
                eseguiAzione(btn.dataset.action, data);
            });
        });
    }

    async function eseguiAzione(action, data) {
        switch (action) {
            case "copy-latex": {
                const latex = data.latex && data.latex.exact;
                if (!latex) return;
                try {
                    await navigator.clipboard.writeText(latex);
                    mostraToast("LaTeX copiato negli appunti");
                } catch (err) {
                    mostraToast("Errore durante la copia", "error");
                }
                break;
            }
            case "copy-text": {
                try {
                    await navigator.clipboard.writeText(data.exact || "");
                    mostraToast("Risultato copiato negli appunti");
                } catch (err) {
                    mostraToast("Errore durante la copia", "error");
                }
                break;
            }
            case "export-png": {
                if (!data.plot_data) return;
                const link = document.createElement("a");
                link.href = "data:image/png;base64," + data.plot_data;
                link.download = "openalpha_plot_" + Date.now() + ".png";
                link.click();
                mostraToast("PNG scaricato");
                break;
            }
            case "export-json": {
                const blob = new Blob([JSON.stringify(data, null, 2)], {
                    type: "application/json",
                });
                const url = URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.download = "openalpha_result_" + Date.now() + ".json";
                link.click();
                URL.revokeObjectURL(url);
                mostraToast("JSON scaricato");
                break;
            }
        }
    }

    function mostraErrore(messaggio) {
        resultContent.innerHTML = `<p class="error">${escapeHtml(messaggio)}</p>`;
    }

    // ---------------------------------------------------------------------
    // Cronologia
    // ---------------------------------------------------------------------

    function leggiCronologia() {
        try {
            const raw = localStorage.getItem(HISTORY_KEY);
            if (!raw) return [];
            const data = JSON.parse(raw);
            return Array.isArray(data) ? data : [];
        } catch {
            return [];
        }
    }

    function scriviCronologia(items) {
        try {
            localStorage.setItem(HISTORY_KEY, JSON.stringify(items));
        } catch (err) {
            console.error("Errore salvataggio cronologia:", err);
        }
    }

    function aggiungiAllaCronologia(entry) {
        const items = leggiCronologia();
        const last = items[0];
        if (last && last.operation === entry.operation && last.expression === entry.expression) {
            return;
        }
        const newEntry = {
            operation: entry.operation,
            expression: entry.expression,
            params: entry.params || {},
            raw: entry.raw || entry.expression,
            exact: entry.exact || null,
            timestamp: new Date().toISOString(),
        };
        items.unshift(newEntry);
        if (items.length > HISTORY_MAX) {
            items.length = HISTORY_MAX;
        }
        scriviCronologia(items);
        renderCronologia();
    }

    function renderCronologia() {
        const items = leggiCronologia();
        historyList.innerHTML = "";

        if (items.length === 0) {
            const li = document.createElement("li");
            li.className = "empty";
            li.textContent = "Nessuna operazione";
            historyList.appendChild(li);
            return;
        }

        items.forEach((entry) => {
            const li = document.createElement("li");
            li.title = "Clicca per ri-eseguire";

            const op = document.createElement("div");
            op.className = "history-op";
            op.textContent = entry.operation;
            li.appendChild(op);

            const expr = document.createElement("div");
            expr.className = "history-expr";
            expr.textContent = entry.raw;
            li.appendChild(expr);

            if (entry.exact) {
                const ex = document.createElement("div");
                ex.className = "history-exact";
                ex.textContent = "→ " + entry.exact;
                li.appendChild(ex);
            }

            const time = document.createElement("div");
            time.className = "history-time";
            time.textContent = formatTimestamp(entry.timestamp);
            li.appendChild(time);

            li.addEventListener("click", () => {
                riEsegui(entry);
            });

            historyList.appendChild(li);
        });
    }

    function formatTimestamp(iso) {
        try {
            const d = new Date(iso);
            const hh = String(d.getHours()).padStart(2, "0");
            const mm = String(d.getMinutes()).padStart(2, "0");
            return `${hh}:${mm}`;
        } catch {
            return "";
        }
    }

    function riEsegui(entry) {
        setExpression(entry.raw || entry.expression);
        operationSelect.value = entry.operation;
        if (previewTimer) clearTimeout(previewTimer);
        previewTimer = setTimeout(aggiornaAnteprima, 100);
        resultContent.innerHTML = `
            <div class="loading-container">
                <span class="spinner"></span>
                <span>Calcolo in corso...</span>
            </div>
        `;
        eseguiOperazione(entry.operation, entry.expression, entry.params || {}, entry.raw || entry.expression);
    }

    clearHistoryButton.addEventListener("click", () => {
        if (confirm("Pulire la cronologia?")) {
            scriviCronologia([]);
            renderCronologia();
            mostraToast("Cronologia pulita");
        }
    });

    // ---------------------------------------------------------------------
    // Toast
    // ---------------------------------------------------------------------

    function mostraToast(message, type = "success") {
        const existing = document.querySelector(".toast");
        if (existing) existing.remove();

        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        const icon = type === "error" ? ICONS.x : ICONS.check;
        toast.innerHTML = `${icon}<span>${escapeHtml(message)}</span>`;
        document.body.appendChild(toast);

        requestAnimationFrame(() => {
            toast.classList.add("visible");
        });

        setTimeout(() => {
            toast.classList.remove("visible");
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    }

    // ---------------------------------------------------------------------
    // Empty state
    // ---------------------------------------------------------------------

    function mostraEmptyState() {
        const esempi = [
            { testo: "(x + 1)**2", op: "simplify" },
            { testo: "x**2 - 1 = 0", op: "solve" },
            { testo: "sin(x)/x", op: "limit" },
            { testo: "plot(sin(x))", op: "plot" },
        ];

        let html = `
            <div class="empty-state">
                <div class="empty-state-icon">${ICONS.broom}</div>
                <p>Prova con un esempio:</p>
                <div class="example-chips">
        `;
        esempi.forEach((es) => {
            html += `<button class="example-chip" data-expr="${escapeHtml(es.testo)}">${escapeHtml(es.testo)}</button>`;
        });
        html += `
                </div>
            </div>
        `;

        resultContent.innerHTML = html;

        document.querySelectorAll(".example-chip").forEach((btn) => {
            btn.addEventListener("click", () => {
                setExpression(btn.dataset.expr);
                aggiornaAnteprima();
                esegui();
            });
        });
    }

    // ---------------------------------------------------------------------
    // Utils
    // ---------------------------------------------------------------------

    function escapeHtml(s) {
        return String(s)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
    }

    function isLatexLike(s) {
        // Euristica: la stringa è "matematica" se contiene solo
        // numeri, lettere, operatori, spazi, parentesi, ^, _, =, .
        // Esclude etichette italiane comuni (es. "primo", "composto").
        if (!s) return false;
        const etichette = ["primo", "composto", "non primo", "Vero", "Falso"];
        if (etichette.includes(s.trim())) return false;
        return /^[\s0-9a-zA-Z+\-*/^_=().,]+$/.test(s);
    }

    // ---------------------------------------------------------------------
    // Avvio
    // ---------------------------------------------------------------------

    calculateButton.addEventListener("click", esegui);
    inputField.addEventListener("keydown", (event) => {
        if (event.key === "Enter") esegui();
    });

    caricaOperazioni();
    setupTastiera();
    renderCronologia();
    mostraEmptyState();
}

// Avvia l'app: se il DOM è già pronto, esegui subito; altrimenti
// aspetta DOMContentLoaded. Necessario perché con MathLive caricato
// nell'<head>, il parsing può ritardare l'esecuzione di questo script
// fino a dopo l'evento DOMContentLoaded.
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initOpenAlpha);
} else {
    initOpenAlpha();
}