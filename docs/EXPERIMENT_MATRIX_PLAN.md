# Plan: Kameramodell-, Splat- und Maskenvergleich

Stand: 06.08.2026

## 1. Entscheidung

Der produktive Rohvideo-Workflow wird **nicht** vor COLMAP entzerrt, solange keine
unabhängige Kamerakalibrierung vorliegt. Der wissenschaftlich sauberste Ablauf
für den aktuellen Datensatz ist:

```text
Rohvideo
  -> Rohframes
  -> COLMAP SIMPLE_RADIAL auf Rohframes
  -> originales COLMAP-Modell für GCP/SfM archivieren
  -> COLMAP image_undistorter
  -> ideale PINHOLE-Szene für STS
  -> Rohmasken mit derselben COLMAP-Abbildung in die ideale Bilddomäne warpen
  -> STS und SuGaR auf idealen Bildern + idealen Masken
```

Eine Entzerrung direkt nach der Frame-Extraktion wäre nur dann korrekt, wenn die
Verzeichnung bereits durch eine **unabhängige** Kalibrierung bekannt ist. Mit den
aktuellen Daten kennt man die Verzeichnung erst nach dem ersten COLMAP-SfM-Lauf.
Eine Vorab-Entzerrung mit später aus COLMAP geschätzten Parametern wäre daher
zirkulär.

## 2. Aktueller Ist-Zustand und festgestellter Fehler

`src/scripts/run_sfm.sh` schätzt mit `SIMPLE_RADIAL` aktuell die Verzeichnung auf
den Rohframes. Danach erzeugt es unter `data/04_sfm/undistorted/` eine ideale
Szene. Die vorhandenen Dateien bestätigen das:

- `data/04_sfm/sparse_txt/cameras.txt`: `SIMPLE_RADIAL`
- `data/04_sfm/undistorted/sparse_txt/cameras.txt`: `PINHOLE`

`src/python/prep_sts_scene.py` verwendet anschließend die idealen Bilder und das
ideale Sparse-Modell. Die SAM3-Masken wurden bisher jedoch auf den Rohframes unter
`data/02_frames` erzeugt und nur per Dateiname beziehungsweise später per
Nearest-Neighbor-Resize an die STS-Bilder angepasst. Eine geometrische
Entzerrung der Masken findet aktuell nicht statt. Die aktuelle ideale Szene ist
beispielsweise 1284 x 720 groß, während der Rohframe 1280 x 720 groß ist.

Damit existiert derzeit tatsächlich ein kleiner bis potenziell relevanter
Bild-/Masken-Domänenfehler. Dieser muss vor einer aussagekräftigen Splat-Evaluation
behoben werden.

## 3. Empfohlene Maskenlösung

### Bevorzugte Lösung: Rohmasken nach COLMAP warpen

1. SAM3 bleibt zunächst auf den Rohframes. Dadurch bleiben Video-Tracking,
   Framenummern und die bisherige Maskenqualität unverändert.
2. Nach `image_undistorter` werden die Masken mit den Original- und Ideal-
   `cameras.txt`-Parametern in die ideale Bilddomäne transformiert.
3. Die drei Stufen `default`, `middle` und `small` werden mit
   `cv2.remap(..., INTER_NEAREST)` gewarpt.
4. Die idealen Masken erhalten dieselben Bildnamen und dieselbe Auflösung wie
   `data/04_sfm/undistorted/images`.
5. STS, SuGaR und die Review-Ausgabe verwenden ausschließlich diese idealen
   Masken zusammen mit den idealen Bildern.
6. Die Rohmasken bleiben separat als Diagnose erhalten.

Dafür wird ein neues Werkzeug benötigt, beispielsweise
`src/python/warp_masks_to_undistorted.py`. Es muss `SIMPLE_RADIAL` und `OPENCV`
unterstützen, mehrere COLMAP-Kameras korrekt behandeln und einen Bericht mit
Anzahl, Auflösung, nichtleeren Masken und Bounding-Boxen schreiben.

Bei `PINHOLE`/`SIMPLE_PINHOLE` wird keine Warping-Stufe ausgeführt; die Masken
werden nur in den jeweiligen Run-Arbeitsbereich kopiert, weil die Eingabebilder
bereits als ideal angenommen werden.

### Alternative Lösung

SAM3 könnte erst nach COLMAP direkt auf den idealen Bildern ausgeführt werden.
Das wäre konzeptionell ebenfalls sauber, erfordert aber einen stabilen
SAM3-Image-Sequence-/Video-Workflow für die entzerrten Einzelbilder und würde
den aktuellen temporalen Videoablauf stärker verändern. Für den ersten
wissenschaftlichen Vergleich ist das Mask-Warping deshalb die kleinere und
besser kontrollierbare Änderung.

