# Gemittelte Matrix-Grafiken (2026-08-17)

Diese Serie mittelt die historischen Matrixdaten (`matrix_full_pipe`,
`matrix_rest`, `matrix_sugar_followup_12`) und die 30 Repeat-Läufe
(`matrix_repeat_20260812`) je Kameramodell, FPS, Auflösung und Modellstufe.

- STS-Übersicht und STS-Boxplots: vollständige Original-GS-Route-A-Läufe.
- SuGaR-Coarse-Übersicht und Boxplots: ausschließlich `sugar_coarse_masked.json`.
- Die Übersichten verwenden arithmetische Mittelwerte je Konfiguration.
- Die Boxplots poolen die `per_frame`-Werte aller zugehörigen historischen und Repeat-Läufe.
- Die Boxplots verwenden keine Kamerafarbcodierung. Kameramodell, FPS und Auflösung stehen eindeutig in den x-Achsenbeschriftungen; dadurch bleibt die Farbcodierung frei von Mehrdeutigkeiten.
- Beide Boxplotserien verwenden dieselben festen y-Achsen: PSNR 10–40 dB, SSIM 0,1–1,0 und LPIPS 0–0,4.
- Delta: gemittelte SuGaR-Coarse-minus-STS-Renderingdifferenz.
- Laufzeit: Mittelwert der archivierten Laufzeiten.
- Alle Werte sind objektmaskierte Renderingmetriken und kein Geometrienachweis.

Die sechs PDFs werden aus den `.tex`-Quellen im Ordner erzeugt. Die zentrale
Datengrundlage liegt in `Datengrundlage/`; `mean_summary.json` dokumentiert die
Quellen und die Aggregationsregel.
