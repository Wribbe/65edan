#!/bin/sh

URL="http://cs.lth.se/edan65/week-by-week/"
KEYWORD="lecture"
SLIDEPATH="slides"
SCRIPTPATH="../scripts"

cd $SLIDEPATH
python ${SCRIPTPATH}/pull_lectures.py $URL $KEYWORD
cd ..
