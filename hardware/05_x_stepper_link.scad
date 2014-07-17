/*--------------------------------------------------------------------------*
* Connect the stepper shaft to the threaded rod
*---------------------------------------------------------------------------*
* 17-Jul-2014 ShaneG
*
* Links the stepper shaft to the threaded rod. Assumes a nylock nut on the
* shaft to grip to and uses a grub screw to bind to the stepper shaft.
*--------------------------------------------------------------------------*/
include <common.scad>;

difference() {
  // Create the main block
  translate(v = [ 0, 0, LINK_LENGTH / 2 ]) {
    cylinder(r = LINK_DIAMETER / 2, h = LINK_LENGTH, center = true, $fs = RESOLUTION);
    }
  // Cut out the hole for the stepper shaft
  cylinder(r = MOTOR_SHAFT_DIAMETER / 2, h = 3 * LINK_LENGTH, center = true, $fs = RESOLUTION);
  // Cut a hole for the nut
  translate(v = [ 0, 0, LINK_LENGTH ]) {
    hexagon(NUT_OUTER_DIAMETER / 2, 3 * NUT_HEIGHT);
    }
  // Cut a slot for the grub screw
  translate(v = [ (NUT_OUTER_DIAMETER / 2) - RESOLUTION, -NUT4_OUTER_DIAMETER / 2, LINK_LENGTH / 4 ]) {
    cube(size = [ NUT4_HEIGHT, NUT4_OUTER_DIAMETER, LINK_LENGTH * 2 ], center = false);
    }
  // Allow for the grub screw nut and bolt
  translate(v = [ (NUT_OUTER_DIAMETER / 2) - RESOLUTION + (NUT4_HEIGHT / 2), 0, LINK_LENGTH / 4 ]) {
    rotate(a = [ 0, 90, 0 ]) {
      hexnut4_negative(spindle = LINK_DIAMETER / 2);
      }
    }
  }

// Show some info
echo("Min grub screw length: ", (LINK_DIAMETER - MOTOR_SHAFT_DIAMETER) / 2);
