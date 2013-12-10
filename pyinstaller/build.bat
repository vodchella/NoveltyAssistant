@echo off
set /p inp="Building novelty_assistant. A you sure [Y/N]? "
if /i "%inp%" == "Y" goto :yes
exit
goto :EOF

:yes
echo Building started...

cd C:\Python27\Scripts

python D:\Distr\PyInstaller-2.1\pyinstaller.py D:\Projects2\novelty_assistant\pyinstaller\novelty_assistant.spec

rmdir /s /q "D:\Projects2\novelty_assistant\pyinstaller\build"
del D:\Projects2\novelty_assistant\pyinstaller\warnnovelty_assistant.txt


echo Compressing started...

:EXED
DEL "D:\Projects2\build_novelty_assistant\Novelty Assistant_compressed.ex_"
IF EXIST "D:\Projects2\build_novelty_assistant\Novelty Assistant_compressed.ex_" GOTO EXED

cd D:\Distr\upx
upx.exe -9 -o"D:\Projects2\novelty_assistant\pyinstaller\dist\Novelty Assistant_compressed.ex_" "D:\Projects2\novelty_assistant\pyinstaller\dist\Novelty Assistant.exe"

:EXED1
DEL "D:\Projects2\novelty_assistant\pyinstaller\dist\Novelty Assistant.exe"
IF EXIST "D:\Projects2\novelty_assistant\pyinstaller\dist\Novelty Assistant.exe" GOTO EXED1

RENAME "D:\Projects2\novelty_assistant\pyinstaller\dist\Novelty Assistant_compressed.ex_" "Novelty Assistant.exe"

pause Press any key to exit