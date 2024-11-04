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

rem Remove the dist directory
rmdir /s /q dist

rem Compile the project and build the MSI installer using cx_Freeze
python setup.py bdist_msi

echo Build done!
explorer dist