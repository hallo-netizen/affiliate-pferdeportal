# PRODUKTVERGLEICH – MARKTRECHERCHE BATCH T

Stand: 2026-09-11
Status: RESEARCH CANDIDATE EVIDENCE / RESTGAP-KLASSIFIKATION / NICHT PRODUCT KNOWLEDGE / NICHT SEO-FREIGEGEBEN

## Hard Rule

Dieser Batch bearbeitet die **letzten acht** `NO_GROUP_EVIDENCE`-Keys des A–J-Checkpoints nach Batch S.

Bearbeitet:
- `turnierplaner`;
- `haftung-im-stall`;
- `stallbau-beratung`;
- `stallwechsel-checkliste`;
- `weidecheckliste`;
- `futterumstellung-checkliste`;
- `weidemanagement-grundlagen`;
- `futterplan-vorlagen`.

Wichtig:
Ein Portal-Key mit Themenkategorie `Vergleich` ist nicht automatisch eine zulässige `PRODUCT_COMPARISON V1`-Produktklasse. Nichtprodukt-/Service-/Wissens-/Vorlagen-Intent bleibt sichtbar, statt künstlich zwei Produkte zu erfinden.

Die finale Entscheidung über Artikeltyp, Paarzulässigkeit und Dossier liegt beim PRODUKTVERGLEICH-System/Plugin.

---

## 1. Turnierplaner

Registry-Key:
`turnierplaner`

### Portal-Intent

Die aktuelle Pferde-Atelier-Seite beschreibt `Turnierplaner` als persönliches Organisationswerkzeug für:
- Starts/Prüfungen;
- Meldeschluss;
- Abfahrt/Fahrzeit;
- Dokumente;
- Ausrüstung;
- Versorgung.

Die Vergleichsseite stellt ausdrücklich **Papierplaner, Tabellen, Kalender und spezialisierte Apps** als unterschiedliche Formen gegenüber.

Portalquellen:
https://pferde-atelier.de/transport/transport-turnier-und-reisen/
https://pferde-atelier.de/category/turnierplaner-vergleich/
https://pferde-atelier.de/category/turnierplaner-faq/

### Marktcheck

Aktuelle Webprodukte mit Bezeichnung `Turnierplaner` sind leicht auffindbar, richten sich jedoch überwiegend an Sportvereine/Turnierveranstalter und Spielplan-/Bracket-Organisation, nicht an die pferdespezifische persönliche Turniertagplanung des Portal-Intents.

Beispiele für **bewusst nicht übernommene** falsche Klasse:
- ligantor Turnierplaner für Sportvereine;
- allgemeine Turnierbaum-/Spielplan-Apps.

### Fachgrenze

Papier-Checkliste, Tabellen-Vorlage, Kalender-App und spezialisierte Reiter-App sind keine automatisch gleiche Produktklasse.
Vor PRODUCT_COMPARISON V1 muss entschieden werden, ob der Key:
- konkrete kaufbare Planerprodukte;
- digitale Anwendungen;
- Vorlagen;
- oder ein redaktionelles Organisationskonzept
meint.

Research-Status:
`PORTAL_INTENT_PROVEN / PRODUCT_CLASS_AMBIGUOUS / EQUESTRIAN_EXACT_PRODUCT_IDENTITY_NOT_BOUND`.

Coverage-Folge:
`NO_GROUP_EVIDENCE -> PARTIAL_AMBIGUOUS`.

---

## 2. Haftung im Stall

Registry-Key:
`haftung-im-stall`

### Portal-Intent

Die aktuelle Portalhauptseite behandelt:
- Verantwortlichkeiten zwischen Pferdehalter, Stallbetreiber, Reitbeteiligungen und Besuchern;
- Schäden/Unfälle;
- Stallordnung/Verträge;
- Versicherungen;
- rechtliche/versicherungsfachliche Beratung.

Die Portal-Vergleichsseite beschreibt ausdrücklich Unterschiede von Versicherungs- und Vertragslösungen je Rolle und Risiko.

