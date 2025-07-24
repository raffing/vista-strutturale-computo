"""
Visualizzatore Ferri Strutturali - Versione Semplificata
Questa versione usa solo librerie standard Python e genera un report HTML
"""

import re
import json
from datetime import datetime
import webbrowser
import os

def parse_ferri_data(file_path):
    """Parser per leggere e strutturare i dati dal file di output"""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    data = []
    
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
                        'elemento': element_type,
                        'piano': piano,
                        'diametro': diametro,
                        'quantita': quantita
                    })
    
    return data

def calculate_statistics(data, filters=None):
    """Calcola statistiche sui dati filtrati"""
    
    filtered_data = data
    
    if filters:
        if filters.get('elemento') and filters['elemento'] != 'Tutti':
            filtered_data = [d for d in filtered_data if d['elemento'] == filters['elemento']]
        
        if filters.get('piano') and filters['piano'] != 'Tutti':
            filtered_data = [d for d in filtered_data if d['piano'] == filters['piano']]
        
        if filters.get('diametro') and filters['diametro'] != 'Tutti':
            filtered_data = [d for d in filtered_data if d['diametro'] == int(filters['diametro'])]
    
    if not filtered_data:
        return None
    
    quantita_list = [d['quantita'] for d in filtered_data]
    
    stats = {
        'totale': sum(quantita_list),
        'media': sum(quantita_list) / len(quantita_list),
        'massimo': max(quantita_list),
        'minimo': min(quantita_list),
        'conteggio': len(filtered_data),
        'elementi_unici': len(set(d['elemento'] for d in filtered_data)),
        'piani_unici': len(set(d['piano'] for d in filtered_data)),
        'diametri_unici': len(set(d['diametro'] for d in filtered_data))
    }
    
    return stats, filtered_data

def group_by_field(data, field):
    """Raggruppa i dati per un campo specifico"""
    groups = {}
    for item in data:
        key = item[field]
        if key not in groups:
            groups[key] = []
        groups[key].append(item['quantita'])
    
    # Calcola totali per gruppo
    result = {}
    for key, values in groups.items():
        result[key] = sum(values)
    
    return result

