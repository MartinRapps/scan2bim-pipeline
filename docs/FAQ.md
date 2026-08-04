# FAQ / Offene Entscheidungen

Die Dokumentation ist gelesen. Dieses Dokument sammelt Punkte, die sich aus den
Unterlagen nicht eindeutig entscheiden lassen oder an denen unterschiedliche
historische Staende beschrieben sind. Bitte die Fragen anhand ihrer IDs
beantworten. Danach koennen die Entscheidungen in Code, README und Expose als
verbindlicher Stand zusammengefuehrt werden.

## 1. Projektziel und Datensaetze

### Q-01: Welcher Datensatz ist aktuell verbindlich?

In den Dokumenten werden `Alurohr_THWS.mp4`, Sonnenbrillen-Experimente und die
spaetere reale Kabeltrasse genannt. Ist das Alurohr der aktuelle
Abnahmedatensatz fuer die Pipeline, waehrend die Sonnenbrille nur fuer
SuGaR-Ablationen dient? Welche Rolle haben die Datensaetze fuer Projektarbeit
und Bachelorarbeit?

### A-01

Das sind alles nur test datensätze mit der sonnebrille habe ich insbesonders sugar geprüft, mit dem Alurohr haeb ich jetzt einen Test, da ich die colmap tests dait gemacht haeb und es eben um ein lineares objekt geht und ich damit erst die ganze pipline laufne lassen kann. Späte in der BA gitb es dann Drohnenvideos von Rohren in den Gräben o. ä. 

### Q-02: Worauf bezieht sich die Toleranz von +/- 10 cm?

Gilt diese Toleranz bereits fuer die Laborobjekte oder erst fuer die reale
Kabeltrasse? Welche Referenzdaten liegen aktuell vor: GNSS, Laserscan, CAD,
bekannte Messpunkte oder nur visuelle Plausibilitaetspruefungen? Ohne eine
metrische Referenz waeren die bisherigen Ergebnisse nur als Funktions- bzw.
Qualitaetsnachweis einzuordnen.

### A-02

Das gilt für die BA jetzt geht es nur um die Pipeline in der Projektarbeit.  Und dass sind dann bekannte messpunkte welche ich auch einmessen will...

### Q-03: Welche Endprodukte sind zwingend?

Soll das primaere Ergebnis eine georeferenzierte Centerline als GeoJSON sein,
oder werden zusaetzlich ein objektbezogenes OBJ-Mesh, eine Full-Scene-Baseline,
PLY-Dateien und ein 3DGS-Checkpoint benoetigt? Welche Datei soll spaeter in
ArcGIS Pro beziehungsweise bei TenneT verwendet werden?

### A-03

Primär geht es um die Centerline aber alle Zwischenshritte sollen verwertbar sein und das sind sie jetzt auch schon, wenn ich sie georeferenziert bekomme, dafür muss aber noch die UI und das GCP Picking geprüft und wohlmöglich verbessert werden.

## 2. Verbindlicher Software- und Hardwarestand

### Q-04: Welches Dokument ist die aktuelle Single Source of Truth?

`agent-memory-repo.md`, `agent-memory-session.md`, `Expose_PA_BA.tex` und die
COLMAP-Auswertungen stammen aus unterschiedlichen Zeitpunkten und beschreiben
teilweise verschiedene Staende. Soll der aktuelle Code als hoechste Autoritaet
gelten, oder soll ein bestimmtes Dokument verbindlich sein? Duerfen veraltete
Angaben in den Dokumenten anschliessend gekennzeichnet oder bereinigt werden?

### A-04
COLAMP Auswertungen also die Test sind seperat und neu. Das agent-memory-repo ist das älteste Memory von Github Copilot, dass memory session ist von opencode instanzen und neuer. Insgesamt sollte aber mit dem Expose_PA_BA.tex die SSOT vorhanden sein und mit dem code und test soll sich die Projektarbeit schreiben lassen. Nicht bereinigen aber das EXPOSE mit höchster Priorität betrachten.

