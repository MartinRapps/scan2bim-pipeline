# Bewertung der PA nach PA/Zielrahmen.md – Befund und To-Do-Liste

> Stand: 22.08.2026 · Bewertungsgrundlage: `PA/build/pa.pdf` (68 S., Build vom 22.08.2026 18:52),
> sämtliche Kapitel in `PA/sections/`, Anhänge in `PA/appendices/`, `references.bib`,
> Build-Log/Toc sowie die tatsächliche Datenlage im Repo (`data/10_runs/`, `docs/grafiken/`, Git-/Submodul-Stände).

---

## 1. Gesamteindruck

Die Arbeit ist **inhaltlich weit fortgeschritten und methodisch ungewöhnlich redlich**: Sie beantwortet
alle 12 Zielkontrollfragen aus Zielrahmen §8, hält die ±10-cm-Abgrenzung durchgängig ein und trennt
sauber zwischen Zwischenmetriken und vollständigen Läufen. Die größten Risiken liegen **nicht im Text,
sondern in der Abgabelogistik**: fehlende Golden-Run-Belege, Anlagenpfade, die so nicht mehr existieren,
ein widersprüchlicher Inline-Vollauf-Status über fünf Textstellen hinweg, sowie Umfang
(≈39 Seiten vs. Richtwert 15–25).

---

## 2. Kriterienbewertung (Gut / Ausbaufähig / Ungenügend)

### ✅ Gut (kein Handlungsbedarf)

