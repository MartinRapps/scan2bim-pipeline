# Arbeitsdatei Fertigstellung – PA Scan-to-BIM

> **Rolle dieser Datei:** Zentrale, **änderbare** Arbeitsdatei für die PA-Fertigstellung.
> Sie liegt bewusst in einem **eigenen Ordner** (`PA/Fertigstellung/`) und ist damit
> **getrennt vom jetzigen Stand** (`PA/sections/`, `PA/appendices/`, `PA/main.tex`,
> `PA/Umsetzungsplan_ToDos.md`). Hier werden Entscheidungen festgehalten, Befunde
> verifiziert und Kürzungskandidaten **nur markiert**. Ausführungen in den .tex-Dateien
> erfolgen später als eigene To-do-Commits auf Branch `pa-fertigstellung`.
>
> Erstellt: 23.08.2026 · Basis: `PA/build/pa.pdf` (Build 22.08.2026), `PA/Zielrahmen.md`,
> `PA/Umsetzungsplan_ToDos.md`, `PA/PA_Bewertung_Zielrahmen_und_Todos.md`, Quelltexte + Repo-Stand.

---

## §1 Entscheidungsprotokoll (Stand 23.08.2026)

| Nr | Thema | Entscheidung | Konsequenz |
|----|-------|--------------|------------|
| D1 | Git-Commits durch Assistent | **Ja – aber auf Branch `pa-fertigstellung`**, getrennt von `master` | Alle To-do-Commits landen auf dem Branch; Merge erst nach Abschluss Phase F |
| D2 | Golden Run | **Ja**: `matrix_qualitaetsvergleich_20260818`, Arm `5fps/720p/opencv_a` | T1 baut Panels aus genau diesem Lauf; Run-ID kommt in Bildunterschrift |
| D3 | Kürzungstiefe | **Nein, nicht kürzen** – weder konservativ noch voll. Text bleibt vollständig | T7 ist auf „Nur markieren“ gestellt; Markierungen stehen in §3 dieser Datei |
| D4 | LoF/LoT-Position | **Noch offen** – bleibt bis zur Prüferklärung (T13) unverändert | Keine Änderung an `main.tex:117-118` bzw. `\printbibliography`-Position |

### Klarstellung zu D4 (wichtig, Missverständnis aufgelöst)

Die Rückfrage zum Golden Run („der normale Golden Run ist auch die Einstellung der
automatisierten Pipeline, nur eben mit den Auflösungseinstellungen; diese Runs werden
im Anhang verglichen“) betrifft **nicht** D4. D4 fragt ausschließlich, ob das
Abbildungs-/Tabellenverzeichnis vorne bleibt oder hinter die Literatur wandert.

Der beschriebene Sachverhalt selbst ist **korrekt und so gewollt umgesetzt**:

- Der Produktionsstandard gilt laut PA für **720p / OPENCV-A / 5 FPS**
  (`06_ergebnisse.tex:204-217`, Abschnitt 7.5).
- Der Autopilot wählt automatisch dieses 720p-Preset
  (`04_implementierung.tex:200-202`).
- Der Golden-Run-Arm `720p/opencv_a` aus `matrix_qualitaetsvergleich_20260818` ist
  dieselbe Konfiguration wie der automatisierte Lauf; nur die **Auflösung** variiert
  zwischen den Matrixarmen (720p/qhd/low).
- Den Vergleich der drei Auflösungen entlang derselben Kette dokumentiert
  **Anhang C** (`appendix_durchlauf.tex`: „Pipeline-Durchlauf in drei Auflösungen,
  5 FPS, OPENCV“, Zeilen 2–12).

→ **Hier ist nichts zu ändern.** Weder T1 noch T4 greift dieses Verhältnis an; sie
ziehen nur fehlende Belege (Run-ID, Archive) nach. D4 bleibt offen.

---

## §2 Verifizierter Faktenstand (Gegenprüfung vom 23.08.2026)

Alle Aussagen des Bewertungs- und Umsetzungsdokuments wurden gegen Quellen geprüft
(`datei:zeile`). Ergebnis: Die Befunde tragen; zwei Präzisierungen (F8, F9) sind
für die Ausführung wichtig.

