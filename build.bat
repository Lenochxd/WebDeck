@echo off
echo Starting...

rem Créer un environnement virtuel
python -m venv webdeck

rem Activer l'environnement virtuel
call webdeck\Scripts\activate.bat

rem Installer les dépendances
pip install -r requirements.txt

rem Compiler le projet
python setup.py build

rem Naviguer vers le répertoire de build
cd build\exe.win-amd64-3.11

rem Signer le premier exécutable
"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool" sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WebDeck.exe

rem Signer le deuxième exécutable
"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool" sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WD_main.exe

rem Signer le troisième exécutable
"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool" sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WD_updater.exe

echo Toutes les commandes ont été exécutées avec succès.
