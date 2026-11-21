# Proposal: 737DIYSIM C172 main panel in our folding (bifold) case (2026-11-21)

Source: https://www.737diysim.com/build-guides-1/c172-main-panel (read in a browser), plus Jason's "172 IP" dimension PDF (Karl Clarke).

## His build in brief
* **Size:** a compact, smaller-than-real C172 panel, about 920 W x 270 H x 200 D overall (369 tall including the curved glareshield top). Desktop or free-standing wooden frame.
* **Panel:** one sheet of 9 mm MDF.
  * Cutouts: PFD 282 x 179, MFD 282 x 179, a 31 mm audio slot, an irregular left switch panel, three 81 mm standby gauges, and an ELT window.
  * Stepped bottom with two 85 mm notches that line up with the pilot and copilot yokes (yoke-through "banking plates" fill them).
  * M4 fixings throughout.
* **Modules:** separate 737DIYSIM designs for the AV switch panel, G1000 (x2), GMA 1347 audio and standby gauges. Each mounts into the MDF from the front with M4 screws.
* **Glareshield:** a printed glareshield screws on top and doubles as the cutting guide for the curved top.
* **CAD:** the MIP CAD is shared as Autodesk links (V1 https://a360.co/4kQ5zin, V2 https://a360.co/4kCYfGI). The module STLs/CAD are sold separately on his shop pages.

## Can it fold? Yes, with five changes

### 1. Split line between the PFD and the standby gauges (about x = 430 from the left)
* **Left half (about 430 wide):** switch panel, PFD, pilot yoke notch.
* **Right half (about 490 wide):** audio, MFD, standby gauges, copilot notch, ELT. The left half folds onto the right (left ≤ right, so it stacks cleanly).
* The gap between the PFD cutout's right edge (about 425) and the airspeed hole's left edge (about 436.5) is only about 11 mm. **Recommend shifting the three standby gauges about 5 mm right** (still clear of the copilot notch) so the seam has room.
* No other seam position works: every other line cuts through the audio/MFD/gauges block.

### 2. Seam structure that fits in that 11 mm
* **At the seam:** instead of our 2040 uprights, each half gets a **40 mm deep aluminum flat-bar rib (40 x 4 mm)** on its seam edge, carrying the side-mounted piano hinge. That's 4 + 3 + 4 mm, so about 11 mm wide.
* **Outer ends:** keep our 2040 + 2020 bumper uprights.
* **Top/bottom:** 40 mm edge lips that follow his stepped bottom and curved top, so the 85 mm face-to-face gap (40 mm knob budget per side) is kept and the case seals when closed.
* **Behind the panel:** horizontal 2020 rails for stiffness and electronics trays, plus rear covers.

### 3. Panel face material
His 9 mm MDF is about 2.3 kg for this sheet and doesn't like hinge screws. Recommend **6 mm ACM (aluminum composite) or 6 mm birch ply, CNC/laser cut from his CAD** (e.g. SendCutSend / local laser), split at the seam. His module screw positions are kept, so his parts bolt straight in.

### 4. Glareshield
It overhangs the face, so it can't sit between the closed halves. **Split it at the seam, and give each half a rear-top hinge so it flips back over the top for travel** (or locate it on dowels + magnets and lift it off). It sits on top of the closed case.

### 5. Depth
His unit is about 200 deep on a wooden frame. The G1000 / AV / audio rear depths aren't published; they need measuring from his files. Our budget becomes:
* 40 mm proud (knob zone),
* 6 mm panel,
* about **60–70 mm behind the panel** for his modules and electronics.

Estimated closed case: **about 495 W x 380 H x 250 D mm** plus the folded glareshield on top. That's bigger than our current bifold (419 x 416 x 191) because his panel is wider (920 vs 831 mm open), but it's the real-layout look he built.

## Electronics and mounting
* His modules are the same family as ours (Arduino Mega for the G1000s, tact switches, PropWash/EC11 encoders, MobiFlight-style), so wiring and software carry over.
* **Hinge crossing:** keep each half self-contained (left: AV panel + PFD; right: audio + MFD + standby), with a USB hub per half, or one hub plus a flexible loop across the hinge.
* **Support:** our clamp feet and outriggers replace his wooden frame. His yoke-through banking plates stay in the notches.

## What I need to model it accurately
1. **His MIP CAD in Fusion.** Open the V2 a360 link and "Open in Fusion" / save to the *Flight Sim Case* project, so I can build the case around his exact geometry instead of re-entering PDF numbers. Some PDF dimensions around the audio slot don't add up.
2. **Rear depth of his G1000, AV panel and audio panel**, from the purchased STLs/CAD (or measured once printed).
3. Your call on the glareshield: **flip-back hinge** (recommended) or **lift-off**.
4. OK to shift the standby gauges about 5 mm right.

Licensing note: his module designs are paid downloads, so I'll build only the case/adapter geometry around them and won't redistribute his files in our repo.
