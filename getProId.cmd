@echo off
for /f "delims=" %%t in ('..\\getProInfo') do set str=%%t
echo %str%

rem 关闭monkeyrunner进程，实际上是一个java.exe进程
for /f " tokens=2 delims= " %%i in ('..\\getProInfo') do set id=%%i
taskkill /f /pid %id%

rem 关闭cmd窗口
for /f " tokens=2 delims= " %%i in ('..\\getCMDProInfo') do taskkill /f /pid %%i

pause