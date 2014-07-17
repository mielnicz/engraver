/*--------------------------------------------------------------------------*
* Mount for the stepper, bearing and link
*---------------------------------------------------------------------------*
* 17-Jul-2014 ShaneG
*
* Defines a mount to hold the stepper motor, a shaft for the threaded rod
* and room for the link component.
*--------------------------------------------------------------------------*/
include <common.scad>;

//--- Common definitions
BEARING_STEM_WIDTH  = BEARING_DIAMETER + (2 * PANEL_DEPTH); // Width (in X) of the stem
BEARING_STEM_HEIGHT = BEARING_HEIGHT + (2 * PANEL_DEPTH);   // Height (in Y) of the stem

MOTOR_STEM_WIDTH  = MOTOR_WIDTH + (2 * PANEL_DEPTH);
MOTOR_STEM_HEIGHT = MOTOR_HEIGHT + (2 * PANEL_DEPTH);
MOTOR_STEM_DEPTH  = (MOTOR_DEPTH + PANEL_DEPTH) / 2;

PLATE_WIDTH  = max(BEARING_STEM_WIDTH, MOTOR_STEM_WIDTH) + (6 * BOLT_SIZE);
PLATE_HEIGHT = BEARING_STEM_HEIGHT + MOTOR_STEM_HEIGHT + (1.5 * LINK_LENGTH);

//---------------------------------------------------------------------------
// Helper modules
//---------------------------------------------------------------------------

/** Create the base
 *
 * The base needs to provide enough space for two connecting bolts and a
 * stem. The resulting object is centered around the Z axis and vertical
 * based at Z = 0.
 */
module baseplate() {
  difference() {
    // Create the base plate
    translate(v = [ 0, 0, PANEL_DEPTH / 2 ]) {
      cube(size = [ PLATE_WIDTH, PLATE_HEIGHT, PANEL_DEPTH ], center = true);
      }
    // Cut holes for the bolts
    translate(v = [ -((PLATE_WIDTH / 2) - (1.5 * BOLT_SIZE)), (PLATE_HEIGHT / 2) - (2 * BOLT_SIZE), PANEL_DEPTH ]) {
      hexnut4_negative(spindle = 3 * PANEL_DEPTH);
      //cylinder(h = PANEL_DEPTH * 4, r = BOLT_SIZE / 2, center = true, $fs = RESOLUTION);
      }
    translate(v = [ -((PLATE_WIDTH / 2) - (1.5 * BOLT_SIZE)), -((PLATE_HEIGHT / 2) - (2 * BOLT_SIZE)), PANEL_DEPTH ]) {
      hexnut4_negative(spindle = 3 * PANEL_DEPTH);
      //cylinder(h = PANEL_DEPTH * 4, r = BOLT_SIZE / 2, center = true, $fs = RESOLUTION);
      }
    translate(v = [ (PLATE_WIDTH / 2) - (1.5 * BOLT_SIZE), -((PLATE_HEIGHT / 2) - (2 * BOLT_SIZE)), PANEL_DEPTH ]) {
      hexnut4_negative(spindle = 3 * PANEL_DEPTH);
      //cylinder(h = PANEL_DEPTH * 4, r = BOLT_SIZE / 2, center = true, $fs = RESOLUTION);
      }
    translate(v = [ (PLATE_WIDTH / 2) - (1.5 * BOLT_SIZE), (PLATE_HEIGHT / 2) - (2 * BOLT_SIZE), PANEL_DEPTH ]) {
      hexnut4_negative(spindle = 3 * PANEL_DEPTH);
      //cylinder(h = PANEL_DEPTH * 4, r = BOLT_SIZE / 2, center = true, $fs = RESOLUTION);
      }
    }
  }

/** Create the stem for the bearing
 *
 * This stem is centered around the Z axis and vertically based at Z = 0. The
 * height of the stem is such that the center of the nut is BED_TO_MOUNT mm
 * from Z = 0.
 */