| # | Befund | Zielrahmen-Bezug |
|---|---|---|
| G1 | Kapitelgliederung entspricht **exakt** der Zielgliederung §3.3 (9 Hauptkapitel, max. 2 Gliederungsebenen) | §3.2/§3.3 |
| G2 | Wissenschaftliche Redlichkeit: negative Ergebnisse systematisch dokumentiert (`appendices/appendix_robustheit.tex`, Vierfeld-Ablation, SuGaR-Renderroute-Fehler), Fehlermuster „Ursache → Korrektur → Erkenntnis" | §2.4 vollständig erfüllt |
| G3 | Keine einzige Überinterpretation: PSNR/SSIM/LPIPS konsequent als Ansichtsmetriken gekennzeichnet; Translation-Fallback nie als Genauigkeit verkauft; PINHOLE-Lauf als Ablation entlarvt | §5.2, §8 (Fragen 7, 8, 11) |
| G4 | Forschungsfragen (1.3) werden in 8.8 explizit und ehrlich beantwortet – inkl. „nicht monoton", „kein Kausalnachweis" | §1.2 |
| G5 | Metrikdefinitionen mit Formeln (maskiertes MSE/PSNR, SSIM-Fenstereinschränkung ehrlich diskutiert in `02_grundlagen.tex:296`) | §2.3 |
| G6 | Anlagenindex ist konkret (Pfad + Zweck statt „siehe Anlagen") – Konzept erfüllt §2.2, nur die Umsetzung stimmt nicht mehr (→ U1) | §2.2 |
| G7 | KI-Erklärung im Deckblattteil + Anhang KI-Dokumentation vorhanden | §5.5 |
| G8 | Build gesund: `pa.pdf` (68 S.) aktueller als alle Quellen, **0** undefined references/citations, nur 4 Overfull-Boxen | §7 |
| G9 | Abbildungs- (17) und Tabellenverzeichnis (13) vorhanden (>3-Schwelle erfüllt) | §3 Punkt 8/9 |

### 🟡 Ausbaufähig (solide angelegt, aber verbesserbar)

| # | Befund | Beleg |
|---|---|---|
| A1 | **Umfang**: Haupttext endet auf S. 39 (vor Anhang) → deutlich über dem 15–25-Seiten-Richtwert; mehrere Inhalte stehen doppelt/tripel | `pa.toc`, s. To-do 7 |
| A2 | **Kurzfassung ohne Ergebnisse**: nennt Methode + Abgrenzung, aber keine wesentlichen Resultate/Zahlen | `main.tex:102-113` vs. §3.1 |
| A3 | Terminologie uneinheitlich: `SAM~3.1` vs. `SAM3`; `qhd` vs. `QHD` (sogar innerhalb von `06_ergebnisse.tex`); `SIMPLE\_RADIAL` vs. `SIMPLE-RADIAL` | §5.1 Konsistenz |
| A4 | Zahlenformat: Anhang A nutzt **Punkt**-Dezimaltrenner + englische Einheit (`0.693 px`), Haupttext Komma; Tausendertrennzeichen fehlt (`139449`, `133723`, `890377`); PSNR-Nachkommastellen schwanken (21,434 / 29,62 / 21,38 dB) | `appendix_colmap.tex:16-20`, `06_ergebnisse.tex:220`, §5.2 |
| A5 | Laufzeiten (34/27/19 min) stehen **dreimal** fast wortgleich: `03_konzept.tex:157`, `04_implementierung.tex:197`, nochmal in 7.5; Maskenhierarchie dreimal (Grundlagen 3.1, Konzept, 5.1); Route-A-Begründung viermal | Redundanzen |
| A6 | Literaturverzeichnis steht **nach** den Anhängen (`main.tex:143-144`) und LoF/LoT vorne – Zielrahmen §3 sieht Literatur **vor** Abbildungs-/Tabellen-/Anlagenteil | §3 Reihenfolge |
| A7 | `\nocite` zwingt 5 Quellen ins Verzeichnis, davon `scan2bimImplementation` und `matrixRestResults` **nie im Text zitiert** | `main.tex:143` vs. §5.4 |
| A8 | Offene Platzhalter: `[Martin Rapps]`, `[08.09.2026]` in Klammern, `\today` statt fixem Datum auf Titelblatt | `main.tex:32-37, 80` |

### ❌ Ungenügend (muss behoben werden, sonst Abgaberisiko)

| # | Befund | Beleg |
|---|---|---|
| U1 | **Anlagenindex beschreibt nicht existierende Pfade**: `matrix_full_pipe`, `matrix_rest`, `matrix_repeat_20260812`, `matrix_sugar_followup_12` liegen **nicht** unter `data/10_runs/` (nur SuGaR-Nebenprodukte unter `third_party/SuGaR/data/sugar_output/`). Prüfer findet leere Hände → verletzt §2.2 und Kriterium „Vollständigkeit der abgegebenen Daten" | `appendix_anlagenindex.tex:32-34`, `results/README.md` |
| U2 | **Widerspruch Inline-Vollauf/Maskenwarp an 5 Stellen**: Fazit + Implementierung sagen „jetzt gefixt" (`08_fazit.tex:8`, `04_implementierung.tex:213`), Konzept + Diskussion + Repro-Anhang sagen „fehlt noch" (`03_konzept.tex:117`, `07_diskussion.tex:14`, `appendix_repro.tex:8`) – direkter logischer Widerspruch im Dokument | §5.1, §1.2 |
| U3 | **Autopilot-Lücke ist längst geschlossen, aber PA kennt es nicht**: 6 archivierte Autopilot-Läufe vom 18./20.08. mit `AUTOPILOT: true`, Status SUCCESS (`data/10_runs/Alurohr_THWS_*`) existieren; PA behauptet fälschlich, Nachweis stehe noch aus (`06_ergebnisse.tex:27`, `07_diskussion.tex:129`, Erfolgskriterium 6 in `05_versuchsaufbau.tex:218`) – unbegründete Selbstschwächung | §2.2 |
| U4 | **Neuer 19-GB-Qualitätsvergleichslauf komplett unerwähnt**: `matrix_qualitaetsvergleich_20260818` (alle 3 Kameramodelle × Route A × 3 Auflösungen + SuGaR-Arme, failed=0, frische Metriken z. B. 29,72 dB / 0,930 SSIM) taucht in der PA nullmal auf – wäre zugleich Golden-Run-Kandidat für den offenen End-to-End-Abbildungsnachweis (7.1 „Offener Abbildungsnachweis") | `06_ergebnisse.tex:12-17` |
| U5 | **Versionsdreieck offen**: Parent-Gitlink `ecda7ef` ≠ Fork-Checkout `eca4ea1` ≠ Arbeitsbaum ≠ SuGaR-Commit der neuen Läufe `a0fc37b` (`run.md`); Text gibt es selbst zu (`04_implementierung.tex:97-103`) – ohne Konsolidierung sind Matrixergebnisse nicht reproduzierbar zuzuordnen | §2.1, §2.2 |
| U6 | Deckblatt-Platzhalter in eckigen Klammern – würde eingereicht, wirkt die Arbeit unfertig | `main.tex:32-37` |

---

## 3. Priorisierte To-Do-Liste

Priorität: **P0 = Abgabeblocker**, P1 = bewertungsrelevant, P2 = Feinschliff.
Kategorie: 🔴 ungenügend / 🟡 ausbaufähig.

### P0 – vor allen anderen Schritten

| Nr | Kat | Aufgabe | Lösungsvorschlag |
|----|-----|---------|------------------|
| 1 | 🔴 | **Golden Run wählen und End-to-End-Panels erzeugen** (schließt den offenen Abbildungsnachweis in 7.1) | Nutze `matrix_qualitaetsvergleich_20260818` (U4): exportiere Rohframe, default/middle-Maske, ideale Domäne, Sparse-Punkte, Splat, Mesh, Centerline **aus einem einzigen Lauf** in dieselbe Ansicht, baue Panel analog `pa_panel_alurohr_endprodukt.png`. Bildunterschrift mit Run-ID + Commit versehen. |
| 2 | 🔴 | **Anlagenindex mit Realität abgleichen** (U1) | a) Kompaktarchive der alten Batches wiederherstellen oder Prüfsummen/Backuport dokumentieren; b) Index um `matrix_qualitaetsvergleich_20260818` und `Alurohr_THWS_*` ergänzen; c) für jeden Eintrag Zeile „Status/Prüfsumme/Standort extern?" ergänzen. Ziel: jeder Pfad klickt sich physisch nachvollziehen. |
| 3 | 🔴 | **Inline-Vollauf-Widerspruch auflösen** (U2) | Prüfe im Code, ob der Warp im Inline-Pfad wirklich läuft. Dann: `03_konzept.tex:115-124` und `appendix_repro.tex:7-9` auf den Stand von Fazit/Implementierung bringen – oder umgekehrt. Eine Version muss überall gelten. Danach `grep -n "Maskenwarp\|Warp"` über alle .tex als Gegenprobe. |
| 4 | 🔴 | **Autopilot-Nachweis einziehen statt versprechen** (U3) | In 7.1, 8.5, 8.8 und Erfolgskriterium 6 (5.9) die 6 archivierten Autopilot-Läufe (Run-IDs, Datum, Status SUCCESS) als Nachweis zitieren. Restriktion ehrlich benennen: Archive enthalten Logs/Manifeste, aber keine Renderartefakte → ggf. einen der Läufe als Golden Run neu archivieren (verbindet sich mit To-do 1). |
| 5 | 🔴 | **SuGaR-Versionsdreieck konsolidieren** (U5) | Arbeitsbaum committen → Submodul-Commit `eca4ea1+a0fc37b` vereinigen, Parent-Gitlink aktualisieren, `SUGAR_REF` im Compose setzen, Diff als Datei nach `PA/appendices/` bzw. Anlagenband. Dann in `04_implementierung.tex:97` den finalen Stand nennen. Erst danach den finalen PDF-Build erzeugen. |
| 6 | 🔴 | **Deckblatt finalisieren** (U6/A8) | Klammern entfernen, fixes Abgabedatum statt `\today`, offizielle THWS-Erklärungsformel gegenzeichnen, Fakultätsbezeichnung gegen aktuelle Ordnung prüfen. |

