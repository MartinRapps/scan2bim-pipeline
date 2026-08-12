# Aussagenprüfung der ausgearbeiteten PA

**Prüfstand:** 11.08.2026, abgeschlossene Run-Archive und aktueller Arbeitsbaum
nach Abschluss der `matrix_sugar_followup_12`. Dieses Dokument bleibt ein
quellenbasierter Auditstand; nach dem finalen Versionsfreeze ist nur noch der
Commit-/Manifestabgleich zu wiederholen.

## Kurzfazit

Die ausgearbeitete PA ist in den wesentlichen historischen Befunden, der
Abgrenzung zur Bachelorarbeit und der Entscheidung für Route A überwiegend
konsistent mit Exposé, README, Code und den archivierten Läufen. Sie darf aber
noch nicht als final faktisch freigegeben gelten. Vier Punkte haben hohe
Priorität:

1. Der Maskenwarp in die ideale Bilddomäne ist im Matrixrunner implementiert,
   aber im normalen Inline-Vollauf und im `--from`-Replaypfad nicht als eigener
   Verarbeitungsschritt verdrahtet. Aussagen wie „die Pipeline verwendet stets
   denselben Warp für Bilder und Masken“ sind deshalb derzeit zu allgemein.
2. Der tatsächlich ausgecheckte SuGaR-Fork ist `eca4ea1` mit lokalen Änderungen;
   der Parent-Gitlink zeigt auf `ecda7ef`, während das Dockerfile `SUGAR_REF` auf
   `e254000...` setzt. Das Exposé und die Memories nennen teilweise einen bereits
   synchronisierten `e254000...`-Stand. Die PA dokumentiert den Widerspruch besser,
   darf den Fork aber noch nicht als versionsfixiert bezeichnen.
3. Die zwölf SuGaR-Coarse-Folgeläufe sind inzwischen abgeschlossen. Alle zwölf
   Manifeste sind `success`; `sugar_coarse_masked.json` ist für alle zwölf
   vorhanden. `sugar_refined_masked.json` ist in allen zwölf Fällen wegen eines
   fehlenden `refined.ply` übersprungen und darf nicht als Refinement-Ergebnis
   interpretiert werden.
4. Die Implementierung berechnet SSIM aus einer vollständigen SSIM-Karte und
   mittelt anschließend nur die Pixelzentren innerhalb der Maske. Der
   Kontext außerhalb der Maske kann dadurch in SSIM-Fenster eingehen. Die PA
   sollte nicht behaupten, dass der Hintergrund bei SSIM vollständig aus jedem
   Berechnungsschritt ausgeschlossen ist.

## Bewertungsmaßstab

Die Quellen wurden in dieser Reihenfolge verwendet:

1. tatsächlich ausgeführter Code, Git-Zustand und Run-Artefakte;
2. der im Exposé als verbindlich bezeichnete aktuelle Projektarbeitsstand;
3. README, Setup- und Matrixdokumentation;
4. Memory-Dateien als zeitbezogene Übergabe- und Entscheidungsnotizen.

Das Exposé besitzt laut FAQ die höchste Dokumentpriorität. Es kann jedoch nicht
belegen, dass ein behaupteter Versions- oder Runstand tatsächlich im aktuellen
Arbeitsbaum vorliegt. Deshalb werden dokumentierter Sollstand und ausführbarer
Iststand getrennt ausgewiesen.

### Statusklassen

- **BESTÄTIGT** – durch aktuellen Code und/oder konkrete Artefakte belegt.
- **HISTORISCH BESTÄTIGT** – im Archiv beziehungsweise Exposé belegt, aber nicht
  notwendigerweise aktueller Default.
- **NUR TEILPFAD** – für Matrix, Replay oder einen bestimmten Runner belegt,
  nicht für die gesamte Pipeline.
- **INTERPRETATION** – zulässige fachliche Deutung, kein direkter Messbeweis.
- **OFFEN/GEPLANT** – noch auszuführen oder mit einem Artefakt zu schließen.
- **WIDERSPRUCH** – Quellen oder Codezustände widersprechen einander.
- **FORMAL OFFEN** – Inhalt plausibel, aber für die Abgabe noch nicht formal
  vollständig.

## 1. Tatsächlicher Prüfstand

