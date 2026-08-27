# followup_12 — SuGaR-Coarse-Folgematrix (12 Läufe, 10.08.2026)

Inhalt: vollständige `sugar_output`-Ordner der zwölf Läufe der Folgematrix
(`matrix_matrix_sugar_followup_12_<fps>_<aufloesung>_<kameramodell>_sugar`),
je Lauf die interne SuGaR-Ausgabe der Refined-Mesh-Extraktion
(`refined_ply/05_3dgs/sugarfine_…_decim200000_….ply`, ~41 MB je Datei).

## Wichtige Einordnung (kein Widerspruch zur PA)

- Die in der PA ausgewertete Folgematrix bewertet **ausschließlich die
  Coarse-Stufe**: `sugar_refined_masked.json` trägt in allen zwölf Läufen den
  Status `skipped` mit der Ursache „no refined.ply exported" (PA 7.8,
  Anhang B). Der dafür vorgesehene Pipeline-Export (`refined.ply` als
  Grundlage des Refined-Renderings) wurde nicht ausgelöst.
- Die hier enthaltenen `sugarfine_…ply`-Dateien sind die **internen**
  SuGaR-Ausgaben der Mesh-Extraktion (Stand 10.08.2026, auto-generierter
  Dateiname). Sie wurden **nicht** gerendert oder mit Metriken belegt und
  stellen daher keinen Widerspruch zur Aussage „kein `refined.ply`
  exportiert" dar.

## Nachweise

- Metrik-/Statusnachweise der zwölf Läufe: CSV-Quellen unter
  `03_Grafiken/matrix_repeat_2026-08-17/`
  (`sugar_coarse_masked_summary.csv`, `sugar_coarse_masked_per_frame.csv`)
  sowie die PA-Kapitel 7.8 und Anhang B (Tabelle 10, Auswertungsregeln).
- Die Original-Batch-Archive (`data/10_runs/matrix_sugar_followup_12/`)
  liegen komprimiert im externen Backup (siehe `ABGABE_Index.md`).

Prüfsummen: `SHA256SUMS.txt` (je Unterordner-Datei).
