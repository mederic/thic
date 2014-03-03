#! /bin/bash

ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)

#cp result.pickle.copy result.pickle

monkeyrunner $ABSOLUTE_PATH/thic.py $@
$ABSOLUTE_PATH/thic_compare.py $@