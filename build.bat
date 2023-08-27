@echo off
echo Starting...

rem Create a virtual environment
python -m venv webdeck

rem Activate the virtual environment
call webdeck\Scripts\activate.bat

rem Install dependencies
pip install -r requirements.txt

rem Compile the project
python setup.py build

rem Navigate to the build directory
cd build
cd exe.win-amd64-3.11

rem Sign the first executable
"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool" sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WebDeck.exe

rem Sign the second executable
"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool" sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WD_main.exe

rem Sign the third executable
"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool" sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WD_updater.exe

echo Build done!
