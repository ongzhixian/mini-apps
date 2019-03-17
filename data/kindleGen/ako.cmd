@ECHO OFF
REM Converts a markdown document to HTML
REM python -m markdown temp.md > temp.html
REM for %%f in (DIR zxtech-md) ECHO %%f
REM FOR %%G IN ("Hello World") DO Echo %%G

IF [%1] == [] GOTO HELP

ECHO Cleaning existing .md.html files.
IF EXIST %1-md\*.html DEL %1-md\*.html

ECHO Generating HTML files from markdown files.
FOR %%G in (%1-md\*.md) DO type %1-md\header.tmpl.txt > %%Ghtml
FOR %%G in (%1-md\*.md) DO python -m markdown %%G >> %%Ghtml
FOR %%G in (%1-md\*.md) DO type %1-md\footer.tmpl.txt >> %%Ghtml

ECHO Renaming file extensions
REN %1-md\*.mdhtml *.html

ECHO Copying files
FOR %%G in (%1-md\*.html) DO COPY %%G %1

ECHO Making MOBI
CALL mk.cmd %1

ECHO ALL DONE!

GOTO END

:HELP
ECHO Incorrect syntax.
ECHO.
ECHO The correct syntax should be as follows:
ECHO.
ECHO Convert [folder-name]
ECHO.
ECHO.


:END