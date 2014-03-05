#!/bin/sh

here=`pwd`
rootDir=`dirname $here`

path=$rootDir/parts/planmate/inflection/__init__.py

if [ ! -e $path ]; then
  echo "touch $path"
  touch $path
fi