### Q-05: Welche Ausfuehrungsumgebung ist produktionsrelevant?

Ist die Docker-GPU-Pipeline unter WSL2 beziehungsweise Linux der eigentliche
Produktionsweg und der Windows-11-CPU-Lauf nur ein Benchmark? Bitte Zielbetriebssystem,
GPU-Modell und geplante Ausfuehrungsumgebung fuer die finale Evaluation festlegen.

### A-05
Ja die Docker GPU Pipline ist der eigentliche Produktuiosweg, da ich zwischendrinn aber nicht auf einem Linux /WSL System arbeiten konnte habe ich eine test auf windows 11 Colmap 4.1 no CUDA / unte CPU gemacht. Jetzt 4.08.26 habe ich aber endlich ein stbailen Linux Ubuntu zugan über eine VM

### Q-06: Welche COLMAP-Version ist verbindlich?

Die Unterlagen nennen `colmap/colmap:latest`, schlagen `colmap/colmap:4.0.4-cuda`
als reproduzierbaren Container vor und verwenden im Windows-Benchmark COLMAP
4.1.1. Welche Version soll fuer die Docker-Pipeline und welche fuer die
wissenschaftlichen Vergleichslaeufe festgeschrieben werden?

### A-06
Vermutlich wird es 4.0.4 cuda, ich könnte mir aber in der BA vorstellen, wenn es verbesserungen in der version gab, dass ich dann zu der neusten im November order so wechsle. Die vergleichsläufe waren aber anders und das muss gekenzzeichent werden. Die besten Fälle überprüfe ich aber auch nochmal hier auf der Ubuntu VM mit 4.0.4 und cuda

### Q-07: Welcher SuGaR-Commit ist verbindlich?

Als projektspezifischer Fork wird `MartinRapps/SuGaR@48bbfdd` genannt. Andere
Dokumente nennen den lokalen beziehungsweise upstream-nahen Stand
`7c10c4ae4a267dece512f5c7f40ed212a0a2ab44`. Welcher Commit enthaelt die
maskenbewussten Aenderungen und soll fuer reproduzierbare Builds verwendet
werden? Soll das lokale Dev-Overlay immer oder nur opt-in geladen werden?

### A-07
Puhh weiß ich gerade nicht ich habe nur bis hetzt docker-compose.yml bzw. docjer compos up -d ausgeführt aber sugar funktioniert nur mti der fork, wie soll ich also vorgehen? Da musst du mir helfen und dass dann bitte auch dokumentieren...

### Q-08: Welche Hardwaregrenze soll garantiert werden?

Im Expose werden 24 GB VRAM als Anforderung genannt, waehrend SAM-3.1-Laeufe
auf einer 16-GB-GPU stabilisiert wurden. Welche GPU ist das Zielsystem? Soll
16 GB nur fuer SAM oder fuer die gesamte Pipeline unterstuetzt werden, oder
sind 24 GB fuer STS/SuGaR verbindlich?

### A-08
Also auf der UBuntu VM habe ich folgendes: # Systemdetailsbericht
---

## Berichtdetails
- **Erstellungsdatum:**                            2026-08-04 16:05:01

## Hardware-Informationen:
- **Hardware-Modell:**                             ASUS Pro WS WRX90E-SAGE SE
- **Speicher:**                                    128,0 GiB
- **Prozessor:**                                   AMD Ryzen™ Threadripper™ PRO 7955WXs × 32
- **Grafik:**                                      Software Rendering
- **Festplattenkapazität:**                        4,0 TB

## Software-Informationen:
- **Firmware-Version:**                            0502
- **Name des Betriebssystems:**                    Ubuntu 24.04.4 LTS
- **Betriebssystem-Build:**                        (null)
- **Betriebssystem-Typ:**                          64-bit
- **GNOME-Version:**                               46
- **Fenstermanager:**                              X11
- **Kernel-Version:**                              Linux 6.8.0-124-generic

