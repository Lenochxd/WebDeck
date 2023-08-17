@echo off

for %%I in ("%~dp0") do set "current_dir=%%~fI"

D:\Users\81len\AppData\Roaming\Python\Python311\Scripts\pyinstaller --noconfirm --onefile --windowed --name "WebDeck" --icon "%current_dir%/static/files/icon.ico" "%current_dir%/main.py"

REM copier racine dans /dist/WebDeck
xcopy "%current_dir%\*" "%current_dir%\dist\" /s /y

D:\Users\81len\AppData\Roaming\Python\Python311\Scripts\pyinstaller --noconfirm --onefile --console --name "WD_main" "%current_dir%/main_server.py"

REM déplacer le dossier /dist/WD_main dans /dist/WebDeck
xcopy "%current_dir%\dist\WD_main\*" "%current_dir%\dist\WebDeck\" /s /y
@RD /S /Q "%current_dir%\dist\WD_main"

D:\Users\81len\AppData\Roaming\Python\Python311\Scripts\pyinstaller --noconfirm --onefile --windowed --name "WD_start" "%current_dir%/start_server.py"

REM déplacer le dossier /dist/WD_start dans /dist/WebDeck
xcopy "%current_dir%\dist\WD_start\*" "%current_dir%\dist\WebDeck\" /s /y
@RD /S /Q "%current_dir%\dist\WD_start"


echo Files moved successfully.
pause