rem Build Plugin
call build.bat

rem Clean old plugin
rmdir /s /q "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\getwkt"
mkdir "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\getwkt"

rem Move plugin to plugins folder
xcopy  /s /y getwkt "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\getwkt\"