module stem_bearing() {
  difference() {
    translate(v = [ -BEARING_STEM_WIDTH / 2, -BEARING_STEM_HEIGHT / 2, 0 ]) {
      cube(size = [ BEARING_STEM_WIDTH, BEARING_STEM_HEIGHT, BED_TO_MOUNT ], center = false);
      }
    translate(v = [ 0, 0, BED_TO_MOUNT ]) {
      rotate(a = [ 90, 0, 0 ]) {
        cylinder(h = BEARING_HEIGHT, r = BEARING_DIAMETER / 2, center = true, $fs = RESOLUTION);
        }
      }
    translate(v = [ 0, 0, BED_TO_MOUNT ]) {
      rotate(a = [ 90, 0, 0 ]) {
        cylinder(h = 4 * BEARING_HEIGHT, r = BEARING_INNER_DIAMETER / 2, center = true, $fs = RESOLUTION);
        }
      }
    }
  }

/** Create the stem for the motor
 *
 * This stem is centered around the Z axis and vertically based at Z = 0. The
 * height of the stem is such that the center of the nut is BED_TO_MOUNT mm
 * from Z = 0.
 */
module stem_motor() {
  translate(v = [ -MOTOR_STEM_WIDTH / 2, -MOTOR_STEM_HEIGHT / 2, 0 ]) {
    difference() {
      // Build the basic cube to work at
      cube(size = [ MOTOR_STEM_WIDTH, MOTOR_STEM_HEIGHT, MOTOR_STEM_DEPTH ], center = false);
      // Cut away space for the motor itself
      translate(v = [ PANEL_DEPTH, PANEL_DEPTH, PANEL_DEPTH - RESOLUTION ]) {
        cube(size = [ MOTOR_WIDTH, MOTOR_HEIGHT, MOTOR_DEPTH ], center = false);
        }
      // Cut away a gap at the front for the shaft
      translate(v = [ MOTOR_STEM_WIDTH / 2, 0, BED_TO_MOUNT ]) {
        rotate(a = [ 90, 0, 0 ]) {
          cylinder(h = 4 * BEARING_HEIGHT, r = MOTOR_SHAFT_BOUNDARY / 2, center = true, $fs = RESOLUTION);
          }
        }
      }
    }
  }

//---------------------------------------------------------------------------
// Main shape
//---------------------------------------------------------------------------

difference() {
  union() {
    baseplate();
    translate(v = [ 0, -(PLATE_HEIGHT - BEARING_STEM_HEIGHT) / 2, 0 ]) {
      stem_bearing();
      }
    translate(v = [ 0, (PLATE_HEIGHT - MOTOR_STEM_HEIGHT) / 2, 0 ]) {
      stem_motor();
      }
    }
  // Cut away space in the center to save some plastic
  translate(v = [ -(PLATE_WIDTH - (NUT4_OUTER_DIAMETER * 3)) / 2, (-PLATE_HEIGHT / 2) + BEARING_STEM_HEIGHT + RESOLUTION, -PANEL_DEPTH ]) {
    cube(size = [ PLATE_WIDTH - (NUT4_OUTER_DIAMETER * 3), PLATE_HEIGHT - (MOTOR_STEM_HEIGHT + BEARING_STEM_HEIGHT + (2 * RESOLUTION)), PANEL_DEPTH * 3 ], center = false);
    }
  // Cut away space in the motor mount to save some plastic
  translate(v = [ -(MOTOR_STEM_WIDTH - (4 * PANEL_DEPTH)) / 2, (PLATE_HEIGHT / 2) - MOTOR_STEM_HEIGHT + (2 * PANEL_DEPTH), -(1.5 * PANEL_DEPTH) ]) {
    cube(size= [ MOTOR_STEM_WIDTH - (4 * PANEL_DEPTH), MOTOR_STEM_HEIGHT - (4 * PANEL_DEPTH), 3 * PANEL_DEPTH ], center = false);
    }
  }

// Show some info
echo("Mount length = ", PLATE_HEIGHT);

