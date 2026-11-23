# C172 Folding Cockpit Case – BOM and Print List

2026-11-23 · Jason · Live version: https://claude.ai/artifact/Y2WVsvdj8FzGZrHrNEVcPA

## Summary

The case is a bifold clamshell that carries the 737DIYSIM C172 main panel: a left half, an 85 mm spacer with the GMA 1347, and a right half. Everything used in flight is on the main panel, including the fuel selector, ignition key and flaps. Deployed, the main unit sits on the desk, overhangs its edge by 40 mm and lowers over the Logitech yoke. Two optional clamp-on pods hang under its front edge: the trim wheel, and throttle / mixture / condition. Packed, the main case closes to about 470 W × 255 D × 399 H mm and the pods travel separately.

All quantities come from the Fusion model (Folding Cockpit Case - C172, latest version). Lengths are in mm.

This BOM covers our case: frame, sheet goods, hardware and our printed parts. The 737DIYSIM instrument modules are listed by name only. Build them from Jason's purchased files and his guides; they are not redistributed here.

## Aluminium extrusion cut list

You need about 3.7 m of 2020, which nests into four 1000 mm bars, plus one 1000 mm bar of 2040 (0.43 m used), allowing 3 mm per cut. All members are cut square; the curved top corners are carried by the rim skins.

| Part | Profile | Length (mm) | Qty | Where |
| --- | --- | --- | --- | --- |
| Outer upright | 2040 | 216.5 | 2 | Front outer edge of each half, up to where the curve starts |
| Front rail, bottom | 2020 | 133 (L) / 254 (R) | 1 / 1 | Left stops at the yoke tunnel, right at the fuel selector |
| Front rail, mid | 2020 | 194.5 (L) / 390 (R) | 1 / 1 | z 126 |
| Front top rail | 2020 | 170 (L) / 164 (R) | 1 / 1 | Straight run of the top |
| Rear post, seam side | 2020 | 369 | 2 | Full height |
| Rear post, outer side | 2020 | 216 | 2 | Up to where the curve starts |
| Rear rail, bottom | 2020 | 133 (L) / 390 (R) | 1 / 1 | Left stops at the tunnel |
| Rear rail, top | 2020 | 170 (L) / 164 (R) | 1 / 1 | Straight top run |
| Depth member | 2020 | 20 (L) / 18 + 38 (R) | 2 / 2 + 2 | Box corners |
| Pod top rail | 2020 | 81 (trim) / 157 (TPM) | 1 / 1 | Behind each pod's desk-edge strip |
| Seam angle | Alu angle 20×20×2 | 369 | 4 | Both halves and both spacer edges; spacer pair trimmed to 16 mm leaves, right one notched behind the ASI |

Suggested nesting on 1000 mm 2020 bars:

1. 390 + 390 + 194.5
2. 369 + 369 + 216
3. 254 + 216 + 170 + 170 + 164
4. 164 + 157 + 133 + 133 + 81 + 38 + 38 + 18 + 18 + 20 + 20

## Sheet goods

The panels are 9 mm plywood and the skins are 3 mm. The rim skins wrap the curved corners, so they need bending plywood or thin aluminium rather than standard ply.

| Part | Material | Size (mm) | Qty | Notes |
| --- | --- | --- | --- | --- |
| Main panel, left | 9 mm ply | 430 × 369 | 1 | From his MIP panel file; yoke hole + slot, ignition key cut-out |
| Main panel, right | 9 mm ply | 430 × 369 | 1 | His right section plus the 6 mm edge strip; fuel selector and flaps cut-outs |
| Spacer panel | 9 mm ply | 85 × 369 | 1 | 48 × 198 cutout for the GMA 1347 |
| TPM pod front plate | 9 mm ply | 163 × 172 | 1 | Throttle 31, mixture 27, prop 31 mm holes |
| Trim wheel pod front plate | 9 mm ply | 87 × 222 | 1 | Trim case cut-out |
| Rim skin, left | 3 mm bending ply or 1.5 mm aluminium | about 1140 × 116 developed | 1 | Tunnel and slot cut in the bottom |
| Rim skin, right | 3 mm bending ply or 1.5 mm aluminium | about 1140 × 134 developed | 1 | Right box is 90 mm deep |
| Rear lid | 3 mm ply | about 433 × 375, curved top corner | 2 | Left lid has the tunnel notch |
| Seam side wall | 3 mm ply | 43 × 375 (left), 61 × 375 (right) | 2 | Hinge side of each box |
| TPM pod box | 3 mm ply | bottom 169 × 302, lid 163 × 131, shelf 163 × 224, back 163 × 38, 2 sides 302 × 134 + 78 × 41 | 1 set | 255 mm deep under the desk for the throttle V2 racks |
| Trim wheel pod box | 3 mm ply | bottom 93 × 187, lid 87 × 181, shelf 87 × 109, back 87 × 38, 2 sides 187 × 184 + 78 × 41 | 1 set | 140 mm deep under the desk |

One 1220 × 610 sheet of 9 mm ply covers all five panels and plates. One 1220 × 610 sheet of 3 mm ply covers the lids, seam walls and both pod boxes. The rim skins are about 1.15 m long, so buy them as a long strip or join them at the top straight run.

## Hardware

Counts include about 20 % spare. Fastener counts are estimates from the joint count, not from a modelled fastener layout.

