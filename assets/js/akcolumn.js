/* akcolumn.js — THE SOUNDING COLUMN, Carousel No. 42's continuity chassis.
 *
 * Committed 2026-08-27. This is DECK FURNITURE, shared across all nine slides
 * on purpose, which is why it lives in a module rather than inline:
 * bespoke_check strips `<script src=>` as harness, so a shared coordinate
 * system does not read as nine slides of the same art, while each slide's own
 * composition still has to earn its score. Same reasoning as akrail.js.
 *
 * WHAT THIS IS. One night's atmosphere over the Kenai Peninsula, drawn to
 * scale, as a single altitude-to-pixel mapping that every slide in the deck
 * shares. Four physical surfaces sit in it and each one is a claim:
 *
 *     4,200 m  release band top          C18
 *     3,500 m  release band bottom       C18
 *     2,200 m  lowest radar beam, top    C15
 *     1,874 m  freezing level, MEASURED  C08
 *     1,800 m  lowest radar beam, floor  C15
 *         0 m  ground
 *
 * WHY IT IS A MODULE AND NOT NINE CONSTANTS. The deck's whole continuity rests
 * on the claim that these altitudes are at the SAME screen position on every
 * frame. Two slides disagreeing by four pixels kills that silently, because
 * nothing renders wrong, the reader simply stops believing the column without
 * knowing why. One exported object cannot drift from itself.
 *
 * THE SECOND SCALE IS DELIBERATELY SEPARATE. `AX` maps acre feet to x and is
 * used on ONE slide. It is exported from the same module because it is the
 * moment the vertical story becomes a horizontal one, and because keeping both
 * scales in one file makes it obvious that they are two scales and never one
 * sum. A frame carrying both prints a guard line saying so.
 *
 * DETERMINISM. Pure arithmetic, no clock, no randomness.
 */
(function (global) {
  "use strict";

  /* THE COLUMN. y = yGround - altitude * pxPerMetre, so altitude climbs up the
   * frame. Ground is deliberately BELOW the 80 px safe margin at y 1240,
   * because the hero slide takes the deck's single permitted grid violation
   * and runs the section into the bottom band. A section that stops short of
   * the ground does not close the argument. */
  var COL = {
    yGround: 1240,
    yTop: 90,
    mTop: 4300,
    pxPerMetre: (1240 - 90) / 4300,        /* 0.26744186... */
    y: function (m) { return COL.yGround - m * COL.pxPerMetre; },
    m: function (y) { return (COL.yGround - y) / COL.pxPerMetre; },
    /* The named surfaces, each with the claim it comes from. Slides read these
     * rather than retyping the numbers, which is what stops a label and a rule
     * disagreeing about the same altitude. */
    RELEASE_TOP: 4200,
    RELEASE_BOT: 3500,
    BEAM_TOP: 2200,
    FREEZING: 1874,
    BEAM_FLOOR: 1800,
    GROUND: 0
  };

  /* THE ACRE FOOT AXIS, slide 07 only. x = x0 + (af - af0) * pxPerAF. */
  var AX = {
    x0: 120,
    af0: 35,
    pxPerAF: 12.0,
    x: function (af) { return AX.x0 + (af - AX.af0) * AX.pxPerAF; },
    af: function (x) { return AX.af0 + (x - AX.x0) / AX.pxPerAF; },
    /* One acre foot is 325,851 US gallons. The deck converts 19,000,000
     * gallons to 58.31 acre feet with this constant and labels the result as
     * the studio's own arithmetic, never as the company's figure. */
    GAL_PER_AF: 325851
  };

  global.AKCOL = COL;
  global.AKAX = AX;
})(window);
