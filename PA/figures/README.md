# PA-Grafiken

Die PA verwendet die bereits erzeugten, zentral archivierten Grafiken aus
`../docs/grafiken`. Die PDF-Dateien werden nicht in diesen Ordner kopiert,
sondern über `\graphicspath` in `main.tex` aus der zentralen Quelle eingebunden.
So werden die Grafiken nicht doppelt gepflegt. Für die Arbeit sind insbesondere
relevant:

- `matrix_overview_table.pdf`: PSNR, SSIM und LPIPS in den Gruppen 2 FPS, 5 FPS
  und Average;
- `matrix_status_table.pdf`: erfolgreich/unvollständig;
- `matrix_time_quality_table.pdf`: sekundäre Effizienz-/Screening-Auswertung;
- `matrix_psnr_table.pdf`, `matrix_ssim_table.pdf`, `matrix_lpips_table.pdf`:
  Detailansichten.
