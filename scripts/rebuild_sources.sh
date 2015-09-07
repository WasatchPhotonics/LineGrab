#!/bin/bash
#
# run supporting pyuic, pyrcc files to generate resource files and qt
# designer conversions. Run this from the home project directory like:
# WasatchAnalyzeIQ $ ./scripts/rebuild_sources.sh

pyuic4 \
    linegrab/ui/linegrab_layout.ui \
    -o linegrab/ui/linegrab_layout.py

pyrcc4 \
    linegrab/ui/iconagraphy.qrc \
    -o linegrab/ui/iconagraphy_rc.py

