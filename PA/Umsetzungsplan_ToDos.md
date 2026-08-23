# Umsetzungsplan: To-Do-Abarbeitung nach Bewertung vom 22.08.2026

> Ergänzung zu `PA/Bewertung_Zielrahmen_und_Todos.md` (Befunde G/A/U und To-dos 1–16).
> Dieses Dokument ist zugleich **Fahrplan, Arbeitsjournal und Drift-Schutz**: Es wird nach jedem
> Schritt aktualisiert und bei jedem Sitzungsstart zuerst gelesen.
>
> **Stand 23.08.2026:** Entscheidungspunkte D1–D4 sind entschieden bzw. festgelegt (§7).
> Konsequenz: **Der Haupttext wird NICHT gekürzt** (D3); Kürzungskandidaten werden nur
> markiert. Arbeitsdokumentation läuft in `PA/Fertigstellung/Arbeitsdatei_Fertigstellung.md`.

---

## 0. Anker-Dokumente (Schutz gegen Verrennen/Drift)

Bevor an einem To-do gearbeitet wird, wird der Bezug zu mindestens einem Anker hergestellt.
Alles, was sich **nicht** auf einen Anker oder ein nummeriertes To-do zurückführen lässt, wird
**nicht** umgesetzt, sondern in §6 (Backlog) notiert.

| Anker | Zweck im Prozess |
|---|---|
| `PA/Zielrahmen.md` | Verbindliche Anforderungen (§2 Nachweise, §3 Aufbau, §5 Formales, §8 Zielkontrolle). Jede Textänderung muss einen Zielrahmen-Bezug nennen. |
| `docs/Expose_PA_BA.pdf` | Ursprünglich vereinbarter Scope und Versprechen des Exposés; Schutz davor, dass beim Kürzen (To-do 7) Exposé-Zusagen verloren gehen. |
| `PA/PA_Aussagenpruefung.md` | Claim-Audit mit Statusklassen und „Verbindlicher Korrekturliste" (§5). Wird nach jeder Textänderung gepflegt: veraltete Aussagen werden dort abgehakt/neu bewertet. |
| `PA/Plan_PA_und_BA_Ergebnisstrategie.md` | Grafikplan (max. **fünf Grafikgruppen** im Haupttext, §4.1), PA/BA-Abgrenzung (§2), konkrete PA-Reihenfolge (§6). Neue Grafiken (Golden Run, To-do 1) müssen in dieses Budget passen. |
| `PA/Arbeitsstand_Langfassung.md` | Laufender Status; erhält am Ende jeder Phase einen Kurzupdate-Eintrag. |

**Sitzungsritual (jeder Start):**
1. Diesen Plan lesen, aktuellen Phasenstand prüfen.
2. `git status` + `git log --oneline -5` – nur unmittelbar nach einem erledigten To-do darf es offene Änderungen geben.
3. Genau **ein** To-do als `in_progress` markieren (hier in §4), nie mehrere parallel.

---

## 1. Dokumentationsstrategie aller Änderungen

### 1.1 Zentrales Änderungsprotokoll

Neu angelegt: `PA/Fertigstellung/Aenderungsprotokoll_Fertigstellung.md`
(abweichend zur ursprünglichen Pfadangabe bewusst im Fertigstellungsordner).
Ein Eintrag pro To-do, zwingend mit folgenden Feldern:

```
## T<n> – <Kurztitel>
- Datum / Phase
- Anker-Bezug:        Zielrahmen §x / Exposé S.x / Aussagenprüfung §y
- Geänderte Dateien:  pfad:zeilen
- Was & Warum:        1–3 Sätze
- Verifikation:       ausgeführte Prüfkommmandos + Ergebnis (siehe je To-do in §4)
- Commit:             <hash> (einer pro To-do, siehe 1.2)
- Rückwirkung:        Aussagenprüfung-Zeile(n), die aktualisiert wurden
```

### 1.2 Git-Konventionen

