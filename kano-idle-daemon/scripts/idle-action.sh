#!/bin/bash

# idle-action.sh
#
# Copyright (C) 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# This script is executed by the kano-idle-daemon.
#
# NOTE: Exiting with a non-zero rc will be interpreted as a retry by the daemon.


echo "Hello from idle_action.sh"

/usr/bin/design-museum-reset
