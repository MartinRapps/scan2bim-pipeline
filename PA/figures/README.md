# PA-Grafiken

Die PA verwendet die zentral archivierten Grafiken aus
`../docs/grafiken/verwendet_verbessert` und
`../docs/grafiken/neu_metriken_2026-08-12`. Die PDF-Dateien werden nicht in
diesen Ordner kopiert, sondern über `\graphicspath` in `main.tex` aus den
zentralen Quellen eingebunden.
So werden die Grafiken nicht doppelt gepflegt. Für die Arbeit sind insbesondere
relevant:

- `neu_metriken_2026-08-12/sts_masked_overview.pdf`: getrennte STS-7000-
  Bildmetriken;
- `neu_metriken_2026-08-12/sugar_coarse_masked_overview.pdf`: ausschließlich
  SuGaR-Coarse-9000-Bildmetriken;
- `neu_metriken_2026-08-12/*boxplots.pdf`: Einzelansichtsstreuung;
- `neu_metriken_2026-08-12/sugar_coarse_vs_sts_delta.pdf`: gepaarter
  Rendervergleich;
- Die Matrixstatuswerte stehen weiterhin als Tabelle im Matrixanhang; die
  separate Statusgrafik ist bewusst nicht Bestandteil der PA.
