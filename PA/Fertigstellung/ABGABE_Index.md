# ABGABE_Index.md – Digitaler Anlagenindex (Abgabeordner)

> Diese Datei gehört in die Wurzel des abgegebenen Anlagenordners (ZIP bzw.
> Datenträger). Sie ersetzt den früheren LaTeX-Anhang „Digitaler Anlagenindex“;
> im PDF der PA steht nur noch ein Kurzverweis auf diese Datei.
>
> Stand: 25.08.2026 · Prüfsummen sind vor Abgabe je Ordner zu ergänzen
> (`sha256sum` je Manifest/CSV).

## Strukturvorschlag für den Abgabeordner

```
ABGABE/
├── ABGABE_Index.md                     ← diese Datei
├── pa.pdf                              ← finale PA
├── Anlage_KI-Nutzung.pdf               ← separate KI-Dokumentation
├── 01_Rohdaten/
│   └── Alurohr_THWS.mp4                ← H.264, 1920x1080, 30 FPS, ~48 s
├── 02_COLMAP_Tests/                    ← Rohberichte der Voruntersuchung
│   ├── <lauf>/report.txt, sparse-Statistiken
│   └── colmap_vorstudie.csv
├── 03_Grafiken/
│   ├── matrix_repeat_2026-08-17/       ← sts_masked_*.pdf/csv, sugar_coarse_*.pdf/csv,
│   │                                      per_frame/, metric_vs_runtime.pdf
│   └── verwendet_verbessert/           ← historische gemeinsame CSV-/Methodikquellen
├── 04_Run-Archive/                     ← Auszüge, keine Vollarchive (s. Empfehlung unten)
│   ├── autopilot_720p/                 ← kanonischer Produktionslauf (OPENCV/5FPS/720p/A)
│   ├── autopilot_qhd/  autopilot_low/  ← weitere Autopilot-Vollläufe
│   ├── followup_12/                    ← 12 SuGaR-Coarse-Läufe (Manifeste + Metriken + Mesh)
│   ├── matrix_24/                      ← Statusmanifeste der historischen Batches
│   └── qualitaetsvergleich_20260818/   ← Golden-Run-Arm 5fps/720p/opencv_a (+ weitere Arme nach Bedarf)
├── 05_SuGaR-Fork/
│   ├── sugar_fork_diff_48bbfdd_a0fc37b.diff
│   └── FORK_README.md                  ← Commit-Kette 48bbfdd → a0fc37b
└── 06_Panels/                          ← pa_panel_*.png in Auflösung der PDF-Version
```

## Zu jedem Eintrag: Herkunft und Zweck

| Bereich | Inhalt und Zweck | Nachweis |
|---|---|---|
| `01_Rohdaten/` | Eingangsvideo; keine metrisch validierte GNSS-Referenzkurve | Datei + Medieneigenschaften |
| `02_COLMAP_Tests/` | Sparse-SfM-Voruntersuchungen; begründet Plain-SIFT 4096 ohne Guided Matching | Berichte je Lauf |
| `03_Grafiken/` | Getrennte STS-/SuGaR-Coarse-Auswertungen, Boxplots, Delta-, Laufzeitgrafik; CSV-Quellen | PDF-Grafiken + CSV |
| `04_Run-Archive/` | Manifeste (`manifest.json`, `parameters.json`, `run.log`, `run.md`), Metriken (`sts_masked.json`, `sugar_coarse_masked.json`), Meshes, Centerlines | je Lauf-Ordner |
| `05_SuGaR-Fork/` | Fork-Diff ab 48bbfdd bis a0fc37b (= `SUGAR_REF` = Parent-Gitlink) | Diff-Datei |
| `06_Panels/` | Historische Entwicklungs- und Endprodukt-Panels aus der PA | PNG |

## Empfehlung: Welche vollständigen Läufe abgeben? (S.28-Rückfrage)

**Mindestumfang (konsistent mit dem Text der PA):**

1. **Kanonischer Produktionslauf** – Autopilot-Vollauf `Alurohr_THWS.mp4`,
   OPENCV / 5 FPS / 720p / Route A (inkl. 87/380-Centerline-Zahlen).
2. **Autopilot-Volläufe der übrigen Stufen** – qHD und low (belegt
   Erfolgskriterium 6 über alle drei Auflösungsstufen).
3. **Golden-Run-Arm** `matrix_qualitaetsvergleich_20260818/5fps/720p/opencv_a`
   – Produktionskonfiguration im Matrixverbund, failed=0.
4. **SuGaR-Folgematrix `matrix_sugar_followup_12`** – alle zwölf Läufe
   (Manifeste + Metriken + Coarse-Mesh); belegt die Vergleichsroute vollständig.

**Optional, wenn Speicherplatz erlaubt:**

5. Ein Arm je weiterer Auflösung aus dem Qualitätsvergleichsbatch
   (`qhd/opencv_a`, `low/opencv_a`) für den gepaarten Vergleich innerhalb der
   Auflösungen.
6. Vierfeld-Ablation-Artefakte (A–D) inklusive Seed-42-Manifeste.

**Nicht mehr abgeben:** Der frühere Smoke-Lauf
`matrix_smoke_low_pipe_full` existiert nicht mehr im Archivbestand und ist im
Text auch nicht mehr referenziert.

## Offene Pflichten vor Abgabe

- [ ] Prüfsummen je Archivordner ergänzen und hier eintragen
- [ ] Tatsächliche Ordnerstruktur gegen diese Datei abgleichen
- [ ] `data/10_runs`-Archive von VM/V-Laufwerk in `04_Run-Archive/` übernehmen
