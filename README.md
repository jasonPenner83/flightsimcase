# Folding MSFS 2024 Cockpit Case

A carry-size folding home cockpit for MSFS 2024. It starts with a full-scale Cessna 172 G1000 panel, with TBM 900 / PC-12 later. The frame is Vevor 2020/2040 aluminum extrusion with 3D-printed (Bambu A1) modules.

- **Current design:** rev E (locked). Three panels (left wing 310, center 350, right wing 350 mm) on side-mounted piano hinges, with a 98 mm right spacer. It folds to 379 x 416 x 289 mm and is sealed when closed.
- **Module standard and cut list:** [Module_Standard_and_Cut_List.md](Module_Standard_and_Cut_List.md)
- **Bill of materials:** [BOM.md](BOM.md)
- **Print files:** [prints/](prints/) (SW-1 switch row, CL-1 dimmers, CL-2 yoke panel)
- **Renders:** [renders/](renders/) (older revisions in subfolders)

## Fusion model
The master model lives in Autodesk Fusion: project "Flight Sim Case", design "Folding Cockpit Case".
The scripts in [fusion/](fusion/) rebuild it through the Fusion API:
- `build_case.py`: frame, hinges, outriggers. Dimensions are in the `P` dict at the top.
- `build_switch_panel.py`: faceplate modules, built as real sketch/extrude features.
- `tools.py`, `run_all.py`: rebuild, fold collision sweep, cut list.
- `*_revA..D.py`: earlier revisions, kept for history.
