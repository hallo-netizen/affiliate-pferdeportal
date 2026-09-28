# LANDINGPAGES – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STATUS: PILOT_DEFINIERT_TECHNISCHE_UMSETZUNG_NOCH_NICHT_FREIGEGEBEN

## Belastbarer Stand

Das Landingpage-Büro ist eingerichtet.

Erster und einziger technischer Pilot:

**Pferdehaftpflicht vergleichen**

Bindung:
- sichtbarer Ort: bestehende Ebene-3-Seite `Pferdehaftpflicht`;
- bestehende echte Kategorien bleiben `Beratung Pferdehaftpflicht` und `FAQ Pferdehaftpflicht`;
- zusätzlich soll genau eine optisch gleichartige Kachel `Pferdehaftpflicht vergleichen` erscheinen;
- Ziel dieser dritten Kachel ist eine normale WordPress-Landingpage, keine Kategorie;
- die Landingpage bleibt außerhalb der normalen Kategorien-, PSERC-, PSTE- und Textmaschinenproduktion.

## SEO-/Inhaltsgrenze

Landingpage:
- transaktionale Suchabsicht;
- eigenes Hauptkeyword;
- Rechner/Angebot als Hauptziel;
- individueller Text.

Journal:
- informative Suchabsicht;
- normale Artikelproduktion;
- darf intern zur Landingpage verlinken;
- darf die transaktionale Hauptsuchabsicht der Landingpage nicht duplizieren.

## Providerstand

Vom Nutzer bestätigt:
- Tarifcheck: Partnerfreigabe vorhanden; Versicherungs-Pilot läuft über Tarifcheck;
- CHECK24: Partnerfreigabe vorhanden; soll jetzt bereits als eigener vorbereiteter Provider im Zielbild mitgeführt werden, auch wenn für den aktuellen Pferdehaftpflicht-Pilot keine zweite Versicherungs-Ausgabe aktiviert wird.

Providerregel für den Pilot:
- Tarifcheck = aktiver Zielprovider für `Pferdehaftpflicht vergleichen`;
- CHECK24 = vorbereitet/registriert für spätere geeignete Bereiche und andere Projekte;
- keine doppelte Versicherungs-Ausgabe auf der Pilot-Landingpage;
- keine erfundene CHECK24-Schnittstelle oder Bannerquelle.

Exakte interne Werbemittel-/Rechner-/Bannerquellen dieser Provider sind noch nicht technisch gebunden. Kein Endpunkt, Feed oder Importweg darf geraten werden.

## Kritischer technischer Befund

Die Landingpage darf für den Pilot **nicht als direkte WordPress-Unterseite von `Pferdehaftpflicht` angelegt werden**.

Grund:
Das aktuelle Template Kit liest direkte veröffentlichte Unterseiten einer Ebene-3-Seite als Themenquelle für deren Kategorietext. Eine echte Parent/Child-Verknüpfung würde die Landingpage damit trotz fehlender Kategorie in bestehende Text-/Darstellungslogik hineinziehen.

Pilotregel deshalb:
- Landingpage als eigenständige normale WordPress-Seite;
- nicht als Kategorie;
- nicht als direkte WordPress-Kindseite von `Pferdehaftpflicht`;
- nicht als normaler Menüpunkt;
- sichtbare Verbindung ausschließlich über genau eine ausdrücklich registrierte Zusatzkachel und interne Links.

Das aktuelle Kachel-Rendering kann Seiten und Kategorien grundsätzlich als gültige Kartenobjekte behandeln. Für den Pilot muss nur die Zusatzkachel separat in die bestehende Kartenliste eingebracht werden; die Kategorie-ID-/Artikelermittlung darf weiterhin ausschließlich echte Kategorien übernehmen.

## Technische Sperre

Die Affiliate-Zentrale besitzt eine eigene technische Current-Autorität:
`control/release-governance/CURRENT_RELEASE.json`.

Solange diese Current-Autorität keine Provider-/Slot-/Landingpage-Änderung erlaubt, wird dort kein Quellcode für diesen Pilot geändert.

Gleiches gilt für DESIGN: die optische Kachel-Erweiterung wird nur im zuständigen Design-Arbeitsweg und ausschließlich für den gebundenen Pilot umgesetzt.

## NEXT ACTION

Den Pilot `Pferdehaftpflicht vergleichen` technisch erst dann umsetzen, wenn die zuständigen AFFILIATE- und DESIGN-Current-Autoritäten die jeweilige Änderung freigeben; dabei ausschließlich diese eine Landingpage/Kachel testen und keinerlei weitere Kategorien oder Landingpages mitändern.
