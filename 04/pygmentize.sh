#!/bin/bash

set -x

for f in `find -iname '*.pycon'`; do
  pygmentize -l pycon -O font_name="DejaVu Sans Mono",font_size=24 -o ${f%.*}.png $f
  pygmentize -l pycon -O full -o ${f%.*}.html $f
done

for f in `find -iname '*.py'`; do
  pygmentize -O font_name="DejaVu Sans Mono",font_size=24 -o ${f%.*}.png $f
  pygmentize -O full -o ${f%.*}.html $f
done
