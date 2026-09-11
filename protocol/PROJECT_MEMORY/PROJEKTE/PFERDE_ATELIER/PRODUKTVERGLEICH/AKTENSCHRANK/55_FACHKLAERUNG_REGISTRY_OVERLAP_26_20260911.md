# PRODUKTVERGLEICH – FACHKLÄRUNG REGISTRY OVERLAP 26

Stand: 2026-09-11
Status: SOURCE-BOUND FACHKLÄRUNG / NICHT PRODUCT KNOWLEDGE / NICHT SEO-FREIGEGEBEN

## Ziel und harte Regel

Die 26 `REGISTRY_OVERLAP_KEY_AMBIGUITY`-Fälle werden fachlich so normalisiert, dass ein Produkt nicht allein wegen überlappender Portalbegriffe in mehrere konkurrierende Paaruniversen fällt.

Vorrangregel für spätere Maschinenbindung:
1. exakter Funktions-/Produkttyp vor Oberbegriff;
2. exakter Material-/Mechanismus-Subtyp vor Orts-/Sammelbegriff;
3. ein Residual-/Obergruppen-Key darf nur Produkte aufnehmen, die keiner spezielleren Registry-Gruppe entsprechen;
4. reine Synonym-/Doppel-/Inhaltskeys bleiben für PRODUCT_COMPARISON V1 fail-closed;
5. finale konkrete Paarfreigabe bleibt beim Plugin.

## 1. Satteldecken / Schabracken

`satteldecken` und `schabracken` werden nicht synonym behandelt.

- `schabracken`: geformte/disziplinspezifische Saddle-Pad/Schabracken-Klasse (Dressur, Springen/Close Contact, GP jeweils getrennt).
- `satteldecken`: nur echte vom Hersteller als Saddle Blanket/Decke bzw. nicht-schabrackenartige Sattelunterlage geführte Produkte.

Batch B bindet starke Schabracken-/Saddle-Pad-Evidence, aber keine ausreichend harte separate Satteldecken-Produktidentität.

Folge:
- `schabracken` -> `EVIDENCE_PRESENT`;
- `satteldecken` -> `EXACT_PRODUCT_IDENTITY_REQUIRED`.

## 2. Boxengitter

Normalisierung:
`boxengitter` = eigenständiges Gitterelement/Gitterfüllung einer Pferdebox, nicht komplette Boxentür, Boxenfront oder Trennwand.

Batch C bindet Boxenfront-/Trennsysteme, aber die eigenständige Serienproduktidentität `Boxengitter` ist noch nicht sauber separat gebunden.

Folge:
`boxengitter` -> `EXACT_PRODUCT_IDENTITY_REQUIRED`.

## 3. Trennwände im Offenstall

Normalisierung:
`trennwaende-im-offenstall` = Gruppenhaltungs-/Offenstall-Trennsysteme, nicht Boxentrennwände und nicht Fressgitter.

Batch C bindet Röwer & Rüb/HÖRMANN/Growi-Systeme für Gruppenhaltung/Offenstall.

Folge:
`trennwaende-im-offenstall` -> `EVIDENCE_PRESENT`.

## 4. Doppelte sichtbare Gruppe `Weidezaungeräte`

Registry besitzt zwei verschiedene Keys mit gleichem sichtbarem Namen:
- `weidezaungeraete`;
- `weide-zauntechnik-weidezaungeraete`.

Zusätzlich existieren spezifische Keys:
- Solar-Weidezaungeräte;
- Batterie-Weidezaungeräte;
- Netzgeräte für Weidezäune.

Canonical Rule:
- `weide-zauntechnik-weidezaungeraete` bleibt der kanonische Residual-Key für echte Kombi-/sonstige Elektrozaungeräte, die keinem spezifischeren Stromversorgungs-Key eindeutig zugeordnet sind;
- `weidezaungeraete` wird als redundanter Legacy-/Obergruppen-Key für PRODUCT_COMPARISON V1 gesperrt;
- Batterie/Solar/Netz gehen immer in den spezifischen Key, nicht zusätzlich in den Residual-Key.

PATURA P1 und vergleichbare Kombigeräte belegen die Residualklasse.

Folge:
- `weide-zauntechnik-weidezaungeraete` -> `EVIDENCE_PRESENT`;
- `weidezaungeraete` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

## 5. Reitplatzplaner / Reitplatzschleppe / Bahnplaner / Sandverteiler

Canonical Rule:
- `reitplatzplaner` = multifunktionales aktives Arena-Grooming-/Planiergerät mit definierter Arbeitsbreite/Anhängung/Funktionsmatrix; OTTO/GGT/Kneilmann Evidence.
- `reitplatzschleppe` = einfache gezogene Pflege-/Schleppklasse, nur wenn als eigenständiges Produkt und nicht derselbe multifunktionale Planer gebunden.
- `bahnplaner` = synonym überlappender Legacy-Key zu `reitplatzplaner`, kein zweites Paaruniversum.
- `sandverteiler` = derzeit nur Funktion einzelner Planer, keine eigenständige Produktklasse.