def generate_html_report(data):
    """Genera un report HTML interattivo"""
    
    # Ottieni liste uniche per i filtri
    elementi = sorted(list(set(d['elemento'] for d in data)))
    piani = sorted(list(set(d['piano'] for d in data)))
    diametri = sorted(list(set(d['diametro'] for d in data)))
    
    # Calcola statistiche globali
    stats, _ = calculate_statistics(data)
    
    # Prepara dati per i grafici
    element_data = group_by_field(data, 'elemento')
    piano_data = group_by_field(data, 'piano')
    diametro_data = group_by_field(data, 'diametro')
    
    html_content = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏗️ Visualizzatore Ferri Strutturali</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .filters {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .filter-group {{
            display: inline-block;
            margin: 10px 15px 10px 0;
        }}
        
        .filter-group label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }}
        
        .filter-group select {{
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            min-width: 150px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .data-table {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 30px;
        }}
        
        .hidden {{
            display: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏗️ Visualizzatore Ferri Strutturali</h1>
            <p>Analisi interattiva dei dati strutturali</p>
        </div>
        
        <div class="filters">
            <h3>🔍 Filtri</h3>
            <div class="filter-group">
                <label for="elemento-filter">Elemento Strutturale:</label>
                <select id="elemento-filter" onchange="applyFilters()">
                    <option value="Tutti">Tutti</option>
                    {''.join(f'<option value="{elem}">{elem}</option>' for elem in elementi)}
                </select>
            </div>
            
            <div class="filter-group">
                <label for="piano-filter">Piano:</label>
                <select id="piano-filter" onchange="applyFilters()">
                    <option value="Tutti">Tutti</option>
                    {''.join(f'<option value="{piano}">{piano}</option>' for piano in piani)}
                </select>
            </div>
            
            <div class="filter-group">
                <label for="diametro-filter">Diametro (mm):</label>
                <select id="diametro-filter" onchange="applyFilters()">
                    <option value="Tutti">Tutti</option>
                    {''.join(f'<option value="{diam}">{diam} mm</option>' for diam in diametri)}
                </select>
            </div>
        </div>
        
        <div class="stats-grid" id="stats-container">
            <div class="stat-card">
                <div class="stat-value" id="total-weight">{stats['totale']:.2f}</div>
                <div class="stat-label">Peso Totale (kg)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="avg-weight">{stats['media']:.2f}</div>
                <div class="stat-label">Peso Medio (kg)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="max-weight">{stats['massimo']:.2f}</div>
                <div class="stat-label">Peso Massimo (kg)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="min-weight">{stats['minimo']:.2f}</div>
                <div class="stat-label">Peso Minimo (kg)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="total-count">{stats['conteggio']}</div>
                <div class="stat-label">Righe Totali</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-container">
                <h3>Distribuzione per Elemento</h3>
                <canvas id="elementChart"></canvas>
            </div>
            <div class="chart-container">
                <h3>Distribuzione per Piano</h3>
                <canvas id="pianoChart"></canvas>
            </div>
            <div class="chart-container">
                <h3>Distribuzione per Diametro</h3>
                <canvas id="diametroChart"></canvas>
            </div>
            <div class="chart-container">
                <h3>Distribuzione Percentuale</h3>
                <canvas id="pieChart"></canvas>
            </div>
        </div>
        
        <div class="data-table">
            <h3>📊 Dati Filtrati</h3>
            <table id="data-table">
                <thead>
                    <tr>
                        <th>Elemento</th>
                        <th>Piano</th>
                        <th>Diametro (mm)</th>
                        <th>Quantità (kg)</th>
                    </tr>
                </thead>
                <tbody id="table-body">
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p><strong>Fonte dati:</strong> output_ferri.txt</p>
            <p><strong>Generato il:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </div>
    </div>

    <script>
        // Dati JavaScript
        const allData = {json.dumps(data)};
        
        let charts = {{}};
        
        function applyFilters() {{
            const elementoFilter = document.getElementById('elemento-filter').value;
            const pianoFilter = document.getElementById('piano-filter').value;
            const diametroFilter = document.getElementById('diametro-filter').value;
            
            // Filtra dati
            let filteredData = allData.filter(item => {{
                return (elementoFilter === 'Tutti' || item.elemento === elementoFilter) &&
                       (pianoFilter === 'Tutti' || item.piano === pianoFilter) &&
                       (diametroFilter === 'Tutti' || item.diametro.toString() === diametroFilter);
            }});
            
            // Aggiorna statistiche
            updateStatistics(filteredData);
            
            // Aggiorna tabella
            updateTable(filteredData);
            
            // Aggiorna grafici
            updateCharts(filteredData);
        }}
        
        function updateStatistics(data) {{
            if (data.length === 0) {{
                document.getElementById('total-weight').textContent = '0.00';
                document.getElementById('avg-weight').textContent = '0.00';
                document.getElementById('max-weight').textContent = '0.00';
                document.getElementById('min-weight').textContent = '0.00';
                document.getElementById('total-count').textContent = '0';
                return;
            }}
            
            const quantities = data.map(d => d.quantita);
            const total = quantities.reduce((a, b) => a + b, 0);
            const avg = total / quantities.length;
            const max = Math.max(...quantities);
            const min = Math.min(...quantities);
            
            document.getElementById('total-weight').textContent = total.toFixed(2);
            document.getElementById('avg-weight').textContent = avg.toFixed(2);
            document.getElementById('max-weight').textContent = max.toFixed(2);
            document.getElementById('min-weight').textContent = min.toFixed(2);
            document.getElementById('total-count').textContent = data.length;
        }}
        
        function updateTable(data) {{
            const tbody = document.getElementById('table-body');
            tbody.innerHTML = '';
            
            data.forEach(item => {{
                const row = tbody.insertRow();
                row.insertCell(0).textContent = item.elemento;
                row.insertCell(1).textContent = item.piano;
                row.insertCell(2).textContent = item.diametro + ' mm';
                row.insertCell(3).textContent = item.quantita.toFixed(2) + ' kg';
            }});
        }}
        
        function groupByField(data, field) {{
            const groups = {{}};
            data.forEach(item => {{
                const key = item[field];
                if (!groups[key]) groups[key] = 0;
                groups[key] += item.quantita;
            }});
            return groups;
        }}
        
        function updateCharts(data) {{
            // Elemento chart
            const elementData = groupByField(data, 'elemento');
            updateBarChart('elementChart', Object.keys(elementData), Object.values(elementData), 'Peso (kg)');
            
            // Piano chart
            const pianoData = groupByField(data, 'piano');
            updateBarChart('pianoChart', Object.keys(pianoData), Object.values(pianoData), 'Peso (kg)');
            
            // Diametro chart
            const diametroData = groupByField(data, 'diametro');
            const diametroLabels = Object.keys(diametroData).map(d => d + ' mm');
            updateBarChart('diametroChart', diametroLabels, Object.values(diametroData), 'Peso (kg)');
            
            // Pie chart
            updatePieChart('pieChart', Object.keys(elementData), Object.values(elementData));
        }}
        
        function updateBarChart(canvasId, labels, data, yLabel) {{
            const ctx = document.getElementById(canvasId).getContext('2d');
            
            if (charts[canvasId]) {{
                charts[canvasId].destroy();
            }}
            
            charts[canvasId] = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [{{
                        data: data,
                        backgroundColor: 'rgba(102, 126, 234, 0.8)',
                        borderColor: 'rgba(102, 126, 234, 1)',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            display: false
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            title: {{
                                display: true,
                                text: yLabel
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        function updatePieChart(canvasId, labels, data) {{
            const ctx = document.getElementById(canvasId).getContext('2d');
            
            if (charts[canvasId]) {{
                charts[canvasId].destroy();
            }}
            
            const colors = [
                'rgba(102, 126, 234, 0.8)',
                'rgba(118, 75, 162, 0.8)',
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)'
            ];
            
            charts[canvasId] = new Chart(ctx, {{
                type: 'pie',
                data: {{
                    labels: labels,
                    datasets: [{{
                        data: data,
                        backgroundColor: colors.slice(0, labels.length),
                        borderWidth: 2,
                        borderColor: '#fff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            position: 'bottom'
                        }}
                    }}
                }}
            }});
        }}
        
        // Inizializza la pagina
        document.addEventListener('DOMContentLoaded', function() {{
            applyFilters();
        }});
    </script>
</body>
</html>
"""
    
    return html_content

def main():
    """Funzione principale"""
    print("🏗️ Visualizzatore Ferri Strutturali")
    print("=====================================")
    
    # Controlla se il file esiste
    if not os.path.exists('output_ferri.txt'):
        print("❌ Errore: File 'output_ferri.txt' non trovato!")
        print("   Assicurati che il file sia presente nella stessa cartella di questo script.")
        input("Premi Enter per uscire...")
        return
    
    try:
        # Carica e analizza i dati
        print("📊 Caricamento dati...")
        data = parse_ferri_data('output_ferri.txt')
        
        if not data:
            print("❌ Errore: Nessun dato trovato nel file!")
            input("Premi Enter per uscire...")
            return
        
        print(f"✅ Caricati {len(data)} record")
        
        # Genera report HTML
        print("🌐 Generazione report HTML...")
        html_content = generate_html_report(data)
        
        # Salva il file HTML
        output_file = 'ferri_report.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Report salvato come '{output_file}'")
        
        # Apri nel browser
        print("🌐 Apertura nel browser...")
        webbrowser.open(f'file://{os.path.abspath(output_file)}')
        
        print("✅ Completato! Il report è stato aperto nel tuo browser.")
        print("   Puoi anche aprire manualmente il file 'ferri_report.html'")
        
    except Exception as e:
        print(f"❌ Errore: {e}")
    
    input("Premi Enter per uscire...")

if __name__ == "__main__":
    main()