| Gegenstand | Befund am 11.08.2026 | Status |
|---|---|---|
| Parent-Gitlink `third_party/SuGaR` | `ecda7efc01cd...` | BESTÄTIGT |
| Ausgecheckter SuGaR-Commit | `eca4ea1facaa...`, Branch `project/masked-sugar` | BESTÄTIGT |
| Lokale Forkänderungen | `gaussian_splatting/scene/dataset_readers.py` und `sugar_scene/gs_model.py` | BESTÄTIGT |
| Docker-Buildreferenz | `SUGAR_REF=e254000b28ef...` | BESTÄTIGT |
| Run-Manifeste der neuen Folgematrix | 12, alle `success`, 6 je Kameramodell | BESTÄTIGT |
| Matrixprozesse | zum Auditzeitpunkt keine aktiven Matrixprozesse; frühere Doppelstart-Gefahr bleibt als Prozesslehre dokumentiert | HISTORISCHER RISIKOBEFUND |
| Frames im Live-Arbeitsbereich | 240 | BESTÄTIGT |
| Hierarchische Live-Masken | je 240 `default`, `middle`, `small` | BESTÄTIGT |
| GCP | `gcp_coordinates.csv`, `gcp_relative.csv`, `anchor.txt`, `gcp_observations.json`, `matrix.txt` und `gcp_report.json` vorhanden; der UI-Smoke-Test ist durchgeführt | BESTÄTIGT |
| Aktuelle echte 4x4-Georeferenzierung | nicht nachgewiesen; Fallback ist der belegte Laufzustand | OFFEN |
| PA-PDF | 38 Seiten, LaTeX-Build erfolgreich; 12 nichtkritische Overfull-Warnungen | BESTÄTIGT |

Die neue Folgematrix ist inzwischen abgeschlossen. Die zwölf Manifeste und
die zugehörigen Coarse-Metriken wurden in die Grafikquelle und die PA
übernommen. Die frühere Doppelstart-Gefahr bleibt als Entwicklungsbefund
dokumentiert, ist aber kein Bestandteil der finalen 12er-Statusauswertung.

## 2. Prüfung der PA-Kapitel

### 2.1 `main.tex`, Frontmatter und Umfang

| PA-Aussage | Quellenprüfung | Status | Maßnahme |
|---|---|---|---|
| Die Arbeit ist ein technischer Machbarkeitsnachweis und kein ±10-cm-Nachweis. | `PA/Arbeitsstand_Langfassung.md`, FAQ A-02, Exposé-FAQ-Stand und PA-Kapitel 1/8 stimmen überein. | BESTÄTIGT | Beibehalten. |
| Die PA ist zunächst als 30–40-seitige Langfassung erlaubt. | Arbeitsstand bestätigt dies; `Zielrahmen.md` nennt weiterhin ca. 15–25 reine Textseiten als THWS-Richtgröße. | FORMAL OFFEN | Als Arbeitsmaster kennzeichnen und vor Abgabe Haupttext/Anlagen trennen. |
| Deckblatt und Erklärung sind abgabefertig. | `PA/main.tex` enthält Platzhalter für Name, Matrikelnummer, Studiengang, Prüfer und Abgabetermin. Die Erklärung ist eine eigene Arbeitsfassung, nicht nachweislich die unveränderte offizielle THWS-Vorlage. | FORMAL OFFEN | Platzhalter ersetzen und offizielle Erklärung/PlagAware-Vorgaben mit dem Prüfer abgleichen. |
| Die KI-Nutzung ist vollständig dokumentiert. | `appendix_ki.tex` beschreibt Kategorien, fordert aber selbst noch tatsächliche Prompts, Werkzeuge und Zeiträume. | FORMAL OFFEN | Digitalen KI-Nachweis ergänzen; nur tatsächlich verwendete Werkzeuge nennen. Außerdem ist „GPT-5.6 Sol“ falsch; die aktuelle Modellbezeichnung lautet GPT-5.6 Luna. |

### 2.2 Einleitung und Datengrundlage

| PA-Stelle | Aussage | Quellenprüfung | Status |
|---|---|---|---|
| `sections/01_einleitung.tex` | Alurohr als kontrollierter linearer Testdatensatz; reale Rohr-/Kabeltrasse erst in der BA. | FAQ A-01/A-02, Exposé-FAQ-Stand und README stimmen überein. | BESTÄTIGT |
| `sections/01_einleitung.tex` | Hauptziel ist die lokale Centerline, nicht die globale Genauigkeit. | FAQ A-03 und die vorhandenen lokalen/Fallback-Artefakte stützen die Aussage. | BESTÄTIGT |
| `sections/02_datengrundlage.tex` | Video etwa 48 s; 5 FPS ergeben 240, 2 FPS 96 Frames. | `docs/COLMAP_Tests/AUSWERTUNG_GESAMT_COLMAP.md` dokumentiert 1920×1080, 30 FPS, etwa 48 s und 240/480/960 Frames; die 2-FPS-Ableitung ist mit dem Matrixdesign vereinbar. | HISTORISCH BESTÄTIGT |
| `sections/02_datengrundlage.tex` | GCP-Dateien sind synthetisch/lokal und keine unabhängige Referenzkurve. | Die aktuellen Dateien und der erfolgreiche Report sind vorhanden; die GCPs bleiben dennoch ein lokaler/synthetischer Test und keine unabhängige Referenzkurve. | BESTÄTIGT |
| `sections/02_datengrundlage.tex` | Translation-Fallback prüft den Exportpfad, nicht Lage-, Maßstabs- oder Höhengenauigkeit. | `src/scripts/postprocess.sh` verwendet bei fehlender Matrix/Anchor eine Einheitsmatrix plus `FALLBACK_ANCHOR`; kein geometrischer Referenztest vorhanden. | BESTÄTIGT |
| `sections/02_datengrundlage.tex` | Netzwerkmodus bleibt außerhalb des PA-Scopes. | Nutzerentscheidung, FAQ/Exposé und aktuelle Defaults `CENTERLINE_MODE=single` stimmen überein. | BESTÄTIGT |

