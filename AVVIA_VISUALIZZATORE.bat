@echo off
echo ============================================
echo    VISUALIZZATORE FERRI STRUTTURALI
echo ============================================
echo.
echo Avvio in corso...
echo.
echo L'applicazione sarà disponibile su:
echo http://localhost:8501
echo.
echo Per fermare l'app: Ctrl+C
echo ============================================
echo.

REM Imposta il percorso Python
set PYTHON_PATH=C:\Users\Utente\AppData\Local\Programs\Python\Python313

REM Avvia Streamlit
"%PYTHON_PATH%\Scripts\streamlit.exe" run app.py --server.port 8501 --server.address localhost

echo.
echo L'applicazione è stata fermata.
pause
