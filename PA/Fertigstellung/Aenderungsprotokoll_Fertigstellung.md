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