### P1 – Qualität und Bewertungsrelevanz

| Nr | Kat | Aufgabe | Lösungsvorschlag |
|----|-----|---------|------------------|
| 7 | 🟡 | **Haupttext auf ≤ ~28–30 Seiten kürzen** (A1/A5) | Kürzungsliste mit bestem Aufwand/Nutzen: (a) Preset-Laufzeiten nur 1× in 7.5 behalten, in 4.5/5.4 nur querverweisen; (b) Maskenhierarchie-Details nur in Grundlagen, 5.1 auf 3 Sätze; (c) Abschnitt 5.7 (Zählerstände-Tabelle) komplett in Anhang D verschieben; (d) 7.2 visuelle Details straffen, Panels sprechen im Anhang C für sich; (e) Tabelle `tab:bildablagen` halbieren. Ziel ≈ −10 Seiten ohne Informationsverlust. |
| 8 | 🟡 | **Kurzfassung um Ergebnisse ergänzen** (A2) | 3 Sätze einfügen: „12/12 Follow-up-Läufe erfolgreich; Produktionsstand OPENCV/5 FPS/720p/Route A (29,62 dB PSNR objektmaskiert); 240/240 Bilder registriert; Autopilot- und Matrixläufe archiviert." Grenzsatz bleibt. |
| 9 | 🟡 | **Terminologie & Zahlen vereinheitlichen** (A3/A4) | Globale Entscheidungen treffen: immer „SAM 3.1", immer „QHD", immer `SIMPLE_RADIAL` (Codebezug) oder immer Schreibweise mit Bindestrich – per sed einmal ziehen. Dezimaltrenner in Anhang A auf Komma, `px` → `Pixel`, Tausenderpunkte setzen (`139.449`). PSNR auf 1–2 Nachkommastellen festlegen (Begründung: Streuung der Einzelansichten rechtfertigt keine dritte). |
| 10 | 🟡 | **Literaturverzeichnis-Ordnung + \nocite** (A6/A7) | `\printbibliography` **vor** `\appendix` ziehen; LoF/LoT-Platzierung mit Prüfer absprechen (Zielrahmen §3 will sie nach der Literatur). `scan2bimImplementation` im Anlagenindex-Absatz zitieren (`\parencite{scan2bimImplementation}`) und `matrixRestResults` in Anhang B – dann ist `\nocite` leer und regelkonform. |
| 11 | 🟡 | **Qualitätsvergleichslauf in Ergebnisse integrieren** (U4-Rest) | Kurzabschnitt in 7.4/7.5: neuer Batch bestätigt die OPENCV-720p-Produktionsentscheidung mit frischer Messreihe (failed=0). Stärkt die Reproduzierbarkeitsargumentation erheblich – die Arbeit gewinnt Substanz statt nur Seiten. |
| 12 | 🟡 | Overfull-Boxen (4×, größte 51 pt in `appendix_repro.tex` Itemize-Block) | `\sloppy` lokal oder manuelle Umbruchstelle in den langen `\texttt{}`-Pfaden; danach Neubuild und Log-Check. |

