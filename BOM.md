# Bill of Materials: Folding C172 Cockpit Case (rev E, C172 layout)

**Layout:**
* **Left wing (350 mm):** G1000 PFD, with the switch rows either side of the pilot yoke below it.
* **Center (414 mm):** GMA audio panel + G1000 MFD on top; standby gauges, 4 dimmers and the copilot yoke blank below.
* **Right wing (350 mm):** flexible space.

Quantities include no spares unless noted. Part numbers are generic specs, so buy the closest match. Prices are left out on purpose.

---

## A. Aluminum extrusion (Vevor, cut at home)

### Cut list
| Profile | Length | Qty | Use |
|---|---|---|---|
| 2040 | 376 mm | 6 | Upright cores (2 per panel) |
| 2020 | 376 mm | 6 | Upright front "bumpers" (bolted to the 2040s) |
| 2020 | 376 mm | 2 | Right spacer verticals |
| 2020 | 374 mm | 4 | Center rails |
| 2020 | 310 mm | 8 | Left + right wing rails (4 each) |
| 2020 | 230 mm | 1 | Right wing outrigger |
| 2020 | 160 mm | 1 | Left wing outer outrigger |
| 2020 | 135 mm | 2 | Center outriggers |
| 2020 | 120 mm | 1 | Left wing inner outrigger (with the outer one, carries the yoke shelf) |

### Stock to buy (1000 mm sticks, 3 mm kerf allowed)
| Profile | Sticks | How they're cut |
|---|---|---|
| 2040 x 1000 | **3** | 376 + 376 per stick |
| 2020 x 1000 | **9** | 376+376+230 · 376+376+160 · 2 sticks of 376+376+135 · 374+374+120 · 374+374 · 2 sticks of 310+310+310 · 310+310 |

Totals: 2040 = 2.26 m, 2020 = 7.76 m.

---

## B. Case hardware

| # | Item | Qty | Notes |
|---|---|---|---|
| B1 | 2020 inside corner bracket (L, 20-series, with screws) | 30 | Rail-to-upright joints: 24, plus 6 extra |
| B2 | M5 x 8 button head screw | 100 | Brackets, edge lips, spacer skin, spare |
| B3 | M5 drop-in T-nut, 2020 (6 mm slot) | 250 | Used everywhere |
| B4 | M5 x 25 socket head cap screw | 24 | Bumper to 2040, 4 per upright |
| B5 | M5 x 40 socket head cap screw | 24 | Rear covers through the printed spacers |
| B6 | M5 x 10 button head + 15 mm OD washer | 40 | Faceplate / bezel edge clamps |
| B7 | M5 x 16 socket head | 4 | Clamp feet into the tapped 2040 end bores |
| B8 | M5 x 45 socket head + washer + nyloc | 5 | Outrigger pivots |
| B9 | M5 tap + 4.2 mm drill | 1 | |
| B10 | Aluminum piano hinge, ~32 mm open width, 762 mm (30 in) | 2 | Cut into 3 x 355 mm (+1 spare) |
| B11 | M4 x 8 countersunk screw + M4 drop-in T-nut | 50 + 50 | Hinge leaves into the bumper side slots |
| B12 | Toggle draw latch, small | 2 | Holds the case closed |
| B13 | Spring indexing plunger M10, or 6 mm quick-release pin | 2 | Locks each fold open |
| B14 | Folding chest handle | 1 | On the center top rail |
| B15 | M8 x 60 hex bolt + nut | 2 + 2 | Desk clamp screws |
| B16 | Adhesive rubber feet, 20 mm | 10 | Clamp feet and outrigger ends |
| B17 | 3 mm sheet (ABS, PVC foam or ACM), 1220 x 610 | 1 | 3 rear covers (414x376, 2 x 350x376), spacer skin, 6 edge lips |
| B18 | 2020 slot cover strip, 1 m | 2 | Optional |

### Printed case parts (PETG)
| # | Part | Qty | Notes |
|---|---|---|---|
| P1 | Rear-cover spacer strip, 20 x 30 mm, ≤ 250 mm segments | 26 | |
| P2 | Spacer cap | 2 | Top and bottom of the right spacer |
| P3 | Clamp foot, 40 mm | 2 | Under the center uprights |
| P4 | Desk clamp jaw | 2 | Comes off for packing |
| P5 | Clamp thumb knob, M8 | 2 | |
| P6 | Outrigger riser / pivot block | 5 | |
| P7 | Blank filler plates (rail spacing − 0.8 tall, ≤ 256 wide) | as needed | Top strips, and the right wing until it gets modules |
| Y1 | Yoke shelf: 6 mm plywood or aluminum, 320 x 270 mm | 1 | Sits on the two deployed left wing outriggers, under the PFD |

---

## C. Case electronics

| # | Item | Qty | Notes |
|---|---|---|---|
| E1 | Powered USB hub, 10 port | 1 | Center rear zone |
| E2 | USB cable to PC, 3 m | 1 | |
| E3 | Short USB cables, 0.3 m | 1 per board | |
| E4 | 12 V 5 A power supply + DC splitter | 1 | Two 10.4 in LCDs (PFD + MFD), plus margin |
| E5 | HDMI cables to PC, 1–2 m | 2 | PFD and MFD pop-outs |
| E6 | Cable ties + adhesive mounts | 1 pack | |

---

## D. Modules

