@echo off
echo Avvio del Visualizzatore Ferri Strutturali con Streamlit...
echo ========================================================
echo.
echo Il visualizzatore si aprirà automaticamente nel browser.
echo Per fermare l'applicazione, premi Ctrl+C
echo.
C:\Users\Utente\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe run app.py --server.headless true --server.port 8501
pause
