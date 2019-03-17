@ECHO OFF

ECHO Zipping files ...
PowerShell -Command "& { Compress-Archive -Path .\%1\* -DestinationPath %1.zip -Force }

IF EXIST %1.epub DEL %1.epub

ECHO Rename zip to epub ...
REN %1.zip %1.epub

ECHO Running kindlegen
kindlegen %1.epub