### 2.3 Grundlagen

| PA-Stelle | Aussage | Quellenprüfung | Status | Maßnahme |
|---|---|---|---|---|
| `sections/02_grundlagen.tex` | `default` ist die Basis-Maske, `middle` eine 5×5-Erosion, `small` zwei Erosionen. | `extract_masks_notebook_flow.py`, `hierarchical_masks.py`, README und Exposé bestätigen dies. | BESTÄTIGT | Beibehalten. |
| `sections/02_grundlagen.tex` | SAM-Video-Predictor und SAHI werden methodisch abgegrenzt; SAHI wurde nicht systematisch getestet. | SAHI ist im älteren Exposé als Fallback beschrieben, aber aus dem aktuellen PA-Flowchart entfernt; kein systematischer Vergleichsrun vorgelegt. | BESTÄTIGT MIT EINSCHRÄNKUNG | Als nicht getestete Alternative formulieren, nicht als gemessene Überlegenheit des Video-Predictors. |
| `sections/02_grundlagen.tex` | COLMAP läuft auf unmaskierten Frames. | `run_sfm.sh` verwendet `/data/02_frames` ohne `ImageReader.mask_path`; Nutzerentscheidung und Exposé bestätigen dies. | BESTÄTIGT |
| `sections/02_grundlagen.tex` | STS/SuGaR arbeiten nach der Entzerrung in einer idealen PINHOLE-Domäne. | `run_sfm.sh` erzeugt für SIMPLE_RADIAL/OPENCV eine `image_undistorter`-Szene; PINHOLE/SIMPLE_PINHOLE wird als Pass-through behandelt. | BESTÄTIGT FÜR BILD-/KAMERA-SZENE |
| `sections/02_grundlagen.tex` | Masken werden mit demselben Mapping in die ideale Domäne gewarpt. | Das ist im Matrixrunner umgesetzt. Im normalen Inline-Vollauf und in `pipeline_lib.sh` gibt es nach COLMAP keinen Aufruf von `warp_masks_to_undistorted.py`; `prep_sts_scene.py` liest dort weiterhin `/data/03_masks`. | NUR TEILPFAD/WIDERSPRUCH | Entweder Warp in Voll- und Replaypfad integrieren oder PA überall „Matrixpfad“/„ideal vorbereiteter Replay“ schreiben. |
| `sections/02_grundlagen.tex` | Route A überspringt SuGaR-Coarse, Refinement und UV-Baking. | `run_masked_sugar.sh` mit `SUGAR_MESH_MODE=original_gs` ruft direkt `extract_mesh.py` auf und exportiert Coarse-PLY plus Kompatibilitäts-OBJ. | BESTÄTIGT |
| `sections/02_grundlagen.tex` | `c=9000` aktiviert die späten DN-/SDF-Terme nicht. | Forkschedule aktiviert diese Terme erst bei `iteration > 9000`; c9000 bleibt dennoch ein Coarse-Trainingslauf mit maskiertem RGB/Entropy und verändert die geladene STS-Wolke. | BESTÄTIGT MIT PRÄZISIERUNG | Nicht den Eindruck erwecken, c9000 sei reiner Export oder unveränderter STS-Checkpoint. |
| `sections/02_grundlagen.tex` | Maskierte PSNR-, SSIM- und LPIPS-Werte sind die einzigen Bildmetriken. | Matrixrunner ruft ausschließlich `evaluate_masked_splat_metrics.py` auf und setzt `full_frame_metrics=false`. | BESTÄTIGT |
| `sections/02_grundlagen.tex` | Die PSNR-Formel entspricht dem Implementierungs-MSE. | Die PA verwendet eine ungeklärte L2-Norm; der Code mittelt zunächst über die drei RGB-Kanäle und dann über gültige Pixel. | WIDERSPRUCH/UNPRÄZISE | Formel als kanalweise gemitteltes MSE schreiben oder den Faktor 1/3 explizit ergänzen. |
| `sections/02_grundlagen.tex` | SSIM wird ausschließlich innerhalb der Objektmaske ausgewertet. | Der Code erstellt eine vollständige SSIM-Karte und mittelt deren Werte an Maskenpixeln; SSIM-Fenster können Hintergrundpixel enthalten. | ZU STARK FORMULIERT | „Maskierte Aggregation der SSIM-Karte“ schreiben und Kontextwirkung als Einschränkung dokumentieren. |
| `sections/02_grundlagen.tex` | LPIPS nutzt einen Objekt-Crop mit neutralisiertem Außenbereich. | `prepare_lpips_inputs()` setzt Pixel außerhalb der Maske im gemeinsamen Crop auf 0,5; der Runner fordert LPIPS. | BESTÄTIGT |

### 2.4 Konzept, Flowchart und Domänentrennung