| Item | Spec | Qty | Use |
| --- | --- | --- | --- |
| Piano hinge | Stainless, 1.5 mm, about 32 mm open width | 2 | Cut to 349 mm; spacer to left half and spacer to right half |
| Corner bracket | 20-series L bracket with tabs | 40 | Frame joints |
| Drop-in T-nut | M5, 20-series | 180 | Brackets, panels, skins, pod brackets |
| Button head screw | M5 × 8 | 80 | Brackets |
| Button head screw | M5 × 10 | 70 | Rim skins, pod boxes and seam walls to frame |
| Button head screw | M5 × 16 | 25 | 9 mm panels and plates to rails |
| M5 star knob screw | M5 × 12 | 8 | Pod hanger brackets, tool-free |
| Machine screw + nyloc nut | M3 × 8 | 30 | Hinge leaves to seam angles, every 50 mm |
| Neodymium magnet | 6 × 3 mm | 6 | Middle glareshield (4), spare |
| Neodymium magnet + steel disc | 10 × 3 mm | 16 + 16 | Rear lids, 8 per lid |
| Toggle latch | Small draw latch | 3 | Hold the closed rims together; not yet modelled |
| Carry handle | Surface mount, about 120 mm | 1 | On the top run of one rim; not yet modelled |

## Electronics and modules

The case holds 737DIYSIM modules built from his files. The rest is off the shelf. His module BOMs are in his build guides and are not repeated here.

| Item | Source | Qty | Where |
| --- | --- | --- | --- |
| G1000 PFD bezel + 10.4 in LCD (Toshiba LTD104EDZS + HDMI board, [AliExpress](https://www.aliexpress.com/item/1005011787148121.html), C$72.38 + C$3.76 shipping) | 737DIYSIM | 1 | Left half |
| G1000 MFD bezel + LCD (same LTD104EDZS kit, about 219 × 174; see [g1000-display-choice.md](g1000-display-choice.md)) | 737DIYSIM | 1 | Right half (without the 346 × 238 back plate in his assembly) |
| GMA 1347 audio panel | 737DIYSIM | 1 | Spacer, mounted flush; volume knob comes off for travel |
| Switch and dimmer panel (172 AV PNL) | 737DIYSIM | 1 | Left half |
| Ignition key (C172 Start sw) | 737DIYSIM | 1 | Left half, between the yoke and the seam |
| Standby ASI, attitude, altimeter | 737DIYSIM | 1 set | Right half |
| Fuel selector (FSP3) | 737DIYSIM | 1 | Right half, right of the standby gauges; face plate trimmed to 135 × 109 |
| Flaps lever | 737DIYSIM | 1 | Right half, right of the MFD |
| ELT switch | 737DIYSIM | 1 | Right half |
| Yoke adapter | 737DIYSIM | 1 | Left half, at the yoke shaft height |
| Trim wheel (Trim v15) | 737DIYSIM | 1 | Trim wheel pod |
| Throttle V2 (172 THROTTLE V2, rack + gear pot) | 737DIYSIM | 2 | TPM pod: throttle and prop |
| Mixture push-pull | 737DIYSIM | 1 | TPM pod |
| Powered USB hub, 7-port (about 115 × 45 × 25) | Off the shelf | 1 | Right box, behind the MFD |
| 12 V power supply, LRS-50-12 size (99 × 82 × 30) | Off the shelf | 1 | Right box, behind the MFD |

The fuse panels are left out. The Logitech yoke (clamped to the desk; the main unit lowers over it), the throttle quadrant, the rudder pedals and both pods travel separately from the main case.

## 3D print list

Every printed case part fits the A1's 256 × 256 × 256 mm build volume. Print in PETG. Faceplates stay plain, with labels as stickers or outsourced artwork.

| Part | Size (mm) | Qty | Fits 256 bed | Print notes |
| --- | --- | --- | --- | --- |
| Fuel selector face plate | 135 × 109 × 10 | 1 | Yes | His embossed face plate file, trimmed 10.5 mm top and bottom (tab kept under the shut-off lever) |
| Pod hanger bracket | 20 × 30 × 2 | 4 | Yes | Two per pod; or 20 × 3 mm aluminium flat bar |
| Glareshield middle piece | 91 × 56 × 9 | 1 | Yes | Top face down; 4 magnet pockets |

Router jigs for the panel cut-outs (16 prints, all within the bed) are in the fabrication files, with the 1:1 tracing PDF. His 737DIYSIM printed parts print from his files; one plate in the MFD assembly is 346 × 238 mm, over the bed.

## Open items

- [ ] Confirm the yoke shaft height: the model assumes about 36 mm above the desk.
- [ ] Check under the desk where the pods go: the TPM pod reaches 255 mm and the trim pod 140 mm back under the desktop.
- [ ] Check the yoke clamp clears the main unit; the panel stands 40 mm in front of the desk edge.
- [ ] Check the MFD's knob encoders: a few sit up to 2 mm into the panel back at the cut-out edges, so relieve the panel there.
- [ ] Pick the rim material: 3 mm bending ply or 1.5 mm aluminium.
- [ ] Model the pod brackets, the closing latches and the carry handle.
- [ ] Confirm the throttle / prop (31 mm) and mixture (27 mm) hole sizes against his throttle guides.