### P2 – Organisatorisches & Feinschliff

| Nr | Kat | Aufgabe | Lösungsvorschlag |
|----|-----|---------|------------------|
| 13 | 🟡 | Mit Prüfer abstimmen (Zielrahmen §9): PlagAware-Einwilligung ja/nein, Sperrvermerk, Form des Anlagenbands, finale Hauptgrafiken | Als E-Mail-Checkliste an Betreuer; Antworten direkt in `Zielrahmen.md` §9 abhaken. |
| 14 | 🟡 | Vortrag (20 min) vorbereiten | Struktur aus Zielrahmen §6.2 übernehmen; Golden-Run-Panel als Leitgrafik; 1 Folie pro Forschungsfrage aus 8.8. |
| 15 | 🟡 | Build-Hygiene | `build/` enthält Leichen (`main.*` eines zweiten Jobnamens, `*-SAVE-ERROR`, `pa_editetd.pdf` mit Tippfehlernamen, Kommentartexte). Vor der Abgabe: `build/` leeren, einen einzigen Jobnamen (`pa`) fahren, nur `pa.pdf` liefern. |
| 16 | 🟡 | Letzter Vollabgleich Text ↔ Artefakte | Die Zahl `87 Rohpunkte / 380 B-Spline-Punkte` (7.8) und alle Tabellenwerte gegen die Manifeste des final gewählten Golden Runs prüfen; Fazit-Versprechen („nochmals gegen tatsächliche Ergebnisartefakte geprüft", `08_fazit.tex:38`) tatsächlich einlösen. |

---

## 4. Empfohlene Reihenfolge

1. **To-dos 3 + 5 zuerst** (Code-/Versionsklärung) – alles Weitere baut auf feststehenden Commits auf.
2. **To-do 1** (Golden Run aus dem neuen 19-GB-Batch) – liefert Abbildungen UND schließt To-do 4 teilweise.
3. **To-do 2** (Anlagenabgleich) parallel dazu.
4. Dann Textarbeit: **7 → 8 → 9 → 10 → 11**, finaler Build, **12 + 15**.
5. **6, 13, 14, 16** in der Abgabewoche.

---

## 5. Fazit

Der Text selbst trägt bereits Note-taugliche Substanz; über die Ziellinie bringt ihn, was **um die
Arbeit herum** fehlt: konsistente Versionsangaben, ein belegbarer Golden Run und ein Anlagenband,
das hält, was der Index verspricht.
