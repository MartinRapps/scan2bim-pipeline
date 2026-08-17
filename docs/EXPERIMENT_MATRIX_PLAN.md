# Plan: Kameramodell-, Splat- und Maskenvergleich

Stand: 11.08.2026

Die erste Implementierung der zentralen Bausteine liegt jetzt vor:
`tools/run_experiment_matrix.sh`, `tools/experiment_matrix.tsv`,
`src/python/warp_masks_to_undistorted.py`,
`src/python/create_eval_split.py`,
`src/python/evaluate_masked_splat_metrics.py`,
`src/python/render_sugar_checkpoint.py` sowie der nichtinteraktive Modus des
Maskenreviews. Ein vollständiger 24er-Matrixlauf wurde noch nicht gestartet.
Der einzelne Low-Resolution-Integrationslauf
`matrix_smoke_low_pipe_full/5fps/low/simple_radial_a` wurde dagegen nach
Behebung des festen Eval-Split-Fehlers erfolgreich per `--from sugar`
wiederholt, ohne SAM3, COLMAP oder STS erneut auszuführen. Die bereits
ausreichend getestete Variante `simple_radial_a` ist inzwischen aus der
Konfigurationsdatei entfernt; die aktuelle Matrix umfasst drei verbleibende
Varianten, drei Auflösungen und zwei FPS-Profile, also 18 neue Versuche.

Die zwölf Läufe wurden unter
`data/10_runs/matrix_sugar_followup_12/` vollständig archiviert. Alle zwölf
Coarse-Routen und Coarse-Renderings waren erfolgreich; die
`sugar_refined_masked.json`-Dateien weisen jedoch jeweils auf den fehlenden
`refined.ply`-Export hin. Ein archivierter 5-FPS-720p-Coarse-Checkpoint war der
technische Vorabnachweis; die abgeschlossene Folgematrix ist die maßgebliche
breitere Coarse-Auswertung.
Jeder Matrixlauf erzeugt vor SAM3 ein eigenes skaliertes Arbeitsvideo. Die
Matrix umfasst standardmäßig `MATRIX_FPS_LIST=5,2`; damit werden sowohl ein
5-FPS- als auch ein ressourcensparender 2-FPS-Workflow getestet. Die drei
Auflösungen beziehen sich innerhalb jedes FPS-Blocks auf denselben zeitlichen
Frame-Rhythmus und nicht auf die native Videoframerate. Das Rohvideo bleibt
unverändert.
Der verwendete SAM3-Prompt ist standardmäßig `pipe`, weil dieser Begriff im
aktuellen Datensatz die vollständige Objektmaske liefert. Andere Prompts müssen
explizit über `MATRIX_PROMPT` gesetzt werden und werden im Parameter-Manifest
archiviert.

Nach SAM3 prüft `src/python/validate_mask_coverage.py` die `middle`-Masken über
alle erzeugten Frames. Der Matrix-Default `MATRIX_MAX_EMPTY_MASK_FRACTION=0.30`
bricht den jeweiligen Lauf bei mindestens 30 Prozent leeren oder fehlenden
Masken vor COLMAP ab. Der Coverage-Report wird trotzdem im Experimentarchiv
gespeichert. Ein Lauf mit hoher Maskenleere wird damit nicht durch gute spätere
Teilbilder schöngerechnet.

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

Für die aktuelle Matrix werden **keine Full-frame-Metriken** als reguläres
Ergebnis berechnet. Es existiert kein vollständiger Full-Scene-Splat als
Vergleichsobjekt, und ein object-only STS- oder SuGaR-Splat würde beim Rendern
außerhalb der Objektmaske typischerweise nur den gesetzten Hintergrund liefern.
Ein Vergleich dieses Renderings mit dem vollständigen Originalframe würde daher
vor allem den nicht rekonstruierten Hintergrund messen und nicht die Qualität
des Kabels oder Rohrs. Das wäre für die aktuelle Forschungsfrage irreführend.

Die Matrix berechnet deshalb ausschließlich **objektmaskierte Splat-Metriken**.
Full-frame-Werte bleiben deaktiviert. Sie dürfen später nur in einer separaten
Studie ergänzt werden, wenn beide Modelle vollständige Szenen-Splats mit
vergleichbarer Hintergrundrepräsentation besitzen.

### Exakte Bedeutung von „maskiert“

