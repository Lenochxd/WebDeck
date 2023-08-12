@echo off

for %%I in ("%~dp0") do set "current_dir=%%~fI"

D:\Users\81len\AppData\Roaming\Python\Python311\Scripts\pyinstaller --noconfirm --onedir --windowed --name "WebDeck" --add-data "%current_dir%;WebDeck/" --icon "%current_dir%/static/files/icon.ico" "%current_dir%/main.py"
D:\Users\81len\AppData\Roaming\Python\Python311\Scripts\pyinstaller --noconfirm --onedir --console --name "WD_main" "%current_dir%/main_server.py"

REM déplacer le dossier /dist/WD_main dans /dist/WebDeck
move /y "%current_dir%\dist\WD_main\*" "%current_dir%\dist\WebDeck\"

D:\Users\81len\AppData\Roaming\Python\Python311\Scripts\pyinstaller --noconfirm --onedir --windowed --name "WD_start" "%current_dir%/start_server.py"

REM déplacer le dossier /dist/WD_start dans /dist/WebDeck
move /y "%current_dir%\dist\WD_start\*" "%current_dir%\dist\WebDeck\"

REM copier racine dans /dist/WebDeck
move /y "%current_dir%\dist\WebDeck\Webdeck\*" "%current_dir%\dist\Webdeck\"


echo Files moved successfully.
pause