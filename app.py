import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
from datetime import datetime

# Configurazione pagina
st.set_page_config(
    page_title="Visualizzatore Ferri Strutturali",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def parse_ferri_data(file_path):
    """Parser per leggere e strutturare i dati dal file di output"""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    data = []
    current_element = None
    
    # Pattern per identificare le sezioni
    element_pattern = r'={60}\n([A-Z]+)\n={60}'
    
    # Trova tutte le sezioni
    sections = re.split(element_pattern, content)
    
    for i in range(1, len(sections), 2):
        element_type = sections[i].strip()
        element_content = sections[i+1] if i+1 < len(sections) else ""
        
        if element_type in ['PILASTRI', 'TRAVI', 'PARETI', 'FONDAZIONE']:
            # Parse delle righe di dati
            lines = element_content.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                # Skip linee vuote e separatori
                if not line or line.startswith('-') or '=' in line:
                    continue
                
                # Pattern per estrarre piano, diametro e quantità
                match = re.match(r'(.+?)\s+ø\s*(\d+)\s+([\d.]+)', line)
                if match:
                    piano = match.group(1).strip()
                    diametro = int(match.group(2))
                    quantita = float(match.group(3))
                    
                    data.append({
                        'Elemento': element_type,
                        'Piano': piano,
                        'Diametro': diametro,
                        'Quantità': quantita
                    })
    
    return pd.DataFrame(data)

def load_data():
    """Carica i dati dal file"""
    try:
        df = parse_ferri_data('data/output_ferri.txt')
        return df
    except Exception as e:
        st.error(f"Errore nel caricamento del file: {e}")
        return pd.DataFrame()

def main():
    st.title("🏗️ Visualizzatore Ferri Strutturali")
    st.markdown("---")
    
    # Caricamento dati
    df = load_data()
    
    if df.empty:
        st.error("Nessun dato disponibile. Verificare che il file 'output_ferri.txt' sia presente.")
        return
    
    # Sidebar con filtri
    st.sidebar.header("🔍 Filtri")
    
    # Filtro per elemento strutturale
    elementi_disponibili = ['Tutti'] + sorted(df['Elemento'].unique().tolist())
    elemento_selezionato = st.sidebar.selectbox(
        "Elemento Strutturale:",
        elementi_disponibili
    )
    
    # Filtro per piano
    piani_disponibili = ['Tutti'] + sorted(df['Piano'].unique().tolist())
    piano_selezionato = st.sidebar.selectbox(
        "Piano:",
        piani_disponibili
    )
    
    # Filtro per diametro
    diametri_disponibili = ['Tutti'] + sorted(df['Diametro'].unique().tolist())
    diametro_selezionato = st.sidebar.selectbox(
        "Diametro (mm):",
        diametri_disponibili
    )
    
    # Applica filtri
    df_filtered = df.copy()
    
    if elemento_selezionato != 'Tutti':
        df_filtered = df_filtered[df_filtered['Elemento'] == elemento_selezionato]
    
    if piano_selezionato != 'Tutti':
        df_filtered = df_filtered[df_filtered['Piano'] == piano_selezionato]
    
    if diametro_selezionato != 'Tutti':
        df_filtered = df_filtered[df_filtered['Diametro'] == diametro_selezionato]
    
    # Layout principale con colonne
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Dati Filtrati")
        
        # Mostra tabella filtrata
        if not df_filtered.empty:
            # Aggiungi colonna con unità di misura
            df_display = df_filtered.copy()
            df_display['Diametro (mm)'] = df_display['Diametro'].astype(str) + ' mm'
            df_display['Quantità (kg)'] = df_display['Quantità'].round(2).astype(str) + ' kg'
            
            st.dataframe(
                df_display[['Elemento', 'Piano', 'Diametro (mm)', 'Quantità (kg)']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("Nessun dato corrisponde ai filtri selezionati.")
    
    with col2:
        st.subheader("📈 Statistiche")
        
        if not df_filtered.empty:
            # Statistiche principali
            total_weight = df_filtered['Quantità'].sum()
            avg_weight = df_filtered['Quantità'].mean()
            max_weight = df_filtered['Quantità'].max()
            min_weight = df_filtered['Quantità'].min()
            
            st.metric("Peso Totale", f"{total_weight:.2f} kg")
            st.metric("Peso Medio", f"{avg_weight:.2f} kg")
            st.metric("Peso Massimo", f"{max_weight:.2f} kg")
            st.metric("Peso Minimo", f"{min_weight:.2f} kg")
            
            # Conteggi
            st.markdown("**Conteggi:**")
            st.write(f"- Elementi: {df_filtered['Elemento'].nunique()}")
            st.write(f"- Piani: {df_filtered['Piano'].nunique()}")
            st.write(f"- Diametri: {df_filtered['Diametro'].nunique()}")
            st.write(f"- Righe totali: {len(df_filtered)}")
    
    # Sezione grafici
    st.markdown("---")
    st.subheader("📊 Visualizzazioni")
    
    if not df_filtered.empty:
        # Crea tabs per diversi tipi di visualizzazione
        tab1, tab2, tab3, tab4 = st.tabs(["Per Elemento", "Per Piano", "Per Diametro", "Distribuzione"])
        
        with tab1:
            # Grafico per elemento
            element_data = df_filtered.groupby('Elemento')['Quantità'].sum().reset_index()
            fig1 = px.bar(
                element_data, 
                x='Elemento', 
                y='Quantità',
                title='Distribuzione Peso per Elemento Strutturale',
                color='Quantità',
                color_continuous_scale='viridis'
            )
            fig1.update_layout(showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with tab2:
            # Grafico per piano
            piano_data = df_filtered.groupby('Piano')['Quantità'].sum().reset_index()
            fig2 = px.bar(
                piano_data, 
                x='Piano', 
                y='Quantità',
                title='Distribuzione Peso per Piano',
                color='Quantità',
                color_continuous_scale='plasma'
            )
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        
        with tab3:
            # Grafico per diametro
            diameter_data = df_filtered.groupby('Diametro')['Quantità'].sum().reset_index()
            fig3 = px.bar(
                diameter_data, 
                x='Diametro', 
                y='Quantità',
                title='Distribuzione Peso per Diametro',
                color='Quantità',
                color_continuous_scale='cividis'
            )
            fig3.update_layout(showlegend=False)
            fig3.update_xaxis(title='Diametro (mm)')
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab4:
            # Grafico a torta per distribuzione elementi
            element_pie_data = df_filtered.groupby('Elemento')['Quantità'].sum().reset_index()
            fig4 = px.pie(
                element_pie_data, 
                values='Quantità', 
                names='Elemento',
                title='Distribuzione Percentuale per Elemento'
            )
            st.plotly_chart(fig4, use_container_width=True)
    
    # Sezione analisi avanzata
    st.markdown("---")
    st.subheader("🔬 Analisi Avanzata")
    
    if not df_filtered.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top 5 Combinazioni per Peso:**")
            top_combinations = df_filtered.nlargest(5, 'Quantità')[['Elemento', 'Piano', 'Diametro', 'Quantità']]
            st.dataframe(top_combinations, hide_index=True)
        
        with col2:
            st.write("**Riepilogo per Diametro:**")
            diameter_summary = df_filtered.groupby('Diametro').agg({
                'Quantità': ['sum', 'count', 'mean']
            }).round(2)
            diameter_summary.columns = ['Peso Totale', 'Conteggio', 'Peso Medio']
            st.dataframe(diameter_summary)
    
    # Footer con informazioni sul file
    st.markdown("---")
    st.markdown("**Fonte dati:** output_ferri.txt")
    st.markdown(f"**Ultimo aggiornamento:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

if __name__ == "__main__":
    main()
