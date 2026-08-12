# Zielrahmen der Projektarbeit

## Zweck dieses Dokuments

Dieses Dokument fasst die für die Projektarbeit relevanten Vorgaben aus dem
bereitgestellten Dokument der Technischen Hochschule Würzburg-Schweinfurt,
Studienbereich Geo, **„Ausarbeitung von Projekt- und Bachelorarbeiten“, Version
3.01, Würzburg, April 2025**, zusammen.

Es dient als interne Arbeitsgrundlage für die Planung und Kontrolle der
Projektarbeit. Maßgeblich bleiben die jeweils gültige Studien- und
Prüfungsordnung, die Allgemeine Prüfungsordnung sowie die mit dem Betreuer oder
Prüfer vereinbarten Festlegungen.

---

## 1. Verbindlicher Zielrahmen

### 1.1 Umfang

Für eine Projektarbeit mit einer bearbeitenden Person gilt als grobe
Richtschnur:

- **ca. 15–25 Seiten reiner Text**;
- Abbildungen, Tabellen und Anlagen sind in dieser Richtgröße nicht enthalten;
- bei zwei Bearbeitenden nennt das THWS-Dokument ca. 20–40 Seiten;
- die Seitenzahl ist kein oberstes Bewertungskriterium;
- Qualität, fachliche Bearbeitung, Nachvollziehbarkeit und wissenschaftliche
  Aussagekraft sind wichtiger als eine möglichst große Seitenzahl.

Für diese Arbeit wird deshalb ein kompakter Haupttext von ungefähr **15–25
Textseiten** angestrebt. Ausführliche Logs, Rohdaten, Konfigurationsdateien,
Quellcode und vollständige Ergebnislisten werden nicht in den Haupttext
kopiert, sondern eindeutig als digitale Anlagen beziehungsweise als archivierte
Projektdateien referenziert.

### 1.2 Charakter der Projektarbeit

Die Projektarbeit ist eine semesterbegleitende Studienleistung mit komplexem
Inhalt und offenem Lösungsweg. Sie soll insbesondere den Nachweis erbringen von:

- theoretisch-wissenschaftlichen Fähigkeiten;
- fachlichen Fähigkeiten;
- kreativen Fähigkeiten;
- Vermittlungskompetenz;
- selbstständiger Bearbeitung einer komplexen Aufgabenstellung.

Für die vorliegende Scan-to-BIM-Arbeit bedeutet das: Nicht die bloße Auflistung
von ausgeführten Skripten oder Containerbefehlen ist das Ziel. Entscheidend ist
die begründete Darstellung, warum die Pipeline so aufgebaut wurde, wie die
Entscheidungen geprüft wurden, welche Ergebnisse entstanden und welche Grenzen
bestehen.

### 1.3 Zeitlicher Rahmen

Nach dem bereitgestellten THWS-Dokument beträgt die effektive
Nettobearbeitungsdauer der Projektarbeit **vier Wochen**. Der gesamte Workload
kann innerhalb einer Bruttobearbeitungsdauer von höchstens **drei Monaten**
erbracht werden.

Eine Fristüberschreitung kann als nicht ausreichend bewertet werden. Falls eine
nicht selbst verschuldete Verzögerung eintritt, muss der Betreuer oder Prüfer
unverzüglich informiert werden. Eine Fristverlängerung ist innerhalb der
Bearbeitungsfrist schriftlich zu beantragen und erst nach schriftlicher
Genehmigung durch die Prüfungskommission gültig.

---

## 2. Inhaltliche Anforderungen

### 2.1 Wissenschaftliche Arbeitsweise

Die Vorgehensweise muss methodisch-systematisch erfolgen. Eine fachkundige
Person soll die wesentlichen Entscheidungen, Datenflüsse und Ergebnisse
objektiv nachvollziehen und grundsätzlich wiederholen können.

Für die Projektarbeit sind deshalb insbesondere zu dokumentieren:

- die präzise Aufgabenstellung;
- Motivation und fachlicher Mehrwert;
- die verwendeten Datengrundlagen;
- die Auswahl und Begründung der Methoden;
- relevante Parameter und Randbedingungen;
- die tatsächlich durchgeführten Verarbeitungsschritte;
- erfolgreiche und nicht erfolgreiche Versuche;
- die Auswertung und Interpretation der Ergebnisse;
- die Grenzen der Aussagekraft;
- die Schlussfolgerungen für die weitere Bearbeitung.

Hypothesen und technische Entscheidungen dürfen nicht nur genannt werden. Sie
sind zu begründen und anhand der Versuche, Daten oder Literatur einzuordnen.

### 2.2 Nachvollziehbarkeit und Überprüfbarkeit

Die Arbeit muss überprüfbar sein. Relevante Nachweise gehören entweder in den
Haupttext oder in einen eindeutig bezeichneten digitalen Anlagenteil.

Für die aktuelle Pipeline sind insbesondere aufzubewahren und auffindbar zu
machen:

- Eingabedaten und verwendete Bild- beziehungsweise Frameprofile;
- Masken beziehungsweise repräsentative Maskenprüfungen;
- COLMAP- und Kameramodellinformationen;
- verwendete Modell- und Pipelineparameter;
- feste Evaluationslisten und Evaluationsmasken;
- Trainings- und Renderkonfigurationen;
- Status, Logs und Fehlerursachen der Matrixläufe;
- erzeugte Mesh-, Centerline- und GIS-Ausgaben;
- Metrikdateien und die Quelldateien der Grafiken;
- verwendete Skripte und Containerdefinitionen;
- eindeutige Versions- oder Commitangaben, soweit für die Reproduktion
  erforderlich.

Ein allgemeiner Hinweis wie „siehe digitale Anlagen“ reicht nicht aus. Jeder
Anlagenverweis muss möglichst konkret auf einen Ordner, eine Datei oder ein
Manifest zeigen.

### 2.3 Verfahrensbeschreibung

Die verwendeten Verfahren müssen so erklärt werden, dass eine fachkundige
Person den Ablauf und die getroffenen Entscheidungen verstehen kann. Die
Projektarbeit ist kein Lehrbuch. Grundlagen, Formeln und Algorithmen müssen nur
so ausführlich dargestellt werden, wie es für die konkrete Aufgabenstellung,
die Implementierung und die Bewertung erforderlich ist.

Für die vorliegende Arbeit bedeutet das:

- COLMAP wird hinsichtlich SfM, Kameramodell und Domänentrennung erläutert;
- SAM wird hinsichtlich Objektprompt und temporaler Maskenkonsistenz erläutert;
- Gaussian Splatting, STS und die gewählte Meshroute werden funktional
  eingeordnet;
- der Unterschied zwischen Original-GS-Route A und SuGaR-Coarse-Vergleich wird
  begründet;
- die objektmaskierte Metrikberechnung wird definiert;
- die Centerline- und Geometrieausgabe wird als nachgelagerter Nachweis
  beschrieben;
- eine vollständige Wiederholung aller Bibliotheksalgorithmen ist nicht
  erforderlich.

Wenn eine Methode direkt programmiert oder wesentlich verändert wird, müssen
die für das Verständnis notwendigen mathematischen oder algorithmischen
Entscheidungen ausführlicher dargestellt werden.

### 2.4 Umgang mit Abweichungen und Problemen

Die Arbeit soll nicht nur erfolgreiche Ergebnisse darstellen. Technische
Probleme, Fehlversuche und Abweichungen vom ursprünglichen Konzept gehören in
die wissenschaftliche Bewertung, wenn sie für die Lösung relevant sind.

Für die Scan-to-BIM-Pipeline betrifft das beispielsweise:

- leere oder unvollständige Masken;
- Fehler bei festen Eval-Splits;
- Unterschiede zwischen Roh- und idealer Kameradomäne;
- fehlgeschlagene SuGaR-Routen;
- Unterschiede zwischen vorhandenen Zwischenmetriken und vollständigem
  Routenerfolg;
- Fallback-Georeferenzierung ohne unabhängigen Genauigkeitsnachweis;
- Grenzen der Bildmetriken gegenüber echten 3D-Geometriemetriken.

Fehler werden sachlich beschrieben: Ursache, Auswirkung, Korrektur oder
Entscheidung und verbleibende Einschränkung müssen nachvollziehbar sein.

---

## 3. Empfohlener Aufbau der Arbeit

Der vom THWS-Dokument vorgeschlagene Aufbau wird für die Projektarbeit wie
folgt umgesetzt:

1. **Deckblatt** nach dem Muster der Hochschule;
2. **Erklärung zur Projektarbeit**;
3. gegebenenfalls **Sperrvermerk**;
4. **Kurzfassung beziehungsweise Abstract**;
5. **Inhaltsverzeichnis**;
6. **Textteil**;
7. **Literatur- und Quellenverzeichnis**;
8. **Abbildungsverzeichnis**, bei mehr als drei Abbildungen;
9. **Tabellenverzeichnis**, bei mehr als drei Tabellen;
10. **Anlagen beziehungsweise Verweis auf den digitalen Anlagenband**;
11. **Einwilligung zur Plagiatsprüfung mit PlagAware**, sofern verwendet;
12. digitaler Datenträger beziehungsweise digitale Abgabe nach den Vorgaben
    der Prüfungskommission.

### 3.1 Kurzfassung und Abstract

Die Kurzfassung steht vor dem Inhaltsverzeichnis und muss unabhängig vom
Haupttext verständlich sein. Sie soll kurz enthalten:

- Aufgabenstellung und Motivation;
- verwendete Methode beziehungsweise Pipeline;
- wesentliche Ergebnisse oder Erkenntnisse;
- wichtigste Einschränkungen und Schlussfolgerung.

Ein englisches Abstract kann ergänzt werden. Es ist nach dem bereitgestellten
Dokument nicht zwingend, sofern der Betreuer oder Prüfer nichts anderes
vereinbart.

### 3.2 Textteil der Projektarbeit

Der Textteil beginnt mit der Einleitung. Die Einleitung soll:

- das Problem motivieren;
- die Aufgabenstellung erläutern;
- Ziel und Mehrwert der Arbeit nennen;
- die Abgrenzung zur späteren Bachelorarbeit erklären;
- den Leser durch die folgenden Kapitel führen.

Die Kapitelüberschriften müssen einen roten Faden erkennen lassen. Die
Gliederungstiefe soll grundsätzlich auf höchstens drei bis vier Ebenen begrenzt
werden. Eine unterste Gliederungsebene sollte nicht nur einen einzelnen
Unterpunkt enthalten.

### 3.3 Zielgliederung für diese Projektarbeit

Die folgende Gliederung ist der aktuelle Zielrahmen, nicht eine unveränderliche
Vorgabe:

1. **Einleitung, Ziel und Abgrenzung**
   - Motivation des Scan-to-BIM-Problems
   - Aufgabenstellung
   - Ziel und Mehrwert
   - Abgrenzung zum späteren ±10-cm-Genauigkeitsnachweis
2. **Grundlagen**
   - Mehrbildgeometrie und COLMAP
   - Segmentierung und temporale Konsistenz
   - Gaussian Splatting und STS
   - SuGaR und Meshgewinnung
3. **Konzept und Pipeline-Idee**
   - Domänentrennung
   - Datenfluss
   - Produktionsroute A und Vergleichsroute
   - Centerline und Georeferenzierung
4. **Implementierung**
   - Containerstruktur
   - relevante Datenverträge
   - Masken- und Eval-Prüfungen
   - Mesh- und Exportpfad
5. **Versuchsaufbau**
   - Testdatensatz
   - Varianten und konstante Parameter
   - Evaluationsmetriken
   - Erfolgskriterien
6. **Ergebnisse**
   - Status der Versuche
   - objektmaskierte PSNR-, SSIM- und LPIPS-Ergebnisse
   - Endstufen und erzeugte Geometrieprodukte
7. **Diskussion und Grenzen**
   - Interpretation der Kameramodell-, FPS- und Auflösungseinflüsse
   - Bedeutung und Grenzen der Zeit-/Qualitätsauswertung
   - technische Fehlversuche
   - fehlender geodätischer Genauigkeitsnachweis
8. **Fazit und Ausblick**
   - erreichte Projektziele
   - Produktionsentscheidung
   - offene Schritte für die Bachelorarbeit

---

## 4. Aufteilung zwischen Haupttext und Anlagen

### 4.1 In den Haupttext gehören

In den Haupttext werden die Informationen aufgenommen, die zum Verständnis und
zur Bewertung der Arbeit notwendig sind:

- Motivation, Aufgabenstellung und Ziel;
- methodische Grundlagen in angemessener Tiefe;
- Konzept und begründete Designentscheidungen;
- Testaufbau und relevante Parameter;
- repräsentative Abbildungen und Tabellen;
- ausgewählte Resultate;
- kritische Interpretation und Grenzen;
- Schlussfolgerungen.

Die vollständige technische Repository-Dokumentation gehört nicht in den
Haupttext. Sie wird über präzise Anlagenverweise zugänglich gemacht.

### 4.2 In den digitalen Anlagenteil gehören

Das THWS-Dokument nennt als Anlagen insbesondere:

- sämtliche Messdaten und gegebenenfalls Zwischenergebnisse;
- relevante Datenbestände und Projektdateien;
- ergänzende Ergebnislisten;
- Quellcodes und nicht sinnvoll in DIN A4 integrierbare Dateien;
- die digitale, lesbare PDF der Arbeit;
- bei einer Bachelorarbeit zusätzlich das Plakat in den geforderten Formaten.

Für diese Projektarbeit wird der digitale Anlagenteil mindestens über folgende
Bereiche organisiert:

- `data/10_runs/` für archivierte Versuchsläufe;
- `docs/grafiken/` für erzeugte Grafiken und tabellarische Auswertungen;
- `tools/` und `src/` für Auswertungs- und Pipelinecode;
- `PA/appendices/` für zusammenfassende technische Anhänge;
- Manifest-, Parameter- und Statusdateien für die eindeutige Zuordnung.

Große Rohdaten müssen nicht in den Fließtext oder mehrfach in den PA-Ordner
kopiert werden. Es muss jedoch ein lesbarer Index vorhanden sein, der Herkunft,
Version, Dateipfad und Zweck der Daten beschreibt.

---

## 5. Formale und sprachliche Regeln

### 5.1 Sprache

Die Arbeit soll in präziser wissenschaftlicher Schriftsprache verfasst werden.
Zu beachten sind insbesondere:

- kurze, klare und strukturierte Sätze;
- eindeutige Bezüge und logisch geschlossene Argumente;
- keine Umgangssprache;
- etablierte englische Fachbegriffe dürfen verwendet werden;
- Fachbegriffe sollen innerhalb der Arbeit konsistent verwendet werden;
- grundsätzlich sachliche und möglichst unpersönliche Formulierungen;
- `Ich`- und `Wir`-Form nur sparsam und begründet einsetzen;
- Rechtschreibung und Grammatik vor der Abgabe prüfen;
- nur projektrelevante Sachverhalte in den Haupttext aufnehmen.

Die Arbeit soll fachlich präzise, aber nicht unnötig schwer verständlich
formuliert sein.

### 5.2 Messwerte und numerische Angaben

Die Anzahl der signifikanten Stellen muss zur Genauigkeit des jeweiligen Werts
passen. Zu viele Nachkommastellen können eine nicht vorhandene Genauigkeit
vortäuschen.

Für die Matrixauswertung bedeutet das:

- Einheiten beziehungsweise dimensionslose Metriken müssen klar benannt
  werden.
- PSNR wird mit einer begründeten Anzahl an Nachkommastellen angegeben.
- SSIM und LPIPS werden nicht mit mehr Stellen dargestellt, als die
  Reproduzierbarkeit und Streuung rechtfertigen.
- Laufzeiten werden mit einer sinnvollen Zeitauflösung angegeben.
- Geometrische Aussagen werden nicht genauer formuliert, als die Datenbasis
  erlaubt.
- Ein technischer Zwischenwert darf nicht als vollständiges Endergebnis
  ausgegeben werden.

### 5.3 Abbildungen und Tabellen

Abbildungen und Tabellen müssen prägnant beschriftet werden. Im Fließtext muss
auf jede relevante Darstellung verwiesen werden. Die Darstellung ist nicht nur
zu zeigen, sondern zu erläutern und zu interpretieren.

Für diese Arbeit bedeutet das:

- jede Abbildung erhält eine aussagekräftige Bildunterschrift;
- jede Tabelle erhält eine eindeutige Tabellenüberschrift oder Beschriftung;
- Achsen, Einheiten, Legenden und Farbcodierungen müssen verständlich sein;
- Statusfarben dürfen erfolgreiche, unvollständige und nicht vergleichbare
  Läufe nicht vermischen;
- Grafiken werden im Text inhaltlich ausgewertet;
- bei mehr als drei Abbildungen wird ein Abbildungsverzeichnis vorgesehen;
- bei mehr als drei Tabellen wird ein Tabellenverzeichnis vorgesehen.

### 5.4 Quellen und Zitate

Es wird ein einheitliches Literatur- beziehungsweise Quellenverzeichnis
geführt. In das Verzeichnis gehören nur Quellen, die im Text tatsächlich
verwendet oder zitiert werden.

Für die aktuelle Arbeit sind vorrangig zu verwenden:

- wissenschaftliche Konferenz- und Journalbeiträge;
- Bücher und verlegte E-Books;
- offizielle Dokumentationen oder Projektseiten für Software;
- aktuelle, fachlich belastbare Quellen für neuere Methoden;
- eigene Projektdateien nur als klar gekennzeichnete interne Artefakte.

Bei zwei Autoren werden beide Namen im Text genannt. Bei mehr als zwei Autoren
kann im Text der erste Autor mit „et al.“ verwendet werden; im Verzeichnis
werden alle Autoren aufgeführt. Internetquellen erhalten URL und letztes
Abrufdatum. Die verwendete Zitierweise muss durchgängig einheitlich sein.

### 5.5 Nutzung von KI

Die Zulässigkeit und der Umfang der Nutzung von KI-Werkzeugen müssen mit dem
Betreuer oder Prüfer transparent abgestimmt werden. KI-generierte Inhalte sind
keine zitierfähige wissenschaftliche Literatur.

Für relevante KI-Nutzung werden separat dokumentiert:

- relevante Prompts beziehungsweise Eingaben;
- Name und Version des KI-Werkzeugs;
- Anbieter oder Betreiber;
- Datum der Generierung;
- gegebenenfalls die übernommenen oder geänderten Inhalte.

Die studierende Person trägt die Verantwortung für die fachliche Richtigkeit,
die Eigenständigkeit und die kritische Überprüfung aller Inhalte. Übernommene
KI-Inhalte müssen nach den mit dem Prüfer abgestimmten Regeln kenntlich gemacht
werden. Reine orthografische oder grammatikalische Korrekturen können nach dem
THWS-Muster ausgenommen sein; dies muss im Zweifel mit dem Prüfer abgestimmt
werden.

---

## 6. Bewertungs- und Präsentationsrahmen

### 6.1 Bewertungsrelevante Kriterien

Nach dem bereitgestellten Dokument werden unter anderem folgende Kriterien
berücksichtigt:

- fachliche Bearbeitung: Motivation, Problemerfassung, Aufgabenlösung und
  Umsetzung;
- Nutzung von Fachwissen und Methodik;
- angemessene Werkzeug- und Methodenwahl;
- kritische Reflexion und wirtschaftliches Denken;
- zielgerichtetes, systematisches Vorgehen;
- Qualität und Schlüssigkeit der Ergebnisse;
- wissenschaftliche Arbeitsweise und Literaturrecherche;
- Selbstständigkeit und Eigeninitiative;
- aufgabenspezifische Kreativität;
- Gliederung und Struktur;
- Qualität von Sprache, Grafiken, Tabellen und Literaturarbeit;
- Vollständigkeit und Nutzbarkeit der abgegebenen Daten.

Die Projektarbeit muss daher nicht nur zeigen, dass ein Lauf technisch
funktioniert. Sie muss auch zeigen, dass die Auswahl, Bewertung und Einordnung
der Lösung eigenständig und fachlich begründet erfolgt sind.

### 6.2 Vortrag

Zur Projektarbeit gehört neben der schriftlichen Ausarbeitung ein mündlicher
Vortrag. Für eine bearbeitende Person ist im bereitgestellten Dokument eine
Dauer von ungefähr **20 Minuten** angegeben; bei zwei Bearbeitenden ungefähr
30 Minuten. Anschließend findet eine Fragerunde der Prüfer statt.

Der Vortrag soll sich auf die wesentlichen Punkte konzentrieren:

- Problem und Motivation;
- eigene Leistung;
- Konzept und wichtigste Entscheidungen;
- ausgewählte Versuche und Ergebnisse;
- Grenzen;
- Fazit.

---

## 7. Abgabe und organisatorische Punkte

Die Projektarbeit wird nach dem bereitgestellten Dokument digital bei den
zuständigen Personen eingereicht. Die genaue Abgabeform, Anzahl der Dateien,
Plagiatsprüfung und eventuelle Anonymisierung sind mit den aktuellen Vorgaben
der Prüfungskommission und dem Betreuer beziehungsweise Prüfer abzugleichen.

Wichtig ist der Grundsatz der vollständigen einmaligen Abgabe: Fehlende
Bestandteile wie Anlagen oder Datenträger dürfen nicht als nachträgliche
Nachlieferung eingeplant werden.

Vor der Abgabe sind insbesondere zu prüfen:

- vollständiges PDF mit Deckblatt, Kurzfassung, Textteil, Quellen und Anlagen-
  verweisen;
- Erklärung zur Projektarbeit;
- eindeutige digitale Anlagen;
- Lesbarkeit aller Dateien;
- korrekte Seitenzahlen und Querverweise;
- vollständige Abbildungs- und Tabellenbeschriftungen;
- Rechtschreibung und Grammatik;
- nachvollziehbare Daten- und Versionsablage;
- abgestimmte KI-Dokumentation;
- abgestimmte Einwilligung zur Plagiatsprüfung.

---

## 8. PA-spezifische Zielkontrolle

Die Projektarbeit gilt im Rahmen dieses Zielrahmens als inhaltlich passend,
wenn sie die folgenden Fragen beantwortet:

1. Welches Scan-to-BIM-Problem wird untersucht und warum ist es relevant?
2. Welches konkrete Ziel und welchen Mehrwert hat die Projektarbeit?
3. Welche Grundlagen sind zum Verständnis der Pipeline erforderlich?
4. Warum wurden die Bild-, Masken- und Geometriedomänen getrennt?
5. Welche Pipelinevarianten wurden untersucht und wie wurden sie ausgewählt?
6. Welche Daten, Parameter und Evaluationsregeln wurden verwendet?
7. Welche Ergebnisse sind vollständig erfolgreich und welche nur
   Zwischenresultate?
8. Was zeigen PSNR, SSIM und LPIPS tatsächlich und was nicht?
9. Welche technischen Fehler und Abweichungen traten auf?
10. Welche Endprodukte wurden erzeugt?
11. Welche Aussagen sind wegen fehlender GNSS-/Vermessungsreferenz noch nicht
    zulässig?
12. Welche konkreten nächsten Schritte folgen in der Bachelorarbeit?

### Zielumfang für die aktuelle Fassung

- Haupttext: **ca. 15–25 Seiten**;
- maximal drei bis vier Gliederungsebenen;
- etwa sechs bis acht ausgewogene Hauptkapitel;
- repräsentative Grafiken im Haupttext;
- vollständige Rohdaten und technische Detailnachweise in digitalen Anlagen;
- keine Behauptung einer realen ±10-cm-Genauigkeit ohne geeignete Referenz;
- keine Gleichsetzung von vorhandenen Zwischenmetriken mit einem
  erfolgreichen vollständigen Pipeline-Lauf.

---

## 9. Offene Abstimmungen mit Betreuer oder Prüfer

Vor der finalen Abgabe sind mindestens folgende Punkte abzustimmen:

- endgültiger Titel und genaue Aufgabenstellung;
- Bearbeitungszeitraum und Abgabetermin;
- Erst- und Zweitprüfer sowie Betreuer;
- Studiengang und Angaben auf dem Deckblatt;
- Zulässigkeit und Kennzeichnung der KI-Unterstützung;
- gewünschte Form des digitalen Anlagenbands;
- Einsatz und Form der PlagAware-Einwilligung;
- Umfang der technischen Anlagen;
- endgültige Auswahl der Hauptgrafiken;
- Anforderungen an den Vortrag.

Diese Abstimmungen werden nicht durch dieses Dokument ersetzt. Der Zielrahmen
ist eine strukturierende Arbeitsgrundlage auf Basis des bereitgestellten
THWS-Dokuments.