## 4. GCP und Bilddomäne

Das GCP-Picking bleibt bewusst im Originalraum:

- UI-Bilder: Rohframes aus `data/02_frames`
- COLMAP-Modell: originales `data/04_sfm/sparse_txt`
- GCP-Triangulation: originales Modell
- STS/SuGaR: ideale `PINHOLE`-Szene und gewarpte Masken

Das ist kein Widerspruch. GCP und SfM werden im Modellraum ausgewertet, in dem
COLMAP tatsächlich die Rohbilder rekonstruiert hat. Die nachgelagerte ideale
Szene ist ein abgeleiteter Arbeitsraum für STS und die Gaussian-Optimierung.

## 5. Kameramodell-Testreihe

### Baseline

`SIMPLE_RADIAL` auf Rohframes, anschließend `image_undistorter` und STS auf der
idealen `PINHOLE`-Szene. Das ist der empfohlene Produktionspfad.

### Direkte PINHOLE-Ablation

`PINHOLE` direkt auf Rohframes. Die Bilder werden dann nicht entzerrt. Dieser
Lauf ist ein Test der starken Annahme, dass die Rohbilder bereits ideal sind;
er ist **nicht** die Bestätigung der bestehenden `SIMPLE_RADIAL -> PINHOLE`-
Konvertierung.

### OPENCV-Ablation

`OPENCV` auf Rohframes, anschließend ebenfalls `image_undistorter`. Dieser Lauf
ist der methodisch sauberere Vergleich für ein komplexeres Verzeichnungsmodell,
insbesondere wenn tangentiale Verzeichnung relevant ist.

Für direkte Metrikvergleiche müssen alle Läufe in eine gemeinsame
Evaluationsdomäne gebracht werden. Für die Baseline und OPENCV ist das die
jeweilige ideale Szene. Für den direkten Roh-PINHOLE-Lauf gibt es zwei Optionen:

1. native Werte separat als `raw_pinhole_native` berichten; oder
2. Renderings und Ground Truth mit einer dokumentierten gemeinsamen
   Referenzabbildung in die Baseline-Ideal-Domäne warpen.

Die zweite Option ist für einen direkten wissenschaftlichen Vergleich besser.
Native PSNR-Werte aus unterschiedlichen Pixelkoordinatensystemen dürfen nicht
ungekennzeichnet in einer Tabelle nebeneinander interpretiert werden.

## 6. Fester Evaluationssplit

Vor STS wird pro Experiment ein unveränderlicher Split erzeugt:

```text
data/10_runs/<batch>/<experiment>/evaluation/eval_frames.txt
```

Der Split enthält Bildnamen, nicht nur numerische Indizes. Alle folgenden
Modelle desselben Experiments verwenden exakt diese Liste:

- STS-Checkpoint
- SuGaR-Coarse-Checkpoint
- SuGaR-Refinement, falls der Legacy-Vergleich aktiviert ist
- alle Render- und Metrikläufe

Der Split darf nicht einmal über `prep_sts_scene.py` mit jedem zehnten und ein
zweites Mal über SuGaR mit jedem achten Bild neu erzeugt werden. `train.txt`,
`test.txt` und SuGaRs `eval_split_interval` müssen auf eine gemeinsame
`eval_frames.txt`-Quelle umgestellt oder für die wissenschaftliche Evaluation
explizit überschrieben werden.

Die Metriken werden jeweils doppelt berechnet:

- **full-frame:** zeigt die gesamte Renderqualität, kann aber vom Hintergrund
  dominiert werden;
- **maskiert:** bewertet die eigentliche Kabel-/Rohrregion und ist für die
  Objektentscheidung wichtiger.

## 7. STS gegen SuGaR vergleichen?

Ja, aber mit der richtigen Interpretation:

- STS-7000 ist die ursprüngliche Gaussian-Splat-Baseline.
- SuGaR-Coarse-9000 ist ein veränderter Gaussian-Splat-Checkpoint.
- SuGaR-Refinement ist ein weiterer, an ein Triangle-Mesh gebundener
  Gaussian-Splat-Checkpoint.
- Variante A erzeugt **keinen neuen SuGaR-Splat**. A verwendet den STS-Splat
  direkt und verändert nur die nachgelagerte Meshgewinnung.

Daher ist der sinnvolle Splatvergleich:

