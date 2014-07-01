#!/bin/sh
rm *.png
python pcbetch.py
avconv -i pcbetch_%04d.png -vcodec mpeg4 -r 30 -pix_fmt yuv420p pcbetch.mp4
