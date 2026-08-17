# Empfehlung zur Archivierung der Matrixläufe

## Kurzantwort

Die vollständigen `live/`-Archive müssen nicht dauerhaft für jeden Matrixlauf
aufbewahrt werden. Ein aktueller SuGaR-Coarse-Run benötigt ungefähr 3–4 GB; die
bestehenden drei großen Matrixarchive belegen zusammen bereits ungefähr 119 GB.
Der größte Anteil entfällt auf wiederholte STS-/COLMAP-Arbeitsdaten, Datenbanken,
Frames und Checkpoints, nicht auf die eigentlichen Ergebnistabellen.

Die richtige Trennung ist:

1. **kleiner Pflichtnachweis für jeden Lauf**;
2. **vollständiges Golden-Run-Archiv für wenige ausgewählte Läufe**;
3. **gemeinsame Grafik- und Auswertungsquellen für die gesamte Matrix**.

Vor dem finalen Backup sollten die bestehenden Archive nicht gelöscht werden.
Sie können nach einer geprüften Kompaktarchivierung und einem externen Backup
bereinigt werden.

## 1. Pflichtnachweis für jeden Matrixlauf

Diese Dateien sind klein und sollten für jeden Lauf erhalten bleiben:

- `manifest.json` – Status, Variante, Kameramodell und Auswertungsumfang;
- `parameters.json` – FPS, Auflösung, SIFT-, STS- und Meshparameter;
- `run.md` und vorzugsweise `pipeline_run/run.md` – Einstellungen, Dauer,
  Git-/SuGaR-Commit und Stufenstatus;
- `metrics/sts_masked.json` – STS-Referenz, sofern der Lauf STS gerendert hat;
- `metrics/sugar_coarse_masked.json` – echte SuGaR-Coarse-Metrik;
- `metrics/sugar_refined_masked.json` – auch dann behalten, wenn der Status
  `skipped` lautet; so ist dokumentiert, dass kein Refinement-Ply exportiert
  wurde;
- `evaluation/eval_frames.txt` – unveränderlicher Evaluationssplit;
- `masks/ideal/mask_coverage_report.json` – Maskenabdeckung;
- `mesh_mode.txt` beziehungsweise eine vergleichbare Routendatei;
- die kleine gemeinsame Grafikquelle
  `docs/grafiken/verwendet_verbessert/matrix_thesis_data.csv` und deren
  Methodikbericht;
- die neue stufenspezifische Grafik- und Einzelansichtsquelle unter
  `docs/grafiken/neu_metriken_2026-08-12/`.

Für diese Dateien reichen normalerweise wenige Kilobyte pro Lauf. Sie erlauben
Status-, Parameter- und Metrikvergleiche, ohne die gesamten Trainingsdaten zu
duplizieren.

## 2. Logs

- **Fehlgeschlagene Läufe:** vollständigen `run.log` und `matrix.log`
  behalten. Gerade bei den historischen Fällen sind sie der Nachweis für
  Ursachen wie leere Eval-Masken, stdin-Verbrauch und SuGaR-Importfehler.
- **Erfolgreiche Routine-Läufe:** `run.md` beziehungsweise
  `pipeline_run/run.md` reicht für die PA. Einen vollständigen Log nur für
  ausgewählte Referenzläufe aufbewahren.
- **Golden Runs:** vollständigen Log, Parameterdatei, Commitnachweis und
  Prüfsummen behalten.

Die Logs sind im Verhältnis zu den Checkpoints klein und für die Fehlerchronik
wissenschaftlich wertvoll. Sie sollten daher nicht pauschal gelöscht werden.

## 3. Vollständige Archive

Ein vollständiges Archiv mit Frames, idealer Szene, Masken, Kameras, Splats,
Mesh und Centerline ist für wenige repräsentative Läufe sinnvoll:

### Empfohlenes Minimum

1. **Golden Run der Produktionsroute:**
   `SIMPLE_RADIAL` + `original_gs` + 720p + 5 FPS;
2. **direkter SuGaR-Coarse-Vergleich:**
   `SIMPLE_RADIAL` + `sugar_coarse` + 720p + 5 FPS;
3. **eine Kameramodell-Ablation:**
   `OPENCV` oder `PINHOLE` + `original_gs` + 720p + 5 FPS;
4. **A/B/C/D-Meshablation:** die vier bereits für die Geometrieentscheidung
   verwendeten Coarse-Meshes;
5. **ein repräsentativer Fehlversuch:** Log und kompakter Status, aber kein
   vollständiges Trainingsarchiv.

Damit bleiben die Produktionsentscheidung, der SuGaR-Vergleich, eine
Kameramodellabweichung und die Robustheitsgeschichte nachvollziehbar.

### Was bei einem Golden Run vollständig bleiben sollte

- verwendete Arbeitsframes beziehungsweise mindestens die für den festen
  Eval-Split relevanten Frames;
- ideale Bilder und ideale Masken für die Evaluationsansichten;
- originales und ideales COLMAP-Sparse-Modell;
- STS-Checkpoint beziehungsweise der für den Vergleich notwendige PLY;
- SuGaR-Coarse-Checkpoint `9000.pt`, wenn der Coarse-Lauf reproduziert werden
  soll;
