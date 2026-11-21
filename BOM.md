# Bill of Materials: C172 Bifold Case (iteration 1)

The layout and dimensions are in [C172_Bifold_Spec.md](C172_Bifold_Spec.md). Quantities include no spares unless noted. Prices are left out.

## A. Extrusion (Vevor, cut at home)
| Item | Qty | Notes |
|---|---|---|
| 2040 x 1000 mm | 2 | 4 x 376 upright cores |
| 2020 x 1000 mm | 6 | 4 x 376 bumpers, 8 x 374 rails, outriggers 160 / 135 / 135 / 120 (cut plan in the spec) |

## B. Case hardware
| # | Item | Qty | Notes |
|---|---|---|---|
| B1 | 2020 inside corner bracket (L) | 20 | 16 rail joints + 4 extra |
| B2 | M5 x 8 button head | 60 | Brackets, edge lips |
| B3 | M5 drop-in T-nut (2020) | 150 | |
| B4 | M5 x 25 SHCS | 16 | Bumper to 2040, 4 per upright |
| B5 | M5 x 40 SHCS | 16 | Rear covers through the printed spacers |
| B6 | M5 x 10 button head + 15 mm washer | 30 | Faceplate / bezel edge clamps |
| B7 | M5 x 16 SHCS | 4 | Clamp feet into the tapped 2040 ends |
| B8 | M5 x 45 SHCS + washer + nyloc | 4 | Outrigger pivots |
| B9 | Aluminum piano hinge, about 32 mm open, 762 mm | 1 | Cut 1 x 355 mm (spare left over) |
| B10 | M4 x 8 countersunk + M4 T-nut | 16 + 16 | Hinge leaves |
| B11 | Toggle draw latch, small | 2 | Holds the case closed |
| B12 | Spring indexing plunger M10, or 6 mm quick pin | 1 | Locks the fold open |
| B13 | Folding chest handle | 1 | Right half top rail |
| B14 | M8 x 60 bolt + nut | 2 + 2 | Desk clamps |
| B15 | Adhesive rubber feet, 20 mm | 8 | |
| B16 | 3 mm sheet (ABS, PVC foam or ACM), 1220 x 610 | 1 | 2 rear covers 414 x 376, 4 edge lips |
| B17 | M5 tap + 4.2 mm drill | 1 | |

## C. Printed case parts (PETG)
| Part | Qty |
|---|---|
| Rear-cover spacer strips, 20 x 30 mm (250 mm segments max) | 16 |
| Clamp feet + desk jaws + M8 thumb knobs | 2 each |
| Outrigger risers | 4 |
| Top-strip blank plates (print in 2 pieces per half) | 4 |
| Yoke shelf: 6 mm plywood or aluminum, 320 x 270 (not printed) | 1 |

## D. Panel modules
Print files are in `prints/`. All PETG black, printed plain; labels come from `labels/`.

| Module | What's on it | Electronics |
|---|---|---|
| **SC-1** switch column (63 x 199) | STBY BATT, MASTER ALT/BAT, AVIONICS BUS1/BUS2 | 4 x KCD1 red rocker, 1 x KCD1 (ON)-OFF-ON |
| **LT-1** mags + lights (191 x 99) | Magneto key + 7 rockers | Lorlin-style 1P12T rotary (stop at 5), 7 x KCD1 black rocker |
| SC-1 + LT-1 controller | | 1 x Raspberry Pi Pico (MobiFlight, 18 inputs) |
| **YK-1** yoke plate (50 x 99) | 40 mm pilot yoke hole | none |
| **CB-1** breakers (127 x 99) | 2 rows x 6 breakers (ESSENTIAL / AVIONICS BUS) | 12 x 10 mm latching panel push buttons with printed breaker caps; dummy for now or wired to a Pico later |
| **MFD-1** GDU 1040 assembly (306 x 199 x 15, 3 pieces or 1 outsourced) | Display window, 12 softkeys, 9 knobs, flip keys, FMS keys, LCD clips, electronics tray | **Full parts + hardware list in [docs/MFD-1_Build_Guide.md](docs/MFD-1_Build_Guide.md)**: AUO G104XVN01.0 + LVDS-HDMI kit, 5 PropWash dual encoders, 3 EC11, ALPS RKJXT1F42001, 20 Omron B3F, Mega 2560 Pro, M2.5/M3 heat-set inserts |
| **PFD-1** GDU 1040 bezel | Same as MFD-1 (bezel only so far; it gets the MFD-1 assembly next) | Same parts as MFD-1 |
| **AU-1** GMA 1347 audio (63 x 199) | 22 keys + volume dual knob | 22 x 12 mm tact switches, 1 dual encoder, 1 x Pico |
| **SB-1** standby gauges (212 x 99 x 20) | Airspeed, attitude, altimeter | 2 x 2.1 in round LCD + ESP32-S3, 1 x 2.8 in round LCD + ESP32-S3. **Gauge software still to pick** |
| **SB-2** dimming (58 x 99 x 20) | SW/CN PNL, STBY IND, PEDESTAL, AVIONICS | 4 x 10 kOhm linear 16 mm pots, 1 x Arduino Pro Micro |
| **CP-1** copilot yoke blank (98 x 99) | 40 mm hole (future) | none |

## E. Power, cables, consumables
| Item | Qty |
|---|---|
| 12 V 5 A supply + splitter (two LCDs) | 1 |
| Powered USB hub, 7+ port | 1 |
| USB cable to PC 3 m + short USB cables, one per board | 1 + 7 |
| HDMI cables to PC | 2 |
| 24 AWG wire kit, 4.8 mm spade connectors, heat-shrink | 1 each |
| PETG black, 1 kg | 2 |
| Matte vinyl sticker sheets + laminate | 3 |
| Epoxy (joining bezel pieces), thread locker | 1 each |

## F. Not yet modeled
Breaker caps, PCB layouts, Pico carriers, magneto key knob, yoke shelf clamp. (MFD-1 knobs, key caps, LCD clips and electronics tray are now modeled.)
