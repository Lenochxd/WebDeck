@echo off

for %%I in ("%~dp0") do set "current_dir=%%~fI"

D:\Users\81len\AppData\Roaming\Python\Python311\Scripts\pyinstaller --noconfirm --onedir --windowed --name "WebDeck" --clean  --icon "%current_dir%/static/files/icon.ico" "%current_dir%/main.py"
D:\Users\81len\AppData\Roaming\Python\Python311\Scripts\pyinstaller --noconfirm --onedir --windowed --name "WD_main" "%current_dir%/main_server.py"

REM déplacer le dossier /dist/WD_main dans /dist/WebDeck
xcopy "%current_dir%\dist\WD_main\*" "%current_dir%\dist\WebDeck\" /s /y
@RD /S /Q "%current_dir%\dist\WD_main"

D:\Users\81len\AppData\Roaming\Python\Python311\Scripts\pyinstaller --noconfirm --onedir --windowed --name "WD_start" "%current_dir%/start_server.py"

REM déplacer le dossier /dist/WD_start dans /dist/WebDeck
xcopy "%current_dir%\dist\WD_start\*" "%current_dir%\dist\WebDeck\" /s /y
@RD /S /Q "%current_dir%\dist\WD_start"

REM copier racine dans /dist/WebDeck
for %%F in ("%current_dir%\*") do (
    set "excludeFolder=0"
    for %%X in (.git .vscode __pycache__ _compile build dist) do (
        if "%%~nxF"=="%%~X" set "excludeFolder=1"
    )
    if "!excludeFolder!"=="0" (
        xcopy "%%F" "%current_dir%\dist\WebDeck\" /s /y
    )
)


echo Files moved successfully.