Portalquellen:
https://pferde-atelier.de/wissen/wissen-versicherungen-und-recht/haftung-im-stall/
https://pferde-atelier.de/category/haftung-im-stall-vergleich/

### Fachgrenze

`Haftung im Stall` ist keine konkrete Produktgruppe. Ein sinnvoller Vergleich müsste zuerst auf einen eigenständigen Artikeltyp/Subintent normalisiert werden, z. B.:
- konkrete Versicherungsart mit exakt gebundenen Tarifen/Versicherern;
- Vertrags-/Dienstleistungsangebot;
- rein redaktioneller Rechtsvergleich.

Ein Versicherungsprodukt darf nicht wie ein physisches PRODUCT_COMPARISON-V1-Modell behandelt werden, solange kein dafür freigegebener Vertrag/Profilweg existiert.

Research-Status:
`LEGAL/INSURANCE_TOPIC / PRODUCT_COMPARISON_V1_CLASS_NOT_PROVEN / ARTICLE_TYPE_REQUIRED`.

Coverage-Folge:
`NO_GROUP_EVIDENCE -> PARTIAL_AMBIGUOUS`.

---

## 3. Stallbau Beratung

Registry-Key:
`stallbau-beratung`

### Portal-Intent

Die aktuelle Pferde-Atelier-Seite definiert Stallbau-Beratung als Planungs-/Beratungsleistung zu:
- Haltungskonzept;
- Pferdezahl;
- Laufwegen;
- Klima;
- Entmistung;
- Futterlagerung;
- Wasser;
- Baurecht/Brandschutz;
- Fachplanern/Architekten.

Portalquellen:
https://pferde-atelier.de/wissen/wissen-beratung-und-partner/stallbau-beratung/
https://pferde-atelier.de/category/stallbau-beratung-beratung/

### Fachgrenze

Das ist eine **Dienstleistung**, kein serienmäßiges Produktmodell.
Ein Anbieter-A-vs-B-Vergleich könnte fachlich möglich sein, braucht aber einen Dienstleistungs-/Anbietervergleichsvertrag; PRODUCT_COMPARISON V1 mit Produktidentität/Herstellerfakten darf nicht still dafür missbraucht werden.

Research-Status:
`SERVICE_CLASS_PROVEN / PRODUCT_COMPARISON_V1_CONTRACT_MISMATCH / SERVICE_COMPARISON_ARTICLE_TYPE_REQUIRED`.

Coverage-Folge:
`NO_GROUP_EVIDENCE -> PARTIAL_AMBIGUOUS`.

---

## 4. Stallwechsel-Checkliste

Registry-Key:
`stallwechsel-checkliste`

### Portal-Intent

Die aktuelle Portalhauptseite beschreibt eine **Checkliste/Planungshilfe** für:
- Kündigungsfristen;
- Gesundheits-/Impfunterlagen;
- Transport;
- Futter;
- Eingewöhnung;
- Herdenintegration.

Portalquelle:
https://pferde-atelier.de/wissen/wissen-vorlagen-und-planung/stallwechsel-checkliste/

### Fachgrenze

Der Key ist aktuell ein redaktionelles Planungs-/Vorlagenthema. Kein Hersteller-/Modellprodukt ist durch den Portal-Intent definiert.

Falls später konkrete kaufbare Checklisten/Planer verglichen werden sollen, braucht es zuerst eine eindeutige Produkt-/Vorlagenklasse und deren Identitäten.

Research-Status:
`CHECKLIST_CONTENT_CLASS / STANDALONE_PRODUCT_CLASS_NOT_PROVEN`.

Coverage-Folge:
`NO_GROUP_EVIDENCE -> PARTIAL_AMBIGUOUS`.

---

## 5. Weidecheckliste

Registry-Key:
`weidecheckliste`

### Portal-Intent