Und auf dem WSL hatte ich meine ich 64 GB RAM, ne Ada 4000 aber nicht vollständig übertragn auf WSL. Dort hat es aber funktioniert.... Ohne einen OOM fehler..

## 3. Frame-, SAM- und COLMAP-Profil

### Q-09: Was ist das verbindliche Standardprofil?

Der Autopilot wird mit 1920x1080, 10 FPS und CRF 23 beschrieben. Die
validierte COLMAP-Baseline ist dagegen 1280x720, 5 FPS, Plain-SIFT mit 4096
Merkmalen; CRF 18 gilt als sichere und CRF 28 als platzsparende Variante.
Welches Profil soll der normale End-to-End-Lauf verwenden? Soll es getrennte
Profile fuer SAM/STS und COLMAP geben, oder muessen alle Stufen denselben
Frame-Satz verwenden?

### A-09 
Nein es muss nicht überall das gleiche sein. der neue standard ist aber sicher 1280 und 720p 5 FPS und Plain SIFT mit 4096. Später will cih dann die möglichkeit geben, dass man die UAflösung für STS auswählt. 

### Q-10: Welche Rohvideo- und Frame-Konfiguration ist aktuell massgeblich?

Die Unterlagen nennen sowohl 30 FPS bei etwa 48 Sekunden als auch ein 60-FPS-
Diagramm. Ausserdem treten Teststaende mit 100, 240 und 699 Ansichten auf.
Welche Ansichten gehoeren zu welchem Datensatz beziehungsweise Experiment,
und welcher Lauf soll als aktuelle Referenz bezeichnet werden?

### A-10
Das ist erstmal egal. Insgesamt wurde dann immer mit 10FPS gekürzt. Ab jezt ann 5 FPS. (Ich schaue das dann nach wenn ich es brauche, denn ich habe alles gepsiechert)

### Q-11: Welcher SAM-Stand und welches Maskenformat gelten?

Soll verbindlich SAM 3 oder SAM 3.1 verwendet werden, mit welchem Checkpoint
und welchem Prompt-Typ (Text oder Punkt)? Sind die morphologisch erzeugten
Masken `small`, `middle` und `default` der gewuenschte Standard? Welche
Quality-Gate-Werte gelten fuer nichtleere Masken, zeitliche Kontinuitaet und
manuelle Sichtpruefung?

### A-11:
SAM 3.1 und lese dir auch noch ./run_pipline.sh durch und alle anderen skripte welche vewendet werden 

### Q-12: Soll COLMAP maskierte oder unmaskierte Bilder verwenden?

Das Expose beschreibt COLMAP ausdruecklich mit unmaskierten Originalbildern,
weil Anker-Features im Hintergrund die Kameraposen stabilisieren. Die
Effizienzanalyse nennt `ImageReader.mask_path` als moegliche Optimierung, warnt
aber gleichzeitig vor dem Verlust dieser Anker. Soll die Maskierung fuer
COLMAP grundsaetzlich deaktiviert bleiben oder nur szenenabhaengig getestet
werden?

### A-12:
COLMAP nutzt die unmaskierten Bilder IMMER sonst funktioniert es nicht stabil (meine ich zumindest bei meinen dünnen objekten + ich brauche es auch für das GCP picking besonders die stbailität)

### Q-13: Welche COLMAP-Parameter sind fest und welche sind Studienparameter?

Soll die Produktionsbaseline verbindlich `SIMPLE_RADIAL`,
`single_camera=1`, 4096 SIFT-Merkmale, Overlap 15, Guided Matching aus,
Peak-Threshold 0.003 und Mapper-Seed 42 sein? Die beiden Benchmark-Skripte
haben derzeit andere Defaults, unter anderem `OPENCV` und 2048 Merkmale.
Sollen die Skript-Defaults an die dokumentierte Baseline angepasst werden,
oder muss jeder Lauf alle Werte explizit uebergeben?

