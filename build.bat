@echo off

rem Rebuild resources using pyrcc (Qt tool) via OSGeo4W Python
setlocal enabledelayedexpansion

echo Attempting to rebuild resources with PyQt5...
rem Use OSGeo4W Python where PyQt5 is installed
python -m PyQt5.pyrcc_main -o resources.py resources.qrc
if errorlevel 1 exit /b 1

rem Replace PyQt5 imports with PyQt6 imports for Qt6 compatibility
powershell -Command "(Get-Content resources.py) -replace 'from PyQt5', 'from PyQt6' | Set-Content resources.py"

rem Clean Build
rmdir /s /q QGIS4-getWKT
mkdir QGIS4-getWKT

rem Copy all files
xcopy *.py QGIS4-getWKT\
xcopy *.ui QGIS4-getWKT\
xcopy LICENSE QGIS4-getWKT\
xcopy metadata.txt QGIS4-getWKT\
xcopy wkt.png QGIS4-getWKT\
