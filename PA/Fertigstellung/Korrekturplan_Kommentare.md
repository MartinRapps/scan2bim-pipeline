# Korrekturplan: 89 Prüferkommentare aus `pa_arbeit_bearbeitet_fertig.pdf`

> Basis: Arbeitsfassung `PA/Fertigstellung/pa_arbeitsfassung/` (Branch `pa-fertigstellung`).
> Quelle: `%TEMP%\pa_kommentare_voll.txt` (vollständige Extraktion aller Highlights +
> Kommentare, 25.08.2026). Mapping über markierten Text, PDF-Seitenzahlen informativ.
>
> **Entscheidungen (25.08.2026):** Kommentare sind maßgeblich (D3-Revision); Code-Änderungen
> inkl. T5 (Submodul/Dockerfile) freigegeben; Anhang F → Kurzverweis im PDF + Indexdatei im
> Abgabeordner; KI-Dokument als separate Anlage (opencode + VS Code, LLMs je nach
> Komplexität/Kosten). Status: 🔲 offen · ✅ erledigt · 🔶 teilt/blockiert

## K1 – Löschen & Kleinkorrekturen

| Nr | S. | Maßnahme | Status |
|----|----|----------|--------|
| K1-01 | 9 | Containeranalyse raus → Rohdatei einfach beschreiben (H.264, Auflösung, FPS) | 🔲 |
| K1-02 | 13 | „supervidiert“ durch einfaches Synonym ersetzen | 🔲 |
| K1-03 | 13 | Satz zu obj_id-/STS-Objektdateien-Zuordnung löschen | 🔲 |
| K1-04 | 20 | Fußnote (Host-UID/-GID) an das tatsächliche Seitenende setzen (Layout) | 🔲 |
| K1-05 | 25 | Satz „Zielzählerangaben … historische Dateinamen“ löschen | 🔲 |
| K1-06 | 26 | Multi-View-Crop-Satz löschen (alter Stand, irrelevant) | 🔲 |
| K1-07 | 29 | Wiederholung „Importpfad und Tensorlayout … zwölf Läufe“ kürzen (3. Wiederholung) | 🔲 |
| K1-08 | 29 | Abschnitt 5.7 „Historische SuGaR-Zählerstände“ komplett streichen (inkl. Tabelle) | 🔲 |
| K1-09 | 33 | Ansichtsmetrik-Wiederholung kürzen (Hinweisprinzip: 1× Hauptort + Querverweis) | 🔲 |
| K1-10 | 45 | Punktwolken-Absatz = Wiederholung von 7.2 → kürzen/streichen | 🔲 |
| K1-11 | 45 | PINHOLE-Absatz = Wiederholung → kürzen | 🔲 |
| K1-12 | 46 | „Zeit/Qualitätsmatrix im Anhang“-Satz: Matrix ist in Ausarbeitung → Anhangsbezug streichen | 🔲 |
| K1-13 | 47 | „Replay runner“ generisch raus (nicht anders als Matrixrun) | 🔲 |
| K1-14 | 47 | „Matrix-/Smoke-/Replaypfad“ → normaler Inline-Lauf mit gemeint | 🔲 |
| K1-15 | 47 | Fazit: Replay-Nennung weglassen; Maskenwarp „bereits nachgewiesen“ statt „separater Nachweis sinnvoll“ | 🔲 |
| K1-16 | 47 | Fazit: Folgematrix-Satz löschen („klingt nach KI-Antwort“) | 🔲 |
| K1-17 | 48 | Fazit: Block „endgültige Kurzfassung … nochmals geprüft“ löschen | 🔲 |
| K1-18 | 49 | COLMAP-Anhang: Satz „Alle fünf dokumentierten Läufe registrierten … archiviert“ löschen | 🔲 |

## K2 – Nutzerformulierungen einbauen (wörtlich/adaptiert)

