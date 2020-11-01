#!/bin/bash

TAG_REF=$1

echo "Performing checks for version $TAG_REF"

# check setup.py
setup_py_version=`grep "version=" setup.py | cut -d '"' -f2`
if [ "$setup_py_version" != "$TAG_REF" ]; then
    echo "ERROR: setup.py contains version $setup_py_version which differs from $TAG_REF"
    exit 1
fi

echo "All checks passed."
exit 0