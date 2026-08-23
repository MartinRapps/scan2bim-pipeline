# T14 · Vortragsgliederung (20 Minuten) – PA Scan-to-BIM-Pipeline

> Vorlage gemäß Umsetzungsplan To-do 14 und Zielrahmen §6.2. Leitgrafik: Golden-Run-Panel
> (To-do 1, sobald erzeugt). Eine Folie pro Forschungsfrage aus Kapitel 8.8 als Rückgrat.

**Zeitbudget gesamt: 20 min Vortrag + Fragerunde.** Faustregel: ~1,5–2 min je Folie,
Puffer 2 min.

| # | Folie / Abschnitt | Inhalt (Kernpunkte) | Zeit | Quelle in der PA |
|---|-------------------|---------------------|------|------------------|
| 1 | Titel | Aufgabe, Kontext Scan-to-BIM, eigenes Bildmaterial (Alurohr) | 1,0 min | Deckblatt, 1. Einleitung |
| 2 | Problem & Motivation | Warum lineare Objekte? Warum Automatisierung? Mehrwert gegenüber manueller Modellierung | 1,5 min | 1.1/1.2 |
| 3 | Ziel & Abgrenzung | Machbarkeitsnachweis PA; ±10-cm-Genauigkeitsnachweis bewusst an BA delegiert | 1,0 min | 1.3, 8 |
| 4 | Pipeline-Konzept | Domänentrennung Rohbild ↔ Idealdomäne; SAM-Masken; Datenverträge der 5 Container | 2,5 min | 3./4. Kapitel, Konzeptgrafik |
| 5 | Methodenwahl & Entscheidungen | COLMAP unmaskiert, STS, Route A (Original-GS-Direktextraktion) vs. SuGaR-Coarse – warum Route A | 2,5 min | Grundlagen 3.4, 7.6 |
| 6 | Versuchsaufbau | Matrixdesign (Kameramodell × FPS × Auflösung × Route), feste Eval-Splits, objektmaskierte Metriken | 2,0 min | 5. Kapitel |
| 7 | **Golden Run / Endprodukt** (Leitgrafik) | Panel: Rohframe → Maske → Sparse → Splat → Mesh → Centerline aus EINEM Lauf; Run-ID nennen | 2,5 min | 7.1, Panel (T1) |
| 8 | Ergebnisse: Zahlen | 240/240 registriert; Produktionsstand OPENCV/5 FPS/720p/Route A = 29,62 dB PSNR objektmaskiert; 12/12 SuGaR-Folgeläufe; nicht-monotone Auflösungseffekte | 2,5 min | 7.4/7.5 |
| 9 | Grenzen & Fehlerbilder | Ansichtsmetriken ≠ Geometrie; Translation-Fallback statt voller Georeferenzierung; SuGaR-Refined offen; ein Testdatensatz | 2,0 min | 7./8. Kapitel, Anhang Robustheit |
| 10 | Fazit & Ausblick BA | Erreichte Projektziele; offene Schritte: GNSS/GCP, geometrische Metriken, reale Trassen | 1,5 min | 8. Fazit |
| – | Puffer / Übergang zu Fragen | — | 1,0 min | — |

## Forschungsfragen-Folienrückgrat (aus 8.8)

Für die Fragerunde bereithalten (nicht aktiv vortragen): je eine Mini-Folie mit Frage +
einezeiger Antwort für F1–F4 aus `sections/01_einleitung.tex` (Forschungsfragen) und den
Antworten in `07_diskussion.tex` 8.8.

## Vorbereitungs-Checkliste

- [ ] Golden-Run-Panel einsetzen (blockiert bis T1-Archive lokal verfügbar)
- [ ] Zahlen auf Folie 8 gegen finale Manifeste prüfen (T16)
- [ ] Kurzform der Folien: keine ganzen Sätze; jede Grafik im Vortrag interpretieren
      (Zielrahmen §5.3: Darstellung wird ausgewertet, nicht nur gezeigt)
- [ ] Probelauf mit Stoppuhr; bei Überlauf: Folie 9 kürzen (Grenzen mündlich)
- [ ] Technik-Check: PDF Vollbild, Fallback auf USB-Stick
