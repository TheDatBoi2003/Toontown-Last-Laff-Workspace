@echo off
title Toontown Online - Developer Mini-Server Launcher

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo Toontown Online Developer Mini-Server Launcher
echo.
echo NOTE: Make sure that "mini-server" is enabled in your settings.json!
echo.

set /P TTOFF_LOGIN_TOKEN="Username (default: dev): " || ^
set TTOFF_LOGIN_TOKEN=player

set /P TTOFF_GAME_SERVER="Game Server (default: 25.66.10.148): " || ^
set TTOFF_GAME_SERVER=25.66.10.148

%PPYTHON_PATH% -m toontown.launcher.TTOffQuickStartLauncher
pause
