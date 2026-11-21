# Folding MSFS 2024 Cockpit Case

A carry-size folding home cockpit for MSFS 2024. It starts with a full-scale Cessna 172 G1000 panel, with TBM 900 / PC-12 later. The frame is Vevor 2020/2040 aluminum extrusion with 3D-printed (Bambu A1) modules.

- **Current design:** C172 G1000 **bifold** (iteration 1, model-specific). Two 414 mm halves on one piano hinge. Left: switch column + PFD over lights/mags, yoke and breakers. Right: audio + MFD over standby gauges, dimming and copilot yoke. Folds to 419 x 416 x 191 mm, sealed when closed. The earlier modular trifold is archived in docs/archive/ (Fusion v1 to v5).
- **Spec and cut list:** [C172_Bifold_Spec.md](C172_Bifold_Spec.md)
- **Bill of materials:** [BOM.md](BOM.md)
- **MFD-1 (GDU 1040) build guide:** [docs/MFD-1_Build_Guide.md](docs/MFD-1_Build_Guide.md) (parts, hardware, A1 print settings, outsourced MJF/SLA option, assembly)
- **Print files:** [prints/](prints/) (SC-1, LT-1, YK-1, CB-1, AU-1, SB-1, SB-2, CP-1, plus the PFD-1 and MFD-1 bezels in 3 pieces each)
- **Label artwork:** [labels/](labels/) (1:1 SVG for stickers or outsourced engraving; regenerate with `python fusion/gen_label_art.py`)
- **Renders:** [renders/](renders/) (older revisions in subfolders)

## Fusion model
The master model lives in Autodesk Fusion: project "Flight Sim Case", design "Folding Cockpit Case - C172" (v1 = rev E lock).
The scripts in [fusion/](fusion/) rebuild it through the Fusion API. For the bifold, run_bifold.py runs build_case_bifold.py, c172_panels.py and build_pfd.py. The trifold scripts are kept for history:
- `build_case.py`: frame, hinges, outriggers. Dimensions are in the `P` dict at the top.
- `build_switch_panel.py`: faceplate modules, built as real sketch/extrude features. It writes `labels/panels.json`.
- `build_gdu1040.py`: full GDU 1040 assembly (bezel pieces + one-piece outsource body, LCD clips, key caps, knobs, electronics tray, purchased-part references).
- `build_pfd.py`: PFD-1 GDU 1040 bezel with LCD, PCBs, encoders and controller placeholders (hidden by default).
- `build_standby.py`: SB-1 standby gauges and SB-2 dimming block.
- `gen_label_art.py`: turns `panels.json` into the SVG label artwork.
- `tools.py`, `run_all.py`: rebuild, fold collision sweep, cut list.
- `*_revA..D.py`: earlier revisions, kept for history.
