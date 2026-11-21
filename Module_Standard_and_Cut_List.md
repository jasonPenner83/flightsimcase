# Folding Cockpit Case: Module Standard and Cut List (rev E, LOCKED 2026-11-21)

The model is in the open Fusion design. Joints:
* "Left wing hinge" (0 to 180)
* "Right spacer hinge" + "Right wing hinge" (0 to 90 each)
* Four "... outrigger swing" joints

Fold the left wing, then the right. On the right, the hinges can move together or one at a time, in either order. Every way was checked clean.

## Rev E: Vevor stock only (2020 / 2040)

**Why 4080 center + 2040 left + 4080 right doesn't close without an extension:**
* The second wing to fold has to reach over the first one, about 80 mm of frame + electronics + cover, before its knobs can start.
* A side-mounted hinge at the frame's front corner always lands the folding wing's face on the center's face plane. So that 80 mm has to come from somewhere.
* With a 4080 right wing, its 60 mm deep face lands on the center face plane, right where the folded left wing already sits. The left wing would have to nest inside the right wing's frame. Its hinge is on the center's outer edge, so it collides with the right wing's perimeter.
* To make the right wing's own frame the bridge, it would need roughly 120 mm of recess. That means about a 140 mm deep perimeter, which isn't a Vevor size.
* 4080 is also roughly 2 to 3 times the weight of a 2040 per meter, which hurts a carry case.

**What rev E does instead (same geometry as rev D, Vevor-buildable):**
1. **Uprights: a 2040 with a 2020 "bumper" bolted to its front.** That makes a 20 x 60 upright standing 40 mm proud of the 2020 rails, so each panel keeps a full 40 mm knob budget inside its frame.
2. **Piano hinges on the side faces of the uprights.** The leaves are hidden in the seam and only the knuckle line shows at the front edge. Nothing faces the pilot.
3. **Left wing: one hinge, no spacer.**
4. **Right side: hinge | 98 mm spacer | hinge.** The spacer is two 2020 verticals plus a 3 mm skin, and carries the audio panel. This spacer is the one unavoidable bridge for the second wing; it doubles as the right side wall.
   * A sliding hinge could replace it, but it would need about 100 mm of travel and leave the side open.
5. **Top and bottom now close up.** 3 mm edge lips run along the top and bottom of every panel, front and rear, plus printed caps on the spacer.
   * Folded, the case is closed on all six sides except ~5 mm seams and a small notch at the top/bottom corner beside the spacer.
   * No separate lids needed.

## 1. Size

| | Value |
|---|---|
| Open width | 1113 mm |
| Closed | 379 W x 416 H x 289 D mm (height includes 40 mm feet; clamp jaws come off) |
| Panels | Left wing 310, center 350, right spacer 98, right wing 350 mm wide; 375.6 mm tall |
| Fold check | Interference every 5° (10° one-hinge-at-a-time), outriggers stored and deployed. All clear |

## 2. Module standard (revised: rails placed per panel)

Rails no longer sit on a fixed grid. Each panel's rails go wherever its real-size modules need them; the T-slot uprights let a rail sit at any height.

| Rule | Value |
|---|---|
| Faceplate height | Rail spacing minus 0.8 mm. Plate edges sit on the rail centerlines |
| Faceplate width | Anything that fits between the uprights. Max 256 mm per printed piece (A1 bed); split wider plates |
| Mounting | Half-hole notches (6.4 mm) on the top/bottom edges about every 110 mm. One M5 x 10 button head + 15 mm washer into a rail T-nut clamps two neighboring plates |
| Rear window | Parts behind the plate must fit between rail faces (rail spacing − 20 mm tall) |
| Depth | **Front 40 mm max** from the rail face; **rear 30 mm max** behind the rails |
| **Panel plane (thickness standard)** | **Every faceplate is exactly 3.0 mm thick where it touches the rails**, so all front faces land on one plane 3.0 mm in front of the rail face. Thicker items (display bezels, gauge bezels) keep a 3.0 mm mounting flange; any extra thickness goes forward of that plane inside the 40 mm budget, never behind it. Thinner sheet (aluminum, ACM) gets a printed 3.0 mm frame or shims |
| Print rule for flatness | Front face down on the textured PEI plate, 0.2 mm layers, 4 walls, 100% infill under the clamp notches. Check with calipers: 3.0 ± 0.1 mm |
| Plate material | PETG. Snap-in parts get a back pocket leaving a 1.4 mm wall |
| Labels | Not printed in the plastic. Each module gets 1:1 SVG artwork in `labels/` (black field, white text, red cut lines), used for a vinyl sticker or an outsourced engraved / UV-printed plate. Outsourced plates must still meet the 3.0 mm panel plane |
| Real-world sizes kept | GA avionics 6.25 in (158.75 mm) wide, 3-1/8 in and 2-1/4 in round gauges, GDU 1040 300 x 196 mm, DZUS 5.75 in via adapter (airliner, later) |
| Electronics | One Pico (MobiFlight) per module, one USB hub in the center rear zone |

### Current rail maps (rail centerlines, mm from panel bottom)
| Panel | Rails | Sections |
|---|---|---|
| Left wing | 10 · 70 · 170 · 365.6 | SW-1 switch row (59.2) · flex section (99.2, blank for now) · standby instruments (194.8) |
| Center | 10 · 110 · 310 · 365.6 | CL-1 dimmers + CL-2 yoke hole (99.2) · PFD (199.2) · top strip (54.8) |
| Right wing | 10 · 110 · 310 · 365.6 | Copilot yoke blank (99.2) · MFD (199.2) · top strip (54.8) |

## 3. Yoke and throttle
* Pilot yoke on the PFD centerline, 100 mm above the desk, through a 2U pass-through plate.
* Throttle on the aircraft centerline at the audio/MFD seam (+250 mm).
* Copilot yoke blank mirrored at +500 mm under the MFD.
* Yoke shelf on the center outriggers.

## 4. Hardware
* 3 piano hinges (~355 mm), side-mounted.
* 4 outriggers stored under the panels; clamp feet with removable desk-edge jaws.
* Still needed: open-position latches, a closed catch, a carry handle.

## 5. Extrusion cut list (all Vevor sizes)

| Profile | Length | Qty | Where |
|---|---|---|---|
| 2040 | 375.6 mm (cut 376) | 6 | Upright cores |
| 2020 | 375.6 mm (cut 376) | 8 | Upright bumpers (6) + right spacer verticals (2) |
| 2020 | 310 mm | 8 | Center + right wing rails |
| 2020 | 270 mm | 4 | Left wing rails |
| 2020 | 230 mm | 2 | Wing outriggers |
| 2020 | 135 mm | 2 | Center outriggers |

Totals: 2040 is 2.25 m (6 pieces). 2020 is 7.30 m (24 pieces).
Sheet: 3 rear covers (~350 x 376), 12 edge lips (~310 x 40 / 310 x 30), one spacer skin (55 x 376), all 3 mm aluminum or ABS.

## 6. Open items
* Latches, closed catch, handle.
* Real yoke shaft height and C172 panel reference measurements.
* Audio panel (GMA 1347) width: the model uses a 64 mm placeholder.

Model files are in fusion/: build_case.py (dimensions in `P`), tools.py and run_all.py. Earlier revisions are build_case_revA to revD.py and renders/revA to revD.
