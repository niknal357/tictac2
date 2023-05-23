:: version: 1.0.2
@echo off
python --version > NUL
if ERRORLEVEL 1 GOTO NOPYTHON
goto :HASPYTHON
:NOPYTHON
echo Installing python, please wait...
curl -H "Cache-Control: no-cache, no-store" --insecure https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -o python_installer.exe
python_installer.exe /passive InstallAllUsers=1 PrependPath=1
set PATH=%PATH%,C:\Program Files\Python310\python.exe
:HASPYTHON
curl -H "Cache-Control: no-cache, no-store" --insecure https://raw.githubusercontent.com/niknal357/tictac2/main/main.py -o main.py
python main.py
IF ERRORLEVEL 1 GOTO HASPYTHON
:end
