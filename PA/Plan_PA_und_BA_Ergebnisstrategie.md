# Plan: PA-Fokus, Grafikverwendung und Übergang zur BA

## 1. Grundentscheidung

Die Projektarbeit (PA, 8 ECTS) weist die technische Funktionsfähigkeit,
Robustheit und Reproduzierbarkeit der Docker-Pipeline nach. Die Bachelorarbeit
(BA, 15 ECTS) übernimmt diese Pipeline als Grundlage und untersucht mit realen
Drohnen-/Trassendaten die geometrische Qualität und Übertragbarkeit.

Die vorhandenen Matrixergebnisse werden deshalb in der PA **dokumentiert, aber
zurückhaltend interpretiert**. Die BA erzeugt mit realen Datensätzen eine neue,
fachlich stärkere Matrix und neue Geometriemetriken. Die PA darf nicht den
Eindruck erwecken, die vorhandenen Bildmetriken seien bereits ein Nachweis der
vermessungstechnischen Genauigkeit.

## 2. Abgrenzung zwischen PA und BA

| Thema | PA, 8 ECTS | BA, 15 ECTS |
|---|---|---|
| Primärziel | technische Pipeline von Bildsequenz bis Centerline funktionsfähig machen | reale geometrische Qualität und Übertragbarkeit bewerten |
| Daten | Alurohr-/Testdaten und archivierte Matrixläufe | reale Drohnenaufnahme an der Trasse mit GNSS-/GCP-Referenz |
| Pipeline | SAM3, COLMAP, Masken-/Bilddomäne, STS, Route A, SuGaR-Coarse, Postprocessing | stabilisierte Pipeline mit begründeten Parametern und realem Datensatz |
| Matrix | technische Robustheits- und Sensitivitätsprüfung | kontrollierte Aufnahme-/Rekonstruktions- und Geometriestudie |
| Bildmetriken | objektmaskiertes PSNR, SSIM, LPIPS als Renderingmetriken | ergänzende Metriken, gemeinsam mit Geometriemetriken |
| Geometrie | Mesh, Centerline und GeoJSON als Funktionsnachweis; keine Genauigkeitsbehauptung | Centerline-RMSE, Hausdorff-Distanz, Vollständigkeit und Toleranzprüfung |
| Interpretation | Was lief? Welche Fehler wurden gefunden? Welche Route ist technisch praktikabel? | Welche Parameter verbessern die reale Geometrie und erfüllen die Zielgenauigkeit? |
| Abschluss | Produktionsroute A als begründeter PA-Arbeitsstand | empirisch begründete Empfehlung für reale Anwendung |

## 3. Was noch in die PA muss

### 3.1 Inhaltlich notwendige Ergänzungen

1. **Klare Arbeitsfrage und Abgrenzung**
   - Hauptfrage: Kann die Docker-basierte Scan-to-BIM-Pipeline eine maskierte
     Bildsequenz reproduzierbar bis zu Mesh, Centerline und GeoJSON verarbeiten?
   - Unterfragen: Welche Datenverträge sichern robuste Stufenübergänge? Welche
     Route ist als technischer Produktionspfad praktikabel? Welche Fehlerfälle
     wurden erkannt und behoben?
   - Explizit ausschließen: reale ±10-cm-Genauigkeit, GNSS-Validierung,
     vollständige Vermessung und allgemeine Rangfolge aller Konfigurationen.

2. **Konzept und Domänentrennung**
   - Rohbild-/COLMAP-Domäne und ideale STS-/Mesh-Domäne erklären.
   - Maskenwarp als Konsistenzschritt zeigen.
   - `default`, `middle` und `small` in ihrer unterschiedlichen Funktion
     erklären.

3. **Technische Umsetzung**
   - SAM3-Masken, COLMAP, STS, Route A, SuGaR-Coarse und Postprocessing als
     Datenverträge beschreiben.
   - Erfolgskriterium eines vollständigen Laufs definieren.
   - Autopilot und Docker-Serverarchitektur als Eigenleistung hervorheben.

4. **Zwischenstände und Fehleranalyse**
   - nicht jede Fehlermeldung ausführen, sondern drei bis vier repräsentative
     Stufen dokumentieren (siehe Abschnitt 5).
   - jeweils Ursache, Änderung, Nachweis und verbleibende Grenze nennen.

5. **Ergebnisinterpretation kürzen**
   - Matrixwerte primär beschreiben, nicht als globale Rangfolge interpretieren.
   - keine Aussage wie „OPENCV/5 FPS ist am korrektesten“.
   - ausdrücklich festhalten: PSNR/SSIM/LPIPS bewerten gerenderte Ansichten,
     nicht Mesh- oder Centerline-Genauigkeit.

