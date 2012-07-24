@echo off
set /p inp="Building novelty_assistant. A you sure [Y/N]? "
if /i "%inp%" == "Y" goto :yes
exit
goto :EOF

:yes
echo Building started...

cd D:\Twister\python\pyinstaller

D:\Twister\python\python.exe Build.py D:\Twister\Dropbox\novelty_assistant\pyinstaller\novelty_assistant.spec

rmdir /s /q "D:\Twister\Dropbox\novelty_assistant\pyinstaller\build"
del D:\Twister\Dropbox\novelty_assistant\pyinstaller\warnnovelty_assistant.txt


echo Compressing started...

:EXED
DEL "D:\Projects\build_novelty_assistant\Novelty Assistant_compressed.ex_"
IF EXIST "D:\Projects\build_novelty_assistant\Novelty Assistant_compressed.ex_" GOTO EXED

cd D:\Programms\upx
upx.exe -9 -o"D:\Projects\build_novelty_assistant\Novelty Assistant_compressed.ex_" "D:\Projects\build_novelty_assistant\Novelty Assistant.exe"

:EXED1
DEL "D:\Projects\build_novelty_assistant\Novelty Assistant.exe"
IF EXIST "D:\Projects\build_novelty_assistant\Novelty Assistant.exe" GOTO EXED1

RENAME "D:\Projects\build_novelty_assistant\Novelty Assistant_compressed.ex_" "Novelty Assistant.exe"

pause Press any key to exit