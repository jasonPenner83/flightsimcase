# C172 Bifold Case: Spec and Cut List (iteration 1, 2026-11-21)

This is a model-specific build for the Cessna 172 G1000. The modular rail standard is retired for this iteration: every faceplate is sized for its exact spot. The trifold/modular design is kept in `docs/archive/` and in Fusion versions v1 to v5.

## Layout (pilot view)
| | Left half (folds) | Right half (stays on the desk) |
|---|---|---|
| **Top strip** | blank | blank |
| **Displays** | **SC-1** switch column (STBY BATT, red MASTER ALT/BAT, red AVIONICS BUS1/BUS2) + **PFD-1** GDU 1040 | **AU-1** GMA 1347 audio + **MFD-1** GDU 1040 |
| **Lower** | **LT-1** magneto key + FUEL PUMP, BCN, LAND, TAXI, NAV, STROBE, PITOT HEAT, **YK-1** pilot yoke, **CB-1** 2 x 6 circuit breakers | **SB-1** standby airspeed / attitude / altimeter, **SB-2** DIMMING (SW/CN PNL, STBY IND, PEDESTAL, AVIONICS), **CP-1** copilot yoke blank |

* The PFD sits beside the seam and the audio panel just across it, so PFD, audio and MFD read continuously, as in the real airplane.
* **Pilot yoke:** on the PFD centerline, 100 mm above the desk. The yoke shelf sits on the two left-half outriggers.
* **Throttle:** on the aircraft centerline at the audio/MFD seam (desk edge). The copilot yoke blank is mirrored about that line.

## Size and weight
| | Value |
|---|---|
| Open | 831 mm wide x 416 mm tall (including 40 mm feet) |
| Closed | **419 W x 416 H x 191 D mm** (clamp jaws come off) |
| Estimated weight | About 7.2 kg before electronics |
| Fold check | Fusion interference every 5 degrees through the 180 degree fold, with every faceplate, bezel and outrigger installed: clean. Internal fit of LCDs, boards, encoders and gauges inside both halves: clean |

## Construction
* **Halves:** each is 414 x 375.6 mm.
  * Uprights are a 2040 core with a 2020 bumper, standing 40 mm proud of the rails so the knobs sit inside the frame depth.
  * 2020 rails at 10 / 110 / 310 / 365.6 mm.
* **Hinge:** one piano hinge (about 355 mm) on the side faces of the seam uprights, with the leaves hidden in the seam. Closed, the two faces meet face to face with an 85 mm gap between rail faces, which gives each side a 40 mm knob budget.
* **Sealing:** 3 mm rear covers and top/bottom edge lips. Closed, the case is sealed on all six sides apart from the roughly 3 mm seam.
* **Faceplates:** 3 mm thick at the rails, edge-clamped with M5 screws and washers into rail T-nuts. The bezels (PFD/MFD 15 mm, standby/dimming 20 mm) stand proud of a 3 mm flange.
* **Labels:** the plates print plain; labels are stickers or outsourced, from `labels/*.svg`.
* **Printing:** every printed part fits the A1's 256 mm bed. The 306 mm display bezels print in 3 pieces each.
* **Support:**
  * Two clamp feet with desk-edge jaws under the right half.
  * Two outriggers under each half that swing back 90 degrees.

## Extrusion cut list (Vevor 2020 / 2040)
| Profile | Length | Qty | Use |
|---|---|---|---|
| 2040 | 376 mm | 4 | Upright cores |
| 2020 | 376 mm | 4 | Upright bumpers |
| 2020 | 374 mm | 8 | Rails (4 per half) |
| 2020 | 160 / 120 mm | 1 / 1 | Left outriggers (outer / inner) |
| 2020 | 135 mm | 2 | Right outriggers |

**Stock to buy** (1000 mm sticks, 3 mm saw cut allowed):
* **2040: 2 sticks**, cut 376 + 376 each.
* **2020: 6 sticks**, cut as:
  * 376 + 376 + 160
  * 376 + 376 + 135
  * 374 + 374 + 135
  * 374 + 374 + 120
  * 374 + 374
  * 374 + 374

Totals: 2040 = 1.50 m, 2020 = 5.05 m.

## Model files
* `fusion/build_case_bifold.py`: frame, hinge, outriggers.
* `fusion/c172_panels.py`: all faceplates, standby/dimming shells and reference parts.
* `fusion/build_pfd.py`: PFD/MFD bezels.
* `fusion/run_bifold.py`: rebuild + fold check + cut list.
* `fusion/gen_label_art.py`: label SVGs.
