# BeamShaperPlots

Auswertung von FlatTop-Kamerabildern (TOPAG-Beamshaper) mit einer PyQt5-Oberfläche.
Eigenständiges Repo – keine Abhängigkeit zu `Lern-repo/Strahlanalyse`.

## Start

```bash
pip install -r requirements.txt
python main.py                  # GUI, fragt beim Start nach der Datei (Ordner Messdaten/)
python main.py "C:/Messungen/2026-09-21"   # GUI mit Ordner
python -m beamshaper.batch "C:/Messungen/2026-09-21"   # --no-pdf: nur Tabellen   # ohne GUI
python -m pytest tests          # Tests mit synthetischen FlatTops
```

## Was ausgewertet wird

Gefittet wird ein rotierter 2D-Supergauss

    I(x, y) = A · exp(-(r²)^m) + B,   r² = (x'/w_a)² + (y'/w_b)²

in einer ROI um den Strahl (für den Fit gebinnt auf max. 250 px → < 1 s pro Bild).
Konvention: `w_a ≥ w_b`, θ = Winkel der langen Achse gegen die Bild-x-Achse (Bild-y nach unten).

| Größe | Herkunft |
|---|---|
| Durchmesser lang/kurz bei 1/e², 50 %, 90 % | Fit: `r(L) = w · (−ln L)^(1/2m)` |
| Kantenbreite 10–90 % | Fit, je Achse |
| Äquivalent-Durchmesser 50 % | Daten: Fläche über `B + A/2` |
| Plateau-Uniformity σ/µ, Peak-Valley | Daten in der 90 %-Ellipse (Level und Skala einstellbar) |
| Flatness-Kurve | σ/µ in Kreisen um das Zentrum mit wachsendem Durchmesser |
| Schnitte horizontal/vertikal/lange/kurze Achse | Daten + Fit, normiert auf `(I−B)/A` |
| Uniformity-Radius | größter Kreis mit σ/µ unter der Schwelle (Standard 5 %), aus der Flatness-Kurve |
| Signal-Durchmesser inkl. Nebenstruktur | Daten: azimutales Mittel über Untergrund |
| Übersteuerung | Anteil der Pixel in der 50 %-Fläche am Sättigungswert |

Die Level-Linien in den Schnitten liegen dort, wo der Schnitt die Level-Ellipse
tatsächlich kreuzt (`ab/√((b cos Δ)² + (a sin Δ)²)`). In `WaistAnalysis.py` wurde
dafür die Bounding-Box-Halbbreite verwendet – bei gedrehten Ellipsen weicht das ab.

Standard: IDS-Kamera (Sony-Sensor) mit 40er Mikroskopobjektiv, Pixelgröße 1,45 µm,
Vergrößerung 43,75 → 1,45/43,75 = 0,0331 µm pro Pixel in der Objektebene.
Alle µm-Angaben gelten in der Objektebene.
Optional kann ein Hintergrundbild abgezogen werden. Dateien mit `Background` oder
`Hintergrund` im Namen werden im Batch übersprungen.

## Plots

Übersicht wie `AOD_Ellipse.pdf`: 2D-Bild links (jet, Fadenkreuz), horizontaler und
vertikaler Schnitt rechts (Intensität in a. u.). In der GUI einzeln schaltbar:
Regionen 1/e²/50 %/90 %, weißer FWHM-Text im 2D-Plot, Fit in den Schnitten,
Flatness-Kreise. Einheiten stehen immer in runden Klammern.

Alle Intensitätsskalen (Farbskala der 2D-Bilder, y-Achse der Schnitte) gehen fest von 0
bis zum maximalen Pixelwert der Bittiefe (255 bei 8 bit). Dadurch sind alle Plots
gleich normiert und direkt vergleichbar (z. B. FlatTop_04 und FlatTop_05).
Beides ist in der GUI getrennt einstellbar: „Farbskala 2D-Bild“ und „y-Achse Schnitte“.
Nützlich bei dunklen Aufnahmen: 2D-Bild auf den hellsten Pixel spreizen, Schnitte
trotzdem bis 255 lassen. Die Schnitte lassen sich auch auf 1 normieren
((I − Untergrund)/(Fit-Peak − Untergrund)), dann liegt die Basislinie auf 0 und das
Plateau auf 1 – gut für den Vergleich der Profilform unabhängig von der Helligkeit.