| PA-Stelle | Aussage | Quellenprüfung | Status |
|---|---|---|---|
| `sections/03_konzept.tex` | Flowchart zeigt aktuelle fünf Container, Route A, SuGaR-Coarse und optionalen Georeferenzierungszweig. | Der TikZ-Flowchart ist im PDF vorhanden und entspricht dem gewünschten Scope ohne UI/SAHI-Hauptroute. | BESTÄTIGT |
| `sections/03_konzept.tex` | UI und SAHI sind nicht Bestandteil des PA-Diagramms. | Nutzerentscheidung und Arbeitsstand bestätigen UI-Ausschluss; SAHI ist nicht systematisch untersucht. | BESTÄTIGT |
| `sections/03_konzept.tex` | Eine identische Bild-/Maskentransformation stellt in der Pipeline die Konsistenz her. | Für `tools/run_experiment_matrix.sh` ja: COLMAP → `warp_masks_to_undistorted.py` → `create_eval_split.py` → idealer STS-Arbeitsbereich. Für `run_pipeline.sh` ohne `--from` und `run_pipeline.sh --from ...` fehlt dieser Verdrahtungsschritt. | NUR TEILPFAD | Anspruch im Haupttext begrenzen oder Code vor der finalen PA vereinheitlichen. |
| `sections/03_konzept.tex` | Replay startet an einer Schrittgrenze und setzt kein Training innerhalb einer Iteration fort. | `run_pipeline.sh --from` bindet `pipeline_lib.sh`; `restore_matrix_replay.sh` restauriert fertige Artefakte. | BESTÄTIGT |
| `sections/03_konzept.tex` | Matrixrunner belegt Batchfähigkeit, nicht automatisch Autopilot oder Serverbetrieb. | Matrixscript ist seriell und nichtinteraktiv; kein unabhängiger Autopilot-/Serverdeployment-Nachweis. | BESTÄTIGT |

### 2.5 Implementierung, Fork und Ablagen

| PA-Stelle | Aussage | Quellenprüfung | Status | Maßnahme |
|---|---|---|---|---|
| `sections/04_implementierung.tex` | Fünf Container kapseln CUDA-/Python-Abhängigkeiten; E ist CPU-only. | `docker-compose.yml` definiert fünf Services; E hat keine GPU-Reservation. | BESTÄTIGT |
| `sections/04_implementierung.tex` | Host-UID/GID werden aus der aufrufenden Umgebung übernommen. | `run_pipeline.sh`, `pipeline_lib.sh`, `run_masked_sugar.sh` exportieren `id -u`/`id -g`; Compose nutzt diese Werte. | BESTÄTIGT |
| `sections/04_implementierung.tex` | Forkänderungen nach Commits `48bbfdd`, `8f4f7a2`, `e254000`, `ecda7ef`, `eca4ea1`. | `git show --stat` bestätigt die genannten historischen Änderungsschichten. `eca4ea1` änderte zusätzlich `sugar_scene/cameras.py`, was in der PA-Tabelle fehlt. | HISTORISCH BESTÄTIGT, TABELLE UNVOLLSTÄNDIG | `sugar_scene/cameras.py` ergänzen. |
| `sections/04_implementierung.tex` | Parent-Gitlink `ecda7ef`, ausgecheckt `eca4ea1`, lokale Splitänderungen noch nicht committed. | Aktueller Git-Zustand bestätigt genau diesen Befund. | BESTÄTIGT |
| `appendix_repro.tex`/`appendix_anlagenindex.tex` | Fork ist versionsfixiert beziehungsweise reproduzierbar. | Arbeitsbaum ist dirty; Dockerfile-Referenz `e254000` und Dev-Overlay `eca4ea1` unterscheiden sich. | WIDERSPRUCH | Bis zum Freeze „historisch versioniert, aktueller Arbeitsbaum dirty“ schreiben. |
| `sections/04_implementierung.tex` | `data/05_3dgs/images` ist ein Symlink auf ideale Bilder. | `prep_sts_scene.py` und `restore_matrix_replay.sh` erzeugen den Symlink. | BESTÄTIGT |
| `sections/04_implementierung.tex` | `_attempts` enthält Prompt-Fallbacks; Hierarchie ist morphologisch abgeleitet. | `extract_masks_notebook_flow.py` probiert `pipe`, `planter`, `plant`, `desk`; `prep_sts_scene.py` wählt bei leerer Hierarchie den besten Versuch; Erosionen sind im Code sichtbar. | BESTÄTIGT |
| `sections/04_implementierung.tex` | Mehrere Ablagen sind Datenverträge/Archive, nicht mehrere notwendige SAM-Inferenzen. | Physische Idealbildkopie, Symlink, morphologische Ebenen und Matrixarchive sind getrennte Funktionen. | BESTÄTIGT |
| `sections/04_implementierung.tex` | Alle Quality-Gates gelten für die Pipeline. | Coverage-Gate, Warp-Split und strengere Evalprüfungen liegen vor allem im Matrixrunner und im Replay; der Inline-Vollauf prüft nicht dieselbe vollständige Menge. | NUR TEILPFAD | Scope der Gates in Tabelle und Diskussion nennen. |