6. **PA-Fazit**
   - Pipeline technisch funktionsfähig und reproduzierbar;
   - Route A als aktueller Produktionspfad begründet;
   - SuGaR-Coarse als separat reparierter Vergleichspfad dokumentiert;
   - reale geometrische Validierung als BA-Aufgabe offen lassen.

### 3.2 Was nicht mehr in die PA vertieft werden sollte

- keine weitere große Interpretation der 24 historischen Matrixläufe;
- keine globale Auflösungs-, FPS- oder Kameramodellrangliste;
- keine geometrische Genauigkeitsbehauptung aus Bildmetriken;
- keine vollständige Darstellung aller Logs und Einzelwerte im Haupttext;
- keine neue große technische Matrix, wenn sie nur dieselbe Aussage wiederholt.

## 4. Grafikplan für die PA

### 4.1 Haupttext: maximal fünf Grafikgruppen

| Priorität | Grafik/Inhalt | Einbauort | Zweck |
|---:|---|---|---|
| 1 | Pipeline-/Datenflussdiagramm | Kapitel Konzept/Versuchsaufbau | Architektur und Stufengrenzen erklären |
| 2 | Zwischenstand 1: Rohframe + SAM3-Maske | Kapitel Umsetzung | Segmentierung und Maskenqualität zeigen |
| 3 | Zwischenstand 2: Rohbild/ideales Bild + Maskenwarp | direkt bei Domänentrennung | geometrische Bild-/Maskenkonsistenz belegen |
| 4 | Zwischenstand 3: STS-Splat/Objektfilterung + Mesh | Kapitel Umsetzung oder Ergebnisse | Übergang von Maske zu objektbezogener Geometrie zeigen |
| 5 | End-to-End-Panel: Mesh + Centerline/B-Spline + GeoJSON-Hinweis | Beginn Ergebnisse | vollständiges technisches Endprodukt zeigen |
| 6 | STS- und SuGaR-Coarse-Übersicht | Ergebnisse, direkt vor der Diskussion | getrennte Bildmetriken knapp dokumentieren |

Die Punkte 1–5 sind wichtiger als eine zweite Metrikgrafik. Wenn der Umfang
zu groß wird, bleiben STS-/SuGaR-Übersichten im Haupttext und die Diagnostik
wandert in die Anlage.

### 4.2 PA-Anhang und digitale Anlage

In die PA-Anlage beziehungsweise digitale Grafikablage gehören vollständig:

- `sts_masked_overview.pdf`;
- `sts_masked_per_frame_boxplots.pdf`;
- `sugar_coarse_masked_overview.pdf`;
- `sugar_coarse_masked_per_frame_boxplots.pdf`;
- `sugar_coarse_vs_sts_delta.pdf`;
- `metric_vs_runtime.pdf`;
- CSV-/JSON-Datengrundlage unter `neu_metriken_2026-08-12/Datengrundlage/`;
- vollständige Matrix- und Einzelansichtsdateien.

Die STS-Grafiken dürfen nur vollständige Original-GS-Route-A-Läufe enthalten.
Die SuGaR-Grafiken dürfen nur `sugar_coarse_masked.json` verwenden. Historische
STS-Zwischenmetriken fehlgeschlagener SuGaR-Routen bleiben Fehlernachweis, aber
werden nicht als zusätzliche Grafikwerte geplottet.

### 4.3 Laufzeitgrafik

Die Laufzeitgrafik bleibt eine optionale PA-Anlagengrafik. Im Haupttext reicht
ein kurzer Satz zur technischen Laufzeit. Falls sie im Haupttext bleibt, muss
sie als explorative Darstellung der **vollständigen archivierten Laufdauer**
bezeichnet werden, nicht als geometrische Effizienzbewertung.

## 5. Plan für Zwischenstände und Screenshots

Die vorhandenen Screenshots sollen nicht als lose Sammlung, sondern als
chronologische Nachweiskette eingebaut werden. Für jeden Screenshot werden
Version/Datum, Eingabestufe, beobachteter Befund, Änderung und Ergebnis in einer
kurzen Bildunterschrift oder einem Absatz dokumentiert.

### Zwischenstand A: Segmentierung und Masken

**Einbauort:** Kapitel Umsetzung, Abschnitt SAM3/Maskenverträge.

**Panel:** Rohframe, SAM3-Maske `default`, `middle` und gegebenenfalls
`small`; optional ein Masken-Review.

**Textaussage:** SAM3 liefert eine verwertbare Objektmaske. `middle` dient
Coverage und Split-Zulassung sowie SuGaR-DN-Supervision; `default` dient der
Bildmetrikaggregation. Eine Maske allein beweist noch keine 3D-Geometrie.

### Zwischenstand B: COLMAP und ideale Bilddomäne

**Einbauort:** Kapitel Konzept oder Umsetzung direkt nach der Erklärung des
Maskenwarps.