| Nr | S. | Maßnahme | Status |
|----|----|----------|--------|
| K2-01 | 8 | Eigenleistung präzisieren: eigene Maskenlogik (dilation/erosion → EIN segmentiertes Objekt statt SAM2+CLIP-Multiobjekt); SAM~3.1-Speedup mit Meta-Blog-Quelle belegen | 🔲 |
| K2-02 | 10 | Produkte bewerten: B-Spline = Produkt; CSV ohne Eigenaussage (raus); Gaussians+Mesh wichtige Produkte (georeferenzierbar, ESRI-Suite) | 🔲 |
| K2-03 | 10 | GCP-Dateien: „nur Approximationen der Wirklichkeit, erstellt/verwendet zum Testen der Transformation“ | 🔲 |
| K2-04 | 11 | Konditionierungssatz durch Nutzerformulierung ersetzen (Freiheitsgrade/Merkmalverteilung/Overfitting) | 🔲 |
| K2-05 | 12 | Iterationssatz durch Nutzerformulierung ersetzen (5000+2000, Trainingsfortführung) | 🔲 |
| K2-06 | 12 | STS ↔ SuGaR sauber trennen bei „maskennutzenden Verlustpfaden des Coarse-Trainings“ (SuGaR!) | 🔲 |
| K2-07 | 14 | Kompletter Neuer SuGaR-/Loss-Block: Nutzer-Langfassung (Poisson-Fußnote kazhdan2006poisson, maskierter RGB-Verlust Gl. eq:masked-rgb-loss, M(p), ε=10⁻⁷, DN erst >9000) ersetzt alten Absatz | 🔲 |
| K2-08 | 15 | MSE-Formel: I und Î definieren (gerendertes vs. Ground-Truth-Bild am Pixel p) | 🔲 |
| K2-09 | 20 | Fork-Abschnitt 5.2 komplett neu nach Nutzervorlage (Zielkonflikt, Teilbild 2, Renderpfad-Fehler vs. maskiertes Training) – integriert K2-06/S.20a | 🔲 |
| K2-10 | 22 | Maskenablagen umformulieren nach Nutzervorlage (03_masks Primärdaten, multiview_masks_* = STS-Kompatibilitätskopien Objekt-ID 000, *_merged flüchtig) | 🔲 |
| K2-11 | 25 | Panel-Beschreibung vervollständigen (Satz fertigstellen + Bilder 2–7 einzeln erklären: Floater/Farbfilterung, schlechte Aufnahme, Sugar vor Fork, falsch übergebener Splat, 15k-Coarse ohne DN, perfektes Segment → Splat → Punktwolke) | 🔲 |
| K2-12 | 25 | „Invertierte Splats“ korrigieren: Auswahl des segmentierten Trainings war invertiert (Fehlorientierung des Bildes), nicht die Splats | 🔲 |
| K2-13 | 25 | „ungesehene Test-Kameras“ → „nicht im Training enthaltene Splats/Kameras“ präzisieren | 🔲 |
| K2-14 | 45 | Auflösungsvergleich „idiotensicher“ ergänzen: Downsampling=Tiefpass (Hochfrequenzfehler weg), mm-pro-Pixel-Argument für BIM/Vermessung, Konsequenz: gepaarter Vergleich innerhalb derselben Auflösung, keine Rangliste | 🔲 |

## K3 – Code-Verifikation + freigegebene Änderungen

