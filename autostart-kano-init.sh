#!/bin/sh

# autostart-kano-init.sh
#
# Copyright (C) 2014 Kano Computing Ltd.
# License:   http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# 0: Disabled
# 1: Name
# 2: Email
# 4: Riddle
# 9: Reset

STAGE=0

if [ `id -u` -eq 0 -a "$STAGE" -gt 0 ]; then
    kano-init "$STAGE"
    kill -HUP $PPID
fi


