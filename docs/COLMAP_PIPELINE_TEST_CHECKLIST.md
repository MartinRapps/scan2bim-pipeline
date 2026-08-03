# COLMAP- und Pipeline-Testcheckliste

Diese Checkliste dokumentiert den nächsten reproduzierbaren Testlauf. Sie trennt
die bestätigte COLMAP-Konfiguration von der späteren FHD-Studie für SAM3/STS.

## 1. Testziel

- [ ] COLMAP-Konfiguration mit 720p und 5 FPS reproduzieren
- [ ] GCP-Registrierung über die UI durchführen
- [ ] Transformationsmatrix und Anchor getrennt speichern
- [ ] Besten COLMAP-Lauf vollständig durch STS, SuGaR und Postprocessing führen
- [ ] Ergebnis gegen GNSS-/Referenzdaten bewerten
- [ ] FHD-SAM3/STS-Test separat planen und nicht mit dem COLMAP-Test vermischen

## 2. Festgelegte COLMAP-Baseline

```text
Kameramodell:          SIMPLE_RADIAL
Frame-Aufloesung:      1280x720
Frame-Rate:            5 FPS
SIFT-Merkmale:         4096
SIFT-Peak-Threshold:   0.003
Sequential-Overlap:    15
Guided Matching:       aus (0)
COLMAP:                4.1.1
Betriebssystem:        Windows 11
GPU:                   keine, CPU-only-COLMAP
```

## 3. Vor dem Lauf

- [ ] Originalvideo und GCP-Datei vorhanden
- [ ] Ausreichend Speicherplatz vorhanden
- [ ] Alte `data/02_frames`, `data/03_masks` und `data/04_sfm` bewusst gesichert oder gelöscht
- [ ] Eine eindeutige Run-ID vergeben, z. B. `colmap_5fps_720p_sift4096`
- [ ] COLMAP-Version, FFmpeg-Version und Hardware notiert
- [ ] `FRAME_PROFILE_SCOPE=all` für einen vollständigen Lauf gesetzt

## 4. Frame-Profil

- [ ] Frame-Scope bei der Abfrage mit `all` bestätigt
- [ ] Bei Unsicherheit `EXPLAIN` eingeben und Erklärung dokumentieren
- [ ] Prüfen, dass der erzeugte Frame-Satz tatsächlich 1280x720 und 5 FPS besitzt
- [ ] Anzahl erzeugter Frames notieren
- [ ] Prüfen, dass alle Dateinamen eindeutig und fortlaufend sind

## 5. COLMAP-Konfiguration

- [ ] `SIMPLE_RADIAL` ausgewählt
- [ ] `4096` SIFT-Merkmale ausgewählt
- [ ] Sequential Overlap `15` ausgewählt
- [ ] Guided Matching `0` ausgewählt
- [ ] COLMAP-Lauf vollständig beendet
- [ ] Registrierungsquote prüfen, Ziel: 100 Prozent oder mindestens 90 Prozent
- [ ] Anzahl der Teilmodelle prüfen, Ziel: ein dominantes Modell ohne unbemerkten Split
- [ ] Anzahl 3D-Punkte notieren
- [ ] Punkte pro registriertem Bild notieren
- [ ] Mittlere Track-Länge notieren
- [ ] Beobachtungen pro Bild notieren
- [ ] Mittleren und möglichst 95%-Reprojektionsfehler notieren
- [ ] Gesamtlaufzeit und Speicherbedarf notieren
- [ ] `cameras.txt` und `images.txt` für die GCP-UI erzeugen

## 6. GCP-Daten

- [ ] `gcp_coordinates.csv` mit eindeutigen IDs vorhanden
- [ ] UTM-Koordinaten korrekt bezeichnet und geprüft
- [ ] Anchor zunächst auf den ersten GCP setzen
- [ ] Separaten Anchor-Wert kontrollieren
- [ ] GCP-Liste in der UI laden oder manuell eingeben
- [ ] GCP-Tabelle speichern
- [ ] GCP-Liste bestätigen
- [ ] Prüfen, dass `gcp_relative.csv` aus Tabelle minus Anchor neu erzeugt wurde
- [ ] Prüfen, dass `anchor.txt` den gewünschten separaten Anchor enthält

## 7. GCP-Bildmarkierung

- [ ] Mindestens 4 GCPs auswählen
- [ ] Jeden GCP in mindestens 5 registrierten Bildern markieren
- [ ] Unterschiedliche Kamerastandpunkte verwenden, nicht nur benachbarte Frames
- [ ] Gute Parallaxe zwischen den Beobachtungen sicherstellen
- [ ] Markerzentrum mit Zoom und Fadenkreuz anklicken
- [ ] Beobachtungsanzahl pro GCP kontrollieren
- [ ] GCPs mit weniger als 5 Beobachtungen nicht für die Matrix verwenden
- [ ] Bei großen Reprojektionsfehlern einzelne Markierungen korrigieren

