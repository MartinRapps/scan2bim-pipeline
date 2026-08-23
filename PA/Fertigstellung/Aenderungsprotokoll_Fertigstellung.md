# Änderungsprotokoll Fertigstellung

> Zentrales Protokoll gemäß `PA/Umsetzungsplan_ToDos.md` §1.1 – bewusst im Ordner
> `PA/Fertigstellung/` abgelegt (statt PA-Root), damit die gesamte Fertigstellungsarbeit
> getrennt vom jetzigen Stand bleibt. Ein Eintrag pro To-do.
>
> **Wichtig:** Textänderungen der To-dos erfolgen ausschließlich in der Arbeitskopie
> `PA/Fertigstellung/pa_arbeitsfassung/` (Branch `pa-fertigstellung`). Das Original unter
> `PA/main.tex`, `PA/sections/`, `PA/appendices/` bleibt bis zum Abschluss unverändert.

---

## Baseline (erhoben 23.08.2026 am Kopie-Build `pa_arbeit`, vor ersten Änderungen)

| Messgröße | Methode | Wert |
|---|---|---|
| Haupttext-Seitenzahl | letzte arabische Seite vor Anhang A (`build/pa_arbeit.toc`) | **40** |
| Overfull-Boxen | `grep -c Overfull build/pa_arbeit.log` | **5** |
| Undefined Ref/Cites | `grep -iE 'undefined' build/pa_arbeit.log \| wc -l` | **0** |
| Terminologie: `SAM3` roh | grep sections+appendices | **3** (04_impl:199, 06_erg:363, 07_disk:139) |
| Terminologie: kleines `qhd` | grep | **13** (davon 7× in Pfadbezügen `appendix_durchlauf` – nicht ersetzbar) |
| Terminologie: `SIMPLE-RADIAL` (Bindestrich) | grep | **4** (05_vers:1? nein – Dateien: 05_versuchsaufbau, 06_ergebnisse, 08_fazit) |
| Dezimalpunkte/Punktformat Anhang A | `appendix_colmap.tex` Zeilen 16–20 | Punkt-Trenner + `px` + Tausender ohne Punkt (139449 etc.) |
| `\nocite`-Quellen ohne echtes Zitat | manuelle Prüfung sections+appendices | **3**: `colmapProject`, `scan2bimImplementation`, `matrixRestResults` (Bewertung nannte nur 2 – `colmapProject` zusätzlich!) |
| Widerspruchsstellen Maskenwarp | grep | **vor T3:** 5 Stellen widersprüchlich → **nach T3:** konsistent |

Abweichungen zur Bewertung: Haupttext 40 statt 39 S.; Overfull 5 statt 4;
unzitierte Quellen 3 statt 2. Baseline gilt ab jetzt als Referenz.

---

## T3 – Inline-Vollauf/Maskenwarp-Widerspruch lösen (U2)
- **Datum / Phase:** 23.08.2026 / Phase A
- **Anker-Bezug:** Zielrahmen §5.1 (Konsistenz), §1.2; Aussagenprüfung Kurzfassung Pkt. 1 + §2.4 + §2.8
- **Geänderte Dateien:**
  - `pa_arbeitsfassung/sections/03_konzept.tex` (Absatz zur Domänenkette, alt ~115–124)
  - `pa_arbeitsfassung/appendices/appendix_repro.tex` (Schlussabsatz Einleitung, alt Zeile 7–9)
  - `pa_arbeitsfassung/sections/07_diskussion.tex` (8.1 Schluss, alt Zeilen 10–14)
  - `PA/PA_Aussagenpruefung.md` (Kurzfassung Pkt. 1 + §2.8 aktualisiert)
- **Was & Warum:** Code-Wahrheit festgestellt (nur gelesen): Der normale Inline-Vollauf
  ruft Maskenwarp + Coverage-Gate selbst auf (`run_pipeline.sh:828-848`); Matrixrunner
  ebenso (`tools/run_experiment_matrix.sh:392`); **ohne** eigene Warp-Stufe bleibt nur der
  `--from`-Replay (`pipeline_lib.sh` → `run_step_sts_prep` nutzt Standardmaskenverzeichnis).
  Die drei Textstellen, die noch den alten Stand („fehlt noch“) behaupteten, wurden auf
  diesen Stand gebracht – Richtung Fazit/Implementierung, die bereits korrekt waren.
- **Verifikation:** `grep -rn 'Maskenwarp|Warp' sections appendices` → alle Fundstellen
  konsistent mit Code-Wahrheit; Build `build_pa.sh` grün (0 Fehler, 0 undefined).
