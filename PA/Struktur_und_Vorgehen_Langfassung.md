# Erweiterte Struktur und Vorgehen der PA-Langfassung

## Kennzeichnung

- **[NUTZER]** ausdrücklich in den Fokusfragen festgelegt;
- **[ABGESTIMMT]** in der anschließenden Auswahl bestätigt;
- **[EXPOSÉ]** aus dem Exposé oder archivierten Versuchen abgeleitet;
- **[ZIELRAHMEN]** formale oder wissenschaftliche THWS-Anforderung;
- **[EMPFEHLUNG]** fachlich sinnvollste Einordnung;
- **[OFFEN]** vor der finalen Aussage noch zu beantworten oder nachzuweisen.

## Leitprofil

- **[NUTZER]** Die Pipeline soll von der Bildsequenz bis zur lokalen Centerline
  funktionieren und auf Robustheit sowie Funktionalität geprüft werden.
- **[NUTZER]** Im Mittelpunkt stehen Pipelinekonzeption, Domänentrennung,
  maskengetriebene Meshgewinnung, Geometrieerhalt und wissenschaftliche Tests.
- **[ABGESTIMMT]** Die Arbeit kombiniert technischen Funktionsnachweis und
  Original-GS-/SuGaR-Coarse-Vergleich.
- **[ABGESTIMMT]** Zunächst wird eine vollständige Langfassung erstellt. Der
  THWS-Richtwert darf bewusst überschritten werden; eine spätere Kürzung bleibt
  möglich.
- **[ABGESCHLOSSEN]** Die zwölf SuGaR-Coarse-Folgeläufe sind archiviert und
  bilden die getrennte Coarse-Auswertung; eine SuGaR-Refined-Auswertung bleibt
  wegen fehlender `refined.ply` ausdrücklich ausgenommen.
- **[NUTZER]** Web-UI und validierte Georeferenzierung sind nicht Bestandteil
  des PA-Nachweises.

## Forschungsrahmen

### Hauptfrage

**[EMPFEHLUNG]** Lässt sich eine Docker-orchestrierte, objektbezogene
Scan-to-BIM-Pipeline aus promptbarer SAM-3.1-Segmentierung,
kameramodellbewusstem COLMAP-SfM, Segment-then-Splat und meshbasierter
Nachverarbeitung für ein lineares Testobjekt robust und reproduzierbar bis zu
einer lokalen Centerline betreiben?

### Unterfragen

1. **[NUTZER/EMPFEHLUNG]** Welche Bilddomänen, Datenverträge und Quality-Gates
   halten Masken, Kameras, Eval-Split, Gaussians, Mesh und Centerline
   konsistent?
2. **[NUTZER/EXPOSÉ]** Wie beeinflussen Kameramodell, FPS und Auflösung den
   Pipelineerfolg und die objektmaskierten Bildmetriken?
3. **[NUTZER/EXPOSÉ]** Bewahrt Route A die für die Centerline benötigte
   Objektgeometrie geeigneter als SuGaR-Coarse?
4. **[NUTZER/EMPFEHLUNG]** Welche Rollen spielen interaktiver Vollauf,
   Autopilot, Replay und Matrixrunner für Reproduzierbarkeit und Batchbetrieb?

## Kapitelstruktur

### 1. Einleitung

- **[ZIELRAHMEN]** Motivation, Problemstellung, Ziel, Mehrwert und Aufbau;
- **[NUTZER]** technischer Funktionsnachweis bis zur lokalen Centerline;
- **[NUTZER]** Eigenleistung und wissenschaftliches Vorgehen;
- **[NUTZER]** Abgrenzung von UI, realer Trasse, ±10 cm, vollständiger
  Computer-Vision-Lehre und rein bildmetrischer Produktionsentscheidung.

### 2. Datengrundlage und Anwendungsrahmen

- **[EXPOSÉ]** Alurohr als kontrollierter linearer Testdatensatz;
- **[EXPOSÉ]** 2/5 FPS und 720p/QHD/Low;
- **[NUTZER]** lineare Einzeltrasse statt verzweigtem Netzwerk;
- **[EMPFEHLUNG]** lokale Centerline als analytischer PA-Endpunkt;
- **[ZIELRAHMEN]** fehlende reale GNSS-/Vermessungsreferenz transparent machen.

### 3. Technische und methodische Grundlagen

