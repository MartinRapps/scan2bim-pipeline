# Anlage: Dokumentation der KI-Nutzung

**Projektarbeit Scan-to-BIM-Pipeline – Martin Rapps (6323014)**
**Zeitraum:** Juni – August 2026
**Abgestimmt mit Betreuung:** Auf Grund des Umfangs und der agentischen Arbeitsweise (selbstständige Änderungen über mehrere Dateien, iterative Überarbeitungen) wird die KI-Nutzung nach Bereichen beschrieben und jeweils durch beispielhafte Prompts veranschaulicht. Eine vollständige Auflistung aller Einzel-Prompts ist bei diesem Arbeitsmodus nicht sinnvoll und wurde so mit dem Prüfer abgestimmt.

---

## Eingesetzte Werkzeuge

| Werkzeug | Version / Anbieter | Einsatz |
|---|---|---|
| **opencode** (CLI-Agent) | aktuelle Version, verschiedene LLMs je nach Aufgabe | Code-Erstellung, Refactoring, Pipeline-Debugging, Textüberarbeitung |
| **VS Code** | aktuelle Version, integrierte KI-Unterstützung | Code-Editierung, Inline-Vorschläge, LaTeX-Bearbeitung |

Die Modellwahl erfolgte je nach Aufgabenkomplexität und Kosten – für einfache Korrekturen schlanke Modelle, für konzeptionelle oder fachliche Fragen leistungsfähigere Modelle. Alle KI-Ausgaben wurden manuell geprüft, verstanden und verantwortet.

---

## 1. Code-Erstellung / Verbesserung / Refactoring

**Worum es ging:** Aufbau und Pflege der Docker-basierten Pipeline (SAM-3.1-Segmentierung, COLMAP, STS, SuGaR-Fork, Centerline-Extraktion), insbesondere die Anpassung der Maskenlogik (Dilatation/Erosion für genau ein Zielobjekt), Fehlerbehandlung in Matrixläufen und die maskenbewusste Erweiterung des SuGaR-Forks.

**Beispielhafte Prompts:**
- „Die SAM-Masken enthalten mehrere Objekte. Passe die Logik so an, dass per Dilatation/Erosion automatisch genau ein zentrales Objekt übrig bleibt. Zeige nur die geänderte Funktion und erkläre die Parameter."
- „Der Matrixrunner bricht ab, wenn die TSV-Datei per stdin konsumiert wird. Finde die Ursache und schlage eine stdin-unabhängige Schleife vor."
- „Im SuGaR-Fork soll der RGB-Loss nur innerhalb der Objektmaske gewertet werden. Implementiere einen maskierten Loss L_RGB^M mit Normierung über die Maskenpixel und Schutz vor Division durch null."

**Prüfung:** Jeder Vorschlag wurde im lokalen Docker-Setup ausgeführt und gegen Manifeste/Logs geprüft; unverstandene Änderungen wurden nicht übernommen.

---

## 2. Allgemeine Überlegungen zum Vorgehen (Sparringspartner)

**Worum es ging:** Struktur der Arbeit, Versuchsplanung (Matrixdesign Kameramodell × FPS × Auflösung), Bewertung von Varianten (Route A vs. SuGaR-Coarse, Tiefenrouten), Interpretation von Metriken.

**Beispielhafte Prompts:**
- „Ich habe PinHole und OpenCV getestet, beide liefern ähnliche Metriken. Welche Argumente sprechen fachlich für welchen Standard, und wie formuliere ich das ehrlich ohne Überinterpretation?"
- „Soll ich die Reproduzierbarkeit als eigenen Anhang oder im Methodenteil beschreiben? Nenne Vor- und Nachteile beider Varianten für diese Arbeit."
- „Hilf mir, die Matrixläufe so zu planen, dass ich Kameramodell, FPS und Auflösung getrennt auswerten kann, ohne die Meshroute zu vermischen."

**Prüfung:** Vorschläge wurden mit dem Betreuer und dem Zielrahmen abgeglichen; fachliche Entscheidungen (z. B. Produktionsstandard) blieben eigene Arbeit.

---

## 3. Schreiben und Überarbeiten von Texten in der Projektarbeit

**Worum es ging:** Gliederung, Formulierung, Kürzung und LaTeX-Feinschliff (Tabellen, Abbildungen, Literatur, Overfull-Boxen).

**Beispielhafte Prompts:**
- „Dieser Absatz über die Domänentrennung ist zu lang. Kürze ihn um 30 %, behalte aber COLMAP, Maskenwarp und ideale Domäne als Kernbegriffe."
- „Formuliere diesen Satz wissenschaftlicher und ohne Füllwörter: ‚Das flexiblere Modell ist nicht grundsätzlich genauer, weil …' – gib zwei Alternativen."
- „Die Tabelle tab:bildablagen ist zu breit. Schlage eine kompaktere Spaltenaufteilung vor, ohne Inhalt zu verlieren."

**Prüfung:** Alle Textvorschläge wurden satzweise gelesen, fachlich geprüft und in eigenen Worten überarbeitet; Zitate und Zahlen wurden gegen Manifeste und Tabellen verifiziert.

---

## 4. Fehleranalyse und Auswertung

**Worum es ging:** Diagnose fehlgeschlagener Läufe (leere Masken, SUGAR-Importfehler, COLMAP-Registrierung), Einordnung von Screenshots und Zwischenständen.

**Beispielhafter Prompt:**
- „Hier ein Log-Auszug mit leeren Eval-Masken. Welche Prüfung fehlt, und wo würdest du ein Quality-Gate einbauen? Erkläre den Vorschlag, bevor du Code änderst."

**Prüfung:** Ursachen wurden im Code und in den Logs nachvollzogen; Korrekturen wurden erst nach manuellem Test übernommen.

---

## 5. Grafiken und Auswertung

**Worum es ging:** Erstellung der Panels (z. B. pa_panel_sugar_iteration), Metrikplots (STS vs. SuGaR, Delta, Runtime) und deren Beschriftung.

**Beispielhafter Prompt:**
- „Das Panel hat 9200er-Labels aus Dateinamen, soll aber konsistent 9001 zeigen. Schreibe ein Pillow-Skript, das die Kacheln neu zusammensetzt und nur 9001 ausgibt."

**Prüfung:** Generierte Grafiken wurden visuell und gegen die Quelldaten (JSON/CSVs) geprüft.

---

## Eigenständigkeit

Alle Inhalte wurden fachlich geprüft, vollständig verstanden und können selbstständig vertreten werden. KI-Ausgaben wurden nicht als wissenschaftliche Quellen zitiert. Die Verantwortung für fachliche Richtigkeit und Eigenständigkeit liegt beim Verfasser.
