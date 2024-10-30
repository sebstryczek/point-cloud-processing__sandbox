#!/bin/sh

echo "Running: setup.sh"
echo "Current directory:" $(pwd)

CMAKE_VERSION="3.22.2"
sh /install-cmake.sh ${CMAKE_VERSION}

echo "Done: setup.sh"

tail -f /dev/null
