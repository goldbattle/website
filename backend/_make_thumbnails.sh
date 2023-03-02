#!/bin/bash



# mogrify -path thumbnails/ -thumbnail 200x200 images/*.png
# mogrify -path thumbnails/ -thumbnail 200x200 images/*.jpg


# conver the static images into thumbnails of uniform size and centering
# https://superuser.com/a/368134/707974
# https://imagemagick.org/script/mogrify.php
# https://askubuntu.com/questions/25356/decrease-filesize-when-resizing-with-mogrify
# convert -define jpeg:size=200x200 original.jpeg  -thumbnail 100x100^ -gravity center -extent 100x100  thumbnail.jpeg
rm -rf thumbnails/
mkdir -p thumbnails/
mogrify -path thumbnails/ -strip -thumbnail 200x200^ -gravity center -extent 200x200 images/*.png
mogrify -path thumbnails/ -strip -thumbnail 200x200^ -gravity center -extent 200x200 images/*.jpg



# convert with lossy compression our gif files!
# sudo apt-get install webp
# https://developers.google.com/speed/webp/docs/gif2webp
rm -rf images_compressed/
mkdir -p images_compressed/
for f in images/*.gif ; do
    NAME="$(basename $f .gif)"
    echo "converting gif: $f"
    gif2webp $f -lossy -min_size -o "images_compressed/${NAME}.webp"
done
for f in images/*.webp ; do
    NAME="$(basename $f .webp)"
    echo "webp to gif: $f"
    ./backend/webp2gif $f "/tmp/converted.gif" &> /dev/null
    echo "converting gif: $f"
    gif2webp "/tmp/converted.gif" -lossy -min_size -o "images_compressed/${NAME}.webp"
done
rm "/tmp/converted.gif"