Die aktuelle Portalhauptseite ordnet eine wiederkehrende Kontrollcheckliste für:
- Zaun;
- Tore;
- Wasser;
- Pflanzen/Giftpflanzen;
- Boden/Flächenzustand;
- Unterstände/Schattenplätze.

Portalquelle:
https://pferde-atelier.de/wissen/wissen-vorlagen-und-planung/weidecheckliste/

### Fachgrenze

Aktuell Wissens-/Checklistenwerkzeug, keine gebundene Serienproduktklasse.
Keine künstlichen A-vs-B-Produkte erzeugen.

Research-Status:
`CHECKLIST_CONTENT_CLASS / STANDALONE_PRODUCT_CLASS_NOT_PROVEN`.

Coverage-Folge:
`NO_GROUP_EVIDENCE -> PARTIAL_AMBIGUOUS`.

---

## 6. Futterumstellung-Checkliste

Registry-Key:
`futterumstellung-checkliste`

### Portal-Intent

Die aktuelle Portalhauptseite beschreibt eine Dokumentations-/Planungshilfe für schrittweisen Futterwechsel mit:
- Ausgangsration;
- neuem Futtermittel;
- Mengen;
- Übergangsschritten;
- Beobachtungen.

Portalquelle:
https://pferde-atelier.de/wissen/wissen-vorlagen-und-planung/futterumstellung-checkliste/

### Fachgrenze

Eine Futterumstellungs-Checkliste ist nicht selbst ein Futterprodukt.
Ein Vergleich von Vorlagen/Formaten wäre ein eigener Vorlagen-/Tool-Artikeltyp und darf nicht mit Produktpaaren aus Futterinventar vermischt werden.

Research-Status:
`CHECKLIST_CONTENT_CLASS / PRODUCT_COMPARISON_V1_CLASS_NOT_PROVEN`.

Coverage-Folge:
`NO_GROUP_EVIDENCE -> PARTIAL_AMBIGUOUS`.

---

## 7. Weidemanagement Grundlagen

Registry-Key:
`weidemanagement-grundlagen`

### Portal-Intent

Die aktuelle Portalhauptseite definiert den Key als **Grundlagen-/Wissensthema** zu:
- Futterangebot;
- Boden-/Grasnarbenschutz;
- Besatz/Ruhezeiten;
- Wasser/Tore/Laufwege;
- Pflege/Nachsaat;
- saisonaler Flächendokumentation.

Portalquelle:
https://pferde-atelier.de/wissen/wissen-buecher-und-ratgeber/weidemanagement-grundlagen/

Die aktuelle Portal-Vergleichsseite vergleicht sogar `Weidesysteme/Konzepte`, nicht zwei konkrete Herstellerprodukte:
https://pferde-atelier.de/category/weidemanagement-grundlagen-vergleich/

### Marktbeleg für angrenzende Buchklasse

Es existieren kaufbare Fachbücher, z. B. das aktuelle FN-Praxishandbuch für Pferdehalter, das Weidemanagement als Teilbereich enthält.

Quelle:
https://www.fnverlag.de/fn-praxishandbuch-fur-pferdehalter-isbn-978-3-88542-795-7.html

Dieses Buch wird **nicht** als Beweis dafür verwendet, dass der Registry-Key eine Buchproduktklasse ist. Der Portal-Intent ist breiter.

Research-Status:
`KNOWLEDGE/CONCEPT_CLASS / BOOK_ADJACENCY_EXISTS / PRODUCT_CLASS_NOT_BOUND`.

Coverage-Folge:
`NO_GROUP_EVIDENCE -> PARTIAL_AMBIGUOUS`.

---

## 8. Futterplan Vorlagen

Registry-Key:
`futterplan-vorlagen`

### Portal-Intent

Die aktuelle Portalarchitektur beschreibt Papierlisten, Tabellen und digitale Lösungen als unterschiedliche Futterplan-Formate.

Portalquellen:
https://pferde-atelier.de/wissen/wissen-vorlagen-und-planung/
https://pferde-atelier.de/category/futterplan-vorlagen-vergleich/