Bei der maskierten Auswertung werden Pixel außerhalb der gültigen Objektmaske
nicht in die Metrik aufgenommen. Sie werden nicht lediglich in beiden Bildern
schwarz eingefärbt und anschließend als vollständiges Bild bewertet, weil das
den Außenbereich weiterhin indirekt in die Kennzahl einfließen lassen würde.

Für jeden Evaluationsframe wird deshalb dieselbe, zur Bilddomäne passende
Referenzmaske verwendet:

1. Renderbild und Ground Truth werden auf dieselbe Auflösung und denselben
  Bildnamen geprüft.
2. Die binäre Objektmaske wird auf Renderbild und Ground Truth identisch
  angewendet.
3. Für PSNR wird der Fehler nur über gültige Objektpixel gemittelt; die Zahl
  gültiger Pixel wird protokolliert.
4. Für SSIM wird zunächst mit `skimage` eine vollständige lokale SSIM-Karte
  berechnet. Anschließend werden nur die SSIM-Werte an gültigen Objekt-
  maskenpixeln aggregiert. Lokale Fenster am Maskenrand können deshalb noch
  Kontext außerhalb der Maske enthalten; diese Randwirkung wird als
  Einschränkung des Messprotokolls dokumentiert.
5. Für LPIPS wird ein dokumentierter Objekt-Crop aus der gemeinsamen Maske
  verwendet. Pixel außerhalb der Maske werden innerhalb dieses Crops auf
  einen neutralen, in beiden Bildern identischen Wert gesetzt. Der Crop und
  seine Padding-Regel werden pro Lauf protokolliert. Ein vollständiges,
  unmaskiertes LPIPS über das ganze Bild darf nicht als „masked LPIPS"
  bezeichnet werden, weil das LPIPS-Netzwerk über seine rezeptiven Felder
  auch benachbarte Pixel berücksichtigen kann.

Damit wird der Außenbereich bei PSNR pixelweise ausgeschlossen; bei SSIM wird
die Aggregation auf Maskenpixel begrenzt, die lokale Fensterauswertung kann aber
Randkontext enthalten. Bei LPIPS wird der Außenbereich auf den gemeinsamen
Objekt-Crop begrenzt und außerhalb der
Maske vereinheitlicht; die verbleibende Randkontextwirkung ist Bestandteil der
explizit dokumentierten LPIPS-Protokolldefinition. Zusätzlich werden immer
`valid_pixel_count`, `mask_bbox`, `mask_area_fraction` und bei LPIPS
`crop_bbox` gespeichert.

Für die fachliche Entscheidung `STS` gegen `SuGaR-Coarse` beziehungsweise
`SuGaR-Refined` sind diese maskierten Werte die alleinigen Bildmetriken. Ein
Lauf darf nicht anhand einer nicht erhobenen oder später ergänzten
Full-frame-Kennzahl bevorzugt werden, wenn seine Objektmetriken oder die
Gaussian-Geometrie schlechter sind.

Die Masken müssen aus derselben Bilddomäne wie die Ground Truth stammen. Für
die `SIMPLE_RADIAL`-Baseline und die `OPENCV`-Ablation sind das die gewarpten
Masken der idealen PINHOLE-Szene. Für den direkten Rohbild-`PINHOLE`-Lauf sind
es die Rohmasken. Ein Masken-Resize ohne geometrisches Warping ist für die
endgültige Vergleichsreihe nicht ausreichend.

Wichtig: Die vorhandene SuGaR-Datei `gaussian_splatting/metrics.py` berechnet
aktuell nur gewöhnliche Full-Image-Werte über Render-/Ground-Truth-Paare. Diese
Routine wird für die aktuelle Matrix nicht unverändert verwendet, weil sie die
falsche Auswertungsdomäne hätte. Der neue maskierte-only-Modus ist ein
Implementierungsschritt des Matrixplans und darf bis dahin nicht als bereits
vorhandene Funktion vorausgesetzt werden.

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

Die Metriken beantworten dabei ausschließlich die Renderfrage im Objektbereich,
nicht die Meshfrage. Ein höheres maskiertes PSNR oder SSIM beweist keine bessere
Oberfläche. Für die Mesh-/Centerline-Entscheidung bleiben später Vollständigkeit,
Hausdorff-Distanz, Centerline-RMSE und GNSS-Fehler maßgeblich.

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

Die Kernmetriken in `metrics.json` und `run.md` lauten ausschließlich:

