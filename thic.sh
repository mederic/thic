#! /bin/bash

ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)

monkeyrunner $ABSOLUTE_PATH/thic.py $@
$ABSOLUTE_PATH/thic_compare.py $@