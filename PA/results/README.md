# Ergebnisquellen

Die PA kopiert keine großen Trainings- oder Renderarchive. Die vollständigen
Experimente liegen unter:

- `../../data/10_runs/matrix_full_pipe/`: historische sechs A-Tests;
- `../../data/10_runs/matrix_rest/`: 18 Folgeexperimente mit PINHOLE, OPENCV und
  der fehlgeschlagenen SuGaR-Coarse-Renderroute;
- `../../data/10_runs/matrix_sugar_followup_12/`: abgeschlossene zwölf SuGaR-
  Coarse-Folgeläufe mit SIMPLE_RADIAL und OPENCV bei 2/5 FPS und drei
  Auflösungen;
- `../../docs/grafiken/`: zusammengeführte CSV, Status-, Metrik- und
  Zeit/Qualitätsauswertung für STS und SuGaR-Coarse. Die SuGaR-Coarse-
  Auswertung verwendet ausschließlich `metrics/sugar_coarse_masked.json`;
  die übersprungenen `sugar_refined_masked.json`-Dateien werden nicht als
  Refinement-Ergebnisse ausgegeben. Die kombinierte Overview ist
  `matrix_combined_overview_table.pdf`.

Die Kernkapitel verwenden nur zusammengefasste Werte. Einzelne Logs und
COLMAP-Benchmarkdateien werden in den optionalen Anhängen referenziert. Die
Empfehlung, welche Runbestandteile dauerhaft beziehungsweise nur für Golden
Runs gespeichert werden sollten, steht in
`../Archivierungsempfehlung_Matrix.md`.
