@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x64 %*
"C:\Panda3D-1.11.0-x64\python\python.exe" -m src.prepare
"C:\Panda3D-1.11.0-x64\python\python.exe" -m src.make
"C:\Panda3D-1.11.0-x64\python\python.exe" -m src.multify
mkdir "bin\panda3d\"
COPY "C:\Panda3D-1.11.0-x64\bin\*.dll" "bin\panda3d\"
COPY "C:\Panda3D-1.11.0-x64\panda3d\*.pyd" "bin\panda3d\"
COPY "C:\Panda3D-1.11.0-x64\python\DLLs\*" "bin\"
COPY "..\dependencies\libpandadna\windows\libpandadna.pyd" "bin\"