- **Arbeitsbranch `pa-fertigstellung`**: Alle To-do-Commits landen auf diesem Branch,
  **nicht** auf `master`. Merge nach master erst, wenn die Phase F abgeschlossen ist
  (Entscheidung zu D1: Commits ja, aber getrennt vom jetzigen Stand).
- **Ein Commit pro erledigtem To-do**, Message-Format: `T<n>: <kurzer Imperativ> (Phase <X>)`
  – Beispiel: `T5: SuGaR-Fork-Stand konsolidieren, SUGAR_REF setzen (Phase A)`
- Der Submodul-Commit (`third_party/SuGaR`) und der Parent-Commit (Gitlink-Update) sind **zwei** Commits;
  Reihenfolge: erst Fork committen, dann Parent.
- Kein Misch-Commit aus mehreren To-dos. Falls eine Datei von zwei To-dos betroffen ist,
  gewinnt die To-do-Reihenfolge aus §4; der zweite Commit enthält dann den Rest-Diff.
- Vor jedem Commit: `git diff --stat` gegen die Dateiliste im Protokolleintrag prüfen
  (Schutz vor versehentlich mitgerutschten Dateien).
- **Niemand berührt Code unter `src/`, `tools/`, `run_pipeline.sh` etc. über die To-dos hinaus** –
  Änderungen gelten nur für PA-Texte/Anhänge/Dokumentation (Nutzer-Vorgabe).

### 1.3 Pflege bestehender Dokumente (nicht nur neue anlegen)

| Dokument | Pflegeregel |
|---|---|
| `PA/PA_Aussagenpruefung.md` | Jede durch ein To-do veränderte Aussage bekommt aktualisierten Status + Datum + Verweis auf Protokolleintrag. Die „Verbindliche Korrekturliste" (§5) schrumpft sichtbar. |
| `PA/Bewertung_Zielrahmen_und_Todos.md` | Statusspalten-Ergänzung je To-do: 🔲 offen / 🔄 in Arbeit / ✅ erledigt (+ kurzes Verifikationsergebnis). |
| `PA/results/README.md`, `figures/README.md` | Werden bei T1/T2/T11 mitgepflegt (neue Batches, neue Panels), damit READMEs nicht lügen. |
| `PA/Arbeitsstand_Langfassung.md` | Ein Absatz pro abgeschlossener Phase. |

---

## 2. Baseline-Erfassung (Startzustand messen, bevor etwas geändert wird)

Zweck: Jede spätere Behauptung „besser/gefixt" wird gegen Zahlen belegt, nicht gegen Gefühl.

| Messgröße | Methode | Erwarteter Baseline-Wert |
|---|---|---|
| Haupttext-Seitenzahl | letzte arabische Seite vor Anhang A in `pa.toc` | 39–40 |
| Overfull-Boxen | `grep -c Overfull build/pa.log` | 4 |
| Undefined Ref/Cites | `grep -iE 'undefined' build/pa.log \| wc -l` | 0 (muss 0 bleiben) |
| Terminologie-Drift | `grep -rc 'SAM3' sections/` etc. (SAM3, qhd/QHD→qHD, SIMPLE-RADIAL-Varianten) | dokumentierte Ist-Zahlen |
| Dezimalpunkte im Anhang A | `grep -c '\.' appendix_colmap.tex` | dokumentieren |
| `\nocite`-Quellen ohne Zitat | manuelle Liste | scan2bimImplementation, matrixRestResults |
| Widerspruchsstellen Maskenwarp | `grep -n 'Maskenwarp\|Warp' sections/*.tex appendices/*.tex` | 5 Fundstellen (U2) |

Ergebnis landet als Tabelle in `Aenderungsprotokoll_Fertigstellung.md` unter „Baseline".

---

## 3. Phasenmodell (empfohlene Reihenfolge aus der Bewertung)

