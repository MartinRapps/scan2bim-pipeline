# Vergleich der Kollegenarbeit und persönliche Fokusfragen

## Zweck des Dokuments

Dieses Dokument soll die weitere Planung der Projektarbeit strukturieren. Es
verbindet zwei Aufgaben:

1. Die Projektarbeit eines Kommilitonen wird nach denselben Kriterien wie der
   [Zielrahmen](Zielrahmen.md) bewertet.
2. Die persönlichen Schwerpunkte der eigenen Projektarbeit werden festgelegt,
   bevor Gliederung, Text und Anlagen weiter ausgebaut werden.

## Bearbeitungsstand und Materialbasis

Die Kollegenarbeit liegt nun als [PA/Watzke_PA.pdf](Watzke_PA.pdf) vor. Sie
trägt den Titel „Postfilterung von SAM-3-Segmentierungen auf bayerischen
DOP20-Orthophotos mit nDSM“, wurde von Philipp Watzke verfasst und umfasst
75 PDF-Seiten. Der eigentliche Textteil reicht laut Inhalts- und
Seitenangaben bis Seite 61. Danach folgen Quellen- und Verzeichnisse sowie die
Dokumentation der KI-Nutzung.

Die folgende Bewertung bezieht sich auf die sichtbare Struktur, die
Argumentation, die Methodik, die Ergebnisdarstellung und die im PDF
dokumentierten Anlagen. Sie ist keine Benotung der Kollegenarbeit und keine
Übernahme fremder Inhalte. Übernommen werden sollen nur Strukturprinzipien,
Begründungsmuster und geeignete Nachweisformen.

Die konkrete Auswertung ist in Abschnitt 0 dokumentiert. Die nachfolgenden
Abschnitte enthalten zusätzlich den allgemeinen Bewertungsmaßstab und die
persönlichen Fokusfragen für die nächste Überarbeitung.

| Prüffeld | Bewertung |
|---|---|
| Allgemein gute Elemente | Struktur, Argumentation, Methodik, Visualisierung, Quellen, Anlagen |
| Passung zum Zielrahmen | Umfang, wissenschaftliche Nachvollziehbarkeit, Haupttext/Anlagen-Trennung |
| Fehlende Elemente | Aufgabenstellung, Begründungen, Quellen, Ergebnisinterpretation, Anlagenverweise usw. |
| Für die eigene PA übernehmen | Prinzipien, nicht ungeprüft fremde Inhalte oder Formulierungen |
| Für die eigene PA weglassen | Überlange technische Details, redundante Dokumentation, nicht benötigte Theorie |
| Konsequenz für die eigene Struktur | Kapitel, Seitenbudget, Abbildungen, Anlagen und offene Entscheidungen |

---

## Konkrete Analyse der Kollegenarbeit

### 0.1 Kurzprofil

Die Arbeit untersucht eine klar abgegrenzte Forschungsfrage: den Einfluss eines
nDSM-Mindesthöhenfilters auf SAM-3-basierte Gebäude-Polygone aus DOP20-
Orthophotos. Die Arbeit verwendet eine SAM-only-Baseline und eine nDSM-
gefilterte Variante, acht AOIs, eine Trennung in In-Sample- und
Out-of-Sample-Gebiete, mehrere Referenz- und Matchingvarianten sowie eine
manuelle Plausibilitätsprüfung.

Die Kapitelstruktur ist:

1. Einleitung mit Motivation, Problemstellung, Zielsetzung, Forschungsfragen,
       Abgrenzung und Aufbau;
2. Datengrundlagen und Fachkontext;
3. technische Grundlagen;
4. Methodik;
5. Implementierung;
6. Ergebnisse;
7. Diskussion;
8. Fazit und Ausblick;
9. Quellen, Abbildungs- und Tabellenverzeichnis;
10. Anhang zur KI-Nutzung und digitaler Nachweis.

Die Arbeit ist damit formal und wissenschaftlich sehr vollständig aufgebaut.
Der wesentliche Kritikpunkt ist nicht eine fehlende Qualität, sondern die
deutliche Überschreitung des für eine einzelne Projektarbeit vorgesehenen
Textumfangs. Der Textteil reicht bereits bis Seite 61, während der THWS-
Zielrahmen für eine einzelne Projektarbeit ungefähr 15–25 Seiten reinen Text
als Richtschnur nennt. Die Kollegenarbeit ist deshalb ein gutes methodisches
Beispiel, aber keine sinnvolle Umfangsvorlage für die eigene PA.

### 0.2 Was allgemein besonders gut ist

#### a) Unabhängige Kurzfassung

