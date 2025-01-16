rem Build Plugin
call build.bat

rem Clean old plugin
rmdir /s /q "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\getwkt_dev"
mkdir "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\getwkt_dev"

rem Move plugin to plugins folder
xcopy /s /y QGIS3-getWKT "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\getwkt_dev\"
xcopy /s /y "metadata-dev.txt" "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\getwkt_dev\metadata.txt"