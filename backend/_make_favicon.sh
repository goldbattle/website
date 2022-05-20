#!/bin/bash

convert -background transparent "downloads/profile.jpg" -define icon:auto-resize=16,24,32,48,64,72,96,128,256 "favicon.ico"
