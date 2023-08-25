python -m venv webdeck
webdeck\Scripts\activate.bat
pip install -r requirements.txt
python setup.py build

cd build
cd exe.win-amd64-3.11
"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool" sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WebDeck.exe
"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool" sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WD_main.exe