# 🏗️ Visualizzatore Ferri Strutturali - Guida Completa

## 🚀 Due Versioni Disponibili

### 1. **Versione HTML** (Pronta all'uso)
- **File**: `ferri_report.html`
- **Vantaggi**: Funziona ovunque, nessuna installazione
- **Uso**: Doppio click → si apre nel browser

### 2. **Versione Streamlit** (Professionale)
- **File**: `app.py`
- **Vantaggi**: Interfaccia più avanzata, aggiornamenti in tempo reale
- **Uso**: Richiede Python + Streamlit

---

## 📱 Come Avviare la Versione Streamlit

### Metodo 1: File Batch (Windows)
```bash
# Doppio click su:
AVVIA_VISUALIZZATORE.bat
```

### Metodo 2: Python Launcher
```bash
# Esegui:
python avvia_visualizzatore.py
```

### Metodo 3: Comando Diretto
```bash
C:\Users\Utente\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe run app.py
```

### Metodo 4: Da VS Code
1. Apri terminale in VS Code
2. Esegui: `streamlit run app.py`
3. L'app si apre su: http://localhost:8501

---

## 🌐 Opzioni di Pubblicazione per Clienti

### 🟢 **OPZIONE 1: File HTML (RACCOMANDATO)**
**Invio immediato via email**

#### Pro:
- ✅ Funziona su qualsiasi computer
- ✅ Nessuna installazione richiesta
- ✅ File piccolo (~17KB)
- ✅ Grafici interattivi inclusi

#### Come fare:
1. Allega `ferri_report.html` all'email
2. Includi le istruzioni sotto

#### Template Email:
```
Oggetto: Analisi Ferri Strutturali - [Nome Progetto]

Gentile Cliente,

In allegato trova il visualizzatore interattivo per l'analisi 
dei ferri strutturali del progetto.

ISTRUZIONI:
1. Salvi il file allegato sul computer
2. Faccia doppio-click su "ferri_report.html"
3. Si aprirà nel browser con tutti i dati

CARATTERISTICHE:
✅ Filtri per elemento, piano, diametro
✅ Statistiche automatiche
✅ Grafici interattivi
✅ Funziona offline

DATI PROGETTO:
- Peso totale ferri: 27,715.40 kg
- 34 voci analizzate
- 4 tipologie strutturali

Resto a disposizione per chiarimenti.

Cordiali saluti
```

---

### 🟡 **OPZIONE 2: Hosting Web Gratuito**

#### A) Netlify Drop (2 minuti)
1. Vai su: https://netlify.com/drop
2. Trascina `ferri_report.html`
3. Ottieni URL pubblico istantaneo
4. Condividi URL con cliente

#### B) GitHub Pages
1. Crea repository GitHub pubblico
2. Carica `ferri_report.html`
3. Attiva GitHub Pages
4. URL: `https://username.github.io/repo-name/ferri_report.html`

#### C) Google Drive (Pubblico)
1. Carica file su Google Drive
2. Imposta condivisione "Chiunque con link"
3. Invia link al cliente

---

### 🔵 **OPZIONE 3: Streamlit Cloud (Professionale)**

#### Vantaggi:
- ✅ URL permanente
- ✅ Aggiornamenti automatici
- ✅ Interfaccia professionale
- ✅ Nessun limite di traffico

#### Setup (10 minuti):
1. **Crea repository GitHub** con:
   - `app.py`
   - `requirements.txt`
   - `output_ferri.txt`

2. **Deploy su Streamlit Cloud**:
   - Vai su: https://share.streamlit.io
   - Connetti GitHub
   - Seleziona repository
   - Deploy automatico

3. **Risultato**: URL tipo `https://nome-app.streamlit.app`

---

### 🟠 **OPZIONE 4: Server Locale (Demo)**

#### Per presentazioni dal vivo:
```bash
# Avvia il server
streamlit run app.py

# Condividi schermo con URL:
http://localhost:8501
```

---

## 🛠️ Personalizzazioni Possibili

### Cambiare Colori/Tema
```python
# In app.py, modifica:
st.set_page_config(
    page_title="Tuo Titolo",
    page_icon="🏢",  # Cambia icona
    layout="wide"
)
```

### Aggiungere Logo Aziendale
```python
# Aggiungi in app.py:
st.image("logo.png", width=200)
```

### Modificare Grafici
```python
# Cambia scala colori:
color_continuous_scale='viridis'  # blu-verde
color_continuous_scale='plasma'   # viola-rosa
color_continuous_scale='cividis'  # blu scuro
```

---

## 🔧 Risoluzione Problemi

### Streamlit non si avvia
```bash
# Verifica installazione:
pip show streamlit

# Reinstalla se necessario:
pip uninstall streamlit
pip install streamlit
```

### File dati non trovato
- Assicurati che `output_ferri.txt` sia nella stessa cartella
- Controlla il nome file (case-sensitive)

### Browser non si apre
- Apri manualmente: http://localhost:8501
- Controlla firewall/antivirus

### Errori di importazione
```bash
# Installa dipendenze mancanti:
pip install pandas plotly
```

---

## 📊 Funzionalità Disponibili

### Filtri Interattivi:
- **Elemento**: Pilastri, Travi, Pareti, Fondazione
- **Piano**: Garage, Mansarda, Primo, Rialzato, Fondazione  
- **Diametro**: 6, 8, 12, 14, 16 mm

### Visualizzazioni:
- **Statistiche**: Peso totale, medio, max, min
- **Grafici a barre**: Per elemento, piano, diametro
- **Grafico a torta**: Distribuzione percentuale
- **Tabella**: Dati filtrati in tempo reale
- **Top 5**: Combinazioni con peso maggiore

### Analisi Avanzate:
- Raggruppamenti automatici
- Conteggi per categoria
- Statistiche descrittive
- Export dati (Streamlit)

---

## 💡 Suggerimenti per Clienti

### Per Architetti/Ingegneri:
- Usa filtri per analizzare singoli piani
- Controlla distribuzione pesi per ottimizzazioni
- Esporta screenshot per report

### Per Imprese Edili:
- Filtra per diametro per ordini materiali
- Analizza quantità per piano per pianificazione
- Stampa tabelle per cantiere

### Per Direzione Lavori:
- Monitora avanzamento per elemento
- Verifica quantità preventivate vs effettive
- Documenta con grafici per relazioni

---

## 📞 Supporto

Per problemi tecnici o personalizzazioni:
- Email: [tua-email]
- Tel: [tuo-numero]
- Disponibile per modifiche su richiesta

---

**Versione Software**: 1.0
**Ultima modifica**: 24/07/2025
**Compatibilità**: Windows, Mac, Linux
**Browser supportati**: Chrome, Firefox, Edge, Safari