### A-13:
Es soll alle einstellbar bleiben, aber eben einen Autopilot geben bzw. drei Genauikeitstufen mit vorher definierten werten. 
Aber ja an sich sind das defaults. Ich würde aber eben dann am ende verschiedene Modi anbieten: Fast mit z. B. 2048 SIFT und Overlap 10 etc. einen normalen mit den aktuellen Default und einen High Quality mit 8192 SIFT Merkmalen overlap 20 etc. Ebenso soll das dann für die ganzen anderen Container auch so sein. 

### Q-14: Welche COLMAP-Ergebnisse sollen zitiert werden?

Die Gesamtauswertung nennt fuer 5 FPS/720p etwa 95.651 Punkte, die neueren
Variantenberichte fuer Plain-SIFT 4096 dagegen 139.449 Punkte. Sind dies
bewusst getrennte Laeufe, zum Beispiel mit 2048 beziehungsweise 4096
Merkmalen? Welche Reports sind fuer die Arbeit verbindlich, und sollen die
anderen als historische oder nicht direkt vergleichbare Laeufe markiert
werden?

### A-14: 
Das entscheide ich noch aber ja an sich nur eben default best und worst case damit ich es damit erkläre und dann kann man eben entweder ne graik machen o. ä. 

## 4. GCP, Georeferenzierung und GIS

### Q-15: Ist eine echte Georeferenzierung fuer jeden Produktionslauf Pflicht?

Die Pipeline kann bei fehlender Matrix und fehlendem Anchor auf eine reine
Translation mit `FALLBACK_ANCHOR` ausweichen. Ist dieser Fallback nur fuer
Diagnosezwecke erlaubt und muss ein Produktionslauf ohne gueltige Matrix
abbrechen? Wie soll sich der Autopilot verhalten, wenn der CloudCompare-
Breakpoint uebersprungen wird, aber noch keine Matrix vorliegt?

### A-15:
Ja georefernzierung ist pflich abter der Fallback bleibt immer bestehen, bzw. soll auch einstellbar sein. Aber mal schauen. Wenn der Cloudcompare Breakpoint ubersprungen wird, dann wird eben mit dem fallback weiter gemacht, sollte es auch laut pipline.sh skript

### Q-16: Was ist der verbindliche GCP- und Matrix-Workflow?

Soll die Matrix manuell aus CloudCompare exportiert, per Screenshot durch OCR
erzeugt oder wahlweise beides verwendet werden? Welche Eingabepfade sind
verbindlich: `data/04_sfm/matrix.txt`, `data/01_raw/matrix_screenshot.png`
und `data/01_raw/anchor.txt`? Wird der erste GCP immer als Anchor genommen oder
gibt es eine feste GCP-ID?

### A-16: 
An sich sll das über die UI laufne aber sonst einfahc mit einer eingabe in text über Cludcompate und der erste GCP ist standardmäßig der Anchor kann aber verändert werden. Aber damit dass dann funktioniert muss dann erstmal eben die GCPs translatiert werden auf null mit dem Anchor, das habe ich aber noch  nicht überprüft... 
Schau dir also bitte auch noch die UI genau an...

### Q-17: Welche GCP-Konfiguration gilt fuer die Evaluation?

Die Checkliste fordert mindestens 4 GCPs mit jeweils 5 Bildbeobachtungen; das
Expose plant einen Vergleich von 3 gegen 5 bis 7 GCPs. Was ist die minimale
gueltige Konfiguration und welche Verteilung ist der Standard? Sind Hoehenwerte
und ein vertikales Bezugssystem vorhanden, oder soll `EPSG:25832` nur die
horizontalen UTM-Koordinaten beschreiben?

