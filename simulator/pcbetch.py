#!/usr/bin/env python
#----------------------------------------------------------------------------
# Simulate the PCB etcher (with animated output)
#----------------------------------------------------------------------------
from math   import asin, degrees, sqrt
from motors import Stepper, Servo
from render import PCB, Platform

#--- Sizing constants
PCB_WIDTH  = 50              # Width of PCB in mm
PCB_HEIGHT = 50              # Height of PCB in mm
ARM_LENGTH = 1.5 * PCB_WIDTH # Length of the etching arm in mm
TOOL_SIZE  = 0.7             # Size of tool head in mm

#--- Stepper motor configuration
STEPPER_STEPS_PER_SECOND = 200
STEPPER_MM_PER_STEP = 0.1

#--- Servo motor configuration
SERVO_DEGREES_PER_SECOND = 10

def closeEnough(a, b, accuracy = 0.1):
  return abs(a - b) <= accuracy

class Etcher:
  """ Wrapper class for the whole system
  """

  # How often to generate frames
  FRAME_RATE = 1.0 / 30

  def __init__(self):
    # Set up the servo (calculate limits)
    angle = degrees(asin((PCB_HEIGHT / 2) / ARM_LENGTH))
    self.servo = Servo(-angle, angle, SERVO_DEGREES_PER_SECOND, ARM_LENGTH)
    # Set up the stepper
    self.stepper = Stepper(-(PCB_WIDTH / STEPPER_MM_PER_STEP), 0, STEPPER_STEPS_PER_SECOND, STEPPER_MM_PER_STEP)
    # Create our blank PCB
    self.pcb = PCB(PCB_WIDTH, PCB_HEIGHT)
    # And a renderer for the whole thing
    self.renderer = Platform(self.pcb, ARM_LENGTH)
    # Miscellaneous state
    self.toolDown = False
    self.timestamp = 0.0
    self.lastframe = 0.0
    self.frame = 0

  def renderFrame(self):
    """ Render a single frame if we need to
    """
    # If the pen is down, make an etch point
    if self.toolDown:
      dx, dy = self.servo.distance(self.timestamp)
      self.pcb.etchPoint(
        PCB_WIDTH + self.stepper.distance() - dx,
        (PCB_HEIGHT / 2) - dy,
        TOOL_SIZE
        )
    # Don't generate a whole frame until the next frame point
    if (self.timestamp - self.lastframe) < Etcher.FRAME_RATE:
      return
    # Generate the new frame
    self.renderer.renderFrame(
      self.servo.where(self.timestamp),
      -self.stepper.distance(self.timestamp),
      "pcbetch_%04d.png" % self.frame
      )
    self.frame = self.frame + 1
    self.lastframe = self.timestamp

  def lastFrame(self):
    """ Force a frame to be generate (capture the last movements)
    """
    self.timestamp = self.timestamp + (2 * Etcher.FRAME_RATE)
    self.renderFrame()

  def home(self):
    """ Move to the home position

      The home position is when the left limit switch on both motors
    """
    # Do the stepper motor first
    self.moveToX(0)
    self.moveToY(0)
#    while not self.stepper.atLeftLimit():
#      self.timestamp = self.timestamp + self.stepper.move(-1)
#      self.renderFrame()
#    # Now do the servo
#    while not self.servo.atLeftLimit():
#      self.servo.move(-1, self.timestamp)
#      self.timestamp = self.timestamp + (Etcher.FRAME_RATE / 2)
#      self.renderFrame()

  def moveToY(self, y):
    print "Moving to Y = %f" % y
    # Calculate the angle we should be at
    angle = degrees(asin((y - (PCB_HEIGHT / 2)) / ARM_LENGTH))
    # Get the 'real' X position
    dx, dy = self.servo.distance(self.timestamp)
    actual = PCB_WIDTH + self.stepper.distance() - dx
    # Set the target
    self.servo.move(angle - self.servo.where(self.timestamp), self.timestamp)
    # Wait for the move to complete
    while not closeEnough(self.servo.where(self.timestamp), angle):
      self.timestamp = self.timestamp + (Etcher.FRAME_RATE / 10)
      self.renderFrame()
    # Correct the X position
    #self.moveToX(actual)

  def moveToX(self, x):
    print "Moving to X = %f" % x
    # Figure out where we are (including offset from servo)
    dx, dy = self.servo.distance(self.timestamp)
    current = PCB_WIDTH + self.stepper.distance() - dx
    # Determine how much we need to move the stepper (assuming servo not changing)
    delta = int((x - current) / STEPPER_MM_PER_STEP)
    step = 1
    if delta < 0:
      step = -1
    for i in range(abs(delta)):
      self.timestamp = self.timestamp + self.stepper.move(step)
      self.renderFrame()

  def moveTo(self, x, y):
    """ Move to a specified position

      This assumes the top left of the PCB is 0,0
    """
    # Move the servo first to get the y position accurate
    self.moveToY(y)
    self.moveToX(x)

  def move(self, dx, dy):
    """ Move dx/dy mm from the current position
    """
    if dy == 0:
      # Move in X direction only
      for steps in range(int(abs(dx / STEPPER_MM_PER_STEP))):
        if dx > 0:
          self.timestamp = self.timestamp + self.stepper.move(1)
        else:
          self.timestamp = self.timestamp + self.stepper.move(-1)
        self.renderFrame()
    else:
      # Figure out where we are (including offset from servo)
      x, y = self.servo.distance(self.timestamp)
      x = PCB_WIDTH + self.stepper.distance() - x
      y = (PCB_HEIGHT / 2) + y
      # Figure out how many steps to take
      steps = int(sqrt((dx * dx) + (dy * dy)) / (TOOL_SIZE / 2))
      ddx = dx / steps
      ddy = dy / steps
      for step in range(steps):
        self.moveToY(y + (step * ddy))
        self.moveToX(x + (step * ddx))
      # Do the final step
      self.moveToY(y + dy)
      self.moveToX(x + dx)

#--- Main program
if __name__ == "__main__":
  etcher = Etcher()
  etcher.home()
  etcher.moveTo(10, 10)
  etcher.toolDown = True
  for x in range(5):
    etcher.move(5, 0)
    etcher.move(0, 5)
  etcher.lastFrame()