Folge:
- `reitplatzplaner` -> `EVIDENCE_PRESENT`;
- `reitplatzschleppe` -> `EXACT_PRODUCT_IDENTITY_REQUIRED`;
- `bahnplaner` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- `sandverteiler` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

## 6. Heuprüfer

`heupruefer` besitzt keine belastbar eigenständige Produktklasse neben `heufeuchtemesser`.
Heufeuchte-/Temperaturmessgeräte gehen ausschließlich in den präziseren Key `heufeuchtemesser`.

Folge:
`heupruefer` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

## 7. Weide-Wassertanks

Canonical Rule:
`weide-wassertanks` = geschlossener/transportabler Vorrats-/Speichertank zur Wasserversorgung auf der Weide.
Offene Tröge wie SUEVIA/PATURA WT gehören nicht in diesen Key.

Die bisherige Evidence belegt Tröge, keine ausreichend harte separate Tank-Produktklasse.

Folge:
`weide-wassertanks` -> `EXACT_PRODUCT_IDENTITY_REQUIRED`.

## 8. Anhängerkupplungen

Canonical Rule:
`anhaengerkupplungen` = Kupplungs-/Zugkugel-/Kupplungskopf-Hardware für den Anhänger, nicht die Fahrzeugkategorie und nicht bloß serienmäßige Ausstattung.

Aktuelle Evidence bindet noch keine konkrete Mehrhersteller-Produktidentität dieser engen Klasse.

Folge:
`anhaengerkupplungen` -> `EXACT_PRODUCT_IDENTITY_REQUIRED`.

## 9. Offenstalltore

`Offenstalltor` beschreibt derzeit primär einen Einsatzort; gefundene Produkte sind Weidetore, Paddock-/Paneltore oder Gebäudetore und besitzen bereits präzisere Funktionsklassen.
Kein zweites Paaruniversum nur wegen Einsatzort.

Folge:
`offenstalltore` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

## 10. Weideunterstände

Der Key überschneidet sich mit `mobile-unterstaende` und `weidezelt`.
Mobile Produkte gehen in diese präziseren Keys.
Der verbleibende Residual-Intent von `weideunterstaende` ist ein fester/baulicher Unterstand und damit überwiegend Anlagen-/Bauklasse.

Folge:
`weideunterstaende` -> `SERVICE_KNOWLEDGE_CHECKLIST_ARTICLE_TYPE`.

## 11. Unterstand-Boden

Der Key überschneidet sich vollständig mit funktional präziseren Gruppen:
- Liegefläche;
- Offenstall-Bodenbefestigung;
- Matten/Bodenstabilisierung/Drainage.

Ein eigener Produktvergleich allein wegen Einbauort `Unterstand` würde dieselben Produkte duplizieren.

Folge:
`unterstand-boden` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

## 12. Festzäune für Pferde

`Festzaun` ist Oberbegriff. Das Portal besitzt präzisere Material-/Funktionskeys:
- Holzzäune;
- Kunststoffzäune;
- Elektrozäune.

Keine Doppelmaterialisierung in der Obergruppe.

Folge:
`festzaeune-fuer-pferde` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

## 13. Paddockzäune

`Paddock` ist Einsatzort, aber aktuelle Evidence bindet konkrete Konstruktionen (Panel, Holz).
Der Key bleibt zulässig, jedoch nur mit Pflicht-Konstruktionssubtyp:
- `PANEL_PADDOCK_FENCE`;
- `WOOD_PADDOCK_FENCE`;
- weitere nur bei eigener gebundener Konstruktion.
Keine Kreuzpaarung zwischen Konstruktionen.

Folge:
`paddockzaeune` -> `EVIDENCE_PRESENT`.

## 14. Isolierte Wasserleitungen

Canonical Rule:
`isolierte-wasserleitungen` = passive thermische Rohr-/Leitungsisolation bzw. isoliertes Rohrsystem.
Heizkabel, Ringleitungs-Heizgeräte und komplette frostsichere Tränken werden ausgeschlossen.

SUEVIA Thermo-Rohr bindet eine konkrete Produktfamilie. Eine zweite unabhängige Herstellerfamilie derselben Klasse ist noch nicht hart gebunden.

Folge:
`isolierte-wasserleitungen` -> `SECOND_MANUFACTURER_REQUIRED`.

## 15. Frostschutz für Weidetränken

Der Key wird als Zubehör-/Nachrüstklasse normalisiert, nicht als komplette frostsichere Tränke:
- Thermostat/Steuerung;
- definierte Tränken-/Zuleitungs-Heizkomponente;
- nur innerhalb gleichen Techniksubtyps paaren.

Komplette frostsichere Tränken bleiben im separaten Key.
Batch S bindet PATURA/SUEVIA Frostschutzkomponenten und macht die Technikgrenzen sichtbar.

Folge:
`frostschutz-fuer-weidetraenken` -> `EVIDENCE_PRESENT`.

## 16. Pferdebürsten

Residual Rule:
`pferdebuersten` enthält nur Bürstenklassen, die nicht bereits `striegel` oder `kardaetschen` sind, z. B. Dandy-/Wurzel-/Scrubbing-Brush. Paarung ausschließlich innerhalb identischem Bürstentyp.

