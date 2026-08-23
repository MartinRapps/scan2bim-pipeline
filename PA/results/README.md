# Ergebnisquellen

Die PA kopiert keine großen Trainings- oder Renderarchive. Die vollständigen
Experimente liegen unter:

- `../../data/10_runs/matrix_full_pipe/`: historische sechs A-Tests;
- `../../data/10_runs/matrix_rest/`: 18 Folgeexperimente mit PINHOLE, OPENCV und
  der fehlgeschlagenen SuGaR-Coarse-Renderroute;
- `../../data/10_runs/matrix_sugar_followup_12/`: abgeschlossene zwölf SuGaR-
  Coarse-Folgeläufe mit SIMPLE_RADIAL und OPENCV bei 2/5 FPS und drei
  Auflösungen;
- `../../data/10_runs/matrix_repeat_20260812/`: vollständiger Repeat-Batch;
  die zugehörige verdichtete Grafikquelle umfasst 30 erfolgreiche Läufe;
- `../../data/10_runs/Alurohr_THWS_*`: sechs archivierte Autopilot-Volläufe
  (18./20.08.2026, `AUTOPILOT: true`, Status SUCCESS);
- `../../data/10_runs/matrix_qualitaetsvergleich_20260818`: Qualitätsvergleichs-
  batch (3 Kameramodelle × Route A × 3 Auflösungen + SuGaR-Arme, failed=0,
  Golden-Run-Quelle für den Arm 5fps/720p/opencv_a);
- `../../docs/grafiken/verwendet_verbessert/`: weiterhin verwendete
  Statusgrafiken und historische gemeinsame CSV-/Methodikquellen;
- `../../docs/grafiken/matrix_repeat_2026-08-17/`: aktuelle, getrennte
  STS-/SuGaR-Coarse-Übersichten, Einzelansichts-Boxplots, Delta- und
  Laufzeitgrafik. Die SuGaR-Coarse-Auswertung verwendet ausschließlich
  `metrics/sugar_coarse_masked.json`; übersprungene
  `sugar_refined_masked.json`-Dateien werden nicht als Refinement-Ergebnisse
  ausgegeben;
- `../../docs/grafiken/archiv_alt_2026-08-12/`: ältere, nicht mehr eingebundene
  Grafikstände.

**Ablagestand 23.08.2026:** `data/10_runs/` ist im Repository nicht vorhanden
(laufzeiterzeugt/gitignored). Die Archive liegen derzeit extern (Arbeits-VM
beziehungsweise V-Laufwerk); vor der Abgabe sind Prüfsummen zu dokumentieren,
siehe `appendices/appendix_anlagenindex.tex` in der Arbeitsfassung.

Die Kernkapitel verwenden nur zusammengefasste Werte. Einzelne Logs und
COLMAP-Benchmarkdateien werden in den optionalen Anhängen referenziert. Die
Empfehlung, welche Runbestandteile dauerhaft beziehungsweise nur für Golden
Runs gespeichert werden sollten, steht in
`../Archivierungsempfehlung_Matrix.md`.
