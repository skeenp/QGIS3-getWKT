rem Clean Build
rmdir /s /q QGIS3-getWKT
mkdir QGIS3-getWKT

rem Compile Resources
CALL python -m PyQt5.pyrcc_main -o resources.py resources.qrc

rem Copy all files
xcopy *.py QGIS3-getWKT\
xcopy *.ui QGIS3-getWKT\
xcopy LICENSE QGIS3-getWKT\
xcopy metadata.txt QGIS3-getWKT\
