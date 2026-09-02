# AFFILIATE-ZENTRALE — CURRENT USER SCOPE LOCK

Stand: 2026-09-02
Branch: `affiliate-release-current`
Status: `USER_SCOPE_AUTHORITY`

## Verbindliche Nutzerentscheidung

Der aktuell autorisierte Betriebsweg für Digistore24-Partnerschaften ist **manueller Bulkimport aus dem vom Nutzer bereitgestellten aktuellen Digistore24-CSV-Export**.

Zielbedienung:

`WordPress-Dashboard -> Affiliate-Zentrale -> Anbieter & APIs -> Datei importieren`

Es gibt **genau ein Uploadfeld**. Das Plugin erkennt den Anbieter selbst und verarbeitet nur eindeutig erkannte Dateiformate fail-closed.

Für Digistore24 gilt:
- die bereits bereitgestellte aktuelle CSV ist die autorisierte Runtime-Quelle für den manuellen Bestandsimport;
- bekannte aktuelle Sollmenge: 18 genehmigte Partnerschaften / 10 Vendoren;
- nur genehmigte Partnerschaften übernehmen;
- Produkt-ID ist der eindeutige Partnerschaftsschlüssel;
- Reimport ist Synchronisation, keine Einzelpflege und keine Dublettenerzeugung;
- danach vorhandenen DS24-Downstream weiterverwenden: Validierung -> Metadaten/Werbemittel -> Creative/Banner -> Bild/Tracking -> Ziel/Slot -> Draft -> Revalidation -> Persistenz -> LKG -> Readback -> Reassignment;
- Fehler eines Partners isolieren, übrige Partner weiterverarbeiten;
- eBay/idealo/Awin/ADCELL nicht regressiv verändern.

## Explizit außer Scope

Die automatische serverseitige Digistore24-Partnerschafts-Discovery ist **für den aktuellen Auftrag außer Scope** und darf den manuellen Import **nicht blockieren**.

Bis der Nutzer diesen Scope ausdrücklich ändert, ist VERBOTEN:
- erneut nach der Partnerliste oder derselben CSV zu fragen;
- erneut Browser-/Network-Screenshots für die DS24-Partnerschafts-Discovery anzufordern;
- erneut einen öffentlichen/private API-Discoveryweg als Voraussetzung für den manuellen Import zu untersuchen;
- den manuellen CSV-Import mit dem Argument abzulehnen, die CSV dürfe nur Testoracle sein;
- AFF-ERR-008, AFF-ERR-012 oder AFF-ERR-015 so auszulegen, dass die ausdrücklich autorisierte manuelle Runtime-CSV wieder gesperrt wird;
- die bekannte 18er-Liste fest im Produktcode zu verdrahten.

## Vorrangregel

Diese Datei dokumentiert die **spätere ausdrückliche Nutzerentscheidung** und supersediert für den aktuellen Auftrag alle älteren Aussagen, nach denen die DS24-CSV ausschließlich Testoracle sein dürfe oder automatische Discovery zuerst gelöst werden müsse.

Nur eine **neue ausdrückliche Nutzerentscheidung** darf diesen Scope wieder ändern.

## Ausführungsregel

Bei jedem Neustart/Chatwechsel ist der aktuelle Scope aus `control/release-governance/CURRENT_RELEASE.json` zu lesen. Wenn dort dieser Scope-Lock referenziert und aktiv ist, lautet der einzige zulässige Arbeitsstrang:

`MANUELLER EIN-FELD-BULKIMPORT -> POSITIV/NEGATIV/GESAMTWORKFLOW -> LIVEKANDIDAT -> LIVE-READBACK`

Keine freiwillige Rückkehr zur automatischen Discovery.
