# FEHLERKATALOG V6.53.0

## E-653-001 – Artikel-Produktkarten erben generische Bannerstruktur

**Live-Symptom:** Produktvorschläge unter Einzelbeiträgen wirken wie große Banner: zu dominante Bilder, unterstrichene Titel/Beschreibungen/Metadaten und nicht portalstandardkonforme Kartenwirkung.

**Ursache:** Beide Artikel-Produktpfade rufen `render_banner()` auf. Das erzeugt `.ppar-banner-*`-Markup. Globale Bannerregeln wirken deshalb innerhalb der Produktkarten weiter; die `.ppar-article-product-*`-CSS ist nur ein Override auf eine fremde Grundstruktur.

**Unzulässige Symptombehandlung:** weitere `!important`-Overrides auf `.ppar-banner-*`, bildspezifische Einzelregeln, Sonderfall für einzelne Produkte oder Beiträge.

**Rootfix:** eigener Produktkarten-Renderer und vollständig eigene `.ppar-article-product-*`-Markup-/CSS-Grenze. Beide Renderpfade verwenden denselben Produktkartenvertrag.

**Scope:** ausschließlich Affiliate-Zentrale. Designplugin unverändert.

**Regression-Schutz:** V6.52 muss am neuen Architekturvertrag mit exakt dokumentiertem RED scheitern; V6.53 muss Architektur/Markup, historische Successor-Tests, Real-WordPress/MariaDB, Fresh-Unpack und Parität bestehen.
