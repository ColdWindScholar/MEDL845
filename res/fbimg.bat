@shift /0
@echo off
mode con cols=90 lines=40
:STARTS
TITLE ��ˢ������
color 5f
cd %cd%
CLS
ECHO. 
ECHO.                                 ��ˢ�����乤���䣨MIX2S��
ECHO.                    
ECHO.                                                                    ----------BY XEKNICE
ECHO.=========================================================================================
ECHO. �ù���������MIX2S�ֻ�fastboot��ˢ
ECHO.       0.ˢ��recovery�������
ECHO.       1.ˢ��boot�������
ECHO.       2.ˢ��system�������
ECHO.       3.ˢ��vendor�������
ECHO.       (��������ֱ�����뾵����)
ECHO.       B.��ʱ����BOOT/REC����
ECHO.       E.��ʽ���������
ECHO.       F.��װ����
ECHO.       R.�����ֻ�
ECHO.       C.�رճ���
ECHO.=========================================================================================
:CHO
set choice=
set /p choice=����������ѡ�����Ҫˢ�ķ�������
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
ECHO.                                  �Զ�����ˢ��������
ECHO.
ECHO.=========================================================================================
echo. 
set local=
set /p choice=�����뾵��·��
fastboot flash %choice% %local%
pause
echo.
GOTO STARTS

:FIX
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                            ���ڰ�װ/�޸�������...
ECHO.
ECHO.=========================================================================================
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\usbflags\18D1D00D0100" /v "osvc" /t REG_BINARY /d "0000" /f
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\usbflags\18D1D00D0100" /v "SkipContainerIdQuery" /t REG_BINARY /d "01000000" /f
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\usbflags\18D1D00D0100" /v "SkipBOSDescriptorQuery" /t REG_BINARY /d "01000000" /f
start /wait FIX.exe /S
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                       ��װ/�޸�������ɣ���������Ч�����
ECHO.
ECHO.=========================================================================================
pause
goto STARTS

:RUN
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                                      �����ֻ���
ECHO.
ECHO.=========================================================================================
fastboot reboot
goto STARTS

:rec
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                                   REC����ˢ�롣����
ECHO.
ECHO.=========================================================================================
echo. 
set localar=
set /p localar=�����뾵��·��
fastboot flash recovery %localar%
pause
echo.
GOTO STARTS

:RUNBOOT
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                        ��ʱ����BOOT/REC����
ECHO.
ECHO.=========================================================================================
echo. 
set BOOT=
set /p BOOT=�����뾵��·��
fastboot boot %BOOT%
pause
echo.
GOTO STARTS

:boot
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                                   BOOT����ˢ�롣����
ECHO.
ECHO.=========================================================================================
echo. 
set locala=
set /p locala=�����뾵��·��
fastboot flash boot %locala%
pause
echo.
GOTO STARTS

:system
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                                  SYSTEM����ˢ�롣����
ECHO.
ECHO.=========================================================================================
echo. 
set localb=
set /p localB=�����뾵��·��
fastboot flash system %localb%
pause
echo.
GOTO STARTS

:VENDOR
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                                  VENDOR����ˢ�롣����
ECHO.
ECHO.=========================================================================================
echo. 
set localc=
set /p localC=�����뾵��·��
fastboot flash vendor %localc%
pause
echo.
GOTO STARTS

:erase
CLS
ECHO.=========================================================================================
ECHO.
ECHO.                              fastboot�Զ����ʽ������
ECHO.
ECHO.=========================================================================================
set erase=
set /p erase=����������Ҫ��ʽ���ķ���
fastboot erase %erase%
pause
echo.
GOTO STARTS

:SB
ECHO. �������Ϊ�գ�������ˢ�룡
pause
echo.
GOTO STARTS

:COLOSE
EXIT