# WORDPRESS-REGISTER

STAND: 2026-09-12
STATUS: CAMPUSWEITER TECHNOLOGIE-INDEX

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Die zentrale Übersicht: Welche WordPress-Plugins/Installer haben wir bereits als Datei erhalten oder eindeutig im Projekt belegt?

**HIER BIST DU RICHTIG, WENN …**  
du wissen willst, ob ein WordPress-Plugin schon vorhanden ist und wo seine Hauptquelle liegt.

**DU DARFST …**  
Plugin-Artefakte finden, Versionen/Dateibelege sehen und zur autoritativen Fach-/Modulquelle weitergehen.

**DU DARFST NICHT …**  
hier einen Live-/Release-Stand erfinden, ein Plugin als allgemeingültig klassifizieren oder eine zweite Plugin-Wahrheit pflegen.

**ALS NÄCHSTES …**  
bei Allgemeingültigkeit → MODULREGISTER; bei Projektstatus → zuständiges Fachbüro; bei Installation/Release → autoritative technische Quelle.

## Harte Trennung

Dieses Register ist NUR ein WordPress-Technologieindex.

Es entscheidet NICHT:
- ob ein Modul allgemeingültig ist → `ALLGEMEINGUELTIGE_BAUSTEINE/MODULREGISTER.md`;
- welcher Projektstand LIVE/RELEASE ist → zuständiges Fachbüro / technische Originalquelle;
- ob ein großes Masterpaket ein Plugin enthält → erst nach Inhaltsprüfung.

## Nachweisbar bereits übergebene Plugin-/Installer-Artefakte

### WP-001 – Bildzentrale

MOD-ID:
MOD-002

Aktuellster allgemeiner Plugin-Dateibeleg:
`ALLGEMEINE_BILDZENTRALE_2.6.9_PROMPTGRENZE_REPARIERT.zip`

Version:
**2.6.9**

SHA-256:
`748f77602bc3d4f64bd24a2f163c53829f0c1e8dc2102a82a642ceb4778e160e`

Nullpunkt:
`NULLPUNKT_BILDSYSTEM_NEU_069_PROMPTGRENZE_REPARIERT.zip`

Nullpunkt SHA-256:
`4258ae194e681dcae2fa37467d1a430d48ef2ae7e2889e2f02939456bbb1d434`

Byte-Abgleich:
separater 2.6.9-Installer = im Nullpunkt eingebetteter 2.6.9-Installer.

Pferde-Atelier:
- WordPress-Live-Version 2.6.9 laut bestehender Nutzerbestätigung
- historische Pferde-Dateien: Plugin 2.4.9 + Master 049
- Projekt-Konfig/Migrationsakten separat erhalten

GitHub:
auf aktuellem `main` kein separater Bildzentrale-Dateistand unter diesen Namen gefunden.

Hauptquellen:
- `ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/`
- `PROJEKTE/PFERDE_ATELIER/BILD/`

### WP-002 – Universal Research & Fill

MOD-ID:
MOD-005

Aktuellster direkt belegter Installer:
`universal-research-fill-v1.9.9.zip`

Dateibeleg:
**1.9.9**

SHA-256:
`154102215a0ef4bf7de3362dbf835f05dc5c10b870e3507dbf173c62fb7079e0`

Master:
`UNIVERSAL_RESEARCH_FILL_MASTER_V1.9.9.zip`

Master SHA-256:
`452fe76c60f770fa95b9e10bcfa50e23f37efe8051a6c194700b7237d502dcbd`

Byte-Abgleich:
externer 1.9.9-Plugin-ZIP = eingebetteter CURRENT_PLUGIN-ZIP im Master.

Historisch:
1.9.5 Plugin + Master.

Modulklasse:
ALLGEMEINGÜLTIG.

Hauptquelle:
`ALLGEMEINGUELTIGE_BAUSTEINE/UNIVERSAL_RESEARCH_FILL/`

Pferde-Anwendung:
`PROJEKTE/PFERDE_ATELIER/HIVEPRESS/`

GitHub:
auf aktuellem `main` kein eigener URF-Dateistand unter diesem Namen gefunden.

### WP-003 – Portal SEO Topic Engine

MOD-ID:
noch nicht vergeben

Aktuellster direkt belegter Installer:
`portal-seo-topic-engine_0.56.25_ATTRIBUTE_RICH_COMPILER_READY_BREADTH_ROOTFIX_VERIFIED.zip`

Dateibeleg:
0.56.25

SHA-256:
`8122e3fa2273fe4d8e53476f557ed0ddd99a197e8b1c40302f35db245ebb0f95`

Quelle:
aktueller STARTMASTER0107-Master / `02_CURRENT_INSTALLERS/`

Archiv:
`/Campus-Archiv/PROJEKTE/PFERDE_ATELIER/SEO/2026-09-05/`

Ältere Installerstände bleiben historisch erhalten.

Modulklasse:
UNGEKLÄRT.

### WP-004 – Portal SEO Editorial Plan Compiler

MOD-ID:
noch nicht vergeben

Aktuellster direkt belegter Installer:
`portal-seo-editorial-plan-compiler_0.28.16_PRODUCTION_PACKAGE_UPLOAD_VISIBILITY.zip`

Dateibeleg:
0.28.16