### 2.6 Versuchsaufbau und Matrix

| PA-Stelle | Aussage | Quellenprüfung | Status |
|---|---|---|---|
| `sections/05_versuchsaufbau.tex` | Die COLMAP-Voruntersuchung umfasst fünf 240-Bild-Läufe und begründet 4096 Plain-SIFT ohne Guided Matching. | `docs/COLMAP_Tests/06_variant_A_*` und `AUSWERTUNG_GESAMT_COLMAP.md` bestätigen die getrennte CPU-Studie. | HISTORISCH BESTÄTIGT |
| `appendix_colmap.tex` | Tabelle mit 139449/142208/140594 Punkten und Laufzeiten 876/1678/925 s. | Die drei Einzelreports enthalten diese Werte; sie sind nicht identisch mit dem älteren Gesamtbenchmark mit 95.651 Punkten. | BESTÄTIGT MIT ABGRENZUNG |
| `sections/05_versuchsaufbau.tex` | Historische sechs A-Läufe plus 18 Folgeexperimente ergeben 24 Versuche. | `matrix_thesis_data.csv` enthält 24 Zeilen: 16 success und 8 failed. | HISTORISCH BESTÄTIGT |
| `sections/06_ergebnisse.tex`/`appendix_matrix.tex` | 24 Läufe: 16 vollständig, 8 unvollständig. | Für die historischen Batches `matrix_full_pipe` + `matrix_rest` exakt belegt. | HISTORISCH BESTÄTIGT |
| `sections/06_ergebnisse.tex` | Die sechs alten SuGaR-Läufe erreichten STS, Mesh und Postprocess, scheiterten erst am SuGaR-Renderhelper. | `matrix_thesis_data.csv`, alte `run.log`-Dateien und Matrixplan stützen dies; STS-Baseline und SuGaR-Metrik sind getrennt. | HISTORISCH BESTÄTIGT |
| `appendix_matrix.tex` | Average wird nur bei zwei erfolgreichen FPS-Läufen gebildet. | `create_matrix_thesis_figures.py` und `matrix_thesis_method.md` implementieren/erklären diese Regel. | BESTÄTIGT |
| `sections/05_versuchsaufbau.tex` | Zwölf SuGaR-Läufe sind offen und Voraussetzung für das finale Kapitel. | Zum ursprünglichen Redaktionsstand korrekt; inzwischen ist `matrix_sugar_followup_12` abgeschlossen und muss im Kapitel als Ergebnis ergänzt werden. | HISTORISCH, AKTUALISIERT |
| aktueller Runstand | Die zwölf Läufe seien bereits ausgeführt. | Jetzt bestätigt: zwölf `success`-Manifeste, Coarse-Metriken und Logs vorhanden. | BESTÄTIGT | Refinement weiterhin separat als nicht exportiert ausweisen. |

### 2.7 Ergebnisse und Interpretation

| PA-Stelle | Aussage | Quellenprüfung | Status |
|---|---|---|---|
| `sections/06_ergebnisse.tex` | Low-Smoke-Test: 240 Kameras, 210 Training, 30 Evaluation, Route-A-Mesh, Rendern, Metriken, Centerline und GeoJSON. | Exposé/Matrixplan und Smoke-Archive belegen diesen Lauf. | HISTORISCH BESTÄTIGT |
| `sections/06_ergebnisse.tex` | Smoke-Metriken PSNR 29.8366 dB, SSIM 0.929862, LPIPS 0.082681. | Exposé, Matrixplan und archivierte JSON-Datei stimmen überein. | HISTORISCH BESTÄTIGT |
| `sections/06_ergebnisse.tex` | A/B/C/D Meshgrößen 68471/135164, 63266/124976, 79711/156935, 68618/135522. | Exposé-Abschnitt Vierfeld-Ablation und Repository-Memory bestätigen die Zahlen. | HISTORISCH BESTÄTIGT |
| `sections/06_ergebnisse.tex` | Gerichtete Stichprobenabstände A/B/C/D liegen ungefähr bei 1.08/0.90, 1.79/3.39 und 1.96/2.73 cm. | Exposé und Memory dokumentieren genau diese relativen Werte. | HISTORISCH BESTÄTIGT |
| `sections/06_ergebnisse.tex` | Route A wird wegen direkterem Geometrieerhalt bevorzugt. | Nutzerentscheidung und kontrollierte relative Ablation stützen die Entscheidung; keine Ground Truth. | INTERPRETATION, ZULÄSSIG |
| `sections/06_ergebnisse.tex` | OPENCV-A-Low bei 5 FPS zeigt besonders hohe Werte. | `matrix_thesis_data.csv` bestätigt PSNR 29.9935, SSIM 0.9336, LPIPS 0.0822. | HISTORISCH BESTÄTIGT |
| `sections/06_ergebnisse.tex` | Diese Werte stammen aus der „nativen Bilddomäne“. | Die Matrix wertet bei SIMPLE_RADIAL/OPENCV die ideale, gewarpte Szene aus; „native“ kann hier nur native Runauflösung bedeuten. | UNKLAR/IRREFÜHREND |
| `sections/06_ergebnisse.tex` | 87 rohe Centerlinepunkte und 380 Grad-10-B-Splinepunkte. | Smoke-Archive, Exposé und Memory bestätigen die Zahlen. | HISTORISCH BESTÄTIGT |
| `sections/06_ergebnisse.tex` | Die zwölf Folgeprüfungen seien zum Zeitpunkt dieser Fassung noch nicht ausgeführt. | Historischer Redaktionsstand; die PA enthält jetzt die abgeschlossene 12er-Coarse-Auswertung und die neuen Grafiken. | HISTORISCH, AKTUALISIERT |
| `sections/07_diskussion.tex` | Bildmetriken beweisen keine 3D-Geometrie oder Centerline-Genauigkeit. | Exposé, Matrixplan, README und Nutzerabgrenzung stimmen überein. | BESTÄTIGT |
| `sections/07_diskussion.tex` | Autopilot ist implementiert, aber Vollaufnachweis fehlt. | Code enthält Autopilotzweige; kein eindeutiges archiviertes Autopilot-End-to-End-Manifests gefunden. | BESTÄTIGT/OFFEN |
| `sections/07_diskussion.tex` | Matrix belegt Batchfähigkeit, nicht Server-Rollout oder formale Usability. | Matrixrunner ist seriell; kein Deployment-/Mehrbenutzertest. | BESTÄTIGT |
| `sections/07_diskussion.tex` | Zeit-/Qualitätsquotient nutzt nur STS-bis-Postprocess-Zeiten und ist sekundär. | `matrix_thesis_method.md` und `create_matrix_thesis_figures.py` bestätigen dies. | BESTÄTIGT |

