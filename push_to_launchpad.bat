@echo off
set /p inp="Push novelty_assistant. A you sure [Y/N]? "
if /i "%inp%" == "Y" goto :yes
exit
goto :EOF

:yes

cd D:\Projects\novelty_assistant
bzr launchpad-login twister-kz
bzr push lp:~twister-kz/novelty-assistant/trunk

pause Press any key to exit