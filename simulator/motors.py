#!/usr/bin/env python
#----------------------------------------------------------------------------
# Simulate a number of motor types.
#----------------------------------------------------------------------------
from math import radians, sin, cos

class Motor:
  """ Base class for simulators

    This class provides the basic information for each motor. In these
    simulations the motors can be moved a specific distance and held at a
    specific location. Some motors (such as steppers or servos) support
    this directly - others require mechanical assistance.

    The motor classes use the terms 'left' and 'right' to indicate direction.
    Negative values move left, positive values move right. Each motor has a
    limit switch at either end of the spectrum and will not move past that
    point.
  """

  def __init__(self, limitLeft, limitRight):
    self.limitLeft = limitLeft
    self.limitRight = limitRight
    self.position = 0

  def atLeftLimit(self):
    return self.position <= self.limitLeft

  def atRightLimit(self):
    return self.position >= self.limitRight

  def where(self, timestamp = 0):
    return self.position

  def distance(self, timestamp = 0):
    """ Return the position as distance in mm from origin
    """
    return self.where(timestamp)

  def move(self, offset, timestamp = 0):
    """ Move in the given direction.

      Return the amount of time (in seconds) taken to complete the operation or
      0 if it will take place in the background. In the later case the caller
      should periodically query the 'where()' function to determine the current
      position at various time intervals.
    """
    return 0

class Stepper(Motor):
  """ Represents a stepper motor
  """

  def __init__(self, limitLeft, limitRight, stepsPerSecond, mmPerStep):
    Motor.__init__(self, limitLeft, limitRight)
    self.stepsPerSecond = stepsPerSecond
    self.mmPerStep = mmPerStep

  def move(self, offset, timestamp = 0):
    if offset > 0:
      self.position = min(self.position + offset, self.limitRight)
    else:
      self.position = max(self.position + offset, self.limitLeft)
#    print "Stepper: position = %f, offset = %f, limitLeft = %f, limitRight = %f" % (self.position, offset, self.limitLeft, self.limitRight)
    return abs(self.stepsPerSecond * offset)

  def distance(self, timestamp = 0):
    """ Return the position as distance in mm from origin
    """
    return self.where(timestamp) * self.mmPerStep

class Servo(Motor):
  """ Represents a servo motor
  """

  # Accuracy of measurement (arbitrary, but should be small)
  ACCURACY = 0.1

  def __init__(self, limitLeft, limitRight, degreesPerSecond, armLength):
    Motor.__init__(self, limitLeft, limitRight)
    self.degreesPerSecond = degreesPerSecond
    self.armLength = armLength
    self.moving = False
    self.moveStart = 0
    self.target = 0

  def move(self, offset, timestamp):
    # Get our current position (we may be in a move)
    self.position = self.where(timestamp)
    self.target = self.position + offset
    if self.target > 0:
      self.target = min(self.target, self.limitRight)
    else:
      self.target = max(self.target, self.limitLeft)
    self.moving = True
    self.moveStart = timestamp
    print "Servo: position = %f, target = %f" % (self.position, self.target)

  def where(self, timestamp):
    position = self.position
    # If we are moving, calculate the new position
    if self.moving:
      # Calculate how much we have moved in the given time
      delta = (timestamp - self.moveStart) * self.degreesPerSecond
      # Calculate the new position
      if self.target < self.position:
        position = self.position - delta
      else:
        position = self.position + delta
      # If we have hit the target, stop movement
      if (self.position > self.target) and (position <= self.target):
        self.position = self.target
        self.moving = False
        position = self.position
      elif (self.position < self.target) and (position >= self.target):
        self.position = self.target
        self.moving = False
        position = self.position
    # Done
    return position

  def distance(self, timestamp):
    """ Return the position as distance in mm from center
    """
    position = self.where(timestamp)
    dx = self.armLength - (self.armLength * cos(radians(abs(position))))
    dy = self.armLength * sin(radians(abs(position)))
    if position < 0:
      dy = -dy
    return (-dx, dy)

