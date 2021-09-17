#!/bin/bash
set -x

echo "test"

read test

if [ $test = "wow" ]
then
	echo "wooo!"
else
	echo "oh no"
fi