- `PSNR_masked`
- `SSIM_masked`
- `LPIPS_masked`
- `evaluation_frame_count`
- `evaluation_domain` (`ideal_pinhole` oder `raw_pinhole_native`)
- `evaluation_scope=object_masked_only`
- `model_stage` (`sts`, `sugar_coarse`, `sugar_refined`)
- `valid_pixel_count`, `mask_bbox`, `mask_area_fraction`, bei LPIPS zusätzlich
  `crop_bbox`
- Gaussian-Anzahl, Checkpointgröße, Renderzeit und Peak-VRAM

Die vorhandene SuGaR-Datei `gaussian_splatting/metrics.py` berechnet weiterhin
nur Full-Image-Werte und wird für diese Matrix nicht unverändert verwendet.
Das neue Werkzeug `src/python/evaluate_masked_splat_metrics.py` ist für den
object-only-Modus vorgesehen und schreibt maskierte PSNR-/SSIM-/LPIPS-Werte,
Per-Frame-Werte, gültige Pixel, Maskenfläche und LPIPS-Crop in eine JSON-Datei.
Der Matrix-Runner übernimmt den Auswertungsumfang und die Pfade zusätzlich in
`run.md` und `run.log`.

## 9. Automatisierter Matrix-Runner

Der Runner `tools/run_experiment_matrix.sh` verwendet die deklarative TSV-Datei
`tools/experiment_matrix.tsv`. Er führt die Experimente **sequenziell** und
isoliert bei allen drei Auflösungen sowie standardmäßig bei 5 FPS und 2 FPS
aus:

- `720p` = `1280x720`
- `qhd` = `960x540`
- `low` = `640x360`

Die Matrixdatei kann um weitere Varianten ergänzt werden:

```text
# id camera_model mesh_mode coarse_iterations refinement_time
simple_radial_sugar SIMPLE_RADIAL sugar_coarse 9000 medium
pinhole_a PINHOLE original_gs - medium
opencv_a OPENCV original_gs - medium
```

Ein sicherer Vorschauaufruf ist:

```bash
./tools/run_experiment_matrix.sh --dry-run
```

Einzelne Ausschnitte können mit `--resolution qhd` oder
`--variant pinhole_a` ausgeführt werden. Ein echter Lauf benötigt ein
Rohvideo und setzt `MATRIX_INPUT_VIDEO`, falls mehrere Videos in `data/01_raw`
liegen.

### Gezielte 12er-SuGaR-Folgeprüfung

Für die erneute Prüfung der Legacy-SuGaR-Coarse-Route wird bewusst eine
separate TSV-Datei verwendet:
`tools/experiment_matrix_sugar.tsv`. Sie enthält genau zwei Routen:

- `SIMPLE_RADIAL` + `sugar_coarse`;
- `OPENCV` + `sugar_coarse`.

Beide werden bei 720p, QHD und Low sowie bei 5 FPS und 2 FPS ausgeführt. Das
ergibt zwölf neue Läufe. Die bereits abgeschlossenen A-Routen werden dadurch
nicht erneut gerechnet. Der vorherige SuGaR-Fehler im Render-Helfer wurde vor
diesem Folgeversuch korrigiert: `/opt/sugar` wird explizit in den Python-
Importpfad aufgenommen und HWC-Renderergebnisse werden vor `save_image` in
CHW-Layout umgewandelt. Ein archivierter 5-FPS-720p-Coarse-Checkpoint wurde
damit bereits erfolgreich auf 30 Testviews gerendert und objektmaskiert
ausgewertet; dieser Smoke-Test ersetzt die zwölf neuen Matrixläufe nicht.

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
10. ausschließlich objektmaskierte PSNR/SSIM/LPIPS; Full-frame-Metriken bleiben
  deaktiviert;
11. Variante-A-Mesh oder explizite `sugar_coarse`-Meshroute;
12. Postprocessing und Centerline;
13. Kopieren der Ergebnisse in den Experimentordner;
14. Schreiben eines Abschlussstatus;
15. Zurücksetzen der generierten Live-Daten für den nächsten Matrixeintrag.

Die Pipeline sollte dafür langfristig einen parametrisierbaren Workspace-Root
für `run_sfm.sh`, `prep_sts_scene.py`, STS und SuGaR erhalten. Bis diese
Parametrisierung umgesetzt ist, darf die Matrix nicht parallel laufen und muss
vor jedem Experiment den Live-Workspace vollständig archivieren und bereinigen.

