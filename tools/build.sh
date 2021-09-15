#!/bin/bash
set -ex

# This is a build script for fonts on linux
# Usage: build.sh <ttf/otf font file> <output file prefix>
# 
# example:
# % build.sh NotoSansJP-Regular.otf NotoSans
# will create:
#   NotoSans16jp.mpy, NotoSans20jp.mpy, ...., and NotoSans52jp.mpy

INPUT=$1
OUTPUT_PREFIX=$2

if [ "$1" == "" ] || [ "$2" == "" ]; then
    echo font converter for SDFont Module. 
    echo This utility converts font from .ttf/.otf to .mpy
    echo "Usage: $0 <font name> <output file prefix>

for i in 16 20 24 28 32 36 40 44 48 52; do 
    FILE=${OUTPUT_PREFIX}${i}jp.py
    ./font_to_py.py -k ascii+jis_x_0208.txt ${INPUT} ${i} ${FILE}
    mpy-cross -O2 -X heapsize=8000000 ${FILE}
done
