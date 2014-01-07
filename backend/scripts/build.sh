#!/bin/sh

PROJECT_NAME=planmate
VIRTUALENV_DIR=/usr/local/bin

ROOT_DIR=$(cd $(dirname $0)/..; pwd)

rm -rf $ROOT_DIR/lib/ $ROOT_DIR/eggs/ $ROOT_DIR/develop-eggs/ $ROOT_DIR/.installed.cfg
$VIRTUALENV_DIR/virtualenv --no-site-packages --clear --distribute $ROOT_DIR
$ROOT_DIR/bin/python $ROOT_DIR/bootstrap.py
$ROOT_DIR/bin/buildout
$ROOT_DIR/bin/python $ROOT_DIR/src/$PROJECT_NAME/setup.py develop