- **[NUTZER]** SAM~3.1 wegen Promptbarkeit und zeitlicher Propagation;
- **[NUTZER]** kompakter Vergleich der Methoden;
- **[NUTZER]** Formeln für Gaussian Splatting, PSNR/SSIM/LPIPS,
  Centerline/B-Spline und Route A;
- **[EXPOSÉ]** unmaskiertes COLMAP, Kameramodelle und ideale Bilddomäne;
- **[EXPOSÉ]** STS-Objektzuordnung, Objektfilter und Hochopazitätskopie;
- **[EXPOSÉ]** Route A gegenüber vollständigem SuGaR-Coarse-Ablauf;
- **[EMPFEHLUNG]** Formeln nur dort, wo sie Implementierung oder Auswertung
  nachvollziehbar machen.

### 4. Methodisches Konzept und Systemarchitektur

- **[NUTZER]** CLI-zentrierte Pipeline ohne UI;
- **[EXPOSÉ]** fünf Container und getrennte CUDA-/Python-Umgebungen;
- **[NUTZER/EXPOSÉ]** Roh-/Ideal-Domänentrennung als zentraler Eigenbeitrag;
- **[EXPOSÉ]** Rollen der Masken in STS, Objektselektion, SuGaR und Metriken;
- **[EMPFEHLUNG]** Vollauf, Autopilot, Replay und Matrixrunner nicht
  gleichsetzen;
- **[EMPFEHLUNG]** Serverbetrieb nur als Architekturpotenzial formulieren.

### 5. Implementierung und Robustheitsmaßnahmen

- **[EXPOSÉ]** Bind-Mounts, UID/GID, Persistenz, Logging und Run-Tags;
- **[NUTZER]** Begründung des zentralen CLI-Skripts;
- **[EXPOSÉ]** Masken-Coverage, Review-Samples und fester Eval-Split;
- **[EXPOSÉ]** COLMAP-Modellprüfung, ideale Szene und Maskenwarp;
- **[EXPOSÉ]** Objekt-ID-, Opazitäts- und Farbfilterung;
- **[EXPOSÉ]** Route-A-PLY/OBJ-Export und SuGaR-Coarse-Vergleich;
- **[EXPOSÉ]** `single`-Centerline und Grad-10-B-Spline;
- **[ZIELRAHMEN]** Fehlversuche mit Ursache, Korrektur und verbleibender
  Einschränkung dokumentieren.

### 6. Versuchsdesign

- **[EMPFEHLUNG]** Reihenfolge: Smoke-Test, COLMAP-Vorstudie, Hauptmatrix,
  Vierfeld-Ablation und abgeschlossene SuGaR-Coarse-Folgematrix;
- **[NUTZER]** Kameramodelle, 2/5 FPS, drei Auflösungen, Maskenprofile,
  COLMAP-Entscheidungen und Meshrouten untersuchen;
- **[NUTZER]** alle Stufen eines vollständigen Laufs als Erfolgskriterien;
- **[EXPOSÉ]** feste Splits, nur nichtleere ideale Eval-Masken und Seed 42;
- **[EMPFEHLUNG]** Beobachtung, Hypothese, Test und Schlussfolgerung trennen.

### 7. Ergebnisse

- **[NUTZER]** vollständige Kette anhand des besten beziehungsweise
  repräsentativen Beispiels zeigen;
- **[NUTZER]** gezielter Vergleich mit schlechten Einstellungen;
- **[NUTZER]** Original-GS und SuGaR-Coarse zentral vergleichen;
- **[EXPOSÉ]** COLMAP-Vorstudie, Hauptmatrix und Vierfeld-Ablation A/B/C/D;
- **[ABGESCHLOSSEN]** zwölf SuGaR-Coarse-Folgeläufe mit stage-getrennten
  Grafiken ergänzen;
- **[OFFEN]** konsistenten Golden Run und identische Vergleichsansichten
  auswählen; die neue Metrikgrafikserie ist bereits stufenspezifisch erzeugt;
- **[EMPFEHLUNG]** negative Ergebnisse als Robustheitsbefunde behandeln.

### 8. Diskussion

- **[ZIELRAHMEN]** Forschungsfragen beantworten und Grenzen diskutieren;
- **[EMPFEHLUNG]** Masken sind kein Geometriebeweis;
- **[EMPFEHLUNG]** PINHOLE auf Rohbildern ist kein Entzerrungsnachweis;
- **[EMPFEHLUNG]** Low-Auflösungsmetriken können durch Downsampling steigen;
- **[EXPOSÉ]** Route A bewahrt die STS-Geometrie direkter;
- **[EMPFEHLUNG]** Matrixrunner belegt Batchfähigkeit, nicht automatisch
  Autopilot oder Server-Rollout;
