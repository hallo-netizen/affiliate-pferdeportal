# AFFILIATE RELEASE – OTTO AUTOMATISIERUNGSKONZEPT

STAND: 2026-09-07
STATUS: GEBUNDENER KISS-UMSETZUNGSVERTRAG
SCOPE: OTTO über bestehenden Awin-Weg; Digistore24 zurückgestellt.

## 1. Ziel

OTTO wird als breite Commerce-Quelle des Pferde-Ateliers weitgehend automatisch genutzt.
Es entsteht **kein eigenes OTTO-Plugin und keine zweite Affiliate-Architektur**.

Technischer Hauptweg:

`Awin -> OTTO-Programm -> Feed/Werbemittel -> Affiliate-Zentrale -> Prüfung -> Ziel -> Slot -> Ausgabe`

Fachlicher Exact-Product-Weg:

`Produktwissen -> exakte Produktidentität -> Affiliate Exact Match -> aktuelles OTTO/Awin-Angebot`

Produktwissen bleibt fachliche Produktwahrheit.
Affiliate bleibt Commerce-Wahrheit für Angebot, Preis, Verfügbarkeit, Verkäufer, Tracking und Werbemittel.

## 2. Offiziell mögliche OTTO-Werbeformen und interne Nutzung

### A. Produktfeed / konkrete Produktwerbung
HAUPTWEG.
- einzelne Produkte;
- Produktkarten auf Hub-/Kategorieebenen;
- Produktkarten in Beiträgen;
- Exact Match für Produktvergleich/Variantenvergleich/Beratung, wenn Produktwissen eine exakte Identität vorgibt.

Pflicht:
- echte Feedzeile;
- aktives Awin-Programm;
- gültiges Tracking;
- echtes Bild;
- Preis/Verfügbarkeit aus Commerce-Quelle;
- bei konkreter OTTO-Produktwerbung Verkäufer;
- tägliche Aktualisierung mindestens.

### B. Banner
HAUPTWEG.
- Startseite/Hubs;
- Kategorie-/Produktgruppenebene;
- Journal/Beitrag, soweit bestehender Designslot passt.

Nur **reale OTTO/Awin-Werbemittel**.
Kein Produktbild wird künstlich zum Banner.

Beschaffung und Verteilung sind getrennt:
- Beschaffung: nur über belegten realen Awin-/OTTO-Creative-Zugang, Export oder andere bestätigte Quelle;
- Verteilung: vorhandene Affiliate-Zentrale klassifiziert, prüft Bild/Tracking, ordnet Ziel + Slot zu und kann verifiziertes Awin-Banner automatisch aktivieren.

Solange kein realer maschinenlesbarer Creative-Katalog belegt ist, bleibt nur die Bannerbeschaffung PENDING.
Die automatische Zuordnung/Activation eines realen importierten OTTO-Banners ist davon unabhängig.

### C. Text-/Deeplink
Deeplinks werden als **Link-Baustein** genutzt:
- Produktkarte -> konkretes Produkt;
- Banner -> konkrete OTTO-Zielseite/Sortiment;
- zukünftiger eigener CTA nur, wenn ein echter Designslot/Vertrag existiert.

V1 führt **keine automatische Textlink-Injektion in redaktionellen Fließtext** ein.
Grund: kein notwendiger zusätzlicher Outputtyp; redaktionelle Integrität und KISS.

### D. OTTO-Logo
Kein eigener Outputpfad.
Ein reales freigegebenes Logo-/Image-Creative darf nur über den bestehenden Bild-/Bannerweg laufen, wenn es fachlich und vom realen Designslot her passt.
Kein eigener Logo-Slot und keine Logo-Pflicht.

### E. Sortimentswerbung
Auf breiten Seiten/Hubs bevorzugt über:
- reales OTTO-Sortimentsbanner/Creative; oder
- konkrete repräsentative Produktkarten.

Eine eigenständige Sortiments-CTA/Textwerbung wird erst aktiviert, wenn ihr realer Werbemittel-/Disclosure-Vertrag technisch vollständig gebunden ist.
Keine still aus Einzelprodukten erfundene Sortimentswerbung.

## 3. Ebenenmodell