```text
STS-7000  vs.  SuGaR-Coarse-9000  vs.  SuGaR-Refined
```

auf exakt denselben idealen Testbildern und mit denselben Masken. Für A gilt
STS-7000 als Gaussian-Baseline; A wird zusätzlich über sein Coarse-Mesh und
später über die Centerline bewertet.

Die Metriken beantworten dabei die Renderfrage, nicht die Meshfrage. Ein höheres
PSNR oder SSIM beweist keine bessere Oberfläche. Für die Mesh-/Centerline-
Entscheidung bleiben später Vollständigkeit, Hausdorff-Distanz, Centerline-RMSE
und GNSS-Fehler maßgeblich.

## 8. Automatisch zu erfassende Ergebnisse

Jeder Experimentordner erhält mindestens:

```text
manifest.json
run.log
run.md
parameters.json
git.txt
colmap/
  original_sparse/
  sparse_txt/
  cameras.txt
  images.txt
  points3D.ply
  reprojection_stats.json
images/
  raw_manifest.json
  ideal_camera_manifest.json
masks/
  raw/
  ideal/
  review_raw/
  review_ideal/
  mask_report.json
sts/
  input_filtered.ply
  checkpoint/
  renders/
  metrics.json
sugar/
  coarse_checkpoint.pt
  refined_checkpoint.pt
  coarse_mesh.ply
  refined_or_compatibility.obj
  renders/
  metrics.json
mesh/
  coarse.ply
  refined_or_compatibility.obj
postprocess/
  centerline_local.csv
  centerline_local_raw.csv
  *.geojson
cleanup.json
```

Die Kernmetriken in `metrics.json` und `run.md` lauten:

- `PSNR_full`, `SSIM_full`, `LPIPS_full`
- `PSNR_masked`, `SSIM_masked`, `LPIPS_masked`
- `evaluation_frame_count`
- `evaluation_domain` (`ideal_pinhole` oder `raw_pinhole_native`)
- `model_stage` (`sts`, `sugar_coarse`, `sugar_refined`)
- Gaussian-Anzahl, Checkpointgröße, Renderzeit und Peak-VRAM

Die vorhandene SuGaR-Datei `gaussian_splatting/metrics.py` kann die eigentliche
PSNR-/SSIM-/LPIPS-Berechnung teilweise wiederverwenden, wird aber um einen
maskierten Modus, einen festen Split und einen maschinenlesbaren Exit-Code
ergänzt. `run_logging.sh` übernimmt danach die Ergebnisse automatisch in
`run.md` und `run.log`.

## 9. Automatisierter Matrix-Runner

Vorgesehen ist ein neuer Runner, beispielsweise
`tools/run_experiment_matrix.sh`, mit einer deklarativen JSON- oder YAML-Datei:

```yaml
experiments:
  - id: sr_a
    camera_model: SIMPLE_RADIAL
    mesh_mode: original_gs
    sts_iterations: 7000
  - id: sr_sugar_coarse
    camera_model: SIMPLE_RADIAL
    mesh_mode: sugar_coarse
    sts_iterations: 7000
    coarse_iterations: 9000
  - id: pinhole_a
    camera_model: PINHOLE
    mesh_mode: original_gs
    sts_iterations: 7000
  - id: opencv_a
    camera_model: OPENCV
    mesh_mode: original_gs
    sts_iterations: 7000
```

Der Runner führt pro Eintrag aus:

1. sichere Vorbereitung und Prüfung von Rohvideo, GCP und HF-Cache;
2. deterministische Frame-Extraktion beziehungsweise Wiederverwendung eines
   vorher archivierten Frame-Satzes;
3. COLMAP mit dem angegebenen Kameramodell;
4. Export des Originalmodells, der TXT-Dateien und der COLMAP-Statistiken;
5. Erzeugung der idealen STS-Szene beziehungsweise Pass-through-Szene;
6. Mask-Warping und Maskenqualitätstest;
7. nichtinteraktive Mask-Review-Samples;
8. STS-Training;
9. Splat-Renderings auf `eval_frames.txt`;
10. PSNR/SSIM/LPIPS full und maskiert;
11. Variante-A-Mesh oder explizite `sugar_coarse`-Meshroute;
12. optionales Postprocessing und Centerline;
13. Kopieren der Ergebnisse in den Experimentordner;
14. Schreiben eines Abschlussstatus;
15. Zurücksetzen der generierten Live-Daten für den nächsten Matrixeintrag.

