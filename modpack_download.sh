#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 -m venv $DIR/python/venv
$DIR/python/venv/bin/pip3 install requests | grep -v 'already satisfied'
$DIR/python/venv/bin/python3 $DIR/python/jaru_download.py "uT32vpVyWz4wHQ" "/LetsFlame's Create 1.0"