**Panel:** Rohbild, undistortiertes/ideales Bild, Rohmaske und gewarpte ideale
Maske; optional Kameramodelle beziehungsweise Sparse-Modell.

**Textaussage:** STS und Mesh arbeiten in der idealen Bilddomäne. Bild und Maske
müssen dieselbe COLMAP-Abbildung verwenden. Nearest-Neighbor-Warp erhält die
binäre Maskensemantik.

### Zwischenstand C: STS-Training und Objektfilterung

**Einbauort:** Kapitel Umsetzung, Abschnitt STS-/Gaussian-Datenvertrag.

**Panel:** STS-Checkpoint/Rendering, Full-Scene-Splat, gefilterte Objektwolke
und `point_cloud_filtered_opacity999999.ply` beziehungsweise dessen Ansicht.

**Textaussage:** Die Maske wird zur Objektzuordnung der Gaussians verwendet.
Die Hochopazitätskopie ist eine geometrieorientierte Initialisierung und keine
Messung physikalischer Transparenz.

### Zwischenstand D: Meshroute A versus SuGaR-Coarse

**Einbauort:** Kapitel Ergebnisse, vor der quantitativen Matrixgrafik.

**Panel:** Route-A-Coarse-Mesh, SuGaR-Coarse-Mesh und möglichst dieselbe Ansicht
oder dasselbe Kamerapaar.

**Textaussage:** Route A erhält die STS-Gaussians direkt; SuGaR-Coarse ist eine
separate Vergleichsroute. Sichtbare Unterschiede werden als qualitative
Routenunterschiede beschrieben, nicht als absolute Genauigkeit.

### Zwischenstand E: Centerline und Postprocessing

**Einbauort:** Kapitel Ergebnisse, unmittelbar vor dem Fazit der PA.

**Panel:** lokales Mesh, DGtal-Skelett beziehungsweise vereinfachte Centerline,
B-Spline und georeferenzierter GeoJSON-Auszug.

**Textaussage:** Die gesamte technische Kette bis zur Centerline funktioniert.
Der aktuelle lokale/synthetische beziehungsweise fallback-basierte
Georeferenzierungsstand ist kein Nachweis realer geodätischer Genauigkeit.

### Zwischenstand F: Fehlerfall

**Einbauort:** kurzer Abschnitt in Umsetzung oder Diskussion, nicht als eigene
lange Fehlerchronik.

**Geeignete Beispiele:** leere Eval-Maske, Dateinamens-/Stem-Fehler oder
SuGaR-Import-/Tensorlayoutfehler. Jeweils mit einem Vorher-/Nachher-Screenshot
oder Logausschnitt.

**Struktur:** Problem → technische Ursache → Änderung → erneuter Nachweis →
verbleibende Einschränkung.

## 6. Konkrete PA-Reihenfolge

1. Einleitung: Ziel, Eigenleistung, Abgrenzung zur BA.
2. Grundlagen: nur COLMAP, Masken, STS/GS, SuGaR-Coarse, Mesh, Centerline und
   objektmaskierte Metriken.
3. Konzept: Datenfluss und Domänentrennung mit Zwischenstand B.
4. Umsetzung: Containerverträge, SAM3 mit Zwischenstand A, STS mit Zwischenstand
   C, Postprocessing mit Zwischenstand E.
5. Versuchsaufbau: Matrixfaktoren, Erfolgskriterien und getrennte Stage-Quellen.
6. Ergebnisse: End-to-End-Panel, Route-A-/SuGaR-Coarse-Vergleich, zwei
   Übersichtsmetriken und höchstens eine Diagnosegrafik.
7. Diskussion: technische Robustheit, Fehleranalyse, Grenzen der Bildmetriken,
   keine reale Geometrieaussage.
8. Fazit/Ausblick: PA-Ergebnis und präziser BA-Plan.

## 7. BA-Plan: neue Daten und neue Grafiken

Die BA sollte die PA nicht nur mit mehr Matrixläufen wiederholen. Sie sollte
mit realen Datensätzen eine neue Referenzebene einführen:

1. Drohnenaufnahme an einer realen linearen Trasse;
2. definierte Flughöhen, zum Beispiel 5 m, 10 m und 15 m;
3. Nadir- und Oblique-Aufnahmen;
4. dokumentierte Überdeckung und konstante Kameraparameter;
5. unabhängige GCP-/GNSS-Messung sowie GNSS-Referenz der Centerline;
6. feste Trainings-/Evaluationssplits;
7. Wiederholung der begründeten Route-A-Baseline und ausgewählter
   SuGaR-Coarse-Vergleiche;
8. Centerline-RMSE, maximale/Hausdorff-Distanz, Vollständigkeit und
   Ausreißer-/Abtragungsanalyse;