```
Phase 0  Baseline & Gerüst            (Protokoll anlegen, §2 messen)          ~0,5 h
Phase A  Code-/Versionsklärung        T3 Inline-Warp · T5 SuGaR-Dreieck       ~1–2 h
Phase B  Belage & Golden Run          T1 Panels · T4 Autopilot · T11 Teil     ~2–4 h (Rechenzeit!)
Phase C  Anlagenabgleich              T2 Index ↔ Realität                     ~1–2 h
Phase D  Textarbeit                   T7 Kürzung nur markieren · T8 Abstract · T9 Einheiten
                                      T10 Lit-Ordnung · T11 Rest              ~3–4 h
Phase E  Build & Hygiene              T12 Overfull · T15 build/ aufräumen     ~0,5 h
Phase F  Absschluss                   T6 Deckblatt · T16 Vollabgleich
                                      T13/T14 Vorlagen (Prüfer/Vortrag)       ~1–2 h
```

Jede Phase endet mit einem **Phasengate** (§5): Build grün + Greps grün + Protokoll geführt,
sonst wird nicht weitergezogen.

---

## 4. Detailplan je To-do (Schritte, DoD, Verifikation)

### Phase A – Code-/Versionsklärung

#### T3 · Inline-Vollauf/Maskenwarp-Widerspruch (U2) 🔴

1. Code lesen (nur lesen): Warp-Aufruf im Inline-Pfad von `run_pipeline.sh` bzw. Matrixrunner suchen
   (`data/03_masks_ideal`, `warp`, `image_undistorter`-Nachfolgeaufrufe).
