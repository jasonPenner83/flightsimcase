# C172 Folding Cockpit Case – BOM and Print List

2026-11-22 · Jason · Live version: https://claude.ai/artifact/Y2WVsvdj8FzGZrHrNEVcPA

## Summary

The case is a bifold clamshell that carries the 737DIYSIM C172 main panel: a left half, an 85 mm spacer with the GMA 1347, and a right half. Open, it is 951 mm wide; closed, it is about 470 W × 355 D × 600 H mm, including feet and desk jaws.

All quantities come from the Fusion model (Folding Cockpit Case - C172, latest version). Lengths are in mm.

This BOM covers our case: frame, sheet goods, hardware and our printed parts. The 737DIYSIM instrument modules are listed by name only. Build them from Jason's purchased files and his guides; they are not redistributed here.

## Aluminium extrusion cut list

You need about 6.1 m of 2020 and 0.7 m of 2040. That nests into seven 1000 mm lengths of 2020 and one 1000 mm length of 2040, allowing 3 mm per cut. All members are cut square, and the corner of the curved top is carried by the rim skin, not by mitred extrusion.

| Part | Profile | Length (mm) | Qty | Where |
| --- | --- | --- | --- | --- |
| Outer upright | 2040 | 341.5 | 2 | Front outer edge of each half, z −125 to 216 |
| Front rail, bottom / mid | 2020 | 390 | 4 | Two per half, behind the panel |
| Front rail, z 126 (left) | 2020 | 194.5 | 1 | Left half, beside the switch panel |
| Front rail, z 126 (right) | 2020 | 390 | 1 | Right half |
| Front top rail (left) | 2020 | 170 | 1 | Straight run of the top, left |
| Front top rail (right) | 2020 | 164 | 1 | Straight run of the top, right |
| Rear post, seam side | 2020 | 494 | 2 | Full height, one per half |
| Rear post, outer side | 2020 | 341 | 2 | Up to where the curve starts |
| Rear rail, bottom | 2020 | 390 | 2 | One per half |
| Rear rail, top (left) | 2020 | 170 | 1 | Straight top run |
| Rear rail, top (right) | 2020 | 164 | 1 | Straight top run |
| Depth member (left) | 2020 | 20 | 2 | Seam corners only; the thin left box bolts its rear frame straight to the 2040 |
| Depth member (right) | 2020 | 118 / 138 | 2 / 2 | Deeper right box |
| Seam angle | Alu angle 20×20×2 | 494 | 4 | Both halves plus both spacer edges |

Suggested nesting on 1000 mm 2020 bars:

1. 494 + 494
2. 390 + 390 + 194.5
3. 390 + 390 + 170
4. 390 + 390 + 170
5. 390 + 341 + 164
6. 341 + 164 + 138 + 138 + 118
7. 118 + 20 + 20 (about 830 mm left over)

## Sheet goods

The panels are 9 mm plywood and the skins are 3 mm. The rim skins wrap the curved corners, so they need bending plywood or thin aluminium rather than standard ply.

| Part | Material | Size (mm) | Qty | Notes |
| --- | --- | --- | --- | --- |
| Main panel, left | 9 mm ply | 430 × 369 | 1 | Cut from his MIP panel file, with our yoke hole and face pocket |
| Main panel, right | 9 mm ply | 430 × 369 | 1 | His right section plus the 6 mm edge strip, so cut it 6 mm wider |
| Spacer panel | 9 mm ply | 85 × 369 | 1 | 48 × 198 cutout for the GMA 1347 |
| Lower panel, left | 9 mm ply | 430 × 125 | 1 | Cutouts for the left fuse panel and fuel selector |
| Lower panel, right | 9 mm ply | 424 × 125 | 1 | Throttle, mixture, condition, flaps |
| Lower panel, spacer | 9 mm ply | 85 × 125 | 1 | Plain |
| Rim skin, left | 3 mm bending ply or 1.5 mm aluminium | about 1270 × 116 developed | 1 | Side, curved corner, top and bottom; runs 46.5 mm in front of the face |
| Rim skin, right | 3 mm bending ply or 1.5 mm aluminium | about 1270 × 234 developed | 1 | Deeper right box |
| Rear lid | 3 mm ply | about 433 × 500, curved top corner | 2 | Removable, one per half |
| Seam side wall | 3 mm ply | 43 × 500 (left), 161 × 500 (right) | 2 | Closes each box on the hinge side |

A 1220 × 610 sheet of 9 mm ply covers all six panels. One 1220 × 610 sheet of 3 mm ply covers both lids and both seam walls. The rim skins are about 1.3 m long, so buy them as a long strip or join them at the top straight run.

## Hardware

Counts include about 20 % spare. Fastener counts are estimates from the joint count (about 20 frame joints per half), not from a modelled fastener layout.