### A-17: 
Es soll UTM Standard sein, aber auch in DHDN2016 die Höhen.... Minimal müssen es 3 GCPS sien sonst lässt sich keine Transformation durchführen aber 4 sind stark empfohlen...

## 5. STS, SuGaR und Mesh-Qualitaet

### Q-18: Welche Objektfilterung ist reproduzierbar?

Ist `object_id=0` zusammen mit Level `m`, `min_opacity=0.01` und
`black_threshold=0.08` nur fuer den aktuellen Datensatz gueltig oder der
allgemeine Standard? Soll die Objekt-ID weiterhin manuell vorgegeben oder
automatisch aus den Masken bestimmt werden? Soll die Full-Scene-Punktwolke
immer als unveraenderte Baseline erhalten bleiben?

### A-18:
Das ist ein allgemeiner Standard aktuell kann aber bei Outodoor aufnahmen in der BA anpassung benötigen also die Opacity und der threshold. 

### Q-19: Welche Maskenvariante ist der Produktpfad?

Als aktuelle Arbeitshypothese wird `default + 0 px` fuer RGB und `middle` fuer
Depth-Normal genannt; `middle + 0 px` bleibt eine Vergleichsvariante. Soll
dieser Default verbindlich werden? Soll Multi-View-Crop im Produktpfad
deaktiviert bleiben und nur als Diagnose dienen? Darf ein konservatives
`postprocess_mesh` vor dem finalen Export eingesetzt werden?

### A-19: 
Ja das sollte der default meine ich sein. Das postprocess mesh weiß ich aktuell nicht, erkläre mir das nochmal wie das gemeint war. 

### Q-20: Welche Iterationswerte sind Baseline und welche Ablation?

STS nennt 7000 Gesamtiterationen und 5000 Stage-2-Iterationen. Fuer SuGaR
werden unter anderem 9001, 12000, 15000 und 18000 als Zielzaehler untersucht.
Welche Kombination ist die feste wissenschaftliche Baseline und welche Werte
sollen nur als Ablationen dokumentiert werden?

### A-20:
Also bei STS ist es so, dass ich bei 7000 gute ergebnisse hinbekomem aber bei guten Splats sind oft 25 - 30k sinnvoll, das gilt aber eher für alllgemeine Splats und eben nicht die Segmentierten. Denn bei den segmentierten ist es oft ausreichend da es ja nur ein teil des gesmaten ist also ist die genauigkeit und iteration meine ich sogar besser. Bei SuGaR ist 9000 (muss meine ich noch im code geändert werden also das es ncht min 9001 iteration sein müssen, vorallem sollten 8k auch ausreichen und das ganze gut beschleunigen) der standard da eigentlich keine Depth daten benötigt werden da es segmentiert ist, das war nur erst ein denkfehler von mir und der Ki da ich mich an dem REPO leitfaden von SIGar orientiert habe, die haben abr eine andere Baseline. 

### Q-21: Welche Artefaktuntersuchungen muessen noch abgeschlossen werden?

Als naechste Tests sind `depth8_v500000`, eine Variante ohne Vertexprojektion,
RGB-Dilatation 0, RGB-Supervision mit `middle`, Opazitaetsschwellen und ein
konservatives Mesh-Postprocessing beschrieben. Welche dieser Tests haben
Prioritaet vor der Endauswertung, und nach welchem Kriterium wird die
Produktvariante ausgewaehlt: Centerline-Fehler, Vollstaendigkeit, Artefakte
oder eine Kombination?

### A-21:
Muss ich noch überprüfen, aber ich fokusiere mich erst auf das GCP Picking in der UI Wohlmöglich und der besseren Centerline extaktion denn dadruch, dass ich nicht von allen seite an eine Rohr rankomme, welche im graben liegt oder an der wand hängt, habe ich eine verschiebung der Centerline. Und zu der Centerline ist noch wichtig anzuerken (ch meine das ist noch nicht dokumentiert), dass ich mit einem B Spline von mindesten 10 es berechnen lasse, denn normalerweiße sind die kruven bei den Erdkabeln sehr viel sanfter und lassen es somit zu.