Die Pipeline sollte dafür langfristig einen parametrisierbaren Workspace-Root
für `run_sfm.sh`, `prep_sts_scene.py`, STS und SuGaR erhalten. Bis diese
Parametrisierung umgesetzt ist, darf die Matrix nicht parallel laufen und muss
vor jedem Experiment den Live-Workspace vollständig archivieren und bereinigen.

## 10. Cleanup-Regeln

Das Cleanup-Werkzeug wird strikt pfadgesichert und standardmäßig als Dry-Run
betrieben. Es darf nur aus dem Repository-Root arbeiten und verlangt eine
explizite Bestätigung des Batch-Namens.

Beibehalten werden:

- `data/01_raw` mit dem echten Rohvideo und GCP-Eingaben;
- `data/hf_cache`;
- `data/10_runs/<batch>/`, also die archivierten Testergebnisse;
- optional ein Prüfsummen-/Manifestfile außerhalb der generierten Stufen.

`data/01_raw/output.mp4` wird als generiertes Arbeitsvideo **nicht** als
unveränderliche Rohquelle behandelt und nach vorheriger Archivierung gelöscht.
Die generierten Arbeitsverzeichnisse `02_frames` bis `09_evaluation`,
`05_3dgs/masked_sugar_input`, `sugar_output` sowie temporäre Docker-/SuGaR-
Ausgaben werden nach erfolgreichem Archivieren gelöscht.

Bei Fehlern gilt: zuerst archivieren, dann Cleanup. Kein Cleanup darf einen
laufenden Docker-Prozess oder den HF-Cache löschen. Vor dem echten Löschen muss
`cleanup.json` die tatsächlich archivierten Pfade und SHA-256-Prüfsummen nennen.

## 11. UI-Maskenreview

`tools/export_mask_review_samples.py` ist aktuell interaktiv und würde in einem
automatisierten UI-/Matrixlauf blockieren. Es erhält daher:

- `--non-interactive`;
- `--indices 0,80,160,...` beziehungsweise `--all`;
- stabile Standardframes ohne `input()`;
- `review_manifest.json` mit Maskenanzahl, leerer-Masken-Anzahl,
  Auflösung und exportierten Dateinamen.

Nach erfolgreichem SAM3-Lauf wird der Review automatisch zweimal ausgeführt,
falls Mask-Warping verwendet wird:

1. Rohframe + Rohmaske direkt nach SAM3;
2. ideales STS-Bild + gewarpte Maske nach `image_undistorter`.

Die UI erhält keinen heuristischen String-Hook, sondern ruft einen expliziten
Wrapper beziehungsweise eine klar definierte Post-SAM3-Callback-Funktion auf.

## 12. Implementierungsreihenfolge

1. `warp_masks_to_undistorted.py` plus Tests mit synthetischer
   `SIMPLE_RADIAL`-Kamera.
2. Gemeinsame `eval_frames.txt`-Erzeugung und Nutzung durch STS/SuGaR.
3. Nichtinteraktiver Maskenreview und automatische UI-/Pipeline-Anbindung.
4. Parametrisierbare Camera-/STS-Workspace-Pfade.
5. Splat-Renderer für STS, SuGaR-Coarse und SuGaR-Refined.
6. Maskierte PSNR-/SSIM-/LPIPS-Evaluation und Übernahme in `run.md`.
7. Deklarativer Matrix-Runner.
8. Sicheres Archiv-/Cleanup-Werkzeug.
9. Erst danach vollständige Matrixläufe.
10. Exposé-Ergebnisabschnitt mit tatsächlichen Messwerten ergänzen.

## 13. Abnahmekriterien

- Keine STS-Kamera verwendet Rohbilder mit verzerrungsbehaftetem Modell.
- Jede STS-Maske hat exakt denselben Dateinamen, dieselbe Auflösung und dieselbe
  Bilddomäne wie das zugehörige STS-Bild.
- GCP-Picking bleibt auf dem originalen COLMAP-Modell reproduzierbar.
- Alle Splat-Metriken verwenden dieselbe `eval_frames.txt`.
- Full-frame und maskierte Metriken sind getrennt.
- STS, SuGaR-Coarse und SuGaR-Refined sind als getrennte Modellstufen
  ausgewiesen.
- Jeder Matrixlauf ist mit Parametern, Commits, Kamera-Modell, Split,
  Maskenreview, COLMAP-Ergebnis und Cleanupstatus reproduzierbar archiviert.
- Kein Testlauf löscht Rohdaten oder `hf_cache`.
- Ein fehlgeschlagener Lauf lässt genügend Logs für die Ursachenanalyse zurück.