- **Commit:** siehe Git-Historie (`T3: …`)
- **Rückwirkung:** Aussagenprüfung Pkt. 1 (Kurzfassung) und §2.8 mit Aktualisierungsnotiz versehen.

## T5 – SuGaR-Versionsdreieck (U5) – 🔶 BLOCKIERT, nur dokumentiert
- **Datum / Phase:** 23.08.2026 / Phase A
- **Blocker:**
  1. Submodul ist im Working Copy **nicht initialisiert** (`git submodule status` → `-a0fc37b`),
     Fork-Arbeitsbaum/Diff daher lokal nicht erzeugbar.
  2. Konsolidierung erfordert Commits im Submodul + Dockerfile-Änderung (`SUGAR_REF`) +
     Parent-Gitlink-Update – das berührt **Code**, was per Nutzer-Vorgabe tabu ist.
- **Konsequenz:** Keine Textänderung (der aktuelle Text in `04_implementierung.tex:97-103`
  beschreibt die Offenheit ehrlich und bleibt korrekt). Nachgereicht werden müssen:
  Fork-Diff-Datei, finaler Commit-Hash, `SUGAR_REF`-Angleich, dann Tex-Zeile + Anlagenindex.
- **Verifikation:** entfällt (nichts geändert).

## T1/T4/T11 – Belege & Golden Run – 🔶 BLOCKIERT durch externe Archive
- **Datum / Phase:** 23.08.2026 / Phase B
- **Blocker:** `data/10_runs/` existiert im Working Copy nicht (gitignored; Laufzeitarchive
  liegen extern, u. a. V-Laufwerk, belegt durch `copy_v_drive_a_routen.txt`). Ohne lokale
  Archive keine Panels (T1), keine Run-ID-Tabelle der Autopilotläufe (T4), keine frischen
  Metriken für den Kurzabschnitt (T11).
- **Teil-Erledigung möglich sobald:** Archive lokal eingebunden oder Run-Manifeste
  (`run.md`, Metrik-JSONs) kopiert sind. Textgerüste können danach in einer Sitzung folgen.

## T8 – Kurzfassung um Ergebnissätze ergänzen (A2)
- **Datum / Phase:** 23.08.2026 / Phase D
- **Anker-Bezug:** Zielrahmen §3.1 (Kurzfassung muss Ergebnisse enthalten); Bewertung To-do 8
- **Geänderte Dateien:** `pa_arbeitsfassung/main.tex` (Abstract)
- **Was & Warum:** Drei belegbare Ergebnissätze eingefügt: 240/240 registrierte Bilder;
  12/12 Folgeläufe + 6 Autopilot-Volläufe + Qualitätsvergleichsbatch ohne Fehlerfall mit
  Status `success`; Produktionskonfiguration OPENCV/5 FPS/720p/Route A mit 29,62 dB
  objektmaskierter PSNR. Grenzsatz (kein geodätischer Genauigkeitsnachweis) bleibt erhalten.
  Bewusst NICHT behauptet: „alle Matrixläufe erfolgreich“ (historische Batches hatten
  dokumentierte Fehlfälle).
- **Verifikation:** Alle genannten Zahlen gegen `06_ergebnisse.tex` (Zeilen 181, 209–212,
  291–298) und Anhang B abgeglichen; Build grün.
- **Commit:** `T8: …`
- **Rückwirkung:** Aussagenprüfung §2.x Abstract-Bewertung damit teilweise erledigt (A2).

## T9 – Terminologie & Zahlen vereinheitlichen (A3/A4)
- **Datum / Phase:** 23.08.2026 / Phase D
- **Anker-Bezug:** Zielrahmen §5.1 (Konsistenz), §5.2 (Messwerte); Bewertung A3/A4
- **Geänderte Dateien:** `sections/03_konzept.tex`, `04_implementierung.tex`,
  `05_versuchsaufbau.tex`, `06_ergebnisse.tex`, `07_diskussion.tex`, `08_fazit.tex`,
  `appendices/appendix_colmap.tex`, `appendices/appendix_matrix.tex`, `appendices/appendix_repro.tex`
