@echo off
echo Installing required packages...
py -m pip install flask flask-cors simpy

echo.
echo Starting Erlang C Simulation Server...
echo Server will be available at http://localhost:5000
echo.

py SimpleErlangC_server.py

pause 