### mrs. RIDE – Futterplan Druckvorlage

Aktuelles kaufbares Produkt:
- PDF-Druckvorlage;
- Sofortdownload;
- DIN A4;
- ausdrücklich für Futterplanung im Stall.

Anbieter-/Produktquelle:
https://mrsride.de/products/futterplan-druckvorlage

### Stallschild-Profi – Futterplan Design Vorlage / Futterplaner

Aktuelles kaufbares Produkt/System:
- eigener Futterplan als physisches Schild;
- individuelle Vorlage/Design wird auf Schildmaterial umgesetzt;
- verschiedene Materialien und Größen;
- für Pferd/Stallgasse, Fütterungszeiten und Mengen.

Anbieterquelle:
https://stallschild-profi.de/alle-produkte/futterplaner-fuer-pferde/deine-futterplan-design-vorlage/

### Fachgrenze

Konkrete Produkte existieren, aber PDF-Druckvorlage und dauerhaftes physisches Stallschild sind nicht automatisch dieselbe Produktklasse.
Weitere Klassen wären Spreadsheet/App/Software.

Research-Status:
`CONCRETE_TEMPLATE/PLAN_PRODUCTS_FOUND / MULTI_FORMAT_CLASS / FORMAT_MATRIX_REQUIRED`.

Coverage-Folge:
`NO_GROUP_EVIDENCE -> EVIDENCE_PRESENT`.

---

## Negativprüfung Batch T

- Allgemeine Sport-Turnierplaner werden nicht als pferdespezifische persönliche Turnierplaner übernommen.
- Rechtsthema `Haftung im Stall` wird nicht in willkürliche Versicherungsprodukte umgedeutet.
- Beratungsdienstleistung wird nicht als physisches Produktmodell materialisiert.
- Checklisteninhalte werden nicht durch erfundene Herstelleridentitäten in PRODUCT_COMPARISON V1 gezwungen.
- Fachbuch zu Weidemanagement macht den breiteren Knowledge-Key nicht automatisch zur Buchproduktklasse.
- PDF-Futterplan und physisches Stallschild werden trotz gleichem Oberzweck nicht ungeprüft direkt gepaart.
- Keine Markt-Vollständigkeitsbehauptung.
- Keine finale Produktpaarentscheidung.

## Ergebnis Batch T

Die letzten acht `NO_GROUP_EVIDENCE`-Keys des A–J-Checkpoints wurden source-bound bearbeitet.

Neue Coverage-Klassifikation:
- `turnierplaner` -> `PARTIAL_AMBIGUOUS`;
- `haftung-im-stall` -> `PARTIAL_AMBIGUOUS`;
- `stallbau-beratung` -> `PARTIAL_AMBIGUOUS`;
- `stallwechsel-checkliste` -> `PARTIAL_AMBIGUOUS`;
- `weidecheckliste` -> `PARTIAL_AMBIGUOUS`;
- `futterumstellung-checkliste` -> `PARTIAL_AMBIGUOUS`;
- `weidemanagement-grundlagen` -> `PARTIAL_AMBIGUOUS`;
- `futterplan-vorlagen` -> `EVIDENCE_PRESENT`.

Damit existiert **für keinen der 175 Registry-Keys mehr der Status `NO_GROUP_EVIDENCE`**.

Das bedeutet ausdrücklich **nicht**:
- 175 markt-vollständige Gruppen;
- 175 Pairing-Ready-Gruppen;
- 175 PRODUCT_COMPARISON-V1-fähige Gruppen;
- Product Knowledge vollständig;
- SEO-Freigabe.

Es bedeutet nur:
Jeder Registry-Key wurde im ersten Research-Coverage-Lauf entweder mit konkreter Evidence oder mit einer sichtbaren fachlichen/Artikeltyp-/Produktklassen-Ambiguität belegt.

Kein Pluginbau aus diesem Dokument.
Kein Product-Knowledge-Import.
Kein SEO-/Providerlauf.
Kein Merge.
Kein Publish.
