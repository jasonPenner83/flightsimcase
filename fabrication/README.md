# Fabrication: tracing sheets and router jigs

Generated from the Fusion model (Folding Cockpit Case - C172). Re-run after design changes:

1. In Fusion (MCP): extract outlines -> `panels.json` (snippet in the session log; bodies `PANEL 737*`, `PANEL lower*`,
   `PANEL spacer`, rear lids; the right panels include the 6 mm edge strip).
2. `python make_trace_pdf.py` -> `Panel_Tracing_1to1_Letter.pdf`
3. In Fusion: `fusion/build_jigs.py` -> `jigs/*.stl` and `jigs/jig_list.txt`; `python jig_preview.py` -> `jigs/jig_contact_sheet.svg`

## Tracing sheets (`Panel_Tracing_1to1_Letter.pdf`, 40 sheets, US Letter)

- Print at **100 % / Actual size** ("Fit to page" off). Check the 100 mm / 4 in scale bar on every sheet.
- Sheets overlap 15 mm. Line up the grey 50 mm grid crosses (labels are panel coordinates in mm), tape, then
  spray-mount or tape the assembled sheet to the panel blank and trace (or prick through) the outline and cut-outs.
- Views are of the front face. Small circles with a cross are drill/screw holes. Cut-outs labelled `jig Jxx` have a jig.

## Router jigs (`jigs/`)

Each jig is an 8 mm plate whose opening is the exact cut-out from the model, with centre-line notches on all four
edges and the nearby screw holes as small drill marks. Print in PETG, 4 walls, 40 % infill, flat.

| Jig | Cut-out | Prints |
| --- | --- | --- |
| J01 | PFD opening | A + B (half-lap, 2 x M3) |
| J02 | Switch / dimmer panel | 1 |
| J03 | Yoke hole, 40 mm, with slot to the bottom edge | 1 |
| J04 | Ignition key | 1 |
| J05 | GMA 1347 opening (spacer) | 1 |
| J06 | MFD opening | A + B (half-lap, 2 x M3) |
| J07-J09 | Standby ASI, attitude, altimeter | 1 each |
| J10 | ELT switch | 1 |
| J11 | Flaps lever (right of the MFD) | 1 |
| J13 | Fuel selector (right of the standby gauges) | 1 |
| J14 | TPM pod: throttle 31 / mixture 27 / condition 31 mm holes | 1 |
| J15 | Trim wheel pod | 1 |

How to use (flush-trim / pattern bit with a top bearing, 1/4 in shank cutter, cutting length >= 12 mm):

1. Trace the panel from the PDF. Drill a start hole and jigsaw the waste out to within about 3 mm of the line.
2. Line the jig opening up with the traced cut-out (the centre-line notches sit on the traced centre lines) and fix
   it with double-sided tape or clamps. Split jigs: bolt A and B together first.
3. Rout with the bearing riding on the jig. Inside corners come out with the bit's radius (3.2 mm for a 1/4 in
   bit); square them with a chisel where a bezel needs a sharp corner.
4. Drill the small screw holes through the jig's marks.

Check the throttle (31 mm) and mixture (27 mm) hole sizes against the 737DIYSIM throttle guide before cutting.
