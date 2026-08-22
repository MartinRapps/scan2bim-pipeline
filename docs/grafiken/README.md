# Matrixgrafiken

Die Grafikablage ist nach Status und Modellstufe getrennt:

- `verwendet_verbessert/`: weiterhin verwendete Statusgrafiken und historische
  gemeinsame Matrixquellen;
- `matrix_repeat_2026-08-17/`: aktuelle vollständige Repeat-Grafiken aus der
  30-Lauf-Datengrundlage;
- `neu_metriken_2026-08-12/`: historischer, bereinigter Grafikstand;
- `archiv_alt_2026-08-12/`: ältere, nicht mehr in Exposé oder PA eingebundene
  Grafikstände.
- `datengrundlage/`: zentrale, verdichtete JSON-/CSV-Datengrundlage für die
  metrischen Grafiken; diese Dateien können unabhängig von den historischen
  Run-Archiven aufbewahrt werden.

## Verbindliche neue Quellen

- STS: `matrix_repeat_2026-08-17/sts_masked_overview.pdf` aus
  `sts_masked.json`;
- SuGaR-Coarse: `matrix_repeat_2026-08-17/sugar_coarse_masked_overview.pdf`
  aus `sugar_coarse_masked.json`;
- Streuung: `matrix_repeat_2026-08-17/*_per_frame_boxplots.pdf` aus dem
  `per_frame`-Feld;
- gepaarte Stage-Differenz:
  `matrix_repeat_2026-08-17/sugar_coarse_vs_sts_delta.pdf`;
- Laufzeitdiagnostik: `matrix_repeat_2026-08-17/metric_vs_runtime.pdf`.

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
Die STS-Boxplots und -Übersichten verwenden dabei SR-blau,
OPENCV-orange und PINHOLE-grau.

Für den STS-Auflösungsvergleich werden nur Kamera-/FPS-Gruppen mit allen drei
Auflösungen dargestellt. Ein isolierter historischer Lauf ohne QHD- und
Low-Partner bleibt als Rohprovenienz erhalten, wird aber nicht als
Auflösungsvergleich geplottet. Die Laufzeitgrafik besitzt eine gemeinsame
Legende für alle drei Metriken; sie kodiert Stufe, FPS-Intensität und
Auflösungsform explizit.