- **[ZIELRAHMEN]** fehlende GNSS-Referenz und Einzeldatensatz begrenzen die
  Übertragbarkeit.

### 9. Fazit und Ausblick

- **[NUTZER]** Funktionsnachweis und Robustheitsgewinn zusammenfassen;
- **[EXPOSÉ]** Route A als begründeten Produktionsstandard nennen;
- **[ABGESCHLOSSEN]** Fazit nach der SuGaR-Coarse-Folgematrix aktualisieren;
- **[ZIELRAHMEN]** reale Referenzmessung, 4x4-Transformation, RMSE und
  Hausdorff als Bachelorarbeitsziele nennen.

## Abbildungen und Tabellen

### Hauptabbildungen

1. **[EMPFEHLUNG]** aktuelle Fünf-Container-Architektur ohne Web-UI;
2. **[NUTZER/EXPOSÉ]** Roh-/Ideal-Domänentrennung inklusive Maskenwarp;
3. **[NUTZER]** vollständige Golden-Run-Artefaktkette;
4. **[NUTZER]** bestes gegen gezielt schlechtes Beispiel;
5. **[EXPOSÉ]** PSNR-/SSIM-/LPIPS-Matrix;
6. **[NUTZER/EXPOSÉ]** A/B/C/D- beziehungsweise A/C-Meshvergleich;
7. **[NUTZER]** Mesh, Roh-Centerline und B-Spline;
8. **[EMPFEHLUNG]** Quality-Gates oder zentrale Fehlerkette.

### Screenshot-Regel

- **[NUTZER]** Screenshots zu Codeverbesserungen, Loss-Einstellungen und
  Autopilotparametern sind erwünscht.
- **[EMPFEHLUNG]** Formeln, Parameter- und Ursache-Lösung-Tabellen sind im
  Haupttext vorzuziehen. Code- oder Terminal-Screenshots gehören überwiegend in
  den Anhang; wissenschaftliche Belegbilder bleiben im Haupttext.

## Anlagen

- **[ZIELRAHMEN]** konkreter Anlagenindex statt pauschalem Repository-Verweis;
- vollständige COLMAP-Berichte;
- vollständige Matrix, Coverage, Laufzeiten und Fehlerlogs;
- historische SuGaR-/Masken-/Iterations-/Opazitäts-/Crop-Ablationen;
- Fehlerchronologie;
- CSV-, B-Spline- und GeoJSON-Ergebnisse;
- CLI-/Autopilot-/Replay-Nachweise;
- Hardware-, Image-, Commit- und Parametersteckbrief;
- relevante KI-Interaktionen und Outputs.

## Wissenschaftliche Sperrregeln

- Keine ±10-cm-Aussage ohne reale Referenz.
- Keine Bildmetrik als Beweis korrekter 3D-Geometrie.
- Keine STS-Metrik als SuGaR-Ergebnis.
- Keine geplanten SuGaR-Werte vorwegnehmen.
- Keine Gleichsetzung von PINHOLE-Ablation und Entzerrung.
- Keine Gleichsetzung von Matrixrunner, Autopilot und Replay.
- Route A nicht als SuGaR-Coarse- oder Refinement-Lauf bezeichnen.
- Historische Brillen-/Gestellversuche nicht als Alurohrergebnisse ausgeben.

## Erstellungsreihenfolge

1. **[ABGESCHLOSSEN]** zwölf SuGaR-Coarse-Folgeläufe abschließen und getrennt
  von den STS-Baselines auswerten;
2. **[OFFEN]** Autopilot-End-to-End-Nachweis archivieren;
3. **[OFFEN]** Golden Run und Abbildungsinventar bestimmen;
4. Versuchsdesign und Erfolgskriterien einfrieren;
5. Ergebnisse nur aus archivierten Artefakten schreiben;
6. Diskussion und Forschungsfragen aktualisieren;
7. Grundlagen und Implementierung gegen aktuellen Code prüfen;
8. Einleitung, Fazit und Kurzfassung zuletzt finalisieren;
9. Quellen-, KI- und Anlagen-Audit durchführen;
10. PDF kompilieren, Verweise prüfen und erst danach gegebenenfalls kürzen.
