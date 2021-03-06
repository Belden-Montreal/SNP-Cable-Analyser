#!/bin/bash

# TODO: replace with a makefile or something better than a shell script

DIR_GUI="."
DIR_UI="$DIR_GUI/ui"
DIR_RES="$DIR_GUI/ressources"

PACKAGE_RES="snpanalyzer.gui.ressources"

find "$DIR_UI" -type f -iname "*.ui" | while read UI_FILE; do
    BASENAME=$(basename "$UI_FILE" ".ui")
    DIRNAME=$(dirname "$UI_FILE")

    UI_FILE="$DIRNAME/$BASENAME.ui"
    PY_FILE="$DIRNAME/$BASENAME.py"

    if [[ "$PY_FILE" -nt "$UI_FILE" ]]; then
        echo "No changed made to '$PY_FILE'"
        continue
    fi

    echo "Generating '$PY_FILE'"
    pyuic5 -x "$UI_FILE" -o "$PY_FILE" --import-from="$PACKAGE_RES"
done

find "$DIR_RES" -type f -iname "*.qrc" | while read RC_FILE; do
    BASENAME=$(basename "$RC_FILE" ".qrc")
    DIRNAME=$(dirname "$RC_FILE")

    RC_FILE="$DIRNAME/$BASENAME.qrc"
    PY_FILE="$DIRNAME/$BASENAME.py"

    if [[ "$PY_FILE" -nt "$RC_FILE" ]]; then
        echo "No changed made to '$PY_FILE'"
        continue
    fi

    echo "Generating '$PY_FILE'"
    pyrcc5 -o "$PY_FILE" "$RC_FILE"
done
