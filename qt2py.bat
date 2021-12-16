pyrcc5 -o Pictures\images.py Pictures\images.qrc
for %%i in ("UI/*.ui") do  pyuic5 -x UI/%%i -o UI/%%~ni.py