| # | Befund | Verifikation | Konsequenz |
|---|--------|--------------|------------|
| F1 | **Code-Wahrheit Maskenwarp:** Der Inline-Vollauf führt den Warp **durch**: `run_pipeline.sh:828-848` ruft `warp_masks_to_undistorted.py` + Coverage-Gate zwischen COLMAP und STS auf. | Bestätigt am Quellcode (nur lesend, kein Code-Change). | T3 auflösen Richtung **Fazit/Implementierung behalten**, stattdessen korrigieren: `03_konzept.tex:115-124`, `appendix_repro.tex:7-9`, `07_diskussion.tex:13-14` (alle drei sagen fälschlich „fehlt noch“). Korrekt sind bereits `08_fazit.tex:8-10` und `04_implementierung.tex:211-222`. |
| F2 | **Golden Run ≙ Produktions-/Autopilot-Konfiguration**, nur Auflösung variiert; Auflösungsvergleich im Anhang C | `06_ergebnisse.tex:204-217`, `04_implementierung.tex:200-202`, `appendix_durchlauf.tex:2-12` | Gewollter Zustand, **keine Änderung** |
| F3 | **U4 bestätigt:** `matrix_qualitaetsvergleich_20260818` kommt im gesamten PA-Text **nullmal** vor; Blockquote „Offener Abbildungsnachweis“ steht in `06_ergebnisse.tex:12-17` | Grep über `sections/` + `appendices/` → 0 Treffer | T1/T11 wie geplant |
| F4 | **U3 bestätigt:** PA hält den Autopilotnachweis für ausstehend: `06_ergebnisse.tex:27-29`, `07_diskussion.tex:129-131` sowie `183`, Erfolgskriterium 6 `05_versuchsaufbau.tex:223-225` | Textstellen gelesen | T4 wie geplant; Formulierung von Erfolgskriterium 6 ist als Dokumentationskriterium lesbar – Korrektur nur soweit nötig, um Widerspruch zum Archivstand zu lösen |
| F5 | **A6/A7 bestätigt:** `\nocite` mit 5 Keys inkl. `scan2bimImplementation`, `matrixRestResults`; Literatur **nach** Anhängen; LoF/LoT vorne | `main.tex:143-144`, `main.tex:117-118` | T10 wie geplant; LoF/LoT-Frage = D4, bleibt offen |
| F6 | **A8 bestätigt:** Deckblatt-Platzhalter `[Martin Rapps]` etc. + `\today` | `main.tex:32-37,80` | T6 wie geplant |
| F7 | **U5 bestätigt:** Submodul-Checkout `a0fc37b` (Branch `project/masked-sugar`) ≠ im Text genannte `ecda7ef`/`eca4ea1`; Text gibt Lücke selbst zu (`04_implementierung.tex:97-103`) | `git submodule status` 23.08.2026 | T5 wie geplant |
| F8 | **Terminologie-Zahlen präzisiert (A3/A4):** `SAM3` roh 3× (`04_implementierung.tex:199`, `06_ergebnisse.tex:363`, `07_diskussion.tex:139`); kleines `qhd` 13× (`03_konzept.tex` ×2, `04_implementierung.tex` ×2, `06_ergebnisse.tex` ×2, `appendix_durchlauf.tex` ×7) | Grep-Zählung 23.08.2026 · **Korrektur 23.08.2026:** korrekte Schreibweise ist **qHD** (quarter HD, 960×540) – weder „QHD“ (Quad HD = 2560×1440) noch kleines „qhd“. Global auf qHD umgestellt; Dateipfade (`_qhd.png`, `qhd_panels`) bleiben kleingeschrieben. | **Achtung bei T9/sed:** Ein Teil der kleinen `qhd` steht in Datei-/Pfadbezügen (`\texttt{qhd\_panels}`, Screenshot-Namen in `appendix_durchlauf.tex`) und darf **nicht** ersetzt werden, sonst brechen Abbildungspfade. Ersetzung nur im Fließtext, Pfadbezüge ausnehmen. |
| F9 | **Datenlage-Hinweis:** `data/10_runs/` existiert derzeit **nicht** im Working Copy (gitignored, Laufzeitartefakte liegen extern, u. a. V-Laufwerk; Struktur belegt via `copy_v_drive_a_routen.txt`) | `ls data/10_runs` → fehlt; `.gitignore` blockt `data/*` | T1/T2/T4 erfordern vorher Zugriff auf VM/Backup (Kopie oder Prüfsummen). Bis dahin können Panels/Tabellen nicht aus lokalen Archiven erzeugt werden. |
| F10 | Exposé-Anker existiert doppelt: `Expose_PA_BA.pdf` (Repo-Root) **und** `docs/Expose_PA_BA.pdf` | Dateitest 23.08.2026 | Anker-Referenz im Umsetzungsplan gültig |

**Fazit der Gegenprüfung:** Die To-do-Liste ist tragfähig. Die einzige inhaltliche
Umsteuerung ist D3 (T7 = nur markieren). Alles Übrige wird wie geplant ausgeführt,
mit den Präzisierungen F1 (Korrekturrichtung) und F8 (sed-Ausnahmen).

---

## §3 Kürzungsmarkierungen (D3 – MARKIERT, NICHT AUSGEFÜHRT)

> Status aller folgenden Punkte: **nur dokumentiert**. Es wurde nichts aus
> `sections/*.tex` oder `appendices/*.tex` entfernt. Falls der Prüfer (T13-Ergebnis)
> doch eine Kürzung wünscht, kann diese Liste direkt abgearbeitet werden.
> Vor jeder Aktivierung gilt das Exposé-Gate (keine Exposé-Zusagen verlieren).