### 2.8 Fazit

Das Fazit ist in der Grundrichtung korrekt: Route A ist der bevorzugte
Projektstandard, die Geometrieentscheidung ist ohne Ground Truth vorläufig,
SuGaR-Coarse bleibt Vergleichsroute und die BA muss GCP/GNSS und geometrische
Referenzmetriken ergänzen. Die Sätze „kann als reproduzierbare Kette betrieben
werden“ und „technische Machbarkeit ist gezeigt“ müssen jedoch auf den
belegten Matrix-/Smoke-/Replaypfad bezogen werden, solange der allgemeine
Inline-Vollauf nicht dieselben Maskenwarp- und Quality-Gate-Schritte nutzt.

### 2.9 GCP/UI-Implementierung und aktueller Nachweis

Die zuvor offene technische Prüfung der GCP-Ansicht wurde abgeschlossen. Die
Fehlerursachen waren getrennt zu bewerten:

1. Die UI lud die Frame-Liste nur beim Öffnen, wählte keinen ersten Frame
   automatisch und blendete fehlgeschlagene Vorschaubilder aus.
2. Der Parser in `src/python/gcp_register.py` erwartete bei `cameras.txt`
   implizit eine Parameteranzahl. Die aktuelle COLMAP-Standardzeile
   `ID MODEL WIDTH HEIGHT PARAMS...` enthält diese Anzahl nicht.
3. Der UI-Dockeraufruf übergab Host-Absolute-Pfade an den Container und lief
   zunächst mit der Compose-Standard-UID/GID `1000:1000`. Dadurch war der
   gemountete Zielordner für die aktuelle Host-Identität nicht beschreibbar.
4. Die rekursive Serverantwort mit `children` wurde in der Dateivorschau nur
   auf der obersten Ebene gerendert.

Die Korrektur unterstützt beide Kamerazeilenformate, führt ein GCP-Preflight
mit strukturierten Fehlern und Warnungen ein, verwendet im Container die
`/data`-Pfade und die aktuelle Host-UID/GID, aktualisiert Frames explizit und
nach einem erfolgreichen Lauf automatisch und rendert rekursive Blattdateien
mit relativem Pfad. Docker und nativer Fallback werden im Fehlerfall getrennt
ausgegeben.

Der verifizierte Teststand ist:

| Nachweis | Ergebnis | Status |
|---|---:|---|
| GCP-Parser-/Geometrie-Regressionstests | 11/11 erfolgreich im Container E | BESTÄTIGT |
| Registrierte Frames / vorhandene Bilddateien | 240 / 240 | BESTÄTIGT |
| GCP-Beobachtungen | 17 für 3 GCPs (5/5/7) | BESTÄTIGT |
| UI-Compute-Modus | Docker, Report und `matrix.txt` erzeugt | BESTÄTIGT |
| Gesamt-RMSE / maximales Residuum | 0,05933 m / 0,07362 m | BESTÄTIGT |
| Browser-Smoke-Test | erster Frame, 240 Thumbnails, Report und verschachtelte Pfade sichtbar | BESTÄTIGT |

