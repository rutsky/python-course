#!/bin/bash

for f in *.pycon; do
  pygmentize -l pycon -O font_name="DejaVu Sans Mono",font_size=24 -o ${f%.*}.png $f
done

for f in *.py; do
  pygmentize -O font_name="DejaVu Sans Mono",font_size=24 -o ${f%.*}.png $f
done
