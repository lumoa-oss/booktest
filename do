#!/bin/bash

_script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

( cd "$_script_dir" && python do.py "$@" )