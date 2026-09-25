# FEHLERKATALOG V6.53.0

## E-653-001 – Artikel-Produktkarten erben generische Bannerstruktur

**Live-Symptom:** Produktvorschläge unter Einzelbeiträgen wirken wie große Banner: zu dominante Bilder, unterstrichene Titel/Beschreibungen/Metadaten und nicht portalstandardkonforme Kartenwirkung.

**Ursache:** Beide Artikel-Produktpfade rufen `render_banner()` auf. Das erzeugt `.ppar-banner-*`-Markup. Globale Bannerregeln wirken deshalb innerhalb der Produktkarten weiter; die `.ppar-article-product-*`-CSS ist nur ein Override auf eine fremde Grundstruktur.

**Unzulässige Symptombehandlung:** weitere `!important`-Overrides auf `.ppar-banner-*`, bildspezifische Einzelregeln, Sonderfall für einzelne Produkte oder Beiträge.

**Rootfix:** eigener Produktkarten-Renderer und vollständig eigene `.ppar-article-product-*`-Markup-/CSS-Grenze. Beide Renderpfade verwenden denselben Produktkartenvertrag.

**Scope:** ausschließlich Affiliate-Zentrale. Designplugin unverändert.

**Regression-Schutz:** V6.52 muss am neuen Architekturvertrag mit exakt dokumentiertem RED scheitern; V6.53 muss Architektur/Markup, historische Successor-Tests, Real-WordPress/MariaDB, Fresh-Unpack und Parität bestehen.

## E-653-002 – Release-Gate bindet historischen Vorgänger an Neuerzeugung statt an verifiziertes Artefakt

**Symptom:** Der V6.53-Gesamtlauf lief zunächst den vollständigen V6.52-Vorgängerworkflow erneut durch und verglich danach den dabei neu erzeugten ZIP-Container mit dem historischen V6.52-Release-SHA. Der Lauf endete deshalb BLOCKED mit Installer-SHA-Mismatch und veröffentlichte korrekt kein V6.53-Release.

**Ursache:** Die Prüfinfrastruktur vermischte zwei unterschiedliche Belege: (1) die bytegenaue Bindung an den bereits freigegebenen V6.52-Ausgangsstand und (2) eine erneute Ausführung von Vorgängertests. Für die MASTER-Bindung ist ausschließlich das unveränderliche verifizierte Release-Artefakt maßgeblich. Eine Neuerzeugung des ZIP-Containers ist kein Ersatz für diese Bindung.

**Rootfix der Prüfinfrastruktur:** Runner v4 lädt das originale GitHub-Actions-Artefakt V6.52 `9489291638`, prüft Artifact-SHA, Installer-SHA, MASTER-SHA und das originale automatische `FINAL_RELEASE_GATE=PASS` sowie den ausdrücklich offenen externen eBay-Livepunkt. Erst aus dieser bytegenau verifizierten MASTER wird V6.53 abgeleitet. Anschließend werden die vollständigen V6.53-Successor-/Real-WordPress-/Fresh-Unpack-/Paritätsprüfungen ausgeführt.

**Produktionsscope:** 0 zusätzliche Produktionsdateien. Die Korrektur betrifft ausschließlich CI/Release-Prüfinfrastruktur und Dokumentation.

**Schutzregel:** Ein historisch freigegebener MASTER-Ausgangspunkt wird künftig über sein unveränderliches Release-Artefakt und seine dokumentierten Hashes gebunden. Ein neu gebauter Container darf diesen Beleg nicht ersetzen.

## E-653-003 – Generierter Release-Runner wurde auf falschen Pfad geschrieben

**Symptom:** Lauf 9 stoppte sofort mit `bash: /tmp/run-v653-full-release-v4-generated.sh: No such file or directory` und erzeugte kein Release-Artefakt.

**Ursache:** Der Python-Generator des v4-Prüfrunners las den Basisscript-Pfad korrekt ein, schrieb die transformierte Fassung aber versehentlich wieder auf den Quellpfad statt auf den übergebenen temporären Zielpfad.

**Rootfix der Prüfinfrastruktur:** Quell- und Zielpfad sind jetzt explizit getrennt (`src`/`dst`). Zusätzlich prüft `test -f` fail-closed, dass der generierte Runner existiert, bevor Syntaxprüfung oder Ausführung beginnen.

**Produktionsscope:** 0 Produktionsdateien. Kein Installer, keine MASTER und kein Plugin-Code wurden durch diesen Infrastrukturfehler verändert.
