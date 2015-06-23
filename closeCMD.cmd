@echo off
rem ¹Ø±Õcmd´°¿Ú
for /f " tokens=2 delims= " %%i in ('..\\getAdbPid') do taskkill /f /pid %%i