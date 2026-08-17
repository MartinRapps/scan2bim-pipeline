# Matrixgrafiken

Die Grafikablage ist nach Status und Modellstufe getrennt:

- `verwendet_verbessert/`: weiterhin verwendete Statusgrafiken und historische
  gemeinsame Matrixquellen;
- `neu_metriken_2026-08-12/`: korrigierte, neu erzeugte Diagramme aus den
  stufenspezifischen JSON-Dateien;
- `archiv_alt_2026-08-12/`: ältere, nicht mehr in Exposé oder PA eingebundene
  Grafikstände.
- `datengrundlage/`: zentrale, verdichtete JSON-/CSV-Datengrundlage für die
  metrischen Grafiken; diese Dateien können unabhängig von den historischen
  Run-Archiven aufbewahrt werden.

## Verbindliche neue Quellen

- STS: `neu_metriken_2026-08-12/sts_masked_overview.pdf` aus
  `sts_masked.json`;
- SuGaR-Coarse: `neu_metriken_2026-08-12/sugar_coarse_masked_overview.pdf`
  aus `sugar_coarse_masked.json`;
- Streuung: `*_per_frame_boxplots.pdf` aus dem `per_frame`-Feld;
- gepaarte Stage-Differenz: `sugar_coarse_vs_sts_delta.pdf`;
- Laufzeitdiagnostik: `metric_vs_runtime.pdf`.

Die zentralen Grafikdaten liegen unter `docs/grafiken/datengrundlage/`.
`matrix_graphics_summary.json` dokumentiert Quellen, Metrikumfang und
Plotregeln; die CSV-Dateien enthalten Lauf-, Einzelansichts- und
Delta-Werte.

`middle` wird upstream für Coverage und die Auswahl nichtleerer Eval-Frames
verwendet. Die eigentliche Bildmetrikaggregation ist mit `default` markiert.
Die Bildmetriken bewerten gerenderte Gaussian-Repräsentationen und sind kein
Ersatz für Mesh- oder Centerline-Geometriemetriken.

In den Boxplots liegen die `per_frame`-Punkte auf der jeweiligen x-Kategorie
und werden nur leicht horizontal verteilt. Die Laufzeitgrafik verwendet eine
feste x-Achse von 15 bis 40 Minuten; helle Farben kodieren 2/5 FPS und
Punkt/Quadrat/Dreieck 720p/QHD/Low. Kameraangaben stehen in den x-Labels; eine
separate SR-/OPENCV-Legende wird nicht verwendet.
