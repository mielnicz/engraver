#!/usr/bin/env python
#-------------------------------------------------------
# Simulation of a stepper motor
#-------------------------------------------------------

class Stepper:
  """ Simulates a stepper motor
  """

  MS_PER_STEP = 1000 / 15
  MM_PER_STEP = 1 / 5

  def __init__(self):
    """ Default constructor
    """
    self.param_ms_per_step = MS_PER_STEP
    self.param_mm_per_step = MM_PER_STEP
    self.where = 0.0 # Start at home position

  def setTimePerStep(self, millis):
    self.param_ms_per_step = millis

  def setDistancePerStep(self, millis):
    self.param_mm_per_step = millis

  def position(self):
    """ Return the current position (in mm)

      @return the current position
    """
    return self.where

  def step(self, clockwise = True):
    """ Make a single step.

      @return the time (in seconds) it took to make the step
    """
    # Update position
    if clockwise:
      self.where = self.where + self.param_mm_per_step
    else:
      self.where = self.where - self.param_mm_per_step
    # Figure out how long it took
    return self.param_ms_per_step