## 6. Centerline und wissenschaftliche Bewertung

### Q-22: Soll der `single`- oder der `network`-Modus verwendet werden?

Der `single`-Modus ist fuer die verrauschten Testmeshes robust, waehrend der
`network`-Modus experimentell bleibt. Ist das Zielobjekt fachlich immer eine
einzige lineare Kabeltrasse, sodass `single` verbindlich ist? Oder muss die
Pipeline auch Aeste, Buegel oder geschlossene Komponenten als Netzwerk
ausgeben?

### A-22:
Ja am ende ist es in meinem Anwendungsfall AWF immer eine Trasse und nciht schlimm, aber an sich ist es natürlich sehr interessant, wenn man das verbessern könnte mit einem Network aber eigtnlich ist das out of scope OOS

### Q-23: Welche B-Spline-Einstellungen gelten fuer die Centerline?

Sind Grad 3, Eckensegmentierung aktiv, Fenster 4, Mindestwinkel 30 Grad und
4 Samples pro Segment die verbindlichen Werte? Soll die geglaettete Kurve
auch fuer die Genauigkeitsmetrik verwendet werden, oder muss zusaetzlich die
ungeglaettete DGtal-Kurve bewertet werden?

### A-23:
Nein keine Eckensegmeiteurng mehr, das war nicht fut zumindest von der aktuellen Exjtraation aus zu sehend. sinst siehe oben

### Q-24: Wie wird die Referenzkurve gebildet?

Soll die GNSS-Referenz als interpolierender oder approximierender B-Spline
modelliert werden? Wird die symmetrische Hausdorff-Distanz aus dem Expose
verbindlich verwendet, und wie werden die Kurven fuer RMSE und Hausdorff
abgetastet beziehungsweise parametrisiert?

### A-24: 
Die Hausdorff Distanz etc. kommt erst in der BA. Und die GSS Refernz wird dann interpoliert bzw. ich frage unsere veremsser die ich kenne. Vlt. auch ohne interpolation...

## 7. Naechster Arbeitsschritt

### Q-25: Was soll als Naechstes priorisiert werden?

Soll zuerst die 5-FPS/720p-COLMAP-Baseline dreimal wiederholt werden, danach
ein vollstaendiger Lauf mit GCP durch STS/SuGaR erfolgen, oder haben die
SuGaR-Artefaktablationen beziehungsweise die Repository-Konsolidierung
Vorrang? Bitte eine Reihenfolge fuer die naechsten verbindlichen Schritte
festlegen.

### A-25:
Jetzt da ich auf der Ubuntu VM bin muss ich erstmal überprüfen ob alles läuft und ich werde dann das GCPs Picking verbessern, danach direkt die Centerline verbessern!!! Dann kommt ein Test von STS und SuGaR und dann muss ich anfangen meine PA zu schreiben alles was drüber hinaus geht ist erstmal nicht wirchtig. 

### Q-26: Soll der geplante Repository-Umzug jetzt umgesetzt werden?

Der Umzug in ein bereinigtes Pipeline-Repository mit Submodul, `tests/`,
zentraler Pipeline-Library und `--from`-Einstieg ist dokumentiert, aber noch
nicht ausgefuehrt. Soll dieser Refactor vor der weiteren Evaluation erfolgen,
oder erst nach Abschluss der wissenschaftlichen Versuche?

## Nachtraegliche technische Rueckfragen

Die folgenden Punkte blieben nach dem Abgleich der Antworten mit dem aktuellen
Code und den Referenzen noch offen.

### Q-27: Welche SuGaR-Iterationsroute ist der Standard?