## 9a. Smoke-Test, Fehler und archivierter SuGaR-Replay

Der Name `matrix_smoke_low_pipe_full` beschreibt einen begrenzten
Integrations-Smoke-Test, nicht die vollständige Matrix. Getestet wurde genau
ein Experiment:

- `pipe`-Prompt, 5 FPS und 640×360 (`low`);
- `SIMPLE_RADIAL`, Variante A (`original_gs`);
- 240 Bilder, davon 210 Training und 30 feste Evaluationsbilder;
- gewarpte ideale Masken mit einer Abbruchgrenze von 30 % leeren
  `middle`-Masken;
- bereits berechneter STS-Checkpoint bei 7000 Iterationen;
- 200.000 Mesh-Vertices, 5.000.000 Oberflächenstichproben, Seed 42.

`full` bedeutet in dieser Run-ID, dass der einzelne Versuch nicht als
`--mask-only` beendet wurde. Es bedeutet nicht, dass die damals geplanten 24
Kombinationen aus vier Varianten, drei Auflösungen und zwei FPS-Profilen
gelaufen sind. Die inzwischen aus der Konfiguration entfernte Variante
`simple_radial_a` wird nicht erneut gerechnet. Der
Smoke-Test dient dazu, die Datenverträge zwischen SAM3, COLMAP, STS und SuGaR
vor dem teuren Matrixlauf zu prüfen.

### Historischer Fehler

Der ursprüngliche Low-Lauf brach in SuGaR vor der Mesh-Extraktion mit
`IndexError: list index out of range` bei `CamerasWrapper([])` ab. Die
Maskenfilterung hatte 240 von 240 Kameras behalten; die Ursache war der feste
Eval-Split. `cameras.json` enthielt Namen wie `00000`, während
`eval_frames.txt` Zeilen wie `00000.jpg` enthielt. Die damalige exakte
Zeichenkettenprüfung fand deshalb keine Testkamera.

### Lösung und Schutzmaßnahmen

- Eval-Einträge und Kameranamen werden als normalisierte Basename/Stems
  verglichen.
- Falls nötig, wird die abschließende numerische Frame-ID als Fallback genutzt.
- Fehlende oder leere Split-Dateien werden explizit abgelehnt.
- SuGaR protokolliert Eintrags-, Kamera- und Match-Anzahl.
- Eine leere `CamerasWrapper`-Eingabe erzeugt einen verständlichen Fehler statt
  eines Indexfehlers.
- `SUGAR_EVAL_FRAMES_PATH` und `EVAL_FRAMES_PATH` zeigen im Replay auf dieselbe
  feste Datei.

### Replay ohne erneute Berechnung

`--from sugar` ist ein Neustart an der SuGaR-Schrittgrenze, kein Fortsetzen
innerhalb eines unterbrochenen Trainingsprozesses. Für den Replay müssen nur
die Eingabeartefakte des Startpunkts wieder im Live-Workspace liegen: ideale
Masken, ideale COLMAP-Bilder, Sparse-Metadaten, STS-`cameras.json`, der
vollständige STS-Ply, der hochopake STS-Ply und `eval_frames.txt`. Das Archiv
wird nicht verändert; Rohvideo, GCP-Dateien und HF-Cache werden nicht benötigt
und nicht kopiert.

Das reproduzierbare Wiederherstellungsskript ist
`tools/restore_matrix_replay.sh`. Es legt außerdem den von SuGaR benötigten
`data/05_3dgs/images`-Link an. Danach kann der Mesh-Smoke-Test mit
`AUTOPILOT=true`, `SUGAR_MESH_MODE=original_gs` und
`STOP_AFTER_COARSE_MESH=1` gestartet werden. Dadurch werden Refinement,
UV-Baking und Postprocessing bewusst übersprungen.

Der erfolgreiche Replay erzeugte einen gültigen Original-GS-Coarse-Ply und
ein kompatibles `refined.obj`. Das SuGaR-Log bestätigte 30 passende
Evaluationskameras und 210 Trainingskameras. Der nachfolgende Postprocess
erzeugte 87 Roh-Centerlinepunkte, 380 Grad-10-B-Splinepunkte und gültige lokale
GeoJSON-/Fallback-Ausgaben.

