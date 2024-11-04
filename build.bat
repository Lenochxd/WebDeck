@echo off
echo Starting...

rem Create a virtual environment
python -m venv venv

rem Activate the virtual environment
call venv\Scripts\activate.bat

rem Install dependencies
pip install -r requirements.txt

rem Remove the build directory
rmdir /s /q build

rem Compile the project and build the MSI installer using cx_Freeze
python setup.py bdist_msi

rem Navigate to the build directory
cd build/exe.win-amd64-3.11

rem Sign the main executable
signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WebDeck.exe

rem Sign the updater executable
signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 update.exe

echo Build done!
explorer .