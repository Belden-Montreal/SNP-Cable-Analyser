#!/bin/bash

# TODO: replace with a makefile or something better than a shell script

DIR_GUI="."
DIR_UI="$DIR_GUI/ui"
DIR_RES="$DIR_GUI/ressources"

PACKAGE_RES="gui.ressources"

find "$DIR_UI" -type f -iname "*.ui" | while read UI_FILE; do
    BASENAME=$(basename "$UI_FILE" ".ui")
    DIRNAME=$(dirname "$UI_FILE")
    echo "Generating '$DIRNAME/$BASENAME.py'"
    pyuic5 -x "$DIRNAME/$BASENAME.ui" -o "$DIRNAME/$BASENAME.py" --import-from="$PACKAGE_RES"
done

find "$DIR_RES" -type f -iname "*.qrc" | while read QRC_FILE; do
    FILENAME=$(basename "$QRC_FILE" ".qrc")
    echo "Generating '$DIR_RES/$FILENAME.py'"
    pyrcc5 -o "$DIR_RES/$FILENAME.py" "$DIR_RES/$FILENAME.qrc"
done
