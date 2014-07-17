/*--------------------------------------------------------------------------*
* X dimension mount connectors
*---------------------------------------------------------------------------*
* 13-Jul-2014 ShaneG
*
* The connector in the X dimension
*--------------------------------------------------------------------------*/
include <common.scad>;

//--- Common definitions
STEM_WIDTH  = (GUIDE_ROD_DIAMETER + LIMIT_SWITCH_WIDTH) * 2; // Width (in X) of the stem
STEM_HEIGHT = GUIDE_ROD_DIAMETER * 2; // Height (in Y) of the stem
STEM_DEPTH  = BED_TO_MOUNT + GUIDE_ROD_DIAMETER + PANEL_DEPTH;

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
  plate_width = STEM_WIDTH + (6 * BOLT_SIZE);
  plate_height = max(STEM_HEIGHT, 3 * BOLT_SIZE);
  difference() {
    // Create the base plate
    translate(v = [ 0, 0, PANEL_DEPTH / 2 ]) {
      cube(size = [ plate_width, plate_height, PANEL_DEPTH ], center = true);
      }
    // Cut holes for the bolts
    translate(v = [ -((plate_width / 2) - (1.5 * BOLT_SIZE)), 0, PANEL_DEPTH ]) {
      hexnut4_negative(spindle = 3 * PANEL_DEPTH);
      }
    translate(v = [ (plate_width / 2) - (1.5 * BOLT_SIZE), 0, PANEL_DEPTH ]) {
      hexnut4_negative(spindle = 3 * PANEL_DEPTH);
      }
    }
  }

/** Create the stem
 *
 * The stem is centered around the Z axis and vertically based at Z = 0. The
 * height of the stem is such that the center of the nut is BED_TO_MOUNT mm
 * from Z = 0.
 */
module stem() {
  grub_slot_height = STEM_WIDTH / 2;
  difference() {
    // The base stem
    translate(v = [ -STEM_WIDTH / 2, -STEM_HEIGHT / 2, 0 ]) {
      cube(size = [ STEM_WIDTH, STEM_HEIGHT, STEM_DEPTH ], center = false);
      }
    // Take away the hole for the rod
    translate(v = [ 0, STEM_WIDTH / 3, BED_TO_MOUNT ]) {
      rotate(a = [ 90, 0, 0 ]) {
        cylinder(h = STEM_WIDTH, r = GUIDE_ROD_DIAMETER / 2, center = true, $fs = RESOLUTION);
        }
      }
    // Subtract a slot for the nut for the grub screw
    translate(v = [ -NUT4_OUTER_DIAMETER / 2, 0, STEM_DEPTH - (2 * PANEL_DEPTH) ]) {
      cube(size = [ NUT4_OUTER_DIAMETER, grub_slot_height * 2, NUT4_HEIGHT ], center = false);
      }
    // Substract space for the nut and bolt for the grub screw
    translate(v = [ 0, 0, STEM_DEPTH - (1.5 * PANEL_DEPTH) ]) {
      hexnut4_negative(spindle = 6 * PANEL_DEPTH);
      }
    // Subtract a slot for the limit switch
    translate(v = [ (STEM_WIDTH / 2) - PANEL_DEPTH - LIMIT_SWITCH_WIDTH, -STEM_HEIGHT, STEM_DEPTH - LIMIT_SWITCH_DEPTH ]) {
      cube(size = [ LIMIT_SWITCH_WIDTH, 3 * STEM_HEIGHT, STEM_DEPTH ], center = false);
      }
    }
  }

//---------------------------------------------------------------------------
// Main shape
//---------------------------------------------------------------------------

//translate(v = [ 0, 0, STEM_HEIGHT / 2 ]) {
//  rotate(a = [ 90, 0, 0 ]) {
    union() {
      baseplate();
      stem();
      }
//    }
//  }

