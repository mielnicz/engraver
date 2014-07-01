#!/usr/bin/env python
#----------------------------------------------------------------------------
# Generate images for etcher simulation. Create video with:
# avconv -r 1 -i pcbetch_%04d.png -vcodec mpeg4 -r 30 -pix_fmt yuv420p pcbetch.mp4
#----------------------------------------------------------------------------
import Image, ImageDraw
from math import radians, sin, cos

COLOR_PCB = (0, 255, 0)
COLOR_ETCH = (255, 0, 0)
COLOR_BACKGROUND = (255, 255, 255)
COLOR_FRAME = (0, 0, 255)
COLOR_ARM = (128, 128, 128)
COLOR_POINT = (0, 0, 0)

WIDTH_FRAME = 4

class PCB:
  def __init__(self, bed_width, bed_height):
    self.width = int(bed_width)
    self.height = int(bed_height)
    self.image = Image.new("RGB", (self.width * 10, self.height * 10), COLOR_PCB)
    self.drawable = ImageDraw.Draw(self.image)

  def etchPoint(self, x, y, toolsize):
    self.drawable.ellipse(
      ( int(x * 10) - int(toolsize * 5),
        int(y * 10) - int(toolsize * 5),
        int(x * 10) + int(toolsize * 5),
        int(y * 10) + int(toolsize * 5)
      ), fill = COLOR_ETCH, outline = COLOR_ETCH)

class Platform:
  def __init__(self, pcb, arm):
    self.pcb = pcb
    self.arm = int(arm)

  def renderFrame(self, angle, pos, filename):
#    print "Rendering - angle = %f, pos = %f" % (angle, pos)
    # Calculate dimensions
    width = self.pcb.width + self.arm + WIDTH_FRAME
    height = self.pcb.height + (2 * WIDTH_FRAME)
    # Create the new image
    image = Image.new("RGB", (width * 10, height * 10), COLOR_BACKGROUND)
    drawable = ImageDraw.Draw(image)
    # Draw the frame
    drawable.rectangle(( 0, 0, width * 10, 10 * WIDTH_FRAME ), fill = COLOR_FRAME)
    drawable.rectangle(( 0, (height - WIDTH_FRAME) * 10, width * 10, height * 10 ), fill = COLOR_FRAME)
    drawable.rectangle(( (width - WIDTH_FRAME) * 10, 0, width * 10, height * 10 ), fill = COLOR_FRAME)
    # Add the PCB
    image.paste(self.pcb.image, (int((width - self.arm - self.pcb.width + pos) * 10), WIDTH_FRAME * 10))
    # Add the arm
    sx = width - (WIDTH_FRAME / 2)
    sy = height / 2
    tx = self.arm * cos(radians(abs(angle)))
    ty = self.arm * sin(radians(abs(angle)))
    tx = sx - tx
    if angle < 0:
      ty = sy + ty
    else:
      ty = sy - ty
    drawable.line((sx * 10, sy * 10, tx * 10, ty * 10), width = WIDTH_FRAME * 10, fill = COLOR_ARM)
    drawable.point((sx * 10, sy * 10), fill = COLOR_POINT)
    drawable.point((sx * 10, sy * 10), fill = COLOR_POINT)
    # Save the image
    image.save(filename)

if __name__ == "__main__":
  from random import randint
  # Set up the PCB
  pcb = PCB(50, 50)
  for x in range(10):
    pcb.etchPoint(20 + x, 20 + x, 0.7)
  # Create the etcher
  etcher = Platform(pcb, 50)
  # Simulate some frames
  pos = pcb.width / 2
  angle = 0
  for frame in range(50):
    etcher.renderFrame(25 - frame, frame, "frame_%03i.png" % frame)
    angle = angle + randint(-1, 1)
    pos = pos + randint(-1, 1)