- **Was & Warum:**
  - `SAM3` → `SAM~3.1` (3 Stellen Fließtext)
  - kleines `qhd` → `QHD` (7 Fließtext-Stellen); die 7 Vorkommen in
    `\durchlaufbild/\durchlaufmasken`-Dateipfaden bewusst **nicht** geändert
    (Abbildungspfade würden brechen) – dokumentierte Ausnahme zu DoD-Grep
  - `SIMPLE-RADIAL` → `SIMPLE\_RADIAL` (4 Stellen)
  - Anhang A: Dezimalpunkt→Komma, `px`→`Pixel`, Tausenderpunkte (139.449 etc.)
  - Zahlenformat global: PSNR 2 Nachkommastellen (u. a. 21,223→21,22), SSIM/LPIPS 3
    (Tabelle Anhang B und FPS-Mittelwerte 06_erg angepasst)
  - Tausenderpunkte: 133.723/890.377, Mesh-Ablation-Tabelle, 20.000 Samples,
    200.000/5.000.000 Parameterwerte
- **Verifikation (Regression-Greps nach DoD):** SAM3=0; qhd im Fließtext=0 (nur Pfade);
  SIMPLE-RADIAL=0; px-Muster colmap-Anhang=0; Build grün (Overfull=5, undefined=0).
- **Befund nebenbei (für T16):** Text nennt QHD-SuGaR-Coarse-Mittelwert 21,69 dB
  (`06_ergebnisse.tex:370`), Anhang-B-Tabelle sagt 21,59 dB (ursprünglich 21,586).
  Diskrepanz bestand bereits vor T9; Klärung gegen Quelldaten (extern) nötig.
- **Ausnahmen dokumentiert:** $\alpha=0{,}999999$ (exakte Technikkonstante),
  Hash-Fragment `e254000…`, Batch-Datumsangaben in `\path{}` (20260812/20260818),
  Frame-Dateinamen (00000 etc.) bleiben unformatiert.
- **Commit:** `T9: …`
- **Rückwirkung:** Aussagenprüfung-Zeilen zu Terminologie damit abgehakt (A3/A4-Teil).

## T10 – Literaturordnung + \nocite (A6/A7)
- **Datum / Phase:** 23.08.2026 / Phase D
- **Anker-Bezug:** Zielrahmen §3 (Reihenfolge), §5.4 (nur verwendete Quellen); Bewertung A6/A7
- **Geänderte Dateien:** `pa_arbeitsfassung/main.tex`, `appendices/appendix_anlagenindex.tex`,
  `appendices/appendix_matrix.tex`, `appendices/appendix_colmap.tex`
- **Was & Warum:** `\printbibliography` vor `\appendix` gezogen (jetzt S. 41 vor Anhang A);
  `\nocite` entfernt; stattdessen inhaltliche Zitate: `scan2bimImplementation` im
  Anlagenindex-Absatz, `matrixRestResults` in Anhang B, `colmapProject` im COLMAP-Anhang.
  **Befund abweichend zur Bewertung:** nicht 2, sondern **3** Quellen waren unzitiert
  (`colmapProject` zusätzlich). LoF/LoT bleiben vorn – D4 offen (Prüferklärung steht aus).
- **Verifikation:** Build grün; `grep nocite main.tex` = 0 Treffer; biber ohne undefined
  citations; Literatur auf S. 41 vor Anhang A (S. 42) laut `pa_arbeit.toc`.
- **Commit:** `T10: …`
- **Rückwirkung:** Aussagenprüfung A6/A7 erledigt (bis auf LoF/LoT = D4 offen).

## T12 – Overfull-Boxen
- **Datum / Phase:** 23.08.2026 / Phase E
- **Anker-Bezug:** Zielrahmen §7 (Abgabequalität); Bewertung To-do 12
- **Geänderte Dateien:** `sections/02_grundlagen.tex` (2 Stellen),
  `sections/06_ergebnisse.tex` (Kurzform für Bildunterschrift Abbildung 7)
- **Was & Warum:** Größte Box (51 pt) durch umbruchunfähiges
  `\texttt{ImageReader.single\_camera=1}` → auf brechbares `\path{}` umgestellt;
  „Normalen/Rotationsquaternionen“ → „Normalen und Rotationsquaternionen“;
  Langcaption der SuGaR-Panels bekam Kurzform für das Abbildungsverzeichnis;
  Route-A-Satz leicht umformuliert. Ergebnis: **alle 5 Overfull-Boxen behoben**
  (Baseline 5 → 0; DoD verlangte nur ≤ 2).
- **Verifikation:** Neubuild; `grep -ac Overfull build/pa_arbeit.log` = 0; undefined = 0.
- **Commit:** `T12: …`
- **Rückwirkung:** keine Aussagenänderung, nur Satzumstellung/Grammatik.