| Item | Spec | Qty | Use |
| --- | --- | --- | --- |
| Piano hinge | Stainless, 1.5 mm, about 32 mm open width, 500 mm | 2 | Cut to 474 mm; spacer to left half and spacer to right half |
| Corner bracket | 20-series L bracket with tabs | 50 | Frame joints |
| Drop-in T-nut | M5, 20-series | 200 | Brackets, panels, skins |
| Button head screw | M5 × 8 | 100 | Brackets |
| Button head screw | M5 × 10 | 70 | Rim skins and seam walls to frame |
| Button head screw | M5 × 16 | 30 | 9 mm panels to front rails |
| Machine screw + nyloc nut | M3 × 8 | 40 | Hinge leaves to seam angles, every 50 mm |
| Neodymium magnet | 6 × 3 mm | 8 | Middle glareshield (4), spare |
| Neodymium magnet + steel disc | 10 × 3 mm | 16 + 16 | Rear lids, 8 per lid |
| Heat-set insert | M3 | 30 | Pod, pedestal base, trays |
| Star knob clamp screw + insert | M6 | 2 | Desk clamp jaws |
| Toggle latch | Small draw latch | 3 | Hold the closed rims together (top and outer side); not yet modelled |
| Carry handle | Surface mount, about 120 mm | 1 | On the top run of the rims when closed; not yet modelled |

## Electronics and modules

The case holds 737DIYSIM modules built from his files. The rest is off the shelf. His module BOMs (encoders, switches, pots, Arduinos, screens) are in his build guides and are not repeated here.

| Item | Source | Qty | Where in the case |
| --- | --- | --- | --- |
| G1000 PFD bezel + 10.4 in LCD | 737DIYSIM | 1 | Left half |
| G1000 MFD bezel + LCD (about 239 × 176) | 737DIYSIM | 1 | Right half |
| GMA 1347 audio panel | 737DIYSIM | 1 | Spacer, mounted flush; volume knob comes off for travel |
| Switch and dimmer panel (172 AV PNL) | 737DIYSIM | 1 | Left half |
| Standby ASI, attitude, altimeter | 737DIYSIM | 1 set | Right half, in the old copilot-yoke area |
| ELT switch | 737DIYSIM | 1 | Right half |
| Left fuse panel with key switch | 737DIYSIM | 1 | Left lower |
| Fuel selector (FSP3) | 737DIYSIM | 1 | Left lower, beside the fuse panel |
| Throttle push-pull (lower-panel version) | 737DIYSIM | 2 | Right lower: one throttle, one used as condition |
| Mixture push-pull | 737DIYSIM | 1 | Right lower |
| Flaps lever | 737DIYSIM | 1 | Right lower |
| Trim wheel (Trim v15) | 737DIYSIM | 1 | Clamp-on pod, stored in the right box |
| Yoke adapter | 737DIYSIM | 1 | Left half, for the Logitech yoke |
| Logitech Flight Throttle Quadrant | Owned | 1 | Stored in the right box |
| Powered USB hub, 7-port (about 115 × 45 × 25) | Off the shelf | 1 | Flat behind the left fuse panel |
| 12 V power supply, LRS-50-12 size (99 × 82 × 30) | Off the shelf | 1 | Behind the blank right lower panel |

The Logitech yoke and the rudder pedals travel separately.

## 3D print list

Every printed case part fits the A1's 256 × 256 × 256 mm build volume. Print in PETG. Faceplates stay plain, with labels as stickers or outsourced artwork.

| Part | Size (mm) | Qty | Fits 256 bed | Print notes |
| --- | --- | --- | --- | --- |
| Pedestal base + desk clamp | 220 × 110 × 45 | 1 | Yes | Flat; M6 insert for the clamp screw; stored in the right box |
| Trim wheel pod shell | 188 × 130 × 83 | 1 | Yes | Open side up; slides onto the pedestal base; stored in the right box |
| Face pocket tray, right | 119 × 92 × 62 | 1 | Yes | Open front down |
| Cable bin, spacer | 115 × 79 × 22 | 1 | Yes | Open top up |
| Cable bin, right | 98 × 49 × 44 | 1 | Yes | Open top up |
| Face pocket tray, left | 92 × 71 × 58 | 1 | Yes | Open front down; shallower to suit the thin left box |
| Glareshield middle piece | 91 × 56 × 9 | 1 | Yes | Top face down; 4 magnet pockets |
| Desk clamp jaw | 60 × 20 × 12 | 2 | Yes | Pad with rubber |
| Foot | 49 × 40 × 20 | 2 | Yes | Left half |
| Clamp foot | 49 × 40 × 20 | 2 | Yes | Right half |

His 737DIYSIM printed parts print from his files. One part runs over the bed: a 346 × 238 mm plate in the MFD assembly. Check his guide for a split version, or outsource it.

## Open items

- [ ] Pick the rim material: 3 mm bending ply (lighter, warmer look) or 1.5 mm aluminium (tougher, easier to bend accurately).
- [ ] Model the closing latches and the carry handle, then add them to the fold check.
- [ ] Confirm the measurements on the real 737DIYSIM parts before cutting.
- [ ] Check whether his MFD plate (346 × 238) has a split version, or outsource it.
- [ ] Decide whether the blank strip on the right lower panel gets a front connector panel (USB for yoke, quadrant, pedals, headset).