Jeder Plot wird als eigenes PDF gespeichert und hat keinen Titel (die Kennzahlen stehen
im JSON). Der Plotausschnitt wird automatisch so groß gewählt, dass Nebenstrukturen
(z. B. Airy-Ringe) nicht abgeschnitten werden: Radius, bis zu dem das azimutal
gemittelte Signal über dem Untergrund (Bildrand) liegt, plus 15 %.

### Titelbild für die Titelseite der Thesis

Reiter „Titelbild“ in der GUI, gespeichert mit „Titelbild als PDF speichern“ nach
`Auswertung/Plots/JJJJ-MM-TT/<name>_title.pdf` (nicht im normalen Export/Batch).

* Kamerabild ohne Fadenkreuz, Ringe, Text oder Achsen im gewählten Farbschema und mit
  der gewählten Farbskala; standardmäßig unbearbeitet, mit „Hintergrund abziehen“ wird
  das oben gewählte Hintergrundbild abgezogen (negative Werte → 0)
* Ausschnitt richtet sich nach dem ganzen Strahl bzw. Muster (z. B. 3×3-Spotgitter):
  Umriss bei 1/e² des Maximums, zentriert
* PDF exakt so groß wie das Bildfenster der Titelseite: 155,0 × 185,7 mm
  (Textbreite, vom Strich unter dem Titelblock bis zum Strich unten, gemessen in der
  Masterthesis; in `APQ_Thesis_Vorlage.pdf` mit anderem Titelblock 184,9 mm), das Bild
  füllt das PDF komplett – kein weißer Rand. Ändert sich der Titelblock (Titel- oder
  Infozeilen), ändert sich die Höhe – mit `\titleimage*` passt LaTeX das automatisch an
* einstellbar: Strahlgröße (Anteil des Musters an der Breite), Strahlposition x/y, Breite/Höhe.
  Die Vorschau zeigt, wo die Logos liegen (nur Vorschau, nicht im PDF)
* das Fenster liegt immer ganz im Kamerabild; ist das Bild zu klein, wird der
  Ausschnitt verkleinert (Hinweis in der Vorschau)

Einbinden **immer mit der Stern-Variante** (ohne Stern wird das PDF in seiner eigenen
Größe gesetzt; ist das Fenster auch nur 0,1 mm höher, bleibt unten ein weißer Streifen
bis zum Strich) – sie skaliert und beschneidet mittig exakt auf das
Fenster zwischen den beiden Strichen, auch wenn der Titelblock etwas höher oder
niedriger ist als in der Vorlage:

```latex
\titleimage*{\includegraphics{graphics/FlatTop_02_title.pdf}}
```

### Vergleich mit der Simulation (Multitone_Simulation)

Simulierte 2D-Profile lassen sich wie Messbilder öffnen und mit einer Messung
vergleichen.

1. In `Multitone_Simulation/GUI/Flattop GUI/Weighted_Multitone_Lens_GUI.py`
   Parameter einstellen und **„Export 2D profile for BeamShaperPlots (.npz)“** drücken.
   Gespeichert wird das statische Profil der eigenen Site (mit dem Interferenzterm
   frequenzentarteter Spots, wie im Hauptplot) als
   `GUI/Bilder/FlatMultiTone_profile_<NxN>_<width>MHz_w<waist>um_f<f1>-<f2>mm_<Zeit>.npz`
   (+ `.txt` mit allen Parametern). Raster wie die Laborkamera (1,45/43,75 µm pro
   Pixel, 20 µm Bildfeld um die Atom-Mitte), normiert auf das Maximum 1, Zeile 0 oben.
2. Die `.npz` in BeamShaperPlots öffnen (z. B. nach `Messdaten/` kopieren). Die
   Pixelgröße kommt aus der Datei, die Kamera-Einstellungen gelten dafür nicht;
   kein Hintergrundabzug, keine Übersteuerung. Alle Plots und der Report wie bei
   einem Messbild (Intensitätsskala 0 … 1).
3. Vergleich: Messbild auswählen, unter **„Vergleich (z. B. Simulation)“** die `.npz`
   wählen → Reiter „Vergleich“: beide 2D-Profile nebeneinander (Simulation links),
   jedes auf sein Maximum normiert ((I − Untergrund)/(Peak − Untergrund)), gleicher
   Ausschnitt in µm um das jeweilige Zentrum, gemeinsame Farbskala.
   „Vergleich als PDF speichern“ →
   `Auswertung/Plots/JJJJ-MM-TT/<Messung>_vs_<Simulation>_comparison.pdf` (16 cm breit).

