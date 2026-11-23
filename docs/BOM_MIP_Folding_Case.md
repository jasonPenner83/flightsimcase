# C172 Folding Cockpit Case – BOM and Print List

2026-11-23 · Jason · Live version: https://claude.ai/artifact/Y2WVsvdj8FzGZrHrNEVcPA

## Summary

The case is a bifold clamshell that carries the 737DIYSIM C172 main panel: a left half, an 85 mm spacer with the GMA 1347, and a right half. Deployed, the main unit sits on the desk and overhangs its front edge by 40 mm. It lowers over the Logitech yoke through a slot and a housing tunnel. The lower panel is three separate pieces bolted under it, hanging below the desktop. The main unit carries no storage. Packed, the lower panel travels separately and the main case closes to about 470 W × 255 D × 399 H mm.

All quantities come from the Fusion model (Folding Cockpit Case - C172, latest version). Lengths are in mm.

This BOM covers our case: frame, sheet goods, hardware and our printed parts. The 737DIYSIM instrument modules are listed by name only. Build them from Jason's purchased files and his guides; they are not redistributed here.

## Aluminium extrusion cut list

You need about 4.8 m of 2020, which nests into five 1000 mm bars, plus one 1000 mm bar of 2040 (0.43 m used), allowing 3 mm per cut. All members are cut square; the curved top corners are carried by the rim skins.

| Part | Profile | Length (mm) | Qty | Where |
| --- | --- | --- | --- | --- |
| Outer upright | 2040 | 216.5 | 2 | Front outer edge of each half, up to where the curve starts |
| Front rail, bottom (left) | 2020 | 133 | 1 | Stops short of the yoke tunnel |
| Front rail, bottom + mid (right) | 2020 | 390 | 2 | z 10 and z 126 |
| Front rail, mid (left) | 2020 | 194.5 | 1 | Beside the switch panel, above the tunnel |
| Front top rail | 2020 | 170 (L) / 164 (R) | 1 / 1 | Straight run of the top |
| Rear post, seam side | 2020 | 369 | 2 | Full height |
| Rear post, outer side | 2020 | 216 | 2 | Up to where the curve starts |
| Rear rail, bottom | 2020 | 133 (L) / 390 (R) | 1 / 1 | Left stops short of the tunnel |
| Rear rail, top | 2020 | 170 (L) / 164 (R) | 1 / 1 | Straight top run |
| Depth member (left) | 2020 | 20 | 2 | Seam corners only |
| Depth member (right) | 2020 | 18 / 38 | 2 / 2 | 90 mm right box |
| Lower panel top rail | 2020 | 390 | 2 | Behind the desk-edge strip of each lower piece |
| Seam angle | Alu angle 20×20×2 | 369 | 4 | Both halves, plus both spacer edges (spacer pair trimmed to 16 mm leaves for the GMA plate) |

Suggested nesting on 1000 mm 2020 bars:

1. 390 + 390 + 194.5
2. 390 + 390 + 170
3. 390 + 369 + 216
4. 369 + 216 + 170 + 164 + 20 + 20
5. 164 + 133 + 133 + 38 + 38 + 18 + 18 (about 450 mm left over)

## Sheet goods

The panels are 9 mm plywood and the skins are 3 mm. The rim skins wrap the curved corners, so they need bending plywood or thin aluminium rather than standard ply.

| Part | Material | Size (mm) | Qty | Notes |
| --- | --- | --- | --- | --- |
| Main panel, left | 9 mm ply | 430 × 369 | 1 | From his MIP panel file; our yoke hole at shaft height with a slot to the bottom edge |
| Main panel, right | 9 mm ply | 430 × 369 | 1 | His right section plus the 6 mm edge strip; flaps lever cut-out right of the standby gauges |
| Spacer panel | 9 mm ply | 85 × 369 | 1 | 48 × 198 cutout for the GMA 1347 |
| Lower panel, left | 9 mm ply | 430 × 170 | 1 | Left fuse panel and fuel selector; top 41 mm is the desk-edge strip |
| Lower panel, right | 9 mm ply | 430 × 222 | 1 | Trim wheel, throttle, mixture, condition |
| Lower panel, spacer | 9 mm ply | 85 × 170 | 1 | Plain |
| Rim skin, left | 3 mm bending ply or 1.5 mm aluminium | about 1140 × 116 developed | 1 | Side, curved corner, top and bottom of the main unit; tunnel and slot cut in the bottom |
| Rim skin, right | 3 mm bending ply or 1.5 mm aluminium | about 1140 × 134 developed | 1 | Right box is 90 mm deep (flaps lever, standby gauges) |
| Rear lid | 3 mm ply | about 433 × 375, curved top corner | 2 | Left lid has the tunnel notch |
| Seam side wall | 3 mm ply | 43 × 375 (left), 61 × 375 (right) | 2 | Hinge side of each box |
| Lower box, left | 3 mm ply | bottom 433 × 119, lid 430 × 129, shelf 430 × 41, back 430 × 38, sides 132 × 119 + 78 × 41 | 1 set | Stepped: 31 mm deep at the desk edge, 72 mm under the desk |
| Lower box, right | 3 mm ply | bottom 433 × 236, lid 430 × 181, shelf 430 × 159, back 430 × 38, sides 236 × 184 + 78 × 41 | 1 set | 190 mm deep under the desk for the push-pull rods and trim wheel |

