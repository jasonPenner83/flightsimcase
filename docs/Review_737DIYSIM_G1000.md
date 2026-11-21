# Review: 737DIYSIM "Garmin G1000 & G1000 NXi" build vs our C172 bifold (2026-11-21)

Source: https://www.737diysim.com/build-guides-1/garmin-g1000-%26-g1000-nxi, with its Parts Guide and Print Guide pages. They were read in a browser; the page is JavaScript-rendered. The STL files and exact overall dimensions are behind the site's downloads, so the dimensions marked "unknown" below need checking once the files are in hand.

## What his design is
| Area | 737DIYSIM G1000 |
|---|---|
| Printing | 12 part types, 28 pieces, all within a 220 x 220 bed (fits our A1). PLA, 0.2 mm layers (0.12 for small parts), supports on for most parts |
| Bezel | 4 frames (left, right, top, bottom) plus a support frame and side supports. Printed in **white PLA, sprayed black, raised text sanded back**, so the legends are **backlit** by 3 mm LEDs. Frames join with M4 countersunk screws |
| Keys | **LED 6x6x7 mm tactile switches** clicked into printed key caps, held in the frame by bending the switch legs. No PCB: point-to-point wiring. 20 keys (std) or 30 (NXi) |
| Encoders | PropWash dual concentric x5 (or EC11 duals, hot-glued) on screwed backplates (M2.6), plus 4 single encoders with lock nuts |
| Screen | **Toshiba LTD104EDZS** 10.4 in 1024x768 with driver kit. Third-party listings give about **219 x 174 x 6.4 mm** with an edge-lit white-LED backlight. The part is listed **obsolete** (surplus/eBay) |
| Electronics | LCD driver board, menu board and power board on a printed "support matrix" behind the screen; **Arduino Mega 2560 R3** on a printed mount (MobiFlight-style) |
| Software | Made for MSFS 2020 (should carry over to 2024 via MobiFlight/SimConnect) |
| Overall size / depth | **Unknown** until we have the files. It's a self-contained box with the boards stacked behind the screen |

## Fit against our bifold
| Check | Verdict |
|---|---|
| Printable on the A1 | **Yes.** It's designed for a smaller bed |
| Slot width (our display slot is 306 x 199.2 per GDU) | **Probably yes** if it's near 1:1 GDU size (about 300 x 196). Confirm from the STL |
| LCD pocket and fold clearance | The LTD104EDZS (about 6.4 mm, LED) would fit our 9.5 mm pocket and is narrower than our AUO panel. But his unit stacks three boards and a full-size Mega **behind the screen**. Our depth budget is 15 mm proud plus **50 mm behind the rail face**, and the rails cross behind the top and bottom edges (180 mm clear between them). **Likely too deep or too tall behind the screen as-is**; needs measuring |
| Mounting to our rails | **No native fit.** It needs an adapter flange to our rail clamp and panel-plane standard, or a re-mixed back half |
| Outsourcing | Fine. He already suggests resin buttons. The 4-frame bezel would need merging for a seamless MJF part |
| Electronics compatibility | **Yes.** Mega + PropWash/EC11 + tact switches is the same family as our MFD-1 (MobiFlight) |
| Parts availability | Screen is **obsolete**. The AUO G104XVN01.0 we specced is current production |

## Recommendation
Keep our MFD-1 assembly as the base, because it already fits the case. Adopt his proven details:

1. **Backlit legends (biggest realism win):** print the bezel face in white or translucent and paint it black (or use a black/white dual-material print on the AMS 2 Pro), then sand the raised legends back, with LEDs behind. Raised text replaces stickers on the bezel.
2. **LED tactile switches** (6x6x7 with built-in LED) in clip-in printed caps, for lit keys like the real unit.
3. **Screwed encoder backplates** (M2.6) instead of PCB-mounted duals, for an easy first build and swaps.
4. **No-PCB option for build #1:** switches clipped into the frame and hand-wired, as he does. Our PCB carriers stay as the upgrade path.
5. **PropWash supplied knobs**, painted black, as he does, until our printed knobs get final bores.

Keep from ours:
* Rail mounting and panel plane.
* The 15 mm bezel / 9.5 mm LCD pocket and fold-checked depth.
* Electronics on the tray behind the rails.
* The current-production AUO screen.
* Split-for-A1 versus one-piece outsource.
* MFD and PFD sharing one design.

Alternative if Jason prefers his look outright: buy his files, and I'll model an **adapter frame** that bolts his 4-frame bezel to our rails and repackages his rear boards onto our tray. First step is measuring his STL's outer size and rear depth against our 306 x 199 slot and 50 mm rear budget.