A bindet konkrete LeMieux-/Waldhausen-Kandidaten.

Folge:
`pferdebuersten` -> `EVIDENCE_PRESENT`.

## 17. Offenstallraufen

Der Key beschreibt überwiegend den Einsatzort und überschneidet sich mit präziseren Raufen-Gruppen (`heuraufen`, `heuraufen-fuer-weiden`, `mobile-heuraufen`, `heuballenraufen`).
Kein zweites Paaruniversum allein aufgrund Offenstall-Einsatz.

Folge:
`offenstallraufen` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

## 18. Weidetränken

Residual Rule:
`weidetraenken` = Außen-/Weidetränke ohne primären Spezialclaim `frostsicher` und ohne Behandlung als eigene reine Automatikklasse.
Spezifisch frostsichere Produkte gehen in den Frost-Key.
Die Paarung erfolgt zusätzlich innerhalb derselben Bauform (Trog/Becken etc.).

D/J/S binden konkrete Weide-/Trogtränken.

Folge:
`weidetraenken` -> `EVIDENCE_PRESENT`.

## 19. Heuraufen

Residual Rule:
`heuraufen` = Stall-/Boxen-/Wandraufen, die nicht in die spezifischeren Weide-, Mobil- oder Großballenraufen fallen.
C/E binden u. a. Wandraufen/Eckraufen.

Folge:
`heuraufen` -> `EVIDENCE_PRESENT`.

## 20. Automatische Tränken

Canonical Rule:
`automatische-traenken` = Tränken mit selbsttätigem Wasser-Nachlauf über Ventil/Schwimmermechanismus, ohne dass Frostschutz der primäre Vergleichsgegenstand ist.
Paarung nur gleiche Bau-/Ventilklasse; frost-special Produkte werden nicht doppelt materialisiert, wenn deren primärer Vergleichsintent Frostschutz ist.

D bindet PATURA/La Buvette/Kerbl automatische Becken-/Trogtränken.

Folge:
`automatische-traenken` -> `EVIDENCE_PRESENT`.

## 21. Verladetraining Zubehör

Der Key überschneidet sich mit `verladehilfen`, ist aber als Trainingsebene enger normalisierbar:
`NON_STRUCTURAL_LOADING_TRAINING_AID`.

Rampen, Stangen und festes Anhängerzubehör sind ausgeschlossen.
Die bisherige Evidence bindet noch keine belastbare konkrete Mehrhersteller-Produktidentität dieser engen Trainingsklasse.

Folge:
`verladetraining-zubehoer` -> `EXACT_PRODUCT_IDENTITY_REQUIRED`.

## Ergebnis

Von 26 Registry-Overlap-Fällen:
- **9** -> `EVIDENCE_PRESENT`;
- **6** -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- **6** -> `EXACT_PRODUCT_IDENTITY_REQUIRED`;
- **1** -> `SECOND_MANUFACTURER_REQUIRED`;
- **1** -> `SERVICE_KNOWLEDGE_CHECKLIST_ARTICLE_TYPE`;
- **3** weitere? Nein: Zählprüfung unten bindet jede Zeile exakt.

### Zählprüfung exakt

`EVIDENCE_PRESENT` (9):
`schabracken`, `trennwaende-im-offenstall`, `weide-zauntechnik-weidezaungeraete`, `reitplatzplaner`, `paddockzaeune`, `frostschutz-fuer-weidetraenken`, `pferdebuersten`, `weidetraenken`, `heuraufen`, `automatische-traenken`.

Korrektur der obigen Zwischenzahl: Das sind **10**, nicht 9.

`PRODUCT_COMPARISON_V1_NOT_APPLICABLE` (8):
`weidezaungeraete`, `bahnplaner`, `sandverteiler`, `heupruefer`, `offenstalltore`, `unterstand-boden`, `festzaeune-fuer-pferde`, `offenstallraufen`.

`EXACT_PRODUCT_IDENTITY_REQUIRED` (6):
`satteldecken`, `boxengitter`, `reitplatzschleppe`, `weide-wassertanks`, `anhaengerkupplungen`, `verladetraining-zubehoer`.

`SECOND_MANUFACTURER_REQUIRED` (1):
`isolierte-wasserleitungen`.

`SERVICE_KNOWLEDGE_CHECKLIST_ARTICLE_TYPE` (1):
`weideunterstaende`.

Summe: 10 + 8 + 6 + 1 + 1 = **26/26**.

`REGISTRY_OVERLAP_KEY_AMBIGUITY` ist damit als Primärursache auf **0** abgearbeitet.

## Harte Grenze

Die fachlichen Residual-/Vorrangregeln müssen vor realer flächiger Paarmaterialisierung maschinenfest in Registry/Profile/Policy gebunden werden. Dieses Dokument allein erzeugt kein Product Knowledge und kein Paar.

Kein SEO-/Providerlauf.
Kein Pluginbau aus bloßer Fachakte.
Kein Merge.
Kein Publish.
