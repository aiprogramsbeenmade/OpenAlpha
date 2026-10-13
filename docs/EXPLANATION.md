# Politica delle spiegazioni in OpenAlpha

## Principio fondamentale

OpenAlpha **non inventa** passaggi matematici. Se il software non ha
un procedimento verificato per una determinata operazione, lo dichiara
esplicitamente, invece di presentare una spiegazione plausibile ma non
verificata.

## Come funziona una spiegazione

Una spiegazione è una sequenza di `Step`. Ogni `Step` è prodotto da
una `Rule` applicata a un sottoalbero dell'espressione. La regola
dichiara:

1. Un **pattern** o una **funzione di analisi** che riconosce quando
   si applica.
2. Una **condizione** opzionale che filtra i match degeneri.
3. Un **replacement** che produce l'output.

L'output dello `Step` è **calcolato** dalla regola, mai scritto a mano.
Questo garantisce che ogni passo mostrato sia verificato: se la regola
è corretta (e i test lo confermano), lo `Step` è corretto.

## Due modalità di regola

Una `Rule` può essere definita in due modi:

### Pattern-based

```python
Rule.from_pattern(
    name="square_of_binomial",
    description="Quadrato del binomio",
    pattern=(a + b) ** 2,
    replacement=lambda m: m[a]**2 + 2*m[a]*m[b] + m[b]**2,
)