Zusätzlich wurde der STS-7000-Splat auf den 30 festen Eval-Views gerendert und
mit ausschließlich objektmaskierten Metriken ausgewertet:

- PSNR masked: `29.8366 dB`
- SSIM masked: `0.929862`
- LPIPS masked: `0.082681`

Full-frame-Metriken wurden nicht berechnet. Die Fallback-Georeferenzierung
wegen fehlendem `matrix.txt` ist kein Genauigkeitsnachweis. Damit sind der
Replay-Vertrag, der Postprocess, das Rendering und die Metrikberechnung auf
dem Smoke-Test nachgewiesen; die wissenschaftliche Bewertung und der
vollständige 24er-Lauf bleiben separate Schritte.

## 9b. Befund des ersten 24er-Matrixstarts

Der erste Start mit `MATRIX_BATCH_ID=matrix_full_pipe` erzeugte nur sechs
Versuche statt der erwarteten 24. Vier Versuche waren erfolgreich:

- `5fps/720p/simple_radial_a`
- `5fps/qhd/simple_radial_a`
- `5fps/low/simple_radial_a`
- `2fps/720p/simple_radial_a`

Zwei Versuche liefen bis zu SuGaR, Postprocess, STS-Rendering und dem
Metrikschritt, brachen aber bei der objektmaskierten Auswertung ab:

- `2fps/qhd/simple_radial_a`
- `2fps/low/simple_radial_a`

In beiden Fällen enthielt der feste Split `00056.jpg`, dessen gewarpte
Evaluationsmaske leer war. Die allgemeine Coverage-Prüfung ließ den Lauf
korrekt passieren, weil nur 2 von 96 Masken leer waren und damit die
Abbruchgrenze von 30 Prozent nicht erreicht wurde. Der Metrikcode behandelte
jedoch bereits eine einzelne leere Eval-Maske als fatalen Fehler.

Die übrigen 18 Läufe (`simple_radial_sugar`, `pinhole_a` und `opencv_a`) wurden
nicht ausgeführt. Ursache war eine Bash-Implementierungsstörung: Die innere
`while read`-Schleife bezog ihre Zeilen aus einem Here-String, während die
Docker-/Pipeline-Kommandos denselben Standardinput erbten und verbrauchten.
Nach dem ersten Varianteneintrag war die Schleife dadurch am Ende der Eingabe.
Das war kein fachlicher Fehler von SuGaR, PINHOLE oder OPENCV.

Der Runner verwendet nun `for`-Schleifen mit zeilenweiser Variablenzuweisung,
plant für die aktuelle TSV alle 18 verbleibenden Einträge und schreibt bei
Fehlern den tatsächlich versuchten FPS-Wert in Manifest und Bericht. Der feste
Eval-Split wird erst
nach dem Mask-Warping aus nichtleeren idealen `middle`-Masken gebildet.
Zusätzlich lehnt SuGaR einen nur teilweise gematchten festen Split nun vor dem
Rendering mit einer klaren Fehlermeldung ab. Ein neuer vollständiger Lauf muss
unter einer neuen Batch-ID gestartet werden; der historische Batch bleibt als
Fehlernachweis erhalten.

## 9c. Interpretation der SuGaR-Metriken und der Auflösungsunterschiede

Bei `simple_radial_sugar` existiert trotz des Status `failed` eine Datei
`metrics/sts_masked.json`. Das ist kein erfolgreicher SuGaR-Wert. Der Runner
rendert und bewertet zuerst den STS-7000-Baseline-Splat. Erst danach wird in
einem getrennten Schritt der SuGaR-Coarse-Splat gerendert und als
`sugar_coarse_masked.json` bewertet. In den `matrix_rest`-Läufen brach dieser
zweite Schritt mit `ModuleNotFoundError: No module named 'sugar_scene'` ab.
Die STS-Baseline-Datei blieb deshalb erhalten, obwohl die ausgewählte
SuGaR-Route insgesamt fehlgeschlagen war. Der Fehler wurde in
`src/python/render_sugar_checkpoint.py` durch einen expliziten
`/opt/sugar`-Importpfad behoben; die historischen SuGaR-Metriken werden
dadurch nicht nachträglich zu erfolgreichen SuGaR-Ergebnissen.

