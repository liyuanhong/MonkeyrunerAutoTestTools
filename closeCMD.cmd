@echo off
rem ¹Ø±Õcmd´°¿Ú
for /f " tokens=2 delims= " %%i in ('..\\getAdbPid') do taskkill /f /pid %%i
rem for /f " tokens=2 delims= " %%i in ('..\\getAdbPid') do set id=%%i
rem taskkill /f /pid %id%