| Nr | S. | Maßnahme | Status |
|----|----|----------|--------|
| K3-01 | 15 | .pt/.ply-Rendering-Äquivalenz im SuGaR-Fork verifizieren (Code lesen) und Aussage belegen oder abschwächen | 🔲 |
| K3-02 | 18/23 | `--from`-Dispatcher: Warp-Stufe ergänzen (FREIGEGEBEN, pipeline_lib.sh) oder dokumentieren; Tex anpassen (auch S.23d „ebenso fraglich ob abgeändert“) | 🔲 |
| K3-03 | 19 | Autopilot-Preset-Logik im Code prüfen: gewähltes Preset respektiert? Tex korrigieren | 🔲 |
| K3-04 | 22a | attempts/Fallback-Logik: Argumente sammeln, Empfehlung geben, Text anpassen | 🔲 |
| K3-05 | 22c/d | „Remap-Schicht“ erklären/vereinfachen; `_attempts`-Satz konsistent zu K3-04 | 🔲 |
| K3-06 | 23e | „Stems“ erklären (Dateiname ohne Endung) oder umschreiben | 🔲 |
| K3-07 | 23f/24 | objektmaskierte Metrik + 11×11-Fensterproblem querverweisen (→ K4 SSIM-Block) | 🔲 |
| K3-08 | 24 | Poisson-Gate: Verhalten bei Verletzung + Definition gültiger Punkte/Normalen ergänzen | 🔲 |
| K3-09 | 23a/46g | Laufzeiten-Archivierung prüfen: Gesamtzeit oder STS-bis-Postprocess? Tex korrigieren | 🔲 |
| K3-10 | 23c | Bildablageorte klären (undistorted: 04_sfm? je nach Pfad unterschiedlich?) und Text/Tabelle angleichen | 🔲 |
| K3-11 | 46c | GCP-Breakpoint: existiert der noch im Code? Text korrigieren | 🔲 |
| K3-12 | 21 🔴 | T5-Versionsdreieck lösen (FREIGEGEBEN): Submodul initialisieren/prüfen → Fork committen → Parent-Gitlink → Dockerfile SUGAR_REF → Diff exportieren → Tex 04_impl:97 ff. final | 🔶 Vorbehalt VM-Stand |
| K3-13 | 46d | Autopilot-Vollauf: „wurde doch schon gemacht“ – Erfolgskriterium 6/Diskussion entsprechend (mit K5-Inventar) | 🔲 |

## K4 – Fachliche Antworten einarbeiten

| Nr | S. | Maßnahme | Status |
|----|----|----------|--------|
| K4-01 | 16 | SSIM-Block erweitern: 11×11 = Literaturstandard Wang et al. (2004) (+cite), Randpixel-Rechnung (40 px Rohr ≈ 12 % Rand bei 720p, 20 px ≈ 25 % bei Low), PSNR/SSIM nur im jeweiligen Pixelgitter | 🔲 |
| K4-02 | 16 | UTM/Translation-Frage beantworten und Text schärfen: lokale Transformation gültig; Translation auf UTM nachträglich addierbar, solange Rotation/Skalierung unverändert – vorsichtig formulieren | 🔲 |
| K4-03 | 28 | COLMAP-Voruntersuchung: Verweis auf Tabelle im Anhang A ergänzen | 🔲 |
| K4-04 | 32 | SIFT/Guided-Matching-Interpretation ehrlich formulieren (Merkmalslimit erklärt identische Punktzahl; Guided Matching fügt schwerere Matches hinzu → Reprojektionsfehler kann steigen; kein Widerspruch) | 🔲 |
| K4-05 | 37 | „intern gut angepasst“ begründen/relativieren (Reprojektionsfehler = Konsistenzmaß, kein Gütesiegel) | 🔲 |
| K4-06 | 38 | Seed 42 erklären (Reproduzierbarkeit stochastischer Schritte) | 🔲 |
| K4-07 | 38 | cm-Angaben relativieren (lokal skalierte Modelle, relative Vergleichsgrößen) + Extraktionsmethode beschreiben (je 20.000 Samples, gerichtete Mittelwerte paarweise) | 🔲 |
| K4-08 | 38 | Route B (Rasterizer-Tiefe) erklären, warum nicht Produktionsstandard | 🔲 |
| K4-09 | 43 | „Ansichtsmetriken“-Disclaimer nur 1× Hauptort, sonst Querverweis (Konsolidierung mit K1-09) | 🔲 |
| K4-10 | 43 | 87 Rohpunkte präzisieren: welcher Lauf/welche Einstellung; Verhältnis zu Anhang-C-Centerlines klarstellen (Grad-10 hier, Grad-3-glätten dort?) | 🔲 |
| K4-11 | 44 | „nicht monoton“ auflösen: bezog sich auf Metrikwerte über Konfigurationen, NICHT Maskestabilität; Satz korrigieren (Rohr wurde in jedem Frame erkannt) | 🔲 |
| K4-12 | 46a | Delta-Grafik: SuGaR stringent niedriger = zulässige Aussage; Formulierung anpassen | 🔲 |
| K4-13 | 46f | „invertierte LPIPS“ streichen → Rankingumkehr als Natur der Metrik | 🔲 |
| K4-14 | 46i | Scheitelachse vs. Centerline klären (Kontext lesen, ggf. präzisieren) | 🔲 |
| K4-15 | 47a | Abzweigungen/Ringschluss: explizit außerhalb BA-Scope stellen (lineare Objekte) | 🔲 |