| Schritt | Kandidat | Konkrete Stelle(n) | Erwartete Ersparnis | Warum entbehrlich (wenn überhaupt) |
|---------|----------|--------------------|---------------------|-------------------------------------|
| a | Preset-Laufzeiten nur 1× statt 3× | `03_konzept.tex:157`, `04_implementierung.tex:195-199`, Hauptort behalten in 7.5 (`06_ergebnisse.tex:237-243`) | ~0,5 S. | Dreifach fast wortgleich; ein Hauptort + Querverweis reicht |
| b | Maskenhierarchie-Detail nur in Grundlagen | Grundlagen (Maskenkapitel), `05_versuchsaufbau.tex:64 ff.` | ~0,5 S. | Zweite Darstellung ist Zusammenfassung; Grundlagen bleiben vollständig |
| c | Abschnitt „Historische Zwischenstände der STS- und Objektfilterungsroute“ → Anhang D | `04_implementierung.tex:247-279` | ~1 S. | Historische Zählerstände sind Anlagenstoff; Kernbefund bleibt als Satz im Haupttext |
| d | 7.2 visuelle Details straffen | `06_ergebnisse.tex:36-85` (Anhang C trägt die Bilder) | ~1 S. | Detailbeschreibungen duplizieren teils das, was Anhang C zeigt |
| e | Tabelle `tab:bildablagen` halbieren | `04_implementierung.tex:112-149` (Label Zeile 149) | ~0,5 S. | Zeilen lassen sich zusammenfassen (gleiche Verträge gruppieren) |
| f | Route-A-Begründung nur 1× als Hauptort | Grundlagen 3.4 (Hauptort), weitere: `04_implementierung.tex:321 ff.`, `06_ergebnisse.tex:278-286`, `06_ergebnisse.tex:300-308` | ~1 S. | Begründung steht viermal; Nebendarstellungen könnten zu Querverweisen werden |
| g | Redundanzen Diskussion 8.1–8.3 vs. Ergebnisse | `07_diskussion.tex` Anfangsdrittel vs. `06_ergebnisse.tex` | ~1–2 S. | Teilweise Wiederholung der Ergebnisinterpretation |
| h | Duplikat Domänenkette Konzept ↔ Implementierung | `03_konzept.tex:105-124` ↔ `04_implementierung.tex:204-228` | ~1 S. | Implementierung könnte sich auf Konzept belegen und nur Gates/Differenzen nennen |

**Summe bei Aktivierung:** ca. −6,5 bis −8 Seiten (Haupttext dann ~31–33 S. statt 39 S.;
Zielwert 25 S. würde ohne inhaltliche Verluste trotzdem nicht erreichbar sein – ein
weiteres Argument, weshalb D3 „nicht kürzen“ vertretbar ist, solange der Prüfer dem
Umfang zustimmt).

---

## §4 Offene Punkte

1. **D4** (LoF/LoT-Position): Frage ist in `T13_Pruefer_Checkliste.md` (Punkt 1) enthalten;
   bis zur Antwort unverändert.
2. **Archivzugriff** (F9): Wo liegen die `data/10_runs`-Archive aktuell physisch?
   Für T1 (Panels) und T4 (Run-IDs) notwendig.
3. **T5-Versionsdreieck:** Submodul initialisieren + Fork committen + `SUGAR_REF` anpassen
   – erfordert ausdrückliche Freigabe, Code zu berühren; danach Tex-Zeile 04_impl:97 ff.
4. **Deckblatt (T6):** Bestätigung der offiziellen Angaben (T13-Checkliste Punkt 7) steht aus;
   Platzhalter bleiben bewusst in Klammern, bis Daten verifiziert sind.
5. **Zahlendiskrepanz für T16:** Text (`06_ergebnisse.tex:370`) nennt QHD-SuGaR-Coarse-
   Mittelwert 21,69 dB; Anhang B sagt 21,59 dB (ursprünglich 21,586). Vor T9 bereits
   vorhanden; Klärung gegen Quelldaten offen.

### Umsetzungsstand nach To-do-Runde 1 (23.08.2026)

Erledigt in der Arbeitsfassung: **T3, T7 (Markierliste §3), T8, T9, T10, T12 (5 → 0
Overfull), T15, T13-/T14-Vorlagen.** Interim: T2. Blockiert: T1/T4/T11 (Archive extern),
T5 (Code tabu + Submodul nicht initialisiert), T6 (Datenbestätigung), T16 (nach Golden Run).
Details je To-do: `Aenderungsprotokoll_Fertigstellung.md`; Commitliste im Statusboard des
`Umsetzungsplan_ToDos.md`. Kopie-Build `pa_arbeit`: Haupttext S. 40, Literatur S. 41,
0 Overfull, 0 undefined.

---

## §5 Protokoll dieser Datei

| Datum | Änderung |
|-------|----------|
| 23.08.2026 | Erstellt: Entscheidungen D1–D4 festgehalten, Faktenstand gegen Quellen geprüft (F1–F10), Kürzungskandidaten gemäß D3 nur markiert |
| 23.08.2026 | §4 erweitert: Umsetzungsstand nach To-do-Runde 1, neue offene Punkte (T5-Freigabe, Deckblattdaten, Zahlendiskrepanz) |