SHA-256:
`3341805f277dfd77c985e6cfbbc2b57e4e0677bef8c59d8c2067f7f0b79be9bc`

Quelle:
aktueller STARTMASTER0107-Master / `02_CURRENT_INSTALLERS/`

Archiv:
`/Campus-Archiv/PROJEKTE/PFERDE_ATELIER/SEO/2026-09-05/`

Ältere Installerstände bleiben historisch erhalten.

Modulklasse:
UNGEKLÄRT.

### WP-005 – Affiliate-Zentrale

PB-ONE-Plugin-ID:
`PBO-PLUGIN-001`

Pluginname:
`Affiliate-Zentrale (Portal-kompatibel)`

Technische Hauptquelle:
- Branch `affiliate-release-current`
- `release/affiliate-zentrale/current/affiliate-portal-router/`
- zuständiges Fachbüro `PROJEKTE/PFERDE_ATELIER/AFFILIATE/`

Kanonischer technischer Kandidat:
**6.72.19**

Kanonisches 26-Dateien-Manifest:
`694af9869c7aa2b01a51f164173b1c51d9be7c24912c2e129420c3d111346a4b`

Kanonischer Testartefakt-Nachweis:
- Run `34692865477` / Job `103551115066` PASS
- Test-ZIP SHA-256 `72f437e5235aaec53631db052e2184b588366c7f8aa7eb72ae1c9e043cdf157f`

Wichtig:
**6.72.19 ist hier kein behaupteter WordPress-LIVE-PASS.**
Die in diesem Chat zuletzt frisch belegte technische Source-/Artefaktversion ist 6.72.19; der reale WordPress-/ADCELL-Live-Preflight AF-066 ist im zuständigen Affiliate-Fachbüro weiterhin offen.

Ältere Live-/Installationsbelege bleiben historische Evidenz an der technischen Fachquelle und werden hier nicht als aktuelle WordPress-Live-Wahrheit hochgestuft.

Plugin-Kontrollvorgang:
`PB_ONE/AKTENSCHRANK/PLUGINS/UPDATEPROTOKOLL.md` → `PU-20260912-001`.

Allgemeiner Gesamtmaster:
`ALLGEMEINGUELTIGE_BAUSTEINE/AFFILIATE/MASTERDATEIEN_INVENTAR.md`

Modulklasse:
UNGEKLÄRT.

### WP-006 – Universal Portal Design Suite / Pferde-Designlinie

MOD-ID:
MOD-003

ALLGEMEINER HAUPTKERN:
**Universal Portal Design Suite 2.2.40 / Contract V104**

Plugin SHA-256:
`fbaf1e36fc814b88b952924b9cf2e71a14913864c226eeed46ed8cf03af8e765`

Master SHA-256:
`5d8ef907b671ea96ae02605466bccbad41c012cbd7b3aed9436f7725a02238d7`

PFERDE-PROJEKTLINIE:
- übergebene Vollbasis: 1.50.469 / V104
- aktueller GitHub/LIVE-Stand: **1.50.472 / V104**
- Live-Branch: `fix/category-intro-targeted-79-v150472-20260831`
- `main` enthält noch 1.50.421 und ist dafür nicht Live-Release-Autorität

Hauptquellen:
- `ALLGEMEINGUELTIGE_BAUSTEINE/DESIGN/`
- `PROJEKTE/PFERDE_ATELIER/DESIGN/`

### WP-007 – Kategoriemodell / Affiliate-Portal Kategorie-Workflow

MOD-ID:
MOD-001

WordPress-Plugin:
`Affiliate-Portal Kategorie-Workflow`

Aktuell belegte Version:
**1.8.0**

Installer SHA-256:
`4c98847e96b091955436230b721a39b5049132037546367a810d4ed642f40845`

Source SHA-256:
`1d17566f309f460e48255b78357912cf5e18b1eba2eed7654516e79c8f9fa7fd`

Master SHA-256:
`2e6990847c5bc32176f87c6f4b006ccdd0f3f57891c176ed5a6874edfdff942c`

Modulklasse:
ALLGEMEINGÜLTIG.

Hauptquelle:
`ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/`

Status:
lokal/fresh stark geprüft; **kein bestätigter Live-WordPress-Deployment-PASS**.

## Aufnahme neuer Plugins

Bei jedem neuen Plugin-/Masterdatei-Eingang:

1. Datei vollständig inventarisieren;
2. prüfen, ob tatsächlich WordPress-Plugin/Installer;
3. hier Dateibeleg ergänzen;
4. Modulklasse nur im MODULREGISTER pflegen;
5. Projekt-/Live-/Release-Status nur an der Fachquelle pflegen.

## Grundsatz

**Ein Plugin kann in mehreren Projekten genutzt werden, aber es hat nur eine Hauptwahrheit.  
Dieses Register zeigt nur den Weg dorthin.**

### WP-008 – HivePress-Anzeigensuche

MOD-ID:
MOD-004

STATUS:
UNGEKLÄRT / separater Audit ausstehend.

In Designmastern nachweisbar:
- Universal HivePress Anzeigensuche v2.1.5
- Pferde Atelier HivePress Anzeigensuche v2.1.5

Regel:
nicht als bloße Design-Datei verschwinden lassen; eigener Modulstatus folgt nach separater Prüfung.
