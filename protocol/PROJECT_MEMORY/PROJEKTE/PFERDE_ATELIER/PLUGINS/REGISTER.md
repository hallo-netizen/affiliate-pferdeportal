# PFERDE-ATELIER – PLUGINREGISTER

STAND: 2026-09-15
ROLLE: ZENTRALES INVENTAR-/ARTEFAKTREGISTER, KEINE FACH-/LIVE-WAHRHEIT

## Statuswerte

`ARTEFAKT_SYNC`: PASS / BLOCKED / NICHT_ERFORDERLICH / UNGEKLÄRT

PASS nur wenn die isolierte aktuelle Datei tatsächlich unter
`/Campus-Plugins/PFERDE_ATELIER/<PLUGIN-ID>/CURRENT.zip`
liegt und aus der persistenten Ablage erneut gelesen, als ZIP geprüft und per SHA-256 gegen den belegten Quellstand verglichen wurde.

## PPA-001 – Affiliate-Zentrale (Portal-kompatibel)

- HERKUNFT: EIGENENTWICKLUNG
- KLASSE: PFERDE-ATELIER / Allgemeingültigkeit ungeklärt
- FACHBÜRO: `../AFFILIATE/`
- AUTORITATIVE TECHNISCHE QUELLE: Branch `affiliate-release-current` → `release/affiliate-zentrale/current/affiliate-portal-router/`
- AKTUELL BELEGTER TECHNISCHER KANDIDAT: 6.72.19
- KANONISCHES 26-DATEIEN-MANIFEST: `694af9869c7aa2b01a51f164173b1c51d9be7c24912c2e129420c3d111346a4b`
- KANONISCHER TESTARTEFAKT-HASH: `72f437e5235aaec53631db052e2184b588366c7f8aa7eb72ae1c9e043cdf157f`
- QUELLBELEG: Run `34692865477`, Artifact `10297556084`, Head `60a174accd71941ebad42501a9d9bd9edc5b6e8a`
- LIVE-GRENZE: AF-066 noch offen; 6.72.19 hier nicht als WordPress-LIVE-PASS hochstufen
- ARTEFAKT_SYNC: PASS

## PPA-002 – Pferde Atelier Design

- HERKUNFT: EIGENENTWICKLUNG / PFERDE-PROJEKTLINIE
- KLASSE: PFERDE-SPEZIFISCH; allgemeiner Designkern separat MOD-003
- FACHBÜRO: `../DESIGN/`
- AUTORITATIVE QUELLE: Branch `fix/category-intro-targeted-79-v150472-20260831` + dortige Design-Baseline/Live-Belege
- AKTUELL BELEGTER LIVE-STAND: 1.50.472 / Contract V104
- FINALER INSTALLERNAME: `PFERDE_ATELIER_DESIGN_V1.50.472_CONTRACT_V104_KATEGORIETEXTE_79_NUR_FAILS_FINAL_INSTALLIEREN.zip`
- INSTALLER SHA-256: `ae59699c2de750e5ebda14096109e60ddfdac55f32e9ffe848305e4dc2e035b9`
- ARTEFAKT_SYNC: BLOCKED – Installername/Hash sind belegt, die Binärdatei ist aktuell nicht direkt erreichbar

## PPA-003 – Bildzentrale

- HERKUNFT: EIGENENTWICKLUNG
- KLASSE: ALLGEMEINGÜLTIGER Kern MOD-002; Pferde-Anwendung separat
- FACHBÜRO: `../BILD/`
- AUTORITATIVE ALLGEMEINE HAUPTQUELLE: `../../../ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/`
- AKTUELL BELEGTER PFERDE-/PLUGINSTAND: 2.6.9
- INSTALLER: `ALLGEMEINE_BILDZENTRALE_2.6.9_PROMPTGRENZE_REPARIERT.zip`
- SHA-256: `748f77602bc3d4f64bd24a2f163c53829f0c1e8dc2102a82a642ceb4778e160e`
- ARTEFAKT_SYNC: PASS

## PPA-004 – Universal Research & Fill

- HERKUNFT: EIGENENTWICKLUNG
- KLASSE: ALLGEMEINGÜLTIG MOD-005; Pferde-Konfiguration separat
- FACHBÜRO: `../HIVEPRESS/`
- AUTORITATIVE ALLGEMEINE HAUPTQUELLE: `../../../ALLGEMEINGUELTIGE_BAUSTEINE/UNIVERSAL_RESEARCH_FILL/`
- AKTUELL BELEGTER STAND: 1.9.9
- INSTALLER: `universal-research-fill-v1.9.9.zip`
- SHA-256: `154102215a0ef4bf7de3362dbf835f05dc5c10b870e3507dbf173c62fb7079e0`
- ARTEFAKT_SYNC: PASS

## PPA-005 – Portal SEO Topic Engine (PSTE)

- HERKUNFT: EIGENENTWICKLUNG
- KLASSE: PFERDE-TEXT/SEO-Bestand; Allgemeingültigkeit nicht aus diesem Register ableiten
- FACHBÜRO: `../TEXT/`
- AUTORITATIVE TECHNISCHE QUELLE: aktueller STARTMASTER0107-/TEXT-Weg, nicht dieses Register
- AKTUELL BELEGTER INSTALLERSTAND: 0.56.25
- INSTALLER: `portal-seo-topic-engine_0.56.25_ATTRIBUTE_RICH_COMPILER_READY_BREADTH_ROOTFIX_VERIFIED.zip`
- SHA-256: `8122e3fa2273fe4d8e53476f557ed0ddd99a197e8b1c40302f35db245ebb0f95`
- ARTEFAKT_SYNC: PASS

## PPA-006 – Portal SEO Editorial Plan Compiler

- HERKUNFT: EIGENENTWICKLUNG
- KLASSE: PFERDE-TEXT/SEO-Bestand
- FACHBÜRO: `../TEXT/`
- AUTORITATIVE TECHNISCHE QUELLE: aktueller STARTMASTER0107-/TEXT-Weg
- STATUS DER VERSIONSBINDUNG: BLOCKED
- BEFUND: Campus-Technologieindex führt 0.28.16; historische spätere Übergaben belegen 0.28.17. Historische Übergaben sind keine CURRENT-Autorität.
- PHYSISCHE REFERENZ: `/Campus-Plugins/PFERDE_ATELIER/PPA-006/REFERENCE_0.28.16.zip`
- REGEL: keine `CURRENT.zip`, bis die aktuelle technische TEXT-/Releasequelle die tatsächlich gültige Installer-Version eindeutig bindet.
- ARTEFAKT_SYNC: BLOCKED

## PPA-007 – Pferde Atelier HivePress Anzeigensuche

- HERKUNFT: EIGENENTWICKLUNG / genauer Modulstatus noch ungeklärt
- KLASSE: MOD-004 UNGEKLÄRT
- FACHBÜRO: `../HIVEPRESS/`
- AKTUELL BELEGTER STAND: v2.1.5
- PFERDE-ARTEFAKT: `PFERDE_ATELIER_HIVEPRESS_ANZEIGENSUCHE_v2.1.5_AJAX_ANZEIGENKATEGORIEN_INSTALLIEREN.zip`
- SHA-256: `5879bb257026ec72fa83fc817994a4764009a7c1fde75a13fcec129eae45d0c3`
- KONTINUITÄT: Pferde-Design V1.50.472 `MASTER_STATUS.md` belegt Search-Plugin-Quelle byte-identisch PASS
- ARTEFAKT_SYNC: PASS

## PPA-008 – Universal Product Comparison

- HERKUNFT: EIGENENTWICKLUNG
- KLASSE: MOD-006 UNGEKLÄRT / erste Anwendung Pferde-Atelier
- FACHBÜRO: `../PRODUKTVERGLEICH/`
- AKTUELLER PRÜFGEGENSTAND: `Universal Product Comparison 0.8.0-prototype`
- ZIP: `universal-product-comparison-0.8.0-prototype.zip`
- SHA-256: `c9eec5b4c7faafa23af6bd5c554d85c2c4d1763e4c618fbd49c3e04dd45abb66`
- WICHTIG: älterer Technikbranch enthält ausdrücklich nicht den vollständigen 0.8.0-Quellstand; die hashgebundene ZIP ist derzeit der Prüfgegenstand
- ARTEFAKT_SYNC: BLOCKED – exakt diese aktuelle ZIP ist aktuell nicht erreichbar; keine Rekonstruktion aus dem älteren Technikbranch

## PPA-009 – Universal Product Knowledge

- HERKUNFT: EIGENENTWICKLUNG
- KLASSE: MOD-007 UNGEKLÄRT / erste Anwendung Pferde-Atelier
- FACHBÜRO: `../PRODUKTVERGLEICH/`
- AKTUELL BELEGTE ABHÄNGIGKEIT IM 0.8.0-GESAMTTEST: 0.5.0
- AUTORITATIVE QUELLE: Produktwissen-Vertrag + aktueller technischer Product-Knowledge-Stand; vor Artefaktsync frisch auf exakte ZIP/Hashbindung prüfen
- ARTEFAKT_SYNC: BLOCKED – exakte aktuelle Installer-ZIP + Hash noch nicht aus einer CURRENT-Autorität in dieses Büro gebunden

## PPA-010 – Affiliate-Portal Kategorie-Workflow

- HERKUNFT: EIGENENTWICKLUNG
- KLASSE: ALLGEMEINGÜLTIG MOD-001
- AUTORITATIVE HAUPTQUELLE: `../../../ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/`
- AKTUELL BELEGTER STAND: 1.8.0
- INSTALLER SHA-256: `4c98847e96b091955436230b721a39b5049132037546367a810d4ed642f40845`
- PFERDE-NUTZUNG: in diesem Erstinventar nicht separat als aktuelle Projektanwendung bewiesen
- ARTEFAKT_SYNC: NICHT_ERFORDERLICH, solange keine aktive Pferde-Projektanwendung frisch belegt ist; allgemeiner Hauptstand bleibt MOD-001

## PPA-011 – Pferde Atelier – Pferderassen Manager

- HERKUNFT: EIGENENTWICKLUNG
- KLASSE: PFERDE-ATELIER / WISSENSDATENBANK / PFERDERASSEN
- FACHBÜRO: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/`
- AUTORITATIVE TECHNISCHE QUELLE: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/TECHNIK_PFERDERASSEN_MANAGER_CURRENT.md`
- LETZTER BELEGTER GRUNDSTAND VOR RELATIONSUMBAU: 0.2.1
- AKTUELLER LOKAL HART GEPRÜFTER KANDIDAT: 0.2.7
- KANDIDATENARTEFAKT: `PFERDE_ATELIER_PFERDERASSEN_MANAGER_0.2.7_INSTALLIEREN.zip`
- SHA-256: `5f72308cb922756cac8ffa2a01a27bfc7f1f1cfbabf6fbf5b4a33728fc8e58f1`
- WORDPRESS-LIVE: OFFEN; keine Aussage aus diesem Register ableiten, welche Version aktuell auf dem Server installiert ist
- UPDATEVORGANG: `PU-20260915-001`
- ARTEFAKT_SYNC: BLOCKED – vorgeschriebener WordPress-LIVE-/Backfill-/Overlap-Test fehlt; deshalb keine isolierte `CURRENT.zip` / kein `MANIFEST.md`

## Harte Regel für neue Einträge

Neue Plugins niemals nur aus Dateinamen ableiten. Erst echte Pluginidentität + aktuelle autoritative Quelle + Versions-/Hashbeleg.

Wenn ein Chat ein Plugin real ändert, muss er genau den betroffenen Eintrag aktualisieren und nach `SYNC_VERTRAG.md` das isolierte Artefakt synchronisieren oder BLOCKED melden.
