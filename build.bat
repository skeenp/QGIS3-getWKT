rem Clean Build
rmdir /s /q getwkt
mkdir getwkt

rem Compile Resources
CALL python -m PyQt5.pyrcc_main -o resources.py resources.qrc

rem Copy all files
xcopy *.png getwkt\
xcopy *.py getwkt\
xcopy *.ui getwkt\
xcopy licence.txt getwkt\
xcopy metadata.txt getwkt\

pause