| Portalebene | Produktfeed | Banner | Auswahlprinzip |
|---|---|---|---|
| Startseite | kein neuer Produktblock | ja, breites reales OTTO-Creative | nur eindeutiger Startseiten-/Breitenfit |
| Hub Ebene 1 | bis zu 3 Produkte | ja | Themenfit + Datenqualität + Aktualität + zentrale Rangfolge |
| Hub Ebene 2 / Produktgruppe | bis zu 3 Produkte | ja | spezifischer Kategorienfit vor Breite |
| Kategorie / Leaf | bis zu 3 Produkte | ja | konkrete Kategorie, keine fachfremden OTTO-Produkte |
| normaler Fachbeitrag | bis zu 3 Produkte | Inline-Banner möglich | vorhandene zentrale Artikel-/Kategorienrelevanz |
| Produktvergleich / Variantenvergleich | Exact Match, keine Substitution | optional thematisch | Produktwissen-Identität gewinnt; fehlendes Angebot = keine Ersatzkarte |
| Beratung mit fachlich bestimmten Modellen | Exact Match, wenn Produktwissen vorgibt | optional thematisch | fachliche Auswahl kommt nicht aus Affiliate |

## 4. Auswahl- und Zuordnungslogik

### Breitenplätze: Hub/Kategorie/normaler Beitrag
Affiliate darf aus dem realen OTTO-Bestand auswählen.

Reihenfolge:
1. technische/rechtliche Sperren;
2. Awin-Programmfreigabe;
3. Verfügbarkeit/Aktualität;
4. Verkäufer/Tracking/Bild;
5. fachliche Zielpassung;
6. Spezifität des Zieles;
7. Deduplizierung;
8. bestehende zentrale Rangfolge/Providerstrategie.

OTTO erhält **keinen künstlichen Provisionsbonus**, der eine fachlich bessere Quelle verdrängt.
Seine Breite erzeugt natürlich mehr passende Kandidaten.

### Exakt gebundene Inhalte
Sobald Produktwissen eine Exact-Product-Anforderung liefert:
1. Identität über stabile Kennung(en), bevorzugt GTIN/EAN, sonst echte MPN;
2. nur identischer Affiliate-Kandidat;
3. mehrere Anbieter desselben Produkts dürfen als Kaufangebote konkurrieren;
4. kein Exact Match -> kein Kaufangebot;
5. niemals ein ähnlich benanntes Ersatzmodell.

## 5. Schnittstelle Produktwissen -> Affiliate

Keine Tabellenkopplung und kein Affiliate-Schreibrecht in Produktwissen.

Affiliate stellt eine read-only Consumer-Schnittstelle bereit:
`ppar_affiliate_exact_product_requirements`

Erwartetes Format pro gewünschtem Produkt/Variante:
- optional `subject_id` als opaque Referenz;
- `identifiers`: Liste aus `type` + `value`;
- zulässige Typen: GTIN, EAN, MPN, MANUFACTURER_ARTICLE_NUMBER.

Affiliate matcht ausschließlich belastbare Identitäten.
Die Produktwissen-Implementierung kann diesen Filter später aus ihrer stabilen Repository-/Post-Bindung speisen, ohne dass Affiliate deren Datenbanktabellen kennt.

## 6. OTTO-Identität im Awin-System

Kanonische technische Identität:
**Awin Advertiser ID 14336**.

Programmnamen sind Anzeige/sekundärer Beleg, nicht die technische Hauptidentität.
Dadurch darf eine Namensabweichung keine falsche OTTO-Aktivierung verursachen.

## 7. Aktualisierung

Produktfeed:
- mindestens täglich;
- Preis, Bestand, Verkäufer und Produktmetadaten sind Bestandteil der Freshness-Bindung;
- Änderungen lösen Update/Verifikation/Neubewertung aus;
- verschwundene Produkte bleiben im vorhandenen Quarantäne-/Inactive-Weg;
- nach kompletter Verifikationswelle Artikelpläne gebündelt neu bewerten.

Banner:
- reale Änderungen nur aus realer Werbemittelquelle;
- bestehende Bild-/Tracking-/Target-/Slot-Verifikation;
- Last-Known-Good bei fehlerhafter Aktualisierung nicht blind überschreiben.

