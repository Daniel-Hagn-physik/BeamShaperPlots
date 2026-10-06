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
    beamshaper/imageio.py    Bilder laden (8/12/16 bit), Hintergrund erkennen
    beamshaper/models.py     Supergauss-Modell, Radius bei Level
    beamshaper/analysis.py   Fit + Kennzahlen -> FlatTopResult   (nur Rechnung)
    beamshaper/plotting.py   Figuren aus FlatTopResult           (nur Plots)
    beamshaper/export.py     PDF / JSON / CSV
    beamshaper/batch.py      Ordner-Auswertung, auch als Kommandozeile
    beamshaper/gui.py        PyQt5-Oberfläche
    tests/                   pytest mit synthetischen Bildern