Die Kurzfassung beschreibt Aufgabenstellung, Daten, Methode, Szenarien,
Evaluationslogik, zentrale Zahlen und Grenzen. Besonders gut ist, dass nicht
nur ein positiver Effekt behauptet wird: Der nDSM-Filter verbessert den
OOS-Area-F1-Wert gegen die primäre Referenz nicht sichtbar, verändert aber
Purity, Coverage und die Zusammensetzung verworfener Polygone. Die Kurzfassung
ist dadurch tatsächlich unabhängig vom Haupttext lesbar.

**Übertragbar auf die eigene PA:** Die Kurzfassung sollte in wenigen Absätzen
Problem, Pipeline, wichtigste Ergebnisse und die fehlende geometrische
Referenzgenauigkeit nennen. Sie sollte keine Installations- oder
Implementierungsdetails enthalten.

#### b) Klare Aufgabenstellung und Forschungsfragen

Die Kollegenarbeit trennt Motivation, Problemstellung, Zielsetzung,
Forschungsfragen und Abgrenzung. Die fünf Forschungsfragen sind direkt mit der
späteren Evaluation verbunden. Die Arbeit beantwortet die Fragen am Ende
nochmals einzeln.

**Übertragbar auf die eigene PA:** Eine Hauptfrage mit höchstens zwei bis drei
Unterfragen ist sinnvoller als eine bloße Pipelinebeschreibung. Die Fragen
sollten direkt zu den vorhandenen Daten und Tests passen.

#### c) Baseline und kontrollierte Variante

Die Gegenüberstellung von `sam_only` und `sam_ndsm_min15` ist methodisch
stark. Nur eine Verarbeitungsentscheidung wird verändert; die übrige Kette
bleibt vergleichbar. Zusätzlich werden IS und OOS räumlich getrennt, sodass die
Arbeit nicht nur die AOIs bewertet, aus denen Entscheidungen abgeleitet wurden.

**Übertragbar auf die eigene PA:** Die Grundidee „Baseline gegen eine
kontrollierte Variante“ sollte übernommen werden. Für die eigene Pipeline
kann das beispielsweise bedeuten: Produktionsroute A als Hauptpfad,
Kameramodell/FPS/Auflösung als definierte Ablation und SuGaR-Coarse als
separater Vergleichspfad.

#### d) Kritische Referenz- und Metrikbetrachtung

Die Kollegenarbeit weist ausdrücklich darauf hin, dass sichtbare Dachflächen
und amtliche Hausgrundrisse nicht identisch sind. Sie verwendet deshalb Area-,
Component- und Strict-F1 sowie Coverage und Purity. Ebenso wird das
Many-to-Many-Problem der Objektgranularität erklärt.

**Übertragbar auf die eigene PA:** Die saubere Trennung zwischen Messgröße und
Aussage ist besonders wichtig. Für die eigene Arbeit muss ebenso erklärt
werden, dass objektmaskierte PSNR-, SSIM- und LPIPS-Werte die
Ansichtsqualität eines object-only Splats bewerten, aber keine geometrische
Genauigkeit, Centerline-RMSE oder GNSS-Übereinstimmung beweisen.

#### e) Fehler- und Wirkungsanalyse

Die Reject-Impact-Analyse und die manuelle Plausibilitätsprüfung sind starke
Elemente. Sie erklären, warum sich globale Kennzahlen kaum verändern können,
obwohl einzelne lokal sichtbare Verbesserungen auftreten. Die Arbeit trennt
außerdem die 30 vor der NMS verworfenen Kandidaten von den 30 Polygonen der
finalen Szenariodifferenz.

**Übertragbar auf die eigene PA:** Mindestens ein technischer Fehlerfall und
eine kurze Ursachenanalyse sollten in den Haupttext. Dazu gehören zum Beispiel
die leere Eval-Maske, die Dateinamens-/Stem-Problematik beim SuGaR-Split und
die Tatsache, dass vorhandene `sts_masked.json`-Metriken keine erfolgreiche
SuGaR-Route beweisen.

#### f) Reproduzierbarkeit

Die Arbeit dokumentiert unter anderem AOI-Konfigurationen, Splits, Schwellen,
SAM-Commit, Checkpoint-Snapshot, Repository-Commit, Python-/PyTorch-Version,
GPU und zentrale Parameter. Die vollständige technische Detailtiefe wird in
den digitalen Nachweis ausgelagert.

**Übertragbar auf die eigene PA:** Ein kompakter Laufsteckbrief im Haupttext
und ein vollständiges Manifest in den Anlagen sind sinnvoller als eine lange
Beschreibung jedes Skripts.

#### g) Transparente KI-Dokumentation

Die Kollegenarbeit enthält einen separaten Anhang mit Werkzeug, Anbieter,
Zeitpunkt, Einsatzbereich, Interaktionsgruppen und digitalem Nachweis. Sie
grenzt Rechercheunterstützung, Implementierungsunterstützung und
LaTeX-Überführung voneinander ab und erklärt die fachliche Kontrolle durch den
Verfasser.

