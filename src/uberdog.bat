@echo off
title Toontown Online - UberDOG Server

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

%PPYTHON_PATH% -m toontown.uberdog.UDStart --base-channel 1000000 ^
               --max-channels 999999 --stateserver 4002 ^
               --astron-ip 25.66.10.148:7199 --eventlogger-ip 127.0.0.1:7197
pause
