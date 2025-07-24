"""
Script per avviare il Visualizzatore Ferri Strutturali con Streamlit
"""
import subprocess
import webbrowser
import time
import sys
import os

def avvia_streamlit():
    print("🏗️ VISUALIZZATORE FERRI STRUTTURALI")
    print("=" * 50)
    print()
    print("Avvio dell'applicazione Streamlit...")
    print()
    
    # Verifica che il file app.py esista
    if not os.path.exists('app.py'):
        print("❌ Errore: File 'app.py' non trovato!")
        input("Premi Enter per uscire...")
        return
    
    # Verifica che il file dati esista
    if not os.path.exists('output_ferri.txt'):
        print("❌ Errore: File 'output_ferri.txt' non trovato!")
        input("Premi Enter per uscire...")
        return
    
    try:
        print("🚀 Avvio Streamlit...")
        print("📍 L'applicazione sarà disponibile su: http://localhost:8501")
        print("⏹️  Per fermare l'app: Ctrl+C nel terminale")
        print()
        
        # Avvia Streamlit
        python_path = r"C:\Users\Utente\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe"
        
        if not os.path.exists(python_path):
            print("❌ Errore: Streamlit non trovato nel percorso specificato!")
            print(f"   Percorso: {python_path}")
            input("Premi Enter per uscire...")
            return
        
        # Comando per avviare streamlit
        cmd = [python_path, "run", "app.py", "--server.port", "8501"]
        
        print("⚡ Comando:", " ".join(cmd))
        print()
        
        # Avvia il processo
        process = subprocess.Popen(cmd, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT, 
                                 universal_newlines=True,
                                 bufsize=1)
        
        # Aspetta un po' e poi apri il browser
        time.sleep(3)
        webbrowser.open('http://localhost:8501')
        
        print("🌐 Browser aperto automaticamente!")
        print("💡 Se non si apre, vai manualmente su: http://localhost:8501")
        print()
        
        # Mostra l'output di Streamlit
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                
    except KeyboardInterrupt:
        print("\n⏹️ Applicazione fermata dall'utente.")
        process.terminate()
    except Exception as e:
        print(f"❌ Errore nell'avvio: {e}")
    
    input("\nPremi Enter per uscire...")

if __name__ == "__main__":
    avvia_streamlit()
