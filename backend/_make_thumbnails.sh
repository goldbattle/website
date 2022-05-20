#!/bin/bash


rm -rf thumbnails/
mkdir -p thumbnails/

# mogrify -path thumbnails/ -thumbnail 200x200 images/*.png
# mogrify -path thumbnails/ -thumbnail 200x200 images/*.jpg


# https://superuser.com/a/368134/707974
# https://imagemagick.org/script/mogrify.php
# https://askubuntu.com/questions/25356/decrease-filesize-when-resizing-with-mogrify
mogrify -path thumbnails/ -strip -thumbnail 200x200^ -gravity center -extent 200x200 images/*.png
mogrify -path thumbnails/ -strip -thumbnail 200x200^ -gravity center -extent 200x200 images/*.jpg

# convert -define jpeg:size=200x200 original.jpeg  -thumbnail 100x100^ -gravity center -extent 100x100  thumbnail.jpeg
