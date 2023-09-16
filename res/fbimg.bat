@shift /0
@echo off
mode con cols=90 lines=40
:STARTS
TITLE 线刷工具箱
color 5f
cd %cd%
CLS
ECHO. 
ECHO.                                 线刷工具箱工具箱（MIX2S）
ECHO.                    
ECHO.                                                                    ----------BY XEKNICE
ECHO.=========================================================================================
ECHO. 该工具适用于MIX2S手机fastboot线刷
ECHO.       0.刷入recovery镜像分区
ECHO.       1.刷入boot镜像分区
ECHO.       2.刷入system镜像分区
ECHO.       3.刷入vendor镜像分区
ECHO.       (其他镜像直接输入镜像名)
ECHO.       B.临时启动BOOT/REC镜像
ECHO.       E.格式化镜像分区
ECHO.       F.安装驱动
ECHO.       R.重启手机
ECHO.       C.关闭程序
ECHO.=========================================================================================
:CHO
set choice=
set /p choice=请输入您的选项或者要刷的分区镜像
if /i "%choice%"=="0" goto rec
if /i "%choice%"=="1" goto boot
if /i "%choice%"=="2" goto system
if /i "%choice%"=="3" goto vendor
if /i "%choice%"=="B" goto RUNBOOT
if /i "%choice%"=="E" goto erase
if /i "%choice%"=="F" goto FIX
if /i "%choice%"=="C" goto COLOSE
if /i "%choice%"=="R" goto RUN
if /i "%choice%"=="" goto SB
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                                  自定义线刷。。。。
ECHO.
ECHO.=========================================================================================
echo. 
set local=
set /p choice=请输入镜像路径
fastboot flash %choice% %local%
pause
echo.
GOTO STARTS

:FIX
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                            正在安装/修复驱动中...
ECHO.
ECHO.=========================================================================================
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\usbflags\18D1D00D0100" /v "osvc" /t REG_BINARY /d "0000" /f
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\usbflags\18D1D00D0100" /v "SkipContainerIdQuery" /t REG_BINARY /d "01000000" /f
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\usbflags\18D1D00D0100" /v "SkipBOSDescriptorQuery" /t REG_BINARY /d "01000000" /f
start /wait FIX.exe /S
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                       安装/修复驱动完成，重启电脑效果最好
ECHO.
ECHO.=========================================================================================
pause
goto STARTS

:RUN
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                                      重启手机中
ECHO.
ECHO.=========================================================================================
fastboot reboot
goto STARTS

:rec
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                                   REC镜像刷入。。。
ECHO.
ECHO.=========================================================================================
echo. 
set localar=
set /p localar=请输入镜像路径
fastboot flash recovery %localar%
pause
echo.
GOTO STARTS

:RUNBOOT
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                        临时启动BOOT/REC镜像
ECHO.
ECHO.=========================================================================================
echo. 
set BOOT=
set /p BOOT=请输入镜像路径
fastboot boot %BOOT%
pause
echo.
GOTO STARTS

:boot
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                                   BOOT镜像刷入。。。
ECHO.
ECHO.=========================================================================================
echo. 
set locala=
set /p locala=请输入镜像路径
fastboot flash boot %locala%
pause
echo.
GOTO STARTS

:system
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                                  SYSTEM镜像刷入。。。
ECHO.
ECHO.=========================================================================================
echo. 
set localb=
set /p localB=请输入镜像路径
fastboot flash system %localb%
pause
echo.
GOTO STARTS

:VENDOR
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                                  VENDOR镜像刷入。。。
ECHO.
ECHO.=========================================================================================
echo. 
set localc=
set /p localC=请输入镜像路径
fastboot flash vendor %localc%
pause
echo.
GOTO STARTS

:erase
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                              fastboot自定义格式化分区
ECHO.
ECHO.=========================================================================================
set erase=
set /p erase=请输入您需要格式化的分区
fastboot erase %erase%
pause
echo.
GOTO STARTS

:SB
ECHO. 您输入的为空！请重新刷入！
pause
echo.
GOTO STARTS

:COLOSE
EXIT