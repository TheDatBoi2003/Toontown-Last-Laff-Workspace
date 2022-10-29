@echo off
title Toontown Online - AI (District) Server


rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

:main
%PPYTHON_PATH% -m toontown.ai.AIStart --base-channel 401000000 ^
               --max-channels 999999 --stateserver 4002 ^
               --astron-ip 25.66.10.148:7199 --eventlogger-ip 25.66.10.148:7197 ^
               --district-name "Toon Valley"
goto main
