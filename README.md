# Visualizzatore Ferri Strutturali

Un'applicazione web interattiva per visualizzare e analizzare i dati dei ferri strutturali.

## Caratteristiche

- 🔍 **Filtri interattivi** per elemento strutturale, piano e diametro
- 📊 **Visualizzazioni grafiche** con grafici a barre e torta
- 📈 **Statistiche** in tempo reale sui dati filtrati
- 🔬 **Analisi avanzata** con top combinazioni e riepiloghi
- 📱 **Interface responsive** ottimizzata per diversi dispositivi

## Installazione

1. Assicurati di avere Python 3.8+ installato
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

## Utilizzo

1. Assicurati che il file `output_ferri.txt` sia presente nella stessa cartella dell'app
2. Avvia l'applicazione:
   ```bash
   streamlit run app.py
   ```
3. Apri il browser all'indirizzo che verrà mostrato (solitamente http://localhost:8501)

## Struttura dell'App

### Filtri Disponibili
- **Elemento Strutturale**: Pilastri, Travi, Pareti, Fondazione
- **Piano**: Piano garage, Piano mansarda, Piano primo, Piano rialzato, Fondazione
- **Diametro**: Tutti i diametri presenti nei dati (6mm, 8mm, 12mm, 14mm, 16mm)

### Visualizzazioni
1. **Tabella Dati Filtrati**: Mostra i dati che corrispondono ai filtri selezionati
2. **Statistiche**: Peso totale, medio, massimo, minimo e conteggi
3. **Grafici per Elemento**: Distribuzione del peso per tipo di elemento strutturale
4. **Grafici per Piano**: Distribuzione del peso per piano
5. **Grafici per Diametro**: Distribuzione del peso per diametro del ferro
6. **Distribuzione Percentuale**: Grafico a torta della distribuzione per elemento

### Analisi Avanzata
- Top 5 combinazioni per peso
- Riepilogo statistico per diametro

## Formato Dati Supportato

L'applicazione legge file di testo con il seguente formato:
```
============================================================
ELEMENTO_STRUTTURALE
============================================================
--------
Piano/Livello          ø diametro    quantità
```

## Tecnologie Utilizzate

- **Streamlit**: Framework per app web
- **Pandas**: Manipolazione e analisi dati
- **Plotly**: Visualizzazioni interattive
- **Python**: Linguaggio di programmazione

## Note

- I dati sono espressi in chilogrammi (kg)
- I diametri sono espressi in millimetri (mm)
- L'app aggiorna automaticamente le visualizzazioni quando cambiano i filtri