Für gleich große Ausschnitte in Übersicht und Vergleich die „Schnitt-Halbbreite“
fest einstellen (z. B. 8 µm).

## LaTeX

Alle PDFs sind genau 16 cm breit (`\textwidth`, A4 mit 2,5 cm Rändern). Alle Texte
(Achsenbeschriftungen, Ticks, Legenden, Teilplot-Titel, Text im Bild) haben **eine**
Schriftgröße, Standard 11 pt, einstellbar in der GUI („Schriftgröße (LaTeX)“).
Mit `\includegraphics[width=\textwidth]{...}` erscheint sie im Dokument exakt so groß.
Schrift: Computer/Latin Modern (wie LaTeX), fehlende Zeichen aus DejaVu Serif.

## Report

Beim Export (einzelnes Bild) und im Batch entsteht zusätzlich ein PDF-Report
(`Auswertung/JJJJ-MM-TT_<name>_report.pdf` bzw. `..._batch_report.pdf`):
je Bild eine A4-Seite mit Übersichtsplot, den Radien w der drei Regionen
(1/e², 50 %, 90 %) entlang der Ellipsen-Halbachsen (lang/kurz, mit Neigungswinkel θ)
und entlang horizontal/vertikal, sowie Uniformity σ/µ und Peak-Valley in jeder Region.
Im Batch vorne eine Vergleichsseite mit Tabelle und Balkendiagramm.

### Uniformity und Crosstalk im Fallengitter

Abschätzung wie in `Multitone_Simulation` (`Combinated_Optimization/lib/single_beam.py`,
`weighted_multitone_flattop_optimizer.py`): das gemessene Profil steht auf einem
Quadratgitter (Pitch, Standard 5,288 µm), die 8 Nachbarn sind dasselbe Profil um ±Pitch
verschoben.

* hart, je Ring (1/e², 50 %, 90 %): U = σ/µ, η = Σ I_Nachbarn / Σ I_eigen über der Ellipse
* atomgewichtet: W = exp(−r²/2σ_atom²), σ_atom aus Rb-85, T = 17 µK, ν_r = 60,4 kHz (≈ 108 nm);
  U_w = σ_W/µ_W, η_w = Σ I_Nachbarn·W / Σ I_eigen·W
* ± bei η: Unsicherheit aus dem Untergrund (8 · δB / ⟨I_eigen⟩)
* reicht das Bild nicht bis zu den Nachbarn (< 95 % der Stützpunkte im Bild), steht „–“

In der GUI einstellbar (Pitch, T, ν_r) und abschaltbar; im Batch wird gefragt, für welche
Bilder gerechnet wird. Kommandozeile: `--pitch 5.288`, `--no-lattice [DATEIEN]`.

Schrift: Latin Modern Roman liegt in `beamshaper/fonts` bei (GUST Font License).
cmr10 wird bewusst nicht verwendet – dort liegt auf dem Zeichen „µ“ ein Akzent.

## Ablage der Ergebnisse (neben den Bildern)

    Auswertung/Plots/JJJJ-MM-TT/<name>_overview.pdf   (+ _axes, _fit, _flatness)
    Auswertung/JJJJ-MM-TT_<name>_results.json          Kennzahlen, Fitparameter ± Fehler, Einstellungen
    Auswertung/JJJJ-MM-TT_<name>_flatness.csv
    Auswertung/JJJJ-MM-TT_batch_summary.csv            ;-getrennt, Dezimalkomma (Excel)

## Aufbau

    main.py                  Start der GUI
    Messdaten/               Messbilder (BMP, PNG, TIFF, JPG); Auswertung landet in Messdaten/Auswertung/
    beamshaper/imageio.py    Bilder laden (8/12/16 bit), Hintergrund erkennen, Simulationen (.npz)
    beamshaper/models.py     Supergauss-Modell, Radius bei Level
    beamshaper/analysis.py   Fit + Kennzahlen -> FlatTopResult   (nur Rechnung)
    beamshaper/plotting.py   Figuren aus FlatTopResult           (nur Plots, inkl. Titelbild, Vergleich)
    beamshaper/report.py     PDF-Report (eine A4-Seite pro Bild, Batch-Vergleich)
    beamshaper/export.py     PDF / JSON / CSV
    beamshaper/batch.py      Ordner-Auswertung, auch als Kommandozeile
    beamshaper/gui.py        PyQt5-Oberfläche
    tests/                   pytest mit synthetischen Bildern