Die scheinbar bessere Qualität einzelner Low-Auflösungsläufe ist nicht als
Beweis einer besseren 3D-Rekonstruktion zu lesen. Jede Auflösung wird derzeit
in ihrer eigenen Pixel- und Maskendomäne ausgewertet. Beim Herunterskalieren
wirkt die Bildbildung wie ein Tiefpass: feine Texturfehler, Kantenversatz,
Pixelrauschen und kleine Maskengrenzen werden gemittelt. Dadurch können PSNR
und SSIM steigen und LPIPS sinken, obwohl die Geometrie nicht besser geworden
ist. Zusätzlich unterscheiden sich die verfügbaren Ansichten, insbesondere
zwischen 2 und 5 FPS.

Die Beobachtung ist außerdem nicht monoton: Bei OPENCV erreicht Low bei 5 FPS
höhere Werte als QHD und 720p, während PINHOLE bei 5 FPS in QHD den höchsten
PSNR-/SSIM-Wert der drei Auflösungen erreicht. Das spricht gegen die Aussage,
dass niedrige Auflösung allein die Ursache ist. Plausibler ist eine
Interaktion aus Downsampling, Kameramodell, konkreter Kamerabewegung,
Maskenabdeckung und STS-Optimierung.

Die Zeit-/Qualitätsmatrix ist deshalb sinnvoll als sekundäre
Engineering-/Screening-Auswertung: Sie zeigt Kosten-Nutzen-Tendenzen und
Pareto-Kandidaten. Für die Bachelorarbeit darf ihr Quotient aber nicht als
alleinige Qualitätsrangfolge verwendet werden. Der aktuelle Quotient basiert
auf einer nachträglichen Min-Max-Normalisierung von PSNR, SSIM und invertiertem
LPIPS mit gleichen Gewichten und umfasst nur die archivierten STS-bis-
Postprocess-Schrittzeiten. SAM3, COLMAP, Rendering und Metrikcontainer sind
nicht vollständig enthalten. Primär sollten daher Rohmetriken und später
Centerline-/GNSS-Geometriemetriken berichtet werden; die Zeit-/Qualitätsmatrix
gehört in einen Sensitivitäts- oder Effizienzabschnitt beziehungsweise in den
Anhang.

Für einen strengeren Auflösungsvergleich müssten alle Renderings und Ground-
Truth-Bilder zusätzlich in eine gemeinsame Zielauflösung gebracht und auf
identischen Eval-Views bewertet werden. Erst dann wäre ein Auflösungsranking
weniger durch den Vorteil des Downsamplings geprägt.

## 10. Cleanup-Regeln

Das wiederhergestellte [clean_data_interactive.sh](../clean_data_interactive.sh)
ist das interaktive Standard-Cleanup für manuelle Läufe. Es löscht nur
ausgewählte abgeleitete Inhalte unter `data/`, erhält die Ordnerstruktur,
behält `data/01_raw` standardmäßig und löscht `data/hf_cache` nur nach einer
separaten Bestätigung. `--new-video` setzt die sinnvollen Defaults für einen
kompletten Neuaufbau und berücksichtigt auch `data/01_raw/output.mp4` als
löschbares Arbeitsvideo.

Für die automatisierte Matrix wird dieses Skript nicht blind mitten im Lauf
aufgerufen, weil es interaktiv ist und keine Archivierung erzeugt. Der
Matrix-Runner muss zuerst den aktuellen Experimentordner vollständig
archivieren, Prüfsummen schreiben und danach entweder die gleichen
Cleanup-Ziele nichtinteraktiv ausführen oder das Skript über einen noch zu
ergänzenden nichtinteraktiven Modus mit explizitem `DELETE`-Schutz verwenden.
Kein automatischer Lauf darf den HF-Cache oder ein laufendes Experiment löschen.

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
- Die Matrix enthält ausschließlich objektmaskierte Splat-Metriken; Full-frame-
  Metriken bleiben deaktiviert, solange kein vollständiger Vergleichssplat
  vorhanden ist.
- STS, SuGaR-Coarse und SuGaR-Refined sind als getrennte Modellstufen
  ausgewiesen.
- Jeder Matrixlauf ist mit Parametern, Commits, Kamera-Modell, Split,
  Maskenreview, COLMAP-Ergebnis und Cleanupstatus reproduzierbar archiviert.
- Kein Testlauf löscht Rohdaten oder `hf_cache`.
- Ein fehlgeschlagener Lauf lässt genügend Logs für die Ursachenanalyse zurück.