## K5 – Struktur-Umbau

| Nr | S. | Maßnahme | Status |
|----|----|----------|--------|
| K5-01 | 29a | matrix_rest-Beschreibung → „welche Tests insgesamt + wo Ergebnisse (Grafiken)“ | 🔲 |
| K5-02 | 29b/d | gerichtete Distanzen + Coarse-not-Refined: Verweise auf Anhang/Grafiken ergänzen | 🔲 |
| K5-03 | 31b | Blockquote „Offener Abbildungsnachweis“ ENTFERNEN → Nachweis via Anhang C referenzieren | 🔲 |
| K5-04 | 31c/32a | Eval-Split (210/30) früher erklären (Kap. 5), in 7.x nur Erinnerung + Anhang-C-Verweis früh geben | 🔲 |
| K5-05 | 31a | Erfolgskriterium 6 gegen Nutzer-Inventar harmonisieren (followup_12, 24er-Matrix, Vierfeld, Produktionslauf, historische Tests, Autopilotläufe, Qualitätsvergleich) | 🔲 |
| K5-06 | 39b/40 | SuGaR-Boxplots + Delta + metric_vs_runtime zu den Splat-Metrik-Grafiken verschieben; Zusatzgrafik-Abschnitt aufräumen | 🔲 |
| K5-07 | 38d | 7.6-Absatz drastisch kürzen (90 % Redundanz); Abbildung 7 zur historischen Entwicklung ordnen | 🔲 |
| K5-08 | 50 | Tabelle (SuGaR-Mittelwerte) in Haupttext übernehmen; Anhang B radikal schlank/streichen | 🔲 |
| K5-09 | 65 | Anhang E (Repro): ausdünnen/streichen (Inhalte im Text mehrfach vorhanden) | 🔲 |
| K5-10 | 66 | Anhang F: Kurzverweis (1–2 Sätze) behalten; vollständigen Index als `ABGABE_Index.md` für Abgabeordner auslagern | 🔲 |
| K5-11 | 28b | Abgabe-Empfehlung: welche vollständigen Läufe liefern (Smoke, Autopilot 720p/qHD/low, Produktionslauf, Golden-Run-Arm) → Dokument im Fertigstellungsordner | 🔲 |
| K5-12 | 49b/66 | Pfade in Ausarbeitung an geplante Abgabeordnerstruktur anpassen (COLMAP_Rohberichte etc.) | 🔲 |

## K6 – Grafikarbeiten

| Nr | S. | Maßnahme | Status |
|----|----|----------|--------|
| K6-01 | 39a | pa_panel_sugar_iteration.png NEU bauen (Skript unter PA/Fertigstellung/, kein Pipeline-Code); 9200er konsistent als 9001, OHNE Dateinamen-Disclaim; Caption + Einordnung „historische Entwicklung“ | 🔲 |

## K7 – KI-Dokumentation

| Nr | S. | Maßnahme | Status |
|----|----|----------|--------|
| K7-01 | 68 | Anhang G im PDF → Kurzverweis auf separate Anlage | 🔲 |
| K7-02 | 68 | Neues Dokument `Anlage_KI-Nutzung.md`: Bereiche (Code-Erstellung/Refactoring, Vorgehen/Sparring, Text, Debugging/Auswertung, Grafikskripte), je Bereich Beispiel-Prompts + Übernahmebeschreibung; Werkzeuge: opencode + VS Code (aktuelle Versionen), LLM-Wahl je nach Aufgabenkomplexität/Kosten; Zeitraum Juni–Aug 2026 | 🔲 |

## K8 – Abschluss

Build (`pa_arbeit`) grün · Greps · Protokoll je Batch · Statusboards/UmsPlan aktualisieren · Arbeitsstand-Update · Restpunkte-Liste (Archive hochladen, Deckblatt-Daten, ggf. VM-Fork-Stand).