## 8. Fail-Closed-Hardrules

BLOCKED statt raten bei:
- falscher/fehlender Awin-Advertiser-ID;
- Feed-Ambiguität;
- fehlendem Tracking;
- fehlendem realen Produktbild;
- fehlendem Verkäufer bei konkreter OTTO-Produktwerbung;
- unklarer Exact-Product-Identität;
- Productwissen-Exact-Anforderung ohne identischen Affiliate-Match;
- fehlender realer Bannerquelle;
- unpassendem Bannerformat/-slot;
- fachlich mehrdeutiger automatischer Zielzuordnung.

## 9. Abnahmegrenze

LOKAL/STRUKTURELL kann geprüft werden:
- ID 14336;
- Productfeed -> Verifikation -> Ziel -> Slot;
- 1/2/3-Produktranking;
- Exact-Match statt Ersatz;
- Verkäufer-Gate;
- Banner-Zuordnung nur für reale Creative-Datensätze;
- Nicht-OTTO-Awin unverändert.

REAL/LIVE bleibt erforderlich:
- OTTO 14336 im eigenen Awin-Konto;
- echter Produktfeed;
- exakte Verkäufer-Spalte im realen Feed;
- WordPress/MariaDB-End-to-End;
- echte öffentliche Produkt-/Kategorie-/Beitragsausgabe;
- realer OTTO/Awin-Bannerbestand bzw. belegter Beschaffungsweg.

Ohne diese Realbelege kein LIVE-PASS.
## 10. Vollautomatische Bannerverteilung nach Anteilen

ZIEL:
Nach der fachlichen und technischen Zuordnung entscheidet das System selbst, **welche freigegebene Bannerquelle einen konkreten Bannerplatz erhält**.

Die Quote ist niemals die erste Entscheidung.

Verbindliche Reihenfolge:
1. manuelle Reparatur/Festzuordnung oder Veto;
2. technische/rechtliche Freigabe;
3. Ziel-/Themenrelevanz;
4. Designslot-/Formatpassung;
5. nur innerhalb der **besten vorhandenen Relevanzstufe**: Anteilssystem;
6. innerhalb der gewählten Quelle bleibt die bestehende Qualitäts-/Prioritätsreihenfolge erhalten.

Damit kann eine Quote niemals ein fachlich schwaches Fallback-Banner gegen einen deutlich passenderen Banner erzwingen.

### Startverteilung

Konfigurierbarer KISS-Startwert:

- OTTO: 40
- andere Awin-Programme: 25
- ADCELL: 20
- Direktpartner: 15
- Digistore24: 0 (zurückgestellt)
- Sonstige: 0

Die Werte sind relative Zielanteile.
Sind auf einer Seite nur OTTO und ADCELL fachlich geeignet, werden nur deren vorhandene Anteile automatisch normalisiert.
Eine nicht verfügbare Quelle erzeugt **keinen leeren Bannerplatz**, solange eine andere gleich relevante freigegebene Quelle vorhanden ist.

Diese Startwerte sind keine dauerhafte Geschäftsentscheidung.
Sie können intern jederzeit geändert werden, ohne die Zuordnungsarchitektur anzufassen.

### Was „Anteil“ bedeutet

V1 verteilt **Bannerplätze**, nicht abrechnungsgenaue Ad-Impressions.

Die Auswahl ist deterministisch pro:
- Kalenderwoche;
- Seite/Kontext;
- Banner-Slot.

Vorteile:
- kein zufälliges Flackern bei jedem Request;
- cachefreundlich;
- reproduzierbar bei Fehlerprüfung;
- trotzdem regelmäßige Rotation;
- keine neue Impression-Counter-/Realtime-Architektur.

Wenn später echte Impression-Shares benötigt werden, ist das eine eigene Ausbaustufe und wird nicht still in V1 hineingebaut.

## 11. Manuelle Reparaturinstanz

Die Automatik ist Normalbetrieb.
Der Mensch repariert nur Ausnahmen.

Die bestehende interne Instanz „Zuordnungen“ wird ausdrücklich als Reparaturinstanz verwendet:

- **Automatik** → System entscheidet wieder selbst;
- **Fest auswählen** → bestimmtes Banner/Produkt erzwingen;
- **Nicht anzeigen** → Ausgabe auf dieser Zuordnung sperren;
- **Vererbung** → Ausnahme auf strukturelle Unterseiten anwenden.

Zusätzlich bleiben die vorhandenen Chef-/Control-Grenzen bestehen:
- Provider-Veto;
- Partner-Veto;
- Creative-Veto;
- Target-Veto;
- Slot-Veto;
- Output-Veto;
- globale Notabschaltung.

Manuelle Reparatur steht **vor** der automatischen Anteilsauswahl.
Beim Zurücksetzen auf „Automatik“ fällt die Seite sofort wieder in das normale Relevanz-/Anteilssystem zurück.

## 12. Leitsatz

**Automatik entscheidet alles, was eindeutig ist.  
Anteile steuern nur zwischen gleich guten Möglichkeiten.  
Der Mensch repariert Ausnahmen – er betreibt nicht den Normalworkflow.**

## 13. Konkret gebundene Bannerquelle

Die Affiliate-Zentrale besitzt jetzt eine fail-closed Anschlussstelle für einen **realen** Awin-Creative-Bestand:

`ppar_affiliate_awin_static_creatives`

Sie erfindet keine Awin-API. Ein später bestätigter Export/API-/Connectorweg liefert darüber reale Zeilen.

Minimaler Realvertrag pro Banner:
- `advertiser_id`
- `creative_id`
- `title`
- `image_url`
- `tracking_url`
- optional Ziel-URL, Breite, Höhe, Tags, Status.

Pflicht:
Die Advertiser-ID muss exakt dem aktuell verarbeiteten Awin-Programm entsprechen.

Fail-closed:
- fremde Advertiser-ID → blockiert;
- Bild fehlt → blockiert;
- Tracking fehlt und kann nicht aus einer realen Ziel-URL erzeugt werden → blockiert;
- ungebundene Quelle → vorhandene Banner werden nicht irrtümlich entfernt.

Für den wichtigen Sonderfall „Quelle ist real gebunden, liefert aber aktuell 0 Banner“ unterstützt der Vertrag ein Envelope:
`['bound'=>true,'rows'=>[]]`.
Nur dann darf die bestehende Reconciliation alte Banner kontrolliert zurückziehen.

## 14. Anteil 0 und Mehrfachplätze

`0` bedeutet im automatischen Bannerbetrieb **Ausschluss**, nicht nur „kein Bonus“.
Eine manuelle Festzuordnung darf als bewusste Reparaturausnahme weiterhin greifen, sofern alle Sicherheitsgates bestehen.

Mehrere Bannerplätze auf derselben Seite erhalten getrennte deterministische Anteilssamen.
Platz 2 darf das auf Platz 1 gewählte Creative nicht wiederholen.

## 15. Reparatur auf allen Ebenen

Seiten/Unterseiten:
`Zuordnungen` → Automatik / fest / keine Ausgabe / Vererbung.
Manuelle Abweichung verlangt Reparaturgrund und speichert letzten Benutzer + Zeitpunkt.

Kategorie-/sonstige Portalziele:
Die vorhandene Creative-Library-Entscheidung `portal_approve_fixed` kann ein konkretes Creative mit Begründung auf ein reales Portalziel + Slot binden.

Übergreifend:
Provider-/Partner-/Creative-/Target-/Slot-/Output-Veto sowie globale Notabschaltung bleiben erhalten.

## 16. Direkte Prüfmöglichkeit

Im Repository ohne Docker:

`bash AFFILIATE_HOBBYRAUM/run_otto_checks.sh`

Der Lauf:
1. PHP-Syntaxprüfung der gebundenen Source-Dateien;
2. statischer OTTO/Awin-/Productwissen-/Banner-Vertrag;
3. ausführbarer Anteil-/Reparatur-/Source-Behavior-Test.

Der isolierte Docker/Podman-Hobbyraum bleibt zusätzlich verfügbar:

`python3 AFFILIATE_HOBBYRAUM/affiliate_hobbyraum.py AFFILIATE_HOBBYRAUM/TASK.current.json`

Beide lokalen Wege ersetzen keinen realen WordPress-/MariaDB-/Awin-Livebeleg.

