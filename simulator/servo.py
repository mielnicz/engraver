#!/usr/bin/env python
#-------------------------------------------------------
# Simulation of a servo motor
#-------------------------------------------------------

class Servo:
  """ Simulate a servo motor
  """

  ANGLE_MAX = 90.0
  ANGLE_MIN = -90.0
  DEGREES_PER_SECOND = 90

  def __init__(self):
    """ Default constructor
    """
    self.current = 0
    self.start_angle = self.current
    self.start_time = 0
    self.target_angle = self.current
    self.move_started = 0
    self.param_degrees_per_second


  def where(self, time):
    """ Determine the angle based on the given time
    """
    # If we have finished moving just return the current position
    if self.current == self.target:
      return self.current
    # Determine the current position
    delta = self.start_angle + (((time - self.start_time) * 1000) * self.param_degrees_per_second)
    if self.target_angle < self.start_angle:
      self.current = self.start_angle - delta
      if self.current < self.target_angle:
        self.current = self.target_angle
    else:
      self.current = self.start_angle + delta
      if self.current > self.target_angle:
        self.current = self.target_angle
    # All done
    return self.current

  def setAngle(self, angle, time):
    """ Set the desired angle
    """
    # Calculate the current position
    self.where(time)
    self.start_angle = self.current
    self.start_time = time
    self.target_angle = angle