- gerenderte Eval-Splats, Ground-Truth-Ansichten und Evaluationsmasken;
- Coarse-PLY/OBJ, Centerline, B-Spline und GeoJSON;
- vollständige Logs, Manifeste, Parameter und Prüfsummen.

Die komplette COLMAP-Datenbank, alle temporären Arbeitsframes und sämtliche
Zwischenkopien sind für einen reinen Ergebnisvergleich nicht zwingend. Sie
werden nur benötigt, wenn der Lauf von ganz vorne ohne Neuberechnung der
betreffenden Stufe reproduziert werden soll.

## 4. Was nicht für jeden Lauf nötig ist

Nicht jeder Run benötigt dauerhaft:

- die komplette `live/sts/`-Struktur mit allen Checkpoints und Datenbanken;
- `live/colmap/database.db`, wenn das Sparse-Modell und die Metrikdaten
  erhalten bleiben;
- alle Arbeitsframes und alle Masken, wenn nur die aggregierten Ergebnisse
  verglichen werden sollen;
- jedes temporäre Arbeitsvideo `input_*.mp4`;
- doppelte STS-/SuGaR-Kompatibilitätskopien;
- vollständige Logs erfolgreicher, unauffälliger Läufe;
- alle Renderbilder außerhalb des festen Eval-Splits.

Die PLY-/OBJ-Meshes und Centerlines sind im Vergleich zu den Trainingsdaten
klein. Für die A/B/C/D-Entscheidung und die ausgewählten Referenzläufe sollten
sie vollständig erhalten bleiben.

## 5. Sind Splats, Mesh, Centerline und Panels ausreichend?

Für eine Präsentation sind Splats, Mesh, Centerline und Panels fast ausreichend.
Für wissenschaftliche Reproduzierbarkeit fehlen dann aber die kleinen
Kontextdateien. Die Minimalergänzung lautet:

- Splats oder gerenderte Eval-Splats;
- Coarse-PLY/OBJ und Centerline für ausgewählte Vergleichsläufe;
- Panels/Grafik-PDFs und die erzeugende CSV;
- `manifest.json`, `parameters.json`, `run.md`;
- `eval_frames.txt`, Coverage-Report und Metrik-JSON;
- Git-/SuGaR-Commit und ein Hash-/Versionsnachweis.

Die vollständigen Splats/Checkpoints müssen nicht für alle Varianten dauerhaft
gespeichert werden. Die aggregierten Metrikdateien allein beweisen allerdings
nicht mehr, dass später mit identischen Renderings erneut ausgewertet werden
kann. Deshalb sollten gerenderte Eval-Splats wenigstens für Golden Runs und
für die direkten STS-vs.-SuGaR-Vergleiche erhalten bleiben.

## 6. Empfehlung für einen weiteren vollständigen Matrixlauf

Ein weiterer Lauf ist sinnvoll, wenn er als **Wiederholungs-/Stabilitätsprüfung**
verstanden wird. Er sollte eine neue Batch-ID erhalten. Vor dem Lauf müssen
Parent-Gitlink, lokaler SuGaR-Checkout, Docker-`SUGAR_REF`, Hardware und
Parameter eingefroren werden.

Während des Laufs:

1. pro Variante nur den kleinen Pflichtnachweis sicher archivieren;
2. Fehlerruns mit vollständigem Log behalten;
3. pro Kameramodell und Meshroute zunächst nur die Metrik-JSONs, Coverage,
   Eval-Split und Render-Evalbilder sammeln;
4. nach Abschluss die Werte mit der bestehenden Matrix vergleichen;
5. nur bei relevanten Abweichungen oder für die besten/schlechtesten Fälle das
   vollständige Checkpoint-/Mesharchiv dauerhaft übernehmen.

Eine Abweichung ist nicht automatisch ein Fehler: STS- und SuGaR-Optimierung,
Surface-Sampling, GPU-/Bibliotheksversionen und einzelne datenabhängige
Verarbeitungsschritte können trotz gleicher nominaler Parameter leicht andere
Werte erzeugen. Für die Beurteilung müssen daher zuerst Commitstand,
Eval-Split, Maskenabdeckung, Framezahl und Seed identisch sein.

## 7. Konkrete Aufbewahrung für die aktuelle PA

Für die aktuelle PA sollten erhalten bleiben:

- die vollständige `matrix_sugar_followup_12`-Metrik-/Statusdokumentation;
- die sechs neuen SuGaR-Coarse-Grafiken und die kombinierte Overview;
- die aktuelle CSV- und Methodikdatei;
- die A/B/C/D-Coarse-Meshes und deren Distanzwerte;
- ein Route-A-Golden-Run und ein gleich konfigurierter
  SuGaR-Coarse-Vergleichslauf;
- die historischen Fehlermeldungen als Logs oder kompakte Fehlerberichte.

Die übrigen großen `live/`-Doppelungen können nach einem externen Backup und
nach Prüfung der später benötigten Golden Runs in eine Kompaktarchivierung
überführt werden. Eine automatische Löschung sollte erst nach einer
Hash-/Manifestprüfung erfolgen.