9. erst danach Bildmetriken, Laufzeit und gegebenenfalls Kosten vergleichen.

### BA-Grafiken

- Aufnahmeplanung mit Flugbahn, Flughöhe, Nadir/Oblique und GCPs;
- reale Bild-/Maskenbeispiele je Aufnahmeparameter;
- COLMAP-Registrierung und GCP-Restfehler;
- Mesh- und Centerline-Vergleich zur GNSS-B-Spline-Referenz;
- RMSE-/Hausdorff-Verteilungen;
- Parameter-/Geometrie-Matrix;
- ergänzend STS-/SuGaR-Bildmetriken und Laufzeit.

Damit werden in der BA neue wissenschaftliche Grafiken erzeugt, statt die PA-
Grafiken nur ausführlicher zu kommentieren.

## 8. Empfohlenes Seitenbudget

### PA-Haupttext

Ziel: **15–25 reine Textseiten**; die aktuelle 52-seitige Fassung bleibt ein
Arbeitsmaster mit Abbildungen und Anlagen, nicht die Zielgröße des Haupttexts.

| Abschnitt | Ziel |
|---|---:|
| Einleitung und Abgrenzung zur BA | 1,5–2 Seiten |
| Grundlagen | 2,5–3 Seiten |
| Konzept/Domänentrennung | 2–2,5 Seiten |
| Umsetzung und Zwischenstände | 3–4 Seiten |
| Versuchsaufbau/Evaluationsregeln | 2–2,5 Seiten |
| Ergebnisse | 3–4 Seiten |
| Diskussion/Grenzen | 2–2,5 Seiten |
| Fazit/Ausblick | 1–1,5 Seiten |
| **Summe** | **17–22 Seiten** |

### BA-Haupttext

Das Exposé sieht eine ungefähr zehnwöchige BA mit 15 ECTS vor. Die konkrete
Seitenvorgabe ist vor Abgabe mit dem Studiengang zu bestätigen; als interne
Planung sind **ca. 35–50 reine Textseiten** für die BA angemessen, sofern der
THWS-Zielrahmen oder die Betreuung keine andere Vorgabe macht. Die BA sollte
nicht einfach die PA aufblähen, sondern neue reale Daten, Referenzen und
Geometriemetriken enthalten.

## 9. Arbeitsreihenfolge ab jetzt

### Phase 1: PA fokussieren

- Arbeitsmaster markieren und Haupttext-/Anlagentrennung festlegen.
- Arbeitsfrage und Abgrenzung einsetzen.
- sechs Zwischenstand-Screenshotgruppen auswählen.
- maximal fünf bis sechs Hauptgrafikgruppen festlegen.
- Matrixinterpretation auf Beobachtung plus Aussagegrenze kürzen.

### Phase 2: PA-Nachweise schließen

- ein konsistentes End-to-End-Panel fertigstellen;
- fehlende Screenshot-Beschriftungen und Quellen ergänzen;
- Route A und SuGaR-Coarse mit identischer Bild-/Kameraansicht vergleichen;
- Fehlerfall mit Vorher/Nachher-Nachweis dokumentieren;
- Anlagenindex und digitale Grafikdatengrundlage verlinken.

### Phase 3: PA-Abgabe vorbereiten

- Haupttext auf 17–22 Seiten ohne Anlagen kürzen;
- vollständige Grafikserie und JSON/CSV in digitale Anlagen verschieben;
- keine historische Vollmatrix als geometrische Rangliste formulieren;
- PA-Build, Referenzen, Abbildungsnummern und Seitenbudget prüfen.

### Phase 4: BA vorbereiten

- reale Trasse und GNSS-/GCP-Messung planen;
- Aufnahmeparameter und Ground Truth vor dem Lauf festlegen;
- Route-A-Baseline und wenige kontrollierte BA-Varianten definieren;
- Geometriemetriken und Toleranzkriterien vorab implementieren;
- BA-Matrix erst nach erfolgreichem Golden Run skalieren.

## 10. Klare Entscheidung

Ja: Die vorhandenen Matrixergebnisse sollten in der PA **weniger stark
interpretiert** werden. Sie bleiben als Nachweis für technische Funktion,
Reproduzierbarkeit, Fehleranalyse und getrennte Renderingmetriken relevant.

Die BA sollte mit realen Datensätzen neue Matrixläufe und vor allem neue
Geometriegrafiken erzeugen. Der zentrale Übergang lautet:

> PA: „Die Pipeline ist technisch robust und reproduzierbar aufgebaut.“
>
> BA: „Die Pipeline erzeugt unter realen Aufnahmebedingungen eine geometrisch
> messbar geeignete Centerline und erfüllt beziehungsweise verfehlt die
> definierte Toleranz nachvollziehbar."