Die drei GCPs erfüllen das mathematische Minimum, der Report warnt aber
korrekt vor der praktischen Empfehlung von mindestens vier räumlich gut
verteilten Punkten. Die höheren Reprojektionsfehler von `GCP_003` (RMSE
6,9943 px; Maximum 10,1059 px) sind als Qualitätswarnung zu dokumentieren.
Wegen der lokalen/synthetischen Koordinaten ist der Lauf ein technischer
Funktionsnachweis und kein geodätischer Genauigkeitsnachweis. Ebenso bleibt
der im Autopilot angezeigte Status von einem echten GCP-Nachweis zu trennen:
entscheidend sind `matrix.txt` und `gcp_report.json`, nicht allein der Exit
Code des Gesamtprozesses.

## 3. Prüfung der Anhänge

### COLMAP-Anhang

**Ergebnis:** fachlich belastbar, wenn die Tabelle klar als separater
Windows-11-/CPU-only-Sparse-Benchmark bezeichnet bleibt. Die Werte 95.651 aus
der Gesamtübersicht und 139.449 aus dem Plain-SIFT-4096-Einzelbenchmark dürfen
nicht ohne Lauf-ID und Parameterprofil in einer Tabelle vermischt werden. Die
PA macht diese Trennung überwiegend, sollte die Quellen-Dateinamen zusätzlich
explizit nennen.

### Matrix-Anhang

**Ergebnis:** Die 24er-Tabelle ist ein historischer Snapshot und als solcher
korrekt. Sie ist nicht die aktuelle Gesamtmatrix, sobald die neue
`matrix_sugar_followup_12` abgeschlossen ist. Der Anhang braucht anschließend
eine getrennte Tabelle für die zwölf SuGaR-Routen mit `sts_masked.json`,
`sugar_coarse_masked.json`, gegebenenfalls `sugar_refined_masked.json`,
Status, Eval-Anzahl, Fehlerursache und Commitstand.

### Robustheitsanhang

**Ergebnis:** Fehlerklassen und Lehren stimmen mit Exposé und Code überein.
Die Formulierung, alle Korrekturen seien „heute als Quality-Gates“ aktiv, ist
zu breit: Split-/Warp-/Coverage-Prüfungen sind insbesondere im Matrix-/Replay-
Pfad wirksam; der Inline-Vollauf besitzt nicht dieselbe Gate-Kette.

### Reproduzierbarkeitsanhang

**Ergebnis:** Pfade, Route A, Maskenstufen, Parameter und Replayprinzip sind
weitgehend korrekt. Zu korrigieren beziehungsweise zu präzisieren sind:

- Fork nicht als sauber versionsfixiert bezeichnen, solange Parent, Docker-
  Referenz, Checkout und Arbeitsbaum nicht identisch sind.
- zusätzlich `sugar_scene/cameras.py` als Teil der `eca4ea1`-Änderungen nennen;
- die `BSPLINE_DEGREE=10`-Aussage als Orchestrator-Default formulieren: In
  `run_pipeline.sh` und `pipeline_lib.sh` ist 10 gesetzt, während
  `src/scripts/postprocess.sh` selbst als Fallback noch 20 definiert.

### Anlagenindex

Der Index ist nützlich und konkret. Die Zeile „versionsfixierter lokaler Fork“
ist am Prüfstand zu stark und sollte in „lokaler Fork; Commit- und
Arbeitsbaumstand im Reproduzierbarkeitsmanifest“ geändert werden. Die
Warp-Ausgaben unter `data/03_masks` sind laufabhängig und sollten als
„kanonische/ideale Masken im Matrix- beziehungsweise Replaypfad“ bezeichnet
werden.

### KI-Anhang

Der Anhang ist als Struktur vorhanden, aber noch nicht abgabefertig. Die
Modellbezeichnung `GPT-5.6 Sol` ist zu ersetzen. Tatsächliche Interaktionen,
Zeiträume und gegebenenfalls weitere verwendete Werkzeuge müssen ergänzt
werden; die KI darf nicht als wissenschaftliche Quelle der technischen
Behauptungen erscheinen.

## 4. Quellenkonflikte außerhalb der PA

