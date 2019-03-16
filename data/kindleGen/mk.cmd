@ECHO OFF

ECHO Zipping files ...
PowerShell -Command "& { Compress-Archive -Path .\zxtech\* -DestinationPath zxtech.zip -Force }

IF EXIST zxtech.epub DEL zxtech.epub

ECHO Rename zip to epub ...
REN zxtech.zip zxtech.epub

ECHO Running kindlegen
kindlegen zxtech.epub