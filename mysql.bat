cls   
@echo off  
:设置窗口字体颜色  
color 0a   
:设置窗口标题  
TITLE MySQL管理程序  
    
call :checkAdmin  
    
goto menu  
:菜单  
:menu  
cls  
echo.   
echo.=-=-=-=-请选择您要对MySQL的操作-=-=-=-=-  
echo.  
echo.1: 启动MySQL  
echo.  
echo.2: 关闭MySQL  
echo.   
echo.3: 重启MySQL  
echo.   
echo.4: 退 出  
echo.  
echo.=-=-=-=-请输入您要选择的项目序号↓-=-=-=-  
set /p id=  
if "%id%"=="1" goto startup  
if "%id%"=="2" goto shutdown  
if "%id%"=="3" goto reboot  
if "%id%"=="4" exit  
pause  
    
:启动  
:startup  
echo.  
call :checkMySQL 1  
echo.启动MySQL......  
net start "MySQL"  
echo.启动MySQL成功！  
pause   
goto menu   
    
:停止  
:shutdown  
echo.  
call :checkMySQL 2  
echo.关闭MySQL......  
net stop "MySQL"  
echo.关闭MySQL成功！  
pause   
goto menu  
    
:重启  
:reboot  
echo.  
call :checkMySQL 2  
echo.关闭MySQL......  
net stop "MySQL"  
echo.关闭MySQL成功！  
goto startup  
goto menu  
    
:退出  
:goout  
pause  
goto menu  
    
:检查MySQL进程是否存在  
:checkMySQL  
set /a count=0  
for /f "tokens=1 delims= " %%i in ('tasklist /nh ^| find /i "MySQL"') do (set /a count+=1)  
if %count% neq 0 if "%1" equ "1" (  
  echo 警告：MySQL已启动  
  goto goout  
)  
if %count% equ 0 if "%1" equ "2" (  
  echo 警告：MySQL未启动  
  goto goout  
)  
    
:检查是否是以管理员身份运行  
:checkAdmin  
echo test am i admin? > %SystemRoot%\System32\test.sunhao  
if not exist %SystemRoot%\System32\test.sunhao (  
  echo 警告：请以管理员身份运行！  
  pause  
  exit  
)  
del %SystemRoot%\System32\test.sunhao  