# Golden-Run-Arm 5 FPS / 720p / opencv_a (Route A)

Vollständiger Archivlauf aus `matrix_qualitaetsvergleich_20260818` (Stand
18.08.2026, Git-Commit siehe `run.md`/`pipeline_run/run.md`): Produktions-
konfiguration OPENCV / 5 FPS / 720p / Route A (original_gs), Status success.

- `manifest.json`, `parameters.json` — Konfiguration und Status
- `run.md`, `run.log`, `matrix.log` — Protokolle
- `live/` — Arbeitsverzeichnis des Laufs:
  - `colmap/` Sparse-Modell + ideale Szene
  - `sts/` STS-Checkpoints (`output/point_cloud/iteration_7000/…`),
    Eval-Split, `masked_sugar_input/` (SuGaR-Eingang)
  - `mesh/` Route-A-Coarse-Mesh, `centerline/` + `gis/` Endprodukte
    (Centerline: `centerline_local_raw.csv` = 85 Punkte,
    `centerline_local.csv` = 372 B-Spline-Punkte)
  - `masks_ideal/` gewarpte ideale Masken + Coverage-Report
- `splats/` gerenderte Test-Views, `metrics/` objektmaskierte Metriken
  (`sts_masked.json`, 30 Eval-Ansichten), `evaluation/eval_frames.txt`
- `masks/` Roh- und ideale Masken, `input_5fps.mp4` Arbeitsvideo
