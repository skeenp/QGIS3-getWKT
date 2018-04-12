rem Clean Build
rmdir /s /q getwkt
mkdir getwkt

rem Setup OSGeo Paths
call o4w_env.bat
call py3_env.bat
call qt5_env.bat

rem Compile Resources
call pyrcc5.bat -o resources.py resources.qrc

rem Copy all files
xcopy *.png getwkt\
xcopy *.py getwkt\
xcopy *.ui getwkt\
xcopy licence.txt getwkt\
xcopy metadata.txt getwkt\
