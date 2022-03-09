#!/bin/bash

mkdir -p thumbnails/

mogrify -path thumbnails/ -thumbnail 200x200 downloads/images/*.png
mogrify -path thumbnails/ -thumbnail 200x200 downloads/images/*.jpg

