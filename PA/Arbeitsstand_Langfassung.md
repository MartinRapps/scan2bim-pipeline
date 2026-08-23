# Arbeitsstand der PA-Langfassung

## Bestätigte Leitentscheidungen

- Profil: technischer Funktionsnachweis plus Geometrie-/Meshroutenvergleich.
- Umfang: zunächst vollständige Langfassung mit ungefähr 30–40 Textseiten;
  spätere Kürzung ist möglich.
- Hauptziel: robuste und reproduzierbare Pipeline von der Bildsequenz bis zur
  lokalen Centerline.
- Zentrale Eigenleistung: Pipelinekonzeption, Roh-/Ideal-Domänentrennung,
  maskengetriebene Objekt- und Meshgewinnung, Quality-Gates,
  Matrixautomatisierung und wissenschaftliche Fehleranalyse.
- Bedienumfang: interaktives CLI, Autopilot, Replay und Matrixrunner; Web-UI ist
  ausgeschlossen.
- Meshrouten: Original-STS-GS-Route A als Produktionspfad; SuGaR-Coarse als
  wissenschaftliche Vergleichsroute.
- Georeferenzierung: vorbereitet, aber im PA-Datensatz nicht metrisch validiert.
- Die zwölf SuGaR-Coarse-Folgeläufe sind abgeschlossen und in die
  stage-getrennten Grafiken sowie Ergebnisabschnitte übernommen; eine
  SuGaR-Refined-Auswertung bleibt offen, weil kein `refined.ply` exportiert
  wurde.

## Bereits in LaTeX umgesetzt

- THWS-orientiertes Deckblatt mit Platzhaltern;
- Eigenständigkeitserklärung und Kurzfassung;
- römische Frontmatter- und arabische Textseiten;
- Inhalts-, Abbildungs- und Tabellenverzeichnis;
- neues Kapitel zur Datengrundlage;
- erweiterte Einleitung mit Haupt- und Unterfragen;
- Grundlagen mit Formeln für Gaussian-Kovarianz, Opazität,
  maskierten Loss, B-Spline und PSNR;
- aktualisierte Maskensemantik;
- ausführliches Konzept der Domänentrennung;
- CLI-/Autopilot-/Replay-/Matrix-Abgrenzung;
- Container-, Quality-Gate- und Robustheitsdarstellung;
- gestuftes Versuchsdesign;
- Vierfeld-Ablation A/B/C/D;
- abgeschlossene zwölf SuGaR-Coarse-Folgeläufe mit stage-getrennten Grafiken;
- erweiterte Ergebnisse und Diskussion;
- Flowchart des Exposés in Kapitel 4.1, angepasst an aktuellen CLI-/Container-
  und Meshroutenstand;
- dokumentierter mask-aware SuGaR-Fork mit Änderungsbereichen und
  Versionierungswarnung;
- Erklärung der mehrfachen Bild-/Maskenablagen und der Abgrenzung zwischen
  funktional notwendiger Idealbildkopie, Symlink, Diagnosekopien und optionaler
  Speicheroptimierung;
- Anlagen für COLMAP, Matrix, Robustheit, Reproduzierbarkeit,
  digitalen Anlagenindex und KI-Nutzung.

## Verbindlich offene Nachweise

1. Die zwölf SuGaR-Coarse-Folgeläufe anhand der finalen Manifeste und
  `sugar_coarse_masked.json`-Dateien nochmals auf Vollständigkeit prüfen.
2. Einen vollständig konsistenten Golden Run auswählen.
4. Artefaktkette des Golden Runs exportieren:
   Rohframe, SAM-Maske, Idealbild/-maske, COLMAP, STS-Gaussians,
   Route-A-Mesh, Centerline und B-Spline.
5. Identische Vergleichsansichten für A/B/C/D beziehungsweise mindestens A/C
   erzeugen.
6. Einen tatsächlichen Autopilot-Vollauf oder einen gleichwertigen
   End-to-End-Vertragstest archivieren.
7. Aktuelle Hardware-, Image-, Parent- und Submodul-Commits in ein finales
   Reproduzierbarkeitsmanifest aufnehmen.
8. Digitale KI-Interaktionsgruppen mit tatsächlichen Prompts, Antworten,
   Modellen und Zeiträumen zusammenstellen.
9. Formale Deckblattdaten sowie Abgabetermin eintragen.
10. KI-Nutzung und PlagAware-Unterlagen mit dem Prüfer abstimmen.

## Wissenschaftliche Sperrregeln

- Kein geodätischer ±10-cm-Nachweis ohne reale Referenz.
- Keine Bildmetrik als Beweis korrekter 3D-Geometrie.
- Keine STS-Baseline als SuGaR-Ergebnis ausgeben.
- Keine geplanten SuGaR-Werte vorwegnehmen.
- PINHOLE auf Rohframes nicht als Entzerrungsnachweis bezeichnen.
- Matrixrunner, Autopilot und Replay nicht gleichsetzen.
- Docker-/Batchfähigkeit nur als Vorbereitung für einen Serverbetrieb, nicht
  als validierten Server-Rollout beschreiben.
- Historische Brillen-, Gestell- oder Kabelresultate nicht als aktuelle
  Alurohrdaten ausgeben.
- Route A nicht als SuGaR-Coarse- oder Refinement-Lauf bezeichnen.

## Empfohlene nächste Bearbeitungsreihenfolge

1. SuGaR-Folgematrix und stage-getrennte Grafikquellen final prüfen.
2. Golden Run und Abbildungsinventar festlegen.
3. Ergebniskapitel finalisieren.
4. Diskussion und Fazit gegen die finalen Ergebnisse prüfen.
5. Kurzfassung zuletzt neu formulieren.
6. Quellen- und Anlagenindex auditieren.
7. Layout und Seitenumfang überprüfen.

## Update Fertigstellung (23.08.2026, Branch `pa-fertigstellung`)

Alle To-do-Änderungen erfolgen in der Arbeitskopie
`PA/Fertigstellung/pa_arbeitsfassung/` (Original bleibt bis zum Abschluss
unverändert); Protokollierung in `PA/Fertigstellung/Aenderungsprotokoll_Fertigstellung.md`.

- Erledigt: T3 (Warp-Widerspruch auf Code-Wahrheit gebracht), T7 im Markier-Modus
  (Kürzungskandidaten nur dokumentiert, D3), T8 (Kurzfassung mit Ergebnissen),
  T9 (Terminologie/Zahlen; Pfadbezüge ausgenommen), T10 (Literatur vor Anhang,
  `\nocite` durch echte Zitate ersetzt; LoF/LoT bleiben vorn wegen D4 offen),
  T12 (alle Overfull-Boxen behoben, 5 → 0), T15 (Build-Leichen entfernt),
  T13/T14 als Vorlagen in `PA/Fertigstellung/`.
- Blockiert: T1/T4/T11 (Laufarchive extern, `data/10_runs/` nicht lokal),
  T5 (SuGaR-Versionsdreieck: Submodul nicht initialisiert + Codeänderungen tabu),
  T6 (Deckblattdaten warten auf Bestätigung, siehe T13-Checkliste Punkt 7).
- Neuer Baselinestand Kopie-Build (`pa_arbeit`): Haupttext endet S. 40,
  Literatur S. 41, 0 Overfull, 0 undefined.
- Offene Diskrepanz für T16 markiert: QHD-SuGaR-Coarse-Mittelwert 21,69 dB im Text
  vs. 21,59 dB in Anhang B – Klärung gegen Quelldaten erforderlich.
