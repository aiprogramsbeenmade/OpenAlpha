/* Gestione dell'interazione utente per OpenAlpha web. */

const HISTORY_KEY = "openalpha_history";
const HISTORY_MAX = 50;

document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById("input-expression");
    const calculateButton = document.getElementById("calculate-button");
    const resultContent = document.getElementById("result-content");
    const operationSelect = document.getElementById("operation-select");
    const previewDiv = document.getElementById("preview");
    const historyList = document.getElementById("history-list");
    const clearHistoryButton = document.getElementById("clear-history");
    const resultArea = document.querySelector(".result-area");

    let previewTimer = null;

    caricaOperazioni();
    setupTastiera();
    renderCronologia();
    mostraEmptyState();

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

    // ---------------------------------------------------------------------
    // Anteprima
    // ---------------------------------------------------------------------

    inputField.addEventListener("input", () => {
        if (previewTimer) clearTimeout(previewTimer);
        previewTimer = setTimeout(aggiornaAnteprima, 300);
    });

    async function aggiornaAnteprima() {
        const expr = inputField.value.trim();
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
        const raw = inputField.value.trim();
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
            autosize: true,
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
            autosize: true,
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
            html += `<p><strong>Procedimento:</strong></p>`;
            html += `<ol class="steps-list">`;
            data.steps.forEach((step, i) => {
                const latexStep = data.latex && data.latex.steps && data.latex.steps[i];
                html += `<li>`;
                html += `<div class="step-description">${escapeHtml(step.description)}</div>`;
                if (latexStep && latexStep.before && latexStep.after) {
                    html += `<div class="math-step">\\[${latexStep.before} \\quad \\to \\quad ${latexStep.after}\\]</div>`;
                } else {
                    html += `<div><code>${escapeHtml(step.before)}</code> → <code>${escapeHtml(step.after)}</code></div>`;
                }
                html += `</li>`;
            });
            html += `</ol>`;
        }
        if (data.error) {
            html += `<p class="error"><strong>Errore:</strong> ${escapeHtml(data.error)}</p>`;
        }

        if (data.status !== "error") {
            html += `<div class="action-bar">`;
            if (data.latex && data.latex.exact) {
                html += `<button class="action-btn" data-action="copy-latex" title="Copia LaTeX">LaTeX</button>`;
            }
            if (data.exact) {
                html += `<button class="action-btn" data-action="copy-text" title="Copia come testo">Testo</button>`;
            }
            if (data.plot_data) {
                html += `<button class="action-btn" data-action="export-png" title="Esporta come PNG">PNG</button>`;
            }
            html += `<button class="action-btn" data-action="export-json" title="Esporta come JSON">JSON</button>`;
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
        inputField.value = entry.raw || entry.expression;
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
        toast.textContent = message;
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
                inputField.value = btn.dataset.expr;
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

    calculateButton.addEventListener("click", esegui);
    inputField.addEventListener("keydown", (event) => {
        if (event.key === "Enter") esegui();
    });
});