Vor der Umsetzung erzwingt der Fork bei `REGULARIZATION=dn_consistency`
`COARSE_ITERATIONS > 9000`; die Depth-Normal- und SDF-Terme starten erst bei
`iteration > 9000`. `c9001` fuehrt daher genau den ersten Schritt dieser Phase
aus. Externe Tiefendaten werden dabei nicht benoetigt, weil die Tiefe intern
aus den Gaussians gerendert wird.

Soll der Standard deshalb vorerst `dn_consistency` mit `c9001` bleiben, oder
soll ich eine echte 8000-/9000-Iteration-Route implementieren? Falls die
kuerzere Route gewuenscht ist: Soll sie als `density` ohne DN/SDF laufen oder
als `dn_consistency`, bei der die spaetere DN-/SDF-Phase bewusst nicht erreicht
wird? Zusaetzlich muss bestaetigt werden, ob `NORMAL_MASK_LEVEL=middle` der
verbindliche Default neben `MASK_LEVEL=default` und null RGB-/UV-Dilatation ist.

### Q-28: Was bedeutet „B-Spline von mindestens 10“ genau?

Der Code unterscheidet zwischen `BSPLINE_DEGREE` und
`BSPLINE_SAMPLES_PER_SEGMENT`. Der aktuelle Default ist Grad 10; die
Punktdichte steht auf 4. Die Frage war, ob „mindestens 10“ den Grad, die
Kontrollpunktzahl oder die Ausgabepunktdichte meint. Meinst du mit
„mindestens 10“ mindestens 10 Samples pro Segment, mindestens 10
Kontrollpunkte fuer die Kurve oder tatsaechlich den B-Spline-Grad 10? Fuer
sanfte Erdkabel waere technisch wahrscheinlich eine hoehere Sample-Dichte bei
Grad 3 sinnvoller als Grad 10. Zusaetzlich soll `SEGMENT_CORNERS=0` verbindlich
gesetzt werden.

### Q-29: Wie soll COLMAP fuer die Docker-Pipeline reproduzierbar gepinnt werden?

Das aktuelle Dockerfile verwendet `colmap/colmap:latest`. Die in den alten
Dokumenten genannte Image-Bezeichnung `colmap/colmap:4.0.4-cuda` sowie der Tag
`4.0.4` sind im Docker-Hub-Repository aktuell nicht vorhanden. Der derzeitige
`latest`-Stand ist als Digest
`sha256:b809882552887b6471094dcadd2f2eb01656b010663564c43a5e7f04c0a08f2f`
verfuegbar; der zugehoerige datierte Tag ist `20260729.7651`.

Soll ich fuer die Projektarbeit diesen Digest beziehungsweise den datierten
Tag pinnen, oder soll COLMAP 4.0.4 aus dem Quellcode selbst gebaut werden? Die
Windows-CPU-Tests bleiben davon getrennte Vergleichslaeufe.

### A-26:
NEIN!!!
Das ist schon passiert, das ist schon das umgezogene! Ich muss eben nur noch den feinschliff machen. 

### A-27:

Der Standard bleibt `dn_consistency` mit `c9000`. Die harte Sperre oberhalb
von 9000 soll aufgehoben werden; der Hinweis zur spaeteren DN-/SDF-Phase soll
aber erhalten und darauf angepasst werden, dass diese Phase fuer den
segmentierten Standard nicht erforderlich ist. Ein schnellerer `density`-Lauf
soll spaeter eingefuehrt werden. Die uebrigen SuGaR-Defaults bleiben bestehen.

### A-28:

Der B-Spline-Grad soll mindestens 10, konkret aktuell Grad 10, betragen. Das
Alurohr-Video ist der Mindestfall fuer diese Glattung. `SEGMENT_CORNERS=0`
soll verbindlich gelten.

### A-29:

COLMAP bleibt fuer die Projektarbeit bei `latest`, auch wenn das fuer die
Reproduzierbarkeit unsauber ist. Die Erkenntnisse sollen im
`agent-memory-session.md` und an geeigneten Stellen ausfuehrlich im Expose
dokumentiert werden.