| Quelle | Konflikt beziehungsweise Einordnung |
|---|---|
| `docs/Expose_PA_BA.tex`, verbindlicher FAQ-Abschnitt | Behauptet Parent-Gitlink und `SUGAR_REF` auf `e254000...`; der tatsächliche Parent zeigt `ecda7ef`, der lokale Lauf `eca4ea1` plus Dirty-Diff. Der Exposé-Stand ist als gewünschter Sollstand, nicht als Ist-Nachweis zu behandeln. |
| `README.md` SuGaR-Fork-Abschnitt | Erwartet noch `48bbfdd...` und eine uncommitted `train.py`-Änderung. Das ist ein älterer Dokumentstand. |
| `docs/agent-memory-repo.md` | Enthält ältere Fork-/Pipelinezustände, unter anderem `7c10c4a`/`48bbfdd`, und darf nicht als aktueller Commitnachweis gelten. |
| `docs/agent-memory-session.md` | Behauptet an einer Stelle, `pipeline_lib.sh` werde von keinem Skript gesourced. Das ist für den heutigen `run_pipeline.sh --from`-Pfad veraltet; der normale Inline-Vollauf bleibt davon getrennt. |
| `/memories/repo/scan2bim-pipeline.md` | Kompakte Übergabenotiz nennt inzwischen `e254000...` als synchronisierten Parent. Der aktuelle Git-Befehl widerspricht dem; Memory ist deshalb als veralteter Snapshot zu markieren. |
| `docs/FAQ.md` | Bestätigt PA-Scope und Exposé-Priorität. Die frühere offene UI/GCP-Prüfung wurde durch die aktuelle Implementierung und den Browser-/Container-Smoke-Test geschlossen; der geodätische Genauigkeitsnachweis bleibt offen. |
| `docs/EXPERIMENT_MATRIX_PLAN.md` | Belegt Matrixlogik, Maskenwarp, festen Split und historische 24er-Auswertung. Der aktuelle Abschlussnachweis der 12er-Folgematrix liegt zusätzlich in `data/10_runs/matrix_sugar_followup_12/`. |

## 5. Verbindliche Korrekturliste vor einer finalen PA-Fassung

### Priorität 1 – wissenschaftlich beziehungsweise technisch

1. Entscheiden, ob der Warp in `run_pipeline.sh` und
   `src/scripts/pipeline_lib.sh` ergänzt wird. Bis dahin in der PA überall
   zwischen Matrix-/Replaypfad und allgemeinem Vollauf unterscheiden.
2. Einen einzigen sauberen SuGaR-Stand herstellen: Parent-Gitlink, Checkout,
   Docker-`SUGAR_REF`, Dev-Overlay und Run-Manifest müssen denselben Commit
   referenzieren; lokale Split-Guards müssen committed werden.
3. Die abgeschlossene 12er-Matrix anhand aller zwölf Manifeste/Logs/Metriken
   nachvollziehbar halten; die frühere doppelte Batch-ID bleibt nur ein
   Entwicklungsrisiko.
4. SSIM- und PSNR-Definition an den tatsächlichen Evaluator anpassen. Besonders
   SSIM als maskierte Aggregation mit möglicher Fenster-Randwirkung beschreiben.
5. Die neue 12er-Coarse-Auswertung weiterhin von einer noch offenen
   SuGaR-Refined-Auswertung getrennt halten.

### Priorität 2 – PA-Konsistenz

6. `eca4ea1`-Änderung von `sugar_scene/cameras.py` im Forktableau ergänzen.
7. `native Bilddomäne` in den Matrixergebnissen durch „jeweilige Runauflösung
   und, bei SIMPLE_RADIAL/OPENCV, ideale gewarpte Bilddomäne“ ersetzen.
8. Quality-Gates als Matrix-/Replay-Gates kennzeichnen, sofern der Inline-
   Vollauf nicht ebenfalls validiert wird.
9. `appendix_anlagenindex.tex` von „versionsfixierter Fork“ auf einen Hinweis
   zum aktuellen Commit-/Arbeitsbaumstand umstellen.
10. Den standalone `postprocess.sh`-Default für den B-Spline mit dem
    orchestrierten Default 10 vereinheitlichen oder die Abweichung explizit
    dokumentieren.

### Priorität 3 – Formalia

11. Deckblattplatzhalter und offizielle Erklärung ersetzen.
12. KI-Anhang mit tatsächlichen Interaktionen vervollständigen und
    `GPT-5.6 Luna` statt `GPT-5.6 Sol` dokumentieren.
13. Nach finaler Faktprüfung Haupttext auf den THWS-Richtwert prüfen und
    Volltabellen/Logs in den digitalen Anlagenindex verschieben.
14. Die technische GCP/UI-Kette ist mit Parser-, Container- und Browser-Smoke-
   Tests bestätigt. Vor einer fachlichen Georeferenzierung bleiben mindestens
   vier gut verteilte reale GCPs, eine unabhängige Referenz und eine
   dokumentierte Genauigkeitsprüfung erforderlich.

## 6. Freigabestatus

Die PA kann derzeit als **wissenschaftlicher Arbeitsmaster mit überwiegend
bestätigten Befunden** verwendet werden. Die 12er-SuGaR-Coarse-Folgematrix und
der technische GCP/UI-Nachweis sind integriert. Sie ist noch **nicht als
finale Abgabefassung freigegeben**, weil
der Maskenwarp im allgemeinen Pfad, der SuGaR-Versionsfreeze, eine mögliche
SuGaR-Refined-Auswertung, die SSIM-Formulierung und die Formalia noch offen
beziehungsweise widersprüchlich sind.

Nach dem finalen Versionsfreeze ist dieses Dokument nochmals gegen die
Manifeste zu prüfen. Ergebnis-, Diskussions-, Fazit- und Kurzfassungskapitel
können nun auf der abgeschlossenen Coarse-Matrix aufbauen; eine Refinement-
Ergänzung bleibt separat.