One 1220 × 610 sheet of 9 mm ply covers all six panels. The 3 mm parts need two 1220 × 610 sheets. The rim skins are about 1.15 m long, so buy them as a long strip or join them at the top straight run.

## Hardware

Counts include about 20 % spare. Fastener counts are estimates from the joint count, not from a modelled fastener layout.

| Item | Spec | Qty | Use |
| --- | --- | --- | --- |
| Piano hinge | Stainless, 1.5 mm, about 32 mm open width | 2 | Cut to 349 mm; spacer to left half and spacer to right half |
| Corner bracket | 20-series L bracket with tabs | 45 | Frame joints |
| Drop-in T-nut | M5, 20-series | 200 | Brackets, panels, skins, lower-panel joints |
| Button head screw | M5 × 8 | 90 | Brackets |
| Button head screw | M5 × 10 | 80 | Rim skins, lower boxes and seam walls to frame |
| Button head screw | M5 × 16 | 30 | 9 mm panels to rails |
| Aluminium flat bar + knob screws | 20 × 3 mm, 60 mm long, M5 star knobs | 6 + 12 | Join each lower piece's top rail to the main unit's bottom rail, tool-free; not yet modelled |
| Machine screw + nyloc nut | M3 × 8 | 30 | Hinge leaves to seam angles, every 50 mm |
| Neodymium magnet | 6 × 3 mm | 6 | Middle glareshield (4), spare |
| Neodymium magnet + steel disc | 10 × 3 mm | 16 + 16 | Rear lids, 8 per lid |
| Heat-set insert | M3 | 20 | Spare (no printed storage parts any more) |
| Star knob clamp screw + insert | M6 | 1 | Not needed (trim wheel now built in) |
| Toggle latch | Small draw latch | 3 | Hold the closed rims together; not yet modelled |
| Carry handle | Surface mount, about 120 mm | 1 | On the top run of one rim; not yet modelled |

## Electronics and modules

The case holds 737DIYSIM modules built from his files. The rest is off the shelf. His module BOMs are in his build guides and are not repeated here.

| Item | Source | Qty | Where in the case |
| --- | --- | --- | --- |
| G1000 PFD bezel + 10.4 in LCD (Toshiba LTD104EDZS + HDMI board, [AliExpress](https://www.aliexpress.com/item/1005011787148121.html), C$72.38 + C$3.76 shipping) | 737DIYSIM | 1 | Left half |
| G1000 MFD bezel + LCD (same LTD104EDZS kit, about 219 × 174; see [g1000-display-choice.md](g1000-display-choice.md)) | 737DIYSIM | 1 | Right half |
| GMA 1347 audio panel | 737DIYSIM | 1 | Spacer, mounted flush; volume knob comes off for travel |
| Switch and dimmer panel (172 AV PNL) | 737DIYSIM | 1 | Left half |
| Standby ASI, attitude, altimeter | 737DIYSIM | 1 set | Right half, in the old copilot-yoke area |
| Flaps lever | 737DIYSIM | 1 | Right half, right of the standby gauges |
| ELT switch | 737DIYSIM | 1 | Right half |
| Left fuse panel with key switch | 737DIYSIM | 1 | Left lower piece |
| Fuel selector (FSP3) | 737DIYSIM | 1 | Left lower piece, beside the fuse panel |
| Throttle push-pull (lower-panel version) | 737DIYSIM | 2 | Right lower piece: one throttle, one used as condition |
| Mixture push-pull | 737DIYSIM | 1 | Right lower piece |
| Trim wheel (Trim v15) | 737DIYSIM | 1 | Right lower piece, left of the throttle |
| Yoke adapter | 737DIYSIM | 1 | Left half, moved down to the yoke shaft height |
| Powered USB hub, 7-port (about 115 × 45 × 25) | Off the shelf | 1 | Right box, behind the MFD |
| 12 V power supply, LRS-50-12 size (99 × 82 × 30) | Off the shelf | 1 | Right box, behind the MFD |

The Logitech yoke (clamped to the desk; the main unit lowers over it), the throttle quadrant, the rudder pedals and the lower panel travel separately from the main case.

## 3D print list

Every printed case part fits the A1's 256 × 256 × 256 mm build volume. Print in PETG. Faceplates stay plain, with labels as stickers or outsourced artwork.

| Part | Size (mm) | Qty | Fits 256 bed | Print notes |
| --- | --- | --- | --- | --- |
| Glareshield middle piece | 91 × 56 × 9 | 1 | Yes | Top face down; 4 magnet pockets |

Router jigs for the panel cut-outs (17 prints, all within the bed) are in the fabrication files, with the 1:1 tracing PDF. His 737DIYSIM printed parts print from his files; one plate in the MFD assembly is 346 × 238 mm, over the bed.

## Open items

- [ ] Confirm the yoke shaft height: the model assumes about 36 mm above the desk (mid-height of the 71 mm housing).
- [ ] Check under the desk: the lower boxes reach 72 mm (left) and 190 mm (right) back under the desktop, 41 to 176 mm below its top surface.
- [ ] Check the yoke clamp clears the main unit; the panel stands 40 mm in front of the desk edge.
- [ ] Pick the rim material: 3 mm bending ply or 1.5 mm aluminium.
- [ ] Model the lower-panel joints, the closing latches and the carry handle.
- [ ] Check whether his MFD plate (346 × 238) has a split version, or outsource it.
- [ ] Confirm the throttle (31 mm) and mixture (27 mm) hole sizes against his throttle guide.
