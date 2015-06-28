@echo off
for /f  "tokens=2 delims= " %%i in ('%cd%\\..\\tools\\platform-tools\\getPidInfo.cmd') do set pid=%%i
echo %pid%