**Übertragbar auf die eigene PA:** Die Dokumentationslogik ist sehr gut. Sie
sollte jedoch auf die tatsächlich verwendeten Werkzeuge und Prompts reduziert
werden und nicht unkritisch kopiert werden.

### 0.3 Was zum THWS-Zielrahmen passt

Die folgenden Elemente entsprechen dem [Zielrahmen](Zielrahmen.md) besonders
gut:

| Element der Kollegenarbeit | Passung zum Zielrahmen | Bedeutung für die eigene PA |
|---|---|---|
| Deckblatt und Erklärung | vollständig passend | übernehmen und eigene Angaben einsetzen |
| unabhängige Kurzfassung | sehr gut passend | beibehalten |
| Einleitung mit Motivation, Ziel, Fragen und Abgrenzung | sehr gut passend | als Muster für den roten Faden verwenden |
| Daten- und Fachkontext | passend | nur auf die eigenen Pipeline-Daten reduzieren |
| getrennte Methodik und Implementierung | passend | in der eigenen PA stärker zusammenfassen |
| Baseline-/Variantenvergleich | wissenschaftlich sehr passend | auf wenige eigene Varianten begrenzen |
| quantitative plus qualitative Bewertung | sehr passend | Bildmetriken plus technische/geometrische Nachweise trennen |
| Diskussion der Referenzgrenzen | vorbildlich | bei fehlender GNSS-Referenz ausdrücklich übernehmen |
| Quellenverzeichnis, Abbildungs- und Tabellenverzeichnis | formal passend | bei ausreichender Anzahl vorsehen |
| KI-Anhang | sehr passend zum aktuellen THWS-Hinweis | eigenen Anhang mit realen Angaben erstellen |
| digitale Anlagen und reproduzierbare Konfigurationen | sehr passend | mit konkreten Pfaden und Manifesten umsetzen |

### 0.4 Was für die eigene PA zu umfangreich wäre

Folgende Elemente sind in der Kollegenarbeit wissenschaftlich sinnvoll, sollten
aber nicht im gleichen Umfang übernommen werden:

- fünf Forschungsfragen; für die eigene PA reichen eine Hauptfrage und zwei bis
      drei Unterfragen;
- acht AOIs mit vier Bebauungsstrukturen und getrennten IS-/OOS-Splits;
- zwei Referenzvarianten plus mehrere Matchingdefinitionen;
- vier Metriksichten mit zusätzlichen Coverage-/Purity-Auswertungen;
- ausführliche Beschreibung jedes Datenzugriffs, jeder Paketstruktur und jeder
      API-Funktion;
- detaillierte Polygon-NMS-, Rasterattributierungs- und Geodatenlogik;
- vollständige tabellarische Darstellung jedes Strukturtyps;
- umfangreiche manuelle Stichproben, wenn keine unabhängige Referenz dafür
      vorliegt;
- ein ausführlicher Alternativenkatalog, der keine Entscheidung für die eigene
      Pipeline verändert;
- technische Details, die in einer reproduzierbaren Anlage besser aufgehoben
      sind.

Die Kollegenarbeit zeigt, wie eine große Untersuchung wissenschaftlich
begründet werden kann. Sie zeigt nicht, dass eine Projektarbeit zwingend alle
diese Ebenen benötigt.

### 0.5 Was für die eigene PA noch ergänzt oder anders formuliert werden sollte

Die Kollegenarbeit ist auf Gebäude-Polygonisierung und eine definierte
amtliche Referenz ausgerichtet. Für die eigene Scan-to-BIM-PA sind daher einige
andere Nachweise entscheidend:

1. **Domänentrennung:** Rohbilder und originales COLMAP-Modell für SfM/GCP,
       ideale PINHOLE-Domäne für STS und Meshroute, Maskenwarp mit derselben
       Abbildung.
2. **Routenstatus:** Zwischenmetriken müssen vom vollständigen Erfolg einer
       Mesh-, Render- und Postprocess-Route getrennt werden.
3. **Metrikgrenzen:** PSNR, SSIM und LPIPS ausschließlich objektmaskiert und
       nicht als 3D-Genauigkeitsnachweis interpretieren.
4. **Geometrieprodukt:** Coarse-Mesh, Centerline, B-Spline und GeoJSON als
       technische Endprodukte zeigen; lokale Geometrie und globale
       Georeferenzierung unterscheiden.
5. **Geodätische Abgrenzung:** Ohne unabhängige GNSS-/Vermessungsreferenz keine
       ±10-cm-Aussage formulieren.
6. **Fehleranalyse:** die behobenen Split-, Masken- und Renderprobleme als
       wissenschaftliche Erkenntnisse dokumentieren, aber nicht in eine lange
       Installationsgeschichte ausweiten.

### 0.6 Klare Empfehlung: übernehmen, anpassen, weglassen

#### Übernehmen

- unabhängige Kurzfassung mit Methode, Ergebnis und Grenze;
- Einleitung mit Motivation, Ziel, Arbeitsfragen und Abgrenzung;
- Baseline gegen kontrollierte Variante;
- feste Evaluationsregeln vor der Ergebnisinterpretation;
- repräsentative quantitative Tabellen;
- eine qualitative oder diagnostische Fehleranalyse;
- getrennte Diskussion von Ergebnis, Interpretation und Limitierung;
- kompakter Reproduzierbarkeitssteckbrief;
- Quellen-, Abbildungs- und Tabellenverzeichnis nach THWS-Zielrahmen;
- separater KI-Nutzungsnachweis;
- digitale Anlagen mit konkreten Datei- und Manifestpfaden.

#### Anpassen

- Forschungsfragen auf eine Hauptfrage plus zwei bis drei Unterfragen reduzieren;
- statt acht AOIs die vorhandene Versuchs- beziehungsweise Matrixstruktur
      verwenden;
- statt vieler Referenzmetriken die drei festgelegten objektmaskierten
      Bildmetriken verwenden;
- die technische Produktionsentscheidung A als Hauptargument führen und
      SuGaR-Coarse als Vergleich oder offenen Follow-up kennzeichnen;
- `Average` nur aus vollständig vergleichbaren 2-FPS-/5-FPS-Läufen bilden;
- Laufzeiten als sekundäres Engineering-Screening und nicht als Primärqualität
      darstellen;
- ausführliche Parameter, Logs und Rohdaten in Anlagen verlagern.

#### Weglassen

- Gebäude- oder Fernerkundungstheorie ohne Bezug zur eigenen Pipeline;
- Polygon- und nDSM-spezifische Verfahren;
- viele alternative Methoden, wenn sie nicht getestet oder entscheidungsrelevant
      sind;
- eine Vollauflistung aller Einzelresultate im Haupttext;
- eine rein bildmetrische Rangfolge als Geometriebeweis;
- unvollständige SuGaR-Läufe als erfolgreiche Vergleichsergebnisse;
- Code- oder Containerdetails ohne wissenschaftliche Funktion;
- fremde Formulierungen, Tabellen oder Abbildungen.

### 0.7 Empfohlene Struktur nach der Analyse

Für die eigene PA wird folgende fokussierte Struktur empfohlen:

| Kapitel | Inhalt | Zielumfang |
|---|---|---:|
| 1 Einleitung | Motivation, Frage, Ziel, Mehrwert, Abgrenzung | 1,5–2 Seiten |
| 2 Grundlagen | nur COLMAP, Masken, STS/GS, Mesh und Metriken | 2,5–3,5 Seiten |
| 3 Konzept | Domänentrennung, Datenfluss, Produktionsroute A | 2–3 Seiten |
| 4 Umsetzung | relevante Datenverträge, Prüfungen, Endstufen | 2–2,5 Seiten |
| 5 Versuchsaufbau | Matrix, konstante Parameter, Eval-Split, Erfolgskriterien | 2–3 Seiten |
| 6 Ergebnisse | Status, Metriken, Endprodukte, ein Fehlerfall | 3–4 Seiten |
| 7 Diskussion | Interpretation, Grenzen, Geometrie-/Metriktrennung | 2–3 Seiten |
| 8 Fazit und Ausblick | Projektziel, Produktionsentscheidung, BA-Schritte | 1–1,5 Seiten |
| **Gesamt** | **Haupttext ohne Verzeichnisse und Anlagen** | **ca. 16–22 Seiten** |

Damit wird der gute wissenschaftliche Kern der Kollegenarbeit übernommen,
ohne deren 61-seitigen Textumfang zu reproduzieren.

---

## 1. Bewertungsmaßstab für die Kollegenarbeit

### 1.1 Allgemein gute Bestandteile

Bei der Analyse wird geprüft, ob die Kollegenarbeit:

- eine klar erkennbare Aufgabenstellung besitzt;
- Motivation, Ziel und Mehrwert verständlich erklärt;
- einen roten Faden von Problem über Methode zu Ergebnis aufweist;
- fachliche Entscheidungen begründet und nicht nur beschreibt;
- Methoden in einer für fachkundige Leser angemessenen Tiefe erläutert;
- Versuche und Ergebnisse reproduzierbar dokumentiert;
- erfolgreiche und fehlgeschlagene Ansätze offen darstellt;
- Abbildungen und Tabellen im Text erklärt und interpretiert;
- geeignete und aktuelle Quellen tatsächlich inhaltlich verwendet;
- Haupttext und Anlagen sinnvoll trennt;
- eine klare Schlussfolgerung aus den Ergebnissen ableitet;
- insgesamt trotz umfangreicher Anlagen lesbar und fokussiert bleibt.

### 1.2 Passung zum THWS-Zielrahmen

Die Kollegenarbeit wird insbesondere gegen folgende Anforderungen aus dem
[Zielrahmen](Zielrahmen.md) geprüft:

- Haupttext ungefähr 15–25 Seiten bei einer bearbeitenden Person;
- Qualität statt bloßer Seitenzahl;
- wissenschaftlich-systematisches und nachvollziehbares Vorgehen;
- konkrete Aufgabenstellung, Motivation, Ziel und Mehrwert;
- angemessene Beschreibung der Verfahren;
- kritische Bewertung und Interpretation der Ergebnisse;
- prägnante Abbildungen und Tabellen mit Verweisen im Fließtext;
- einheitliche, zitierfähige Quellen;
- eindeutige digitale Anlagen und Datenpfade;
- sachliche Sprache, konsistente Begriffe und angemessene Genauigkeit;
- transparente Dokumentation einer zulässigen KI-Nutzung.

Ein längerer Text ist daher nicht automatisch besser. Ein Abschnitt wird nur
dann als Vorbild für die eigene PA bewertet, wenn sein Umfang durch seine
wissenschaftliche Funktion gerechtfertigt ist.

### 1.3 Typische Elemente, die häufig fehlen

Bei der Analyse wird besonders auf folgende mögliche Lücken geachtet:

- präzise Abgrenzung zwischen Ziel, Methode und Ergebnis;
- explizite Forschungs- oder Arbeitsfragen;
- Begründung der Parameter- und Variantenwahl;
- Definition der Erfolgskriterien;
- Trennung von Beobachtung, Interpretation und Schlussfolgerung;
- Bewertung von Fehlern und nicht erfolgreichen Versuchen;
- quantitative Vergleichswerte statt nur Screenshots;
- Angaben zu Datenherkunft, Versionen und Reproduzierbarkeit;
- Quellen direkt an den fachlichen Aussagen;
- Quellenverzeichnis ohne ungenutzte Literatur;
- Anlagenverweise mit konkreten Datei- oder Ordnernamen;
- Aussagegrenzen und Übertragbarkeit auf den späteren Anwendungsfall;
- persönliche Eigenleistung bei Nutzung fremder Software oder Methoden.

---

## 2. Fragen zur persönlichen Ausrichtung der PA

Bitte die Fragen zunächst mit kurzen Stichworten beantworten. Die Antworten
dienen anschließend als Grundlage für die endgültige Gliederung und das
Seitenbudget.

### 2.1 Hauptziel der Projektarbeit

**Welche Aussage soll eine fachkundige Person nach dem Lesen sicher treffen
können?**

Antwort:

> 

**Welche Formulierung beschreibt das Hauptziel am besten?**

- [ ] Die technische Pipeline funktioniert von der Bildsequenz bis zur
      Centerline.
- [ ] Die Original-GS-Meshroute A ist für den Projektstand die sinnvollste
      Produktionsroute.
- [ ] Kameramodell, FPS und Auflösung werden systematisch verglichen.
- [ ] Objektmaskierte Bildmetriken werden reproduzierbar bestimmt.
- [ ] Die gesamte Scan-to-BIM-Kette wird als Vorbereitung für die
      Bachelorarbeit validiert.
- [ ] Ein anderes Ziel:

Antwort beziehungsweise Priorisierung:

> Die technische Pipeline funktioniert von der Bildsequenz bis zur Centerline und wurde dabei auf Robustheit und Funktionalität geprüft

### 2.2 Wichtigstes Endprodukt

**Welches Ergebnis soll im Mittelpunkt stehen?**

- [ ] Objektmaske beziehungsweise temporale Segmentierung
- [ ] Kameramodell und ideale Bilddomäne
- [ ] objektspezifische Gaussian-Repräsentation
- [ ] Original-GS-Mesh
- [ ] Centerline und B-Spline
- [ ] GeoJSON beziehungsweise GIS-Export
- [ ] reproduzierbare Matrixauswertung
- [ ] Vergleich von Original-GS und SuGaR-Coarse
- [ ] anderes Endprodukt:

**Welches Endprodukt soll im Haupttext gezeigt werden und welches nur in den
Anlagen?**

Haupttext:

> Es soll alles in dem Haupttext anhand des besten besipiel zu sehen sein oder im vergleich zu schlechten einstellungen. + Vegleich von Orginal GS und Sugar Coarse. Das Endprodukt ist also die Pipline in interaktivem bzw. Autopliot betrieb. (abgeshen von der Georeferenzierung) 

Anlagen:

> Die Posptrocess ergebnisse also vorallem das GEOJSON

### 2.3 Abgrenzung

**Welche Aussagen sollen ausdrücklich nicht Ziel der PA sein?**

Mögliche Punkte:

- [ ] kein Nachweis einer realen ±10-cm-Genauigkeit;
- [ ] keine vollständige Vermessung einer realen Rohr- oder Kabeltrasse;
- [ ] keine vollständige Dokumentation jedes Repository-Skripts;
- [ ] keine allgemeine Einführung in alle Verfahren der Computer Vision;
- [ ] keine vollständige Leistungsbewertung aller denkbaren Kameramodelle;
- [ ] keine Produktionsempfehlung allein auf Basis von PSNR, SSIM und LPIPS;
- [ ] anderes:

Eigene Abgrenzung:

> alles obere

### 2.4 Persönlicher Schwerpunkt

**Welcher Schwerpunkt soll erkennbar als eigene Leistung hervortreten?**

- [ ] Pipeline-Konzeption und Domänentrennung
- [ ] robuste Masken- und Eval-Datenverträge
- [ ] kameramodellbewusste Verarbeitung
- [ ] Matrixautomatisierung und reproduzierbare Auswertung
- [ ] Original-GS-Meshgewinnung und Geometrieerhalt
- [ ] Centerline- und GIS-Nachverarbeitung
- [ ] wissenschaftliche Interpretation und Fehleranalyse
- [ ] anderes:

Begründung:

> Pipeline Konzeption und Domänentrennung; GS Meshgewinngung und Geometrie erhalt, aber insbesondere die Meshgewinnung über die Masken von SAM3; wissenschafltiche test und deren Interpretation (wissenschaftliches vorgehen)

---

## 3. Fragen zur wissenschaftlichen Tiefe

### 3.1 Grundlagen

**Wie viel Grundlagenwissen soll die Leserin oder der Leser benötigen, um die
Arbeit zu verstehen?**

- [ ] nur die für die konkrete Pipeline notwendigen Grundlagen;
- [x] zusätzlich ein kompakter Vergleich der verwendeten Methoden;
- [ ] ausführlichere mathematische Darstellung einzelner Algorithmen;
- [ ] vorwiegend praktische Beschreibung mit wenigen Formeln;
- [ ] anderes:

**Bei welchen Verfahren soll eine Formel oder ein Algorithmus explizit
erscheinen?**

- [ ] Kameramodell und Ent-/Verzeichnung
- [ ] Bundle Adjustment beziehungsweise SfM
- [x] PSNR, SSIM und LPIPS
- [x] Gaussian Splatting
- [ ] Poisson-Rekonstruktion
- [x] Centerline/B-Spline
- [ ] keine zusätzlichen Formeln außer den Evaluationsmetriken
- [x] anderes: SuGar Methode mit dem Weg A

Entscheidung:

> siehe kreuze oben

### 3.2 Methodische Begründung

**Welche drei Entscheidungen sollen besonders ausführlich begründet werden?**

1. Warum SAM3 genommen wurde (weil es promptbar ist und für jeden Nutzer somit anwendbar)
2. Warum nur lineaer Objekte Postprocessed werden (mehrere Abzweigungen etc. sind nicht im Scope und zu kompliziert)
3. Warum nur ein CMD Line Skript existiert (Weil es den rahmen sprengen würde und es um eine robuste anwendung geht die überhaupt läuft) => UI erstmal heraus lassen bitte. 

**Welche Entscheidungen sollen nur kurz dokumentiert werden, weil sie nicht
zum wissenschaftlichen Kern der PA gehören?**

> Entschiedung für 7000 Iterations bei STS und andere Einstellungen beim Autopilot

### 3.3 Reproduzierbarkeit

**Welche Informationen muss eine fachkundige Person erhalten, um den
entscheidenden Versuch zu wiederholen?**

- [ ] Datensatz und Frameauswahl
- [ ] Hardware und Container-/Softwareversionen
- [ ] Kameramodelle und Auflösungen
- [ ] FPS-Profile
- [ ] Maskenprofil und Eval-Split
- [ ] Trainingsparameter
- [ ] Mesh- und Postprocess-Parameter
- [ ] Seeds
- [ ] Metrikdefinitionen
- [ ] Ergebnis- und Logpfade
- [ ] anderes:

Nicht in den Haupttext, aber in den Anlagen gehören:

> Datensatz und Frameauswahl (es reicht eine lineares Objekt wie eben ein rohr zu haben);
---

## 4. Fragen zum Versuchs- und Ergebnisteil

### 4.1 Versuchsmatrix

**Welche Faktoren sollen im Haupttext als wissenschaftlicher Vergleich
erscheinen?**

- [x] Kameramodell: SIMPLE_RADIAL, PINHOLE, OPENCV
- [x] zeitliche Abtastung: 2 FPS und 5 FPS
- [x] Auflösung: 720p, QHD und Low
- [x] Meshroute: Original-GS und SuGaR-Coarse
- [x] Maskenprofil
- [x] anderes: COLMAP entscheidungen 

**Welche Faktoren sollen nur als technische Ablation oder Anlage erscheinen?**

> Versuche bei der Sugar Coarse Optimierung 

**Soll die SuGaR-Folgeprüfung in der PA als Ergebnis, als offener
Vergleichstest oder nur als technischer Anhang behandelt werden?**

> Ergebnis, da ich mich da zuerst verrant habe aufgrund einer falschen implemntierung des existierenden Vanilla GS

### 4.2 Qualitätskriterien

**Welche Kriterien entscheiden, ob ein Lauf als erfolgreich gilt?**

- [x] vollständiger Pipeline-Lauf bis zur Centerline
- [x] gültige Maskenabdeckung
- [x] gültiger fester Eval-Split
- [x] erfolgreicher STS-Checkpoint
- [x] erfolgreiches Mesh
- [x] erfolgreiches Postprocessing
- [x] erfolgreiche objektmaskierte Metriken
- [x] alle definierten Endprodukte vorhanden
- [ ] anderes:

**Welche Metriken sollen die zentrale Bildauswertung bilden?**

- [ ] PSNR
- [ ] SSIM
- [ ] LPIPS
- [ ] Maskenabdeckung als technische Zusatzgröße
- [ ] Laufzeit als sekundäre Zusatzgröße
- [ ] keine weiteren Bildmetriken

**Welche geometrische Aussage darf aus den aktuellen Daten gezogen werden und
welche nicht?**

Zulässige Aussage:

> Innerhalb der visuellen Qualität basierend auf dem Input reicht eine niedrige qualität aus, da die Masken die Geometrie korrekt halten sollten, solange COLMAP richtig registriert

Nicht zulässige Aussage:

> OPENCV mit Weg A in SuGaR und 5 FPS ist am korrektesten

### 4.3 Ergebnisinterpretation

**Welche Beobachtung soll die Arbeit erklären und nicht nur tabellarisch
zeigen?**

> Das der Fokus rein auf dem Aufbau der Piline liegt auf der robustheit, dr testbarkeit und der Userfreundlichktei und der Architektur mit Docker für einen Server Rollout

**Welche technischen Fehlversuche müssen transparent enthalten sein?**

- [ ] leere Eval-Maske
- [ ] falsche Dateinamens-/Stem-Zuordnung
- [ ] SuGaR-Import- oder Renderfehler
- [ ] nicht vollständige Matrixläufe
- [x] Translation-Fallback bei der Georeferenzierung
- [x] andere: Schaue dir bitte ganz genau das EXPOSE an es gibt nämlich noch viel mehr als nur die Matrix tests

**Welche Schlussfolgerung soll aus der Matrix gezogen werden?**

> Robustes und autonomes testen über den autopilot möglich und damit auch Batch Bearbeitung 

---

## 5. Fragen zu Abbildungen und Tabellen

**Welche drei bis sechs Abbildungen sind für das Verständnis unverzichtbar?**

1. Screeenshots (hast du noch nicht zu jeglichen verbesserungen des Codes, von Lossfunktionseinstellung bis allem was im autopilot eingestellt ist.)
2. 
3. 
4. 
5. 
6. 

**Welche Tabellen sind im Haupttext nötig?**

- [x] kompakte Pipeline-/Parameterübersicht
- [ ] Matrixstatus
- [x] PSNR/SSIM/LPIPS-Übersicht
- [ ] Zeit-/Qualitätsauswertung
- [ ] Endprodukt-/Artefaktübersicht
- [ ] keine weiteren Tabellen
- [ ] andere:

**Welche Grafiken wären zwar interessant, würden aber den Haupttext unnötig
verlängern?**

> 

Diese Grafiken kommen in die Anlagen oder werden weggelassen:

> 

---

## 6. Fragen zu Anlagen und Datenabgabe

**Welche digitalen Anlagen sollen tatsächlich abgegeben werden?**

- [ ] Rohvideo beziehungsweise Verweis auf den Datenträger
- [ ] ausgewählte Rohframes
- [ ] Masken und Maskenstatistik
- [ ] COLMAP-Modell und Kameraparameter
- [ ] feste Eval-Listen
- [ ] Matrix-TSV-Dateien
- [ ] Trainings- und Renderkonfigurationen
- [ ] Logs und Laufmanifeste
- [ ] Meshes und Centerlines
- [ ] GeoJSON/GIS-Dateien
- [ ] Quellcode beziehungsweise Repository-Commit
- [ ] Grafik-Quelldateien
- [ ] anderes:

**Wie soll die Anlage für eine fachkundige Person auffindbar werden?**

- [ ] Ordnerstruktur mit README
- [ ] Anlagenindex mit Dateipfaden
- [ ] komprimiertes Archiv pro Verarbeitungsschritt
- [ ] Git-Commit plus reproduzierbares Manifest
- [ ] anderes:

Geplante Anlagenstruktur:

> 

---

## 7. Fragen zur persönlichen Darstellung

### 7.1 Schreibstil

**Soll die Arbeit eher technisch-kompakt oder stärker erklärend geschrieben
werden?**

- [ ] technisch-kompakt und fachkundig
- [x] ausgewogen: kurze Grundlagen, ausführliche eigene Ergebnisse
- [ ] stärker einführend, damit externe Leser folgen können

Begründung:

> 

### 7.2 Eigene Leistung

**Welche Arbeitsschritte wurden selbst konzipiert, implementiert, geprüft oder
wissenschaftlich ausgewertet?**

> 

**Welche Bestandteile stammen aus externen Projekten oder Bibliotheken und
müssen deshalb als verwendete Grundlage abgegrenzt werden?**

> 

### 7.3 Verwendung der Kollegenarbeit

Aus der Kollegenarbeit dürfen grundsätzlich **Strukturideen, Darstellungs-
prinzipien und Hinweise auf sinnvolle Nachweise** übernommen werden. Nicht
übernommen werden dürfen ohne eigene Prüfung:

- Formulierungen oder längere Textpassagen;
- fremde Abbildungen oder Tabellen ohne Rechte und Quellenangabe;
- fremde Ergebnisse als eigene Ergebnisse;
- unpassende Kapitel nur, weil sie den Umfang vergrößern;
- Methodenbeschreibungen, die für die eigene Aufgabenstellung nicht benötigt
  werden.

**Welche Elemente der Kollegenarbeit wirken nach der späteren Analyse als
methodisch stark und übertragbar?**

> 

**Welche Elemente wirken zu umfangreich, redundant oder für die eigene PA nicht
relevant?**

> 

---

## 8. Vorläufiges Seitenbudget

Das Seitenbudget dient dazu, den Zielrahmen von 15–25 Textseiten einzuhalten.
Die Zahlen sind Planungsvorschläge und können nach den Antworten angepasst
werden.

| Abschnitt | Zielumfang | Persönliche Festlegung |
|---|---:|---|
| Einleitung, Motivation, Ziel, Abgrenzung | 1,5–2,5 Seiten | |
| Grundlagen | 2,5–4 Seiten | |
| Konzept und Pipeline-Idee | 2–3 Seiten | |
| Implementierung | 2–3 Seiten | |
| Versuchsaufbau und Evaluationsregeln | 2–3 Seiten | |
| Ergebnisse | 3–5 Seiten | |
| Diskussion und Grenzen | 2–3 Seiten | |
| Fazit und Ausblick | 1–1,5 Seiten | |
| **Gesamt** | **16–25 Seiten** | |

**Welche Abschnitte sollen bewusst mehr Platz erhalten?**

> 

**Welche Abschnitte sollen bewusst kurz bleiben?**

> 

---

## 9. Entscheidungsprofil für die nächste Fassung

Bitte am Ende eine Variante auswählen oder ein eigenes Profil formulieren:

### Profil A: Technischer Funktionsnachweis

Der Schwerpunkt liegt auf der reproduzierbaren Kette von Segmentierung über
SfM und STS bis zur lokalen Centerline. Die Matrix und die Kameramodelle dienen
als kontrollierte Zusatztests.

### Profil B: Methodischer Kameramodell- und Metrikvergleich

Der Schwerpunkt liegt auf der Frage, wie Kameramodell, FPS und Auflösung die
objektmaskierten Bildmetriken und den Pipelineerfolg beeinflussen. Die
Geometrieendstufen werden als Funktionsnachweis dargestellt.

### Profil C: Geometrie- und Meshroute

Der Schwerpunkt liegt auf der Entscheidung zwischen Original-GS und SuGaR-
Coarse sowie auf Mesh, Centerline und deren Grenzen. Bildmetriken bleiben
unterstützende, nicht allein entscheidende Kriterien.

### Profil D: Eigenes Profil

> 

**Meine Auswahl:**

> 

**Ein-Satz-Arbeitsziel:**

> 

**Wichtigstes Ergebnis:**

> 

**Wichtigste Grenze:**

> 

---

## 10. Nächster Arbeitsschritt nach Beantwortung

Nach Beantwortung der Fragen werden daraus abgeleitet:

1. eine endgültige Forschungs- beziehungsweise Arbeitsfrage;
2. eine priorisierte Gliederung mit Seitenbudget;
3. eine Liste der Hauptgrafiken und Haupttabellen;
4. eine Liste der digitalen Anlagen;
5. eine Entscheidung, welche Matrix- und SuGaR-Ergebnisse in den Haupttext
   gehören;
6. eine Liste offener technischer oder organisatorischer Nachweise;
7. eine gekürzte und auf die eigene Leistung zugeschnittene PA-Fassung.