2. Befund mit `datei:zeile` ins Protokoll schreiben → daraus folgt die **eine** Wahrheit.
3. Alle fünf Textstellen auf diesen Stand bringen:
   `03_konzept.tex:115-124`, `appendix_repro.tex:7-9` (falls „fehlt noch" falsch) bzw.
   `08_fazit.tex:8`, `04_implementierung.tex:213` (falls „gefixt" falsch).
4. Aussagenprüfung §2.4/§2.9 entsprechende Zeile aktualisieren.

**DoD:** `grep -rn 'Maskenwarp' PA/sections PA/appendices` liefert nur noch konsistente Aussagen;
Code-Befund im Protokoll zitiert.

#### T5 · SuGaR-Versionsdreieck (U5) 🔴

1. Ist-State sichern: `git submodule status` (aktuell `a0fc37b`, Branch `project/masked-sugar`),
   `git -C third_party/SuGaR status --short`, Diff-Datei erzeugen
   (`docs/sugar_fork_diff_<hash>.diff`) und im Anlagenband referenzieren.
2. Dockerfile-Default `SUGAR_REF=e254000…` (docker/container-d-sugar/Dockerfile:62) auf finalen
   Commit heben; Compose-Parameter prüfen.
3. Parent-Gitlink committen (Submodul-Commit zuerst!).
4. Text anpassen: `04_implementierung.tex:97-103` (Fork-Tabelle um `a0fc37b`-Zeile ergänzen),
   `appendix_repro.tex` (Versionsabschnitt), Anlagenindex (Diff-Pfad).

**DoD:** `git submodule status` == Parent-Gitlink == Dockerfile-Default == Angabe im Tex;
alle vier Hashes stehen im Protokoll. Erst danach darf der finale PDF-Build erfolgen.

### Phase B – Belege & Golden Run

#### T1 · Golden Run wählen + End-to-End-Panels (U4) 🔴

1. **Kandidatenfestlegung** (Entscheidungspunkt D2): Empfehlung
   `matrix_qualitaetsvergleich_20260818`, Arm `5fps/720p/opencv_a` (= Produktionskonfiguration).
   Alternativ ein `Alurohr_THWS_*`-Autopilotlauf, falls dessen Artefakte vollständig archivierbar sind.
2. Aus dem **einen** Lauf exportieren: Rohframe, default/middle-Maske, ideale Domäne, Sparse-Punkte,
   STS-Splat, Route-A-Mesh, Centerline+B-Spline – jeweils identische Ansicht.
   Export-Schritte als Skript unter `tools/export_golden_run_views.sh`(o. ä.) festhalten
   (Reproduzierbarkeit > Handklick).
3. Panel bauen analog bestehendem Pillow-Skript (`pa_panel_golden_run.png`),
   Ablage in `PA/figures/`, Erzeuger-Skript im Anlagenindex nennen.
4. Einbau in `06_ergebnisse.tex` 7.1: Blockquote „Offener Abbildungsnachweis" entfernen,
   Abbildung + Bildunterschrift mit Run-ID, Commit (aus T5!), Eval-Anzahl.
5. Grafikbudget prüfen: laut Strategieplan §4.1 max. fünf Grafikgruppen im Haupttext –
   ggf. ersetzt das Panel eine schwächere Gruppe statt sie zu ergänzen.

**DoD:** Jede Ansicht des Panels stammt aus Run-ID X (im Protokoll belegt);
Abbildung im PDF; Blockquote weg; Grafikgruppen-Zahl ≤ 5.

#### T4 · Autopilot-Nachweis einziehen (U3) 🔴

1. Die sechs Läufe tabellieren (Run-ID, Datum, Konfiguration, Status SUCCESS, Exit 0) –
   Quelle: `run.md` je Ordner; Ablageort ins Protokoll.
2. Textstellen korrigieren: `06_ergebnisse.tex` 7.1, `07_diskussion.tex` 8.5 + 8.8 (Antwort 4),
   Erfolgskriterium 6 in `05_versuchsaufbau.tex:218`.
3. Ehrliche Einschränkung behalten: Archive enthalten Logs/Manifeste, keine Renderartefakte →
   entweder einen Lauf zum vollständigen Archiv machen (verbindet mit T1) oder Restriktion benennen.

**DoD:** Keine Stelle behauptet mehr, der Autopilotnachweis fehle; Tabellenbezug im Text oder Anhang.

#### T11 (Teil 1) · Qualitätsvergleichslauf erwähnen

Ergebnisdaten des Batches (failed=0, frische Metriken) sichten und als Kurzabsatz in 7.4/7.5
vorbereiten – Volltextintegration passiert in Phase D nach T7 (Seitenbudget!).

### Phase C – Anlagenabgleich

#### T2 · Anlagenindex ↔ Realität (U1) 🔴

1. Bestandserhebung: Welche der genannten Pfade existieren physisch, welche nur als Backup/Kompaktarchiv?
   Für fehlende: Prüfsummen (`sha256sum` der Manifeste/CSVs) + Backuport dokumentieren.
2. Validierungs-Skript `tools/check_anlagenindex.sh`: geht jede Zeile des Index durch,
   `test -e` auf jeden Pfad, gibt Report aus. Skript selbst wird Anlage (bleibt nutzbar!).
3. Index ergänzen: `matrix_qualitaetsvergleich_20260818`, `Alurohr_THWS_*`,
   `third_party/SuGaR/data/sugar_output/matrix_matrix_sugar_followup_12_*` (tatsächlicher Ort!),
   Fork-Diff aus T5, Golden-Run-Panel-Skripte.
4. `results/README.md` synchron ziehen.

**DoD:** `check_anlagenindex.sh` läuft mit 0 Fehlern OER dokumentierten, erklärten Ausnahmen
(externes Backup mit Prüfsumme).

### Phase D – Textarbeit

#### T7 · Kürzung NUR MARKIEREN, nicht durchführen (A1/A5) 🟡 – **ENTSCHIEDUNG D3: nicht kürzen**

Der Nutzer hat entschieden (D3, 23.08.2026): Der Haupttext bleibt **vollständig erhalten**;
weder konservative noch vollständige Kürzung wird angewendet. Stattdessen:

1. Die acht Kürzungskandidaten (Schritte a–h) werden **nur dokumentiert** – mit konkreter
   Stelle (`datei:zeile`), Inhalt, erwarteter Ersparnis und Begründung, warum sie entbehrlich wäre.
2. Ablageort der Markierungen: `PA/Fertigstellung/Arbeitsdatei_Fertigstellung.md` (§ Kürzungsmarkierungen).
3. Kein einziger dieser Schnitte wird in `sections/*.tex` oder `appendices/*.tex` ausgeführt.
4. Falls der Prüfer später doch eine Kürzung verlangt (T13-Ergebnis), kann die Liste dort
   direkt abgearbeitet werden; bis dahin bleibt sie unverbindliche Vorbereitung.

| Schritt | Kandidat (nur markiert, NICHT ausgeführt) | Erwartete Ersparnis |
|---|---|---|
| a | Preset-Laufzeiten nur 1× (in 7.5); 4.5 + 5.4 auf Querverweis | ~0,5 S. |
| b | Maskenhierarchie-Detail nur in Grundlagen 3.1; 5.1 auf 3 Sätze | ~0,5 S. |
| c | Abschnitt 5.7 (SuGaR-Zählerstände) komplett → Anhang D | ~1 S. |
| d | 7.2 visuelle Details straffen; Anhang C spricht für sich | ~1 S. |
| e | Tabelle `tab:bildablagen` halbieren (Zeilen zusammenfassen) | ~0,5 S. |
| f | Route-A-Begründung: Grundlagen 3.4 als Hauptort, 4.4/7.6/7.7 nur Querverweis | ~1 S. |
| g | Redundanzen Diskussion 8.1–8.3 vs. Ergebnisse streichen | ~1–2 S. |
| h | Duplikate Konzept 4.2 ↔ Implementierung 5.5 (Domänenkette) | ~1 S. |

**Exposé-Gate:** entfällt im Markier-Modus (es wird nichts entfernt); bei späterer
Aktivierung der Liste gilt es weiterhin vor jedem Schnitt.

**DoD:** Alle acht Kandidaten sind mit Stelle + Begründung markiert; `git diff` zeigt
**keine** Änderung an `sections/`/`appendices/` durch T7; Seitenzahl unverändert.

#### T8 · Kurzfassung (A2) 🟡 – 3 Ergebnissätze einfügen (Text wie in Bewertung To-do 8).
#### T9 · Terminologie & Zahlen (A3/A4) 🟡

- Globale Ersetzung mit `sed` über `sections/ appendices/`: SAM3→SAM~3.1,
  QHD/qhd→**qHD** (quarter HD, 960×540 – NICHT „QHD“=Quad HD!; Korrektur 23.08.2026
  auf Nutzerangabe), `SIMPLE-RADIAL`→`SIMPLE\_RADIAL` (nur im Fließtext, nicht in
  Code-/Pfadbezügen wie `_qhd.png`, `qhd_panels` – dort bleibt Kleinschreibung!).
- Anhang A: Punkte→Komma, `px`→`Pixel`, Tausenderpunkte.
- PSNR-Format global festlegen (Empfehlung: 2 Nachkommastellen), SSIM/LPIPS 3.

**DoD (Regressionstests, alle = 0 Treffer):**

```bash
grep -rn 'SAM3' PA/sections PA/appendices          # 0
grep -rn 'qhd' PA/sections PA/appendices           # 0 (qHD erlaubt; _qhd.png-Pfade ausgenommen)
grep -rnE '[0-9]{6,}' PA/sections PA/appendices    # 0 (Tausendertrennung überall)
grep -n '[0-9]\.[0-9][0-9] px' PA/appendices/appendix_colmap.tex  # 0
```

#### T10 · Literaturordnung + \nocite (A6/A7) 🟡

`\printbibliography` vor `\appendix`; `\parencite{scan2bimImplementation}` im Anlagenindex-Absatz,
`\parencite{matrixRestResults}` in Anhang B; danach `\nocite` leer/entfernen.
LoF/LoT-Position → Entscheidungspunkt D4 (mit Prüfer klären, bis dahin unverändert lassen).

**DoD:** `grep -n nocite PA/main.tex` leer; biber-Lauf ohne WARN; Verzeichnis-Reihenfolge lt. Protokollnotiz.

#### T11 (Teil 2) · Qualitätsvergleich integrieren – Kurzabschnitt 7.4/7.5 final schreiben.

### Phase E – Build & Hygiene

#### T12 · Overfull-Boxen 🟡 – größte (51 pt, `appendix_repro.tex` Itemize) fixen, Rest prüfen.
**DoD:** `grep -c Overfull build/pa.log` ≤ Baseline − 3 (oder jede verbliebene begründet).
#### T15 · Build-Hygiene 🟡 – `build/` leeren (nur `.gitkeep`), ausschließlich `build_pa.sh`
(Jobname `pa`) verwenden; Leichen (`main.*`, `*-SAVE-ERROR`, `pa_editetd*`, Kommentar-.txt)
löschen oder ins Anlagenband verschieben.

### Phase F – Abschluss

#### T6 · Deckblatt 🔴 – Platzhalterklammern weg, fixes Datum, THWS-Original-Erklärung.
#### T16 · Vollabgleich 🟡 – alle Zahlen im Text (87/380 Punkte, Metrikwerte, Seitenzahlen,
Querverweise) gegen Manifeste des Golden Runs; Fazit-Versprechen („gegen Artefakte geprüft") einlösen;
`check_anlagenindex.sh` final laufen lassen.
#### T13/T14 · Vorlagen erstellen (keine Eigenentscheidung!): Prüfer-Mail-Checkliste (PlagAware,
Sperrvermerk, Anlagenform, LoF/LoT) + Vortragsgliederung 20 min nach Zielrahmen §6.2.

---

## 5. Phasengates (Abbruch-/Weiterkriterium)

Eine Phase gilt erst als geschlossen, wenn **alle** Punkte erfüllt sind:

1. `./build_pa.sh` läuft fehlerfrei; `grep -iE '^!|undefined' build/pa.log` → 0 Treffer.
2. Regression-Greps der Phase (je To-do in §4 gelistet) ausgeführt und im Protokoll notiert.
3. Jedes To-do der Phase hat: Protokolleintrag + Commit(s) + aktualisierte Aussagenprüfungs-Zeilen.
4. Status hier in §4 und in `Bewertung_Zielrahmen_und_Todos.md` aktualisiert.
5. Seitenumfang notiert (Trend gegenüber Baseline).

Bei Gate-Fehler: zurück zum letzten grünen Commit (`git stash`/revert des To-do-Commits),
Ursache ins Protokoll, erneut versuchen. **Nie** mit offenem Gate in die nächste Phase.

---

## 6. Backlog (Fundstücke während der Arbeit – NICHT spontan umsetzen)

Wird laufend ergänzt; Aufnahme in die To-dos nur mit neuer Nummer + Priorität + Anker-Bezug:

- *(noch leer)*

---

## 7. Entscheidungspunkte (brauchen deine Zustimmung, bevor Phase startet)

**Status: D1–D3 entschieden (23.08.2026), D4 bleibt offen bis Prüferklärung (T13).**

| Nr | Frage | Empfehlung | Entscheidung |
|----|-------|------------|--------------|
| D1 | Darf ich selbst git-committen (ein Commit pro To-do)? | Ja – sonst kann die Dokumentationskette (Commit↔Protokoll) nicht funktionieren | ✅ **Ja, aber auf Branch `pa-fertigstellung`**, getrennt vom jetzigen Stand; Merge erst nach Phase F |
| D2 | Golden Run: `matrix_qualitaetsvergleich_20260818 / 5fps / 720p / opencv_a`? | Ja – entspricht Produktionskonfiguration, failed=0, 19 GB vollständig lokal | ✅ **Ja** – genau dieser Arm wird Golden Run (T1) |
| D3 | Kürzungstiefe: konservativ (Schritte a–d, ~−2,5 S.) oder voll (a–h, ~−7 bis −10 S.)? | Voll – Richtwert 25 S. sonst unerreichbar; Exposé-Gate schützt vor Zuviel | ❌ **Nein, weder noch: NICHT kürzen.** Text bleibt vollständig; die acht Kandidaten werden nur in der Arbeitsdatei markiert |
| D4 | LoF/LoT vorn lassen (wie jetzt) oder hinter Literatur (THWS-Muster)? | Mit Prüfer klären (Teil von T13); bis dahin: unverändert | ⏳ **Offen** – unverändert bis Prüferantwort. Hinweis: D4 betrifft AUSSCHLIESSLICH die Position von Abbildungs-/Tabellenverzeichnis vs. Literatur; am Verhältnis Golden-Run-/Pipeline-Konfiguration (Auflösungsvarianten, Anhang-Vergleich) ändert sich nichts – das ist wie gewollt korrekt umgesetzt |

**Klarstellung zum Missverständnis rund um D4:** Die Frage D4 hat nichts mit dem Golden Run
oder den Auflösungseinstellungen zu tun. Der Sachverhalt „Golden-Run-Arm == Produktions-/Autopilot-
Konfiguration, nur Auflösungen variieren, Vergleich im Anhang (`appendix_durchlauf.tex`)" ist
so gewollt und wird nicht angetastet (bestätigt gegen Quelle am 23.08.2026).

---

## 8. Statusboard (wird laufend aktualisiert)

| To-do | Titel | Kat | Phase | Status | Commit | Verifikation |
|-------|-------|-----|-------|--------|--------|--------------|
| T1 | Golden-Run-Panels | 🔴 | B | 🔶 blockiert (Archive extern) | – | – |
| T2 | Anlagenabgleich | 🔴 | C | 🔄 interim erledigt; Prüfsummen/extern offen | fd6c741 | Index ↔ lokale Realität abgeglichen |
| T3 | Warp-Widerspruch lösen | 🔴 | A | ✅ erledigt (Arbeitsfassung) | 32415bb | Warp-Greps konsistent, Build grün |
| T4 | Autopilot-Nachweis | 🔴 | B | 🔶 blockiert (Run-IDs extern) | – | – |
| T5 | SuGaR-Versionen konsolidieren | 🔴 | A | 🔶 blockiert (Submodul nicht initialisiert; Code tabu) | – | – |
| T6 | Deckblatt | 🔴 | F | 🔲 offen (wartet auf Datenbestätigung, T13 Pkt. 7) | – | – |
| T7 | Kürzung nur markieren (D3) | 🟡 | D | ✅ erledigt (Liste in Arbeitsdatei §3, kein Textschnitt) | – | `git diff sections/` leer |
| T8 | Kurzfassung | 🟡 | D | ✅ erledigt (Arbeitsfassung) | 9a1e6f6 | Zahlen belegt |
| T9 | Terminologie/Zahlen | 🟡 | D | ✅ erledigt (Arbeitsfassung) | 8513d11 | DoD-Greps = 0 (Pfade ausgenommen) |
| T10 | Literatur/\nocite | 🟡 | D | ✅ erledigt; D4 (LoF/LoT) weiter offen | 2c9a1e8 | Literatur S. 41 vor Anhang |
| T11 | Qualitätsvergleich integrieren | 🟡 | B/D | 🔶 blockiert (Metrikdaten extern) | – | – |
| T12 | Overfull | 🟡 | E | ✅ erledigt (5 → 0) | 157f7ad | Log-Grep = 0 |
| T13 | Prüfer-Checkliste | 🟡 | F | ✅ Vorlage erstellt (inkl. D4-Frage) | c45d279 | Versand aussteht |
| T14 | Vortragsgliederung | 🟡 | F | ✅ Vorlage erstellt | c45d279 | Panel folgt mit T1 |
| T15 | Build-Hygiene | 🟡 | E | ✅ erledigt | c45d279 | PA/main.* entfernt |
| T16 | Vollabgleich | 🟡 | F | 🔄 teilweise (Diskrepanz 21,69 vs. 21,59 dB markiert) | – | nach Golden Run final |