## 8. Matrixberechnung

- [ ] Mindestens 4 GCPs besitzen jeweils mindestens 5 Beobachtungen
- [ ] Matrixberechnung lokal oder über Container E starten
- [ ] `data/04_sfm/matrix.txt` vorhanden
- [ ] `data/04_sfm/gcp_report.json` vorhanden
- [ ] Reprojektionsfehler pro GCP prüfen
- [ ] Fit-Residual pro GCP prüfen
- [ ] Gesamt-RMSE und Maximalresiduum notieren
- [ ] Matrix und Report unter der Run-ID archivieren

## 9. Vollständiger Downstream-Lauf

- [ ] Exakt passende SAM3-Masken für denselben Frame-Satz vorhanden
- [ ] STS mit dokumentierten Iterationen und identischem Maskensatz starten
- [ ] SuGaR mit identischen Parametern starten
- [ ] Mesh-Export und Ausgabeordner unter eindeutiger Run-ID speichern
- [ ] DGtal-Centerline extrahieren
- [ ] B-Spline- und GeoJSON-Export erzeugen
- [ ] Georeferenzierte Centerline gegen GNSS-Referenz prüfen
- [ ] Centerline-RMSE berechnen
- [ ] Hausdorff-Distanz berechnen
- [ ] GCP-/Transformationsresiduen dokumentieren
- [ ] Prüfung gegen ±10-cm-Ziel durchführen

## 10. Optionale Vergleichsläufe

Diese Läufe werden erst nach der Baseline durchgeführt:

- [ ] 10 FPS / 720p / Plain-SIFT 4096
- [ ] CRF18 mit exakt denselben COLMAP-Parametern
- [ ] CRF28 mit exakt denselben COLMAP-Parametern
- [ ] 5 FPS / 1080p als Auflösungskontrolle
- [ ] 8192 SIFT-Merkmale nur als COLMAP-Sensitivitätslauf
- [ ] Guided Matching 4096 nur als Zusatzablation

## 11. Metriken für STS/SuGaR

- [ ] PSNR auf einem festen, nicht zum Training verwendeten View-Split
- [ ] SSIM auf demselben View-Split
- [ ] LPIPS auf demselben View-Split
- [ ] Maskierte und unmaskierte Werte getrennt dokumentieren
- [ ] Anzahl Gaussians als `#G(M)` dokumentieren
- [ ] PLY-/Checkpoint-Größe dokumentieren
- [ ] Training- und Meshingzeit dokumentieren
- [ ] Peak-VRAM und Peak-RAM dokumentieren
- [ ] Rendering-FPS mit fester Hardware und fester Auflösung dokumentieren

## 12. Wirtschaftlichkeit

- [ ] Frame-Extraktionszeit
- [ ] COLMAP-Zeit
- [ ] STS-Trainingszeit
- [ ] SuGaR-Zeit
- [ ] Postprocessing-Zeit
- [ ] Manuelle GCP-Zeit
- [ ] Wiederholungs-/Fehlerrate
- [ ] Speicherbedarf
- [ ] Energieverbrauch oder belastbare Hardware-Stundensätze
- [ ] Kosten pro erfolgreicher Szene
- [ ] Prüfen, ob die Variante die geometrische Toleranz erfüllt

## 13. Ergebnisentscheidung

Eine Variante wird nur dann als Produktionskandidat übernommen, wenn sie:

- [ ] eine ausreichende COLMAP-Registrierungsquote besitzt
- [ ] keinen unbemerkten Multi-Model-Split erzeugt
- [ ] reproduzierbare Reprojektionswerte liefert
- [ ] die benötigte Objektgeometrie für STS/SuGaR unterstützt
- [ ] die Centerline-Toleranz erfüllt oder deren Nichterfüllung erklärt
- [ ] einen vertretbaren Zeit-, Speicher- und Kostenaufwand besitzt

## 14. FHD-Studie für SAM3/STS

Die FHD-Studie ist ein separater Versuchsblock:

- [ ] 1920x1080 für SAM3/STS verwenden
- [ ] passende SAM3-Masken für genau diesen Frame-Satz erzeugen
- [ ] gleiche STS-/SuGaR-Parameter wie bei der 720p-Baseline verwenden
- [ ] nur die Auflösung beziehungsweise das klar definierte Frame-Profil variieren
- [ ] PSNR, SSIM, LPIPS und Centerline-Metriken vergleichen
- [ ] keine Ergebnisse aus dem FHD-Block als direkte COLMAP-Baseline verwenden