Every faceplate prints plain, at most 256 mm per piece. Labels are vinyl stickers or outsourced engraving, from `labels/*.svg`.
Placeholder parts (switch bodies, LCDs, boards) are in the Fusion model, hidden by default.

### D1. Left wing, lower section: SW-1L / YK-1 / SW-1R (rails 10–110)
* **SW-1L (127 mm):** magneto key, red MASTER ALT | BAT, STBY BATT, red AVIONICS BUS 1 | BUS 2.
* **YK-1 (50 mm):** pilot yoke pass-through, 40 mm hole on the PFD centerline, 100 mm above the desk.
* **SW-1R (127 mm):** FUEL PUMP, BCN, LAND, TAXI, NAV, STROBE, PITOT HEAT.

| # | Item | Qty |
|---|---|---|
| S1 | KCD1 rocker ON-OFF 21x15 cutout, red | 4 |
| S2 | KCD1 rocker ON-OFF 21x15 cutout, black | 7 |
| S3 | KCD1 rocker (ON)-OFF-ON 21x15 cutout, black (STBY BATT) | 1 |
| S4 | Rotary switch 1P12T with stop set to 5 (Lorlin CK1049 style), 3/8 in bushing (magnetos) | 1 |
| S5 | Raspberry Pi Pico, MobiFlight (both switch plates) | 1 |
| S6 | 4.8 mm spade connectors, 24 AWG wire, heat-shrink | 1 kit |

### D2. PFD-1 (left wing) and MFD-1 (center): GDU 1040 style bezels (rails 110–310)
Each bezel is 306 x 199.2 x 15 mm deep and prints in 3 pieces (37 / 232 / 37 mm).
* **Face:** 211.2 x 158.4 mm window and 12 softkeys.
* **Knobs:** NAV/COM VOL, NAV/COM/ALT/CRS-BARO/FMS dual knobs, HDG, RANGE, flip keys and the FMS key grid.
* **Inside the bezel:** the LCD and three key/encoder boards.
* **Behind the rails:** the HDMI driver board and a Mega Pro Mini.

> **Monitor fit:** the cavity is **9.5 mm deep**. Use an **LED-backlit 10.4 in 1024x768 module, ≤ 228.6 x 175.8 x 9 mm**. Older CCFL panels are 10–12 mm thick and won't fit.

| # | Item | Qty (PFD + MFD) |
|---|---|---|
| PF1 | 10.4 in 1024x768 LED-backlit LCD + HDMI driver kit | 2 |
| PF2 | Dual-concentric encoder with push | 10 |
| PF3 | EC11 encoder with push | 8 |
| PF4 | Tact switch 6x6x5 mm | 40 |
| PF5 | Arduino Mega 2560 Pro Mini (MobiFlight) | 2 |
| PF6 | Key/encoder PCBs (3 per bezel; perfboard for a first build) | 2 sets |
| PF7 | M2.5 x 6 screws (PCB and LCD clips) | 32 |

### D3. AU-1: GMA 1347 style audio panel (center, left of the MFD, 63 x 199.2 mm)
22 keys in 2 columns (COM/NAV/MKR/etc., legends on the caps) and the PILOT/COPLT volume dual knob.

| # | Item | Qty |
|---|---|---|
| AU1 | Tact switch 12x12 mm with printed 22x8 caps | 22 |
| AU2 | Dual-concentric encoder with push | 1 |
| AU3 | Raspberry Pi Pico, MobiFlight | 1 |

### D4. SB-1 standby instruments + SB-2 dimming (center, lower section)
Shell bezels 20 mm deep, side by side so they read as one panel.
* **SB-1 (212 mm):** AIRSPEED (2-1/4 in), ATTITUDE (3-1/8 in), ALTIMETER (2-1/4 in) windows. Round LCDs sit inside the shell.
* **SB-2 (58 mm):** DIMMING block with SW/CN PNL, STBY IND, PEDESTAL and AVIONICS knobs, as Jason asked.

| # | Item | Qty | Notes |
|---|---|---|---|
| SB1 | Round LCD 2.1 in (480x480) with ESP32-S3 | 2 | Airspeed, altimeter. **Gauge software still to pick** (custom ESP32 firmware or a PC-driven option) |
| SB2 | Round LCD 2.8 in with ESP32-S3 | 1 | Attitude. Check that the module is ≤ 83 mm across and ≤ 13 mm deep |
| SB3 | Potentiometer 10 kΩ linear, 16 mm, D-shaft | 4 | Dimmers |
| SB4 | Arduino Pro Micro (4 analog inputs, MobiFlight) | 1 | A Pico only has 3 ADCs |

### D5. CP-1: copilot yoke blank (center, lower right, 98 mm)
A 40 mm hole mirrored about the aircraft centerline, for a future second yoke.

---

## E. Consumables and tools

| Item | Qty |
|---|---|
| PETG filament, black, 1 kg | 3 (case parts, bezels, faceplates; about 2 kg total) |
| Matte vinyl sticker sheets + laminate (labels), A4 | 3 |
| Miter saw with a non-ferrous blade, drill bits, M5 tap, deburring tool | |
| Epoxy (joining bezel pieces), medium thread locker | |

---

## F. Not in this BOM yet
* Knobs and key caps (all modules)
* PCB layouts
* GFC 700 autopilot strip and circuit breakers (candidates for the right wing)
* Throttle/mixture, flaps, trim
* Yoke shelf clamp details
