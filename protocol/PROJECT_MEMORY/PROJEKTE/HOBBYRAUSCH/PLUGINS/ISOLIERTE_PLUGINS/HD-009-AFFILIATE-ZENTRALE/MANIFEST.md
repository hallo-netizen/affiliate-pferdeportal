# HD009 – Affiliate-Zentrale Hobby Depot – gültiger Stand

**Version: 0.1.24 (07.11.2026)**

- **Installationsdatei:** `HOBBY_DEPOT_AFFILIATE_HD009_0.1.24.zip`; derselbe geprüfte Inhalt als `CURRENT.zip`.
- 1.068.611 Bytes; SHA-256 `e1bc7cc4d7ab69bc711c424c3d1a612c4710f66155eba7a401552329a800f3a6`; Git-Blob `a803da717395689cfd69698611fdef723f94166c`. WordPress-Pluginroot unverändert `affiliate-portal-router/`.
- **KISS: Ein bestehender Router, ein Rückfallweg.** Der bestehende native Partner-/Kampagnenvorrang ist unverändert. Nur wenn kein passender zulässiger Banner vorhanden ist, rendert das vorhandene HD009 einen thematisch passenden Amazon-Suchbanner am bereits von HD003/HD007 festgelegten Platz.
- Neu: Fallback auch ohne genehmigtes Foto als textlicher Banner im Farbkonzept der Seite (kein erfundenes Motiv). Für Hobbyregister-Einzelprofile: Quadratbanner bewusst als Bild-freier, gestalteter Themenbanner, Querbanner mit vorhandener genehmigter Themenfotografie; dadurch Hero + maximal **ein** bebilderter Affiliate-Banner statt zwei fast identischer Fotos. Bei fehlendem Foto beide als textliche Anzeigen.
- Neu: `pp_affiliate_slot` erkennt `category`-Taxonomiearchive anhand des echten Kategorieobjekts, unabhängig von `get_the_ID()`. Dadurch sind niedrigste Kategorieebenen am **bestehenden** Werbeplatz erreichbar.
- Neu: Für **normale WordPress-Artikel** ohne bereits enthaltene Affiliate-Anzeige wird exakt ein bestehender `post_inline_banner` nach der Einleitung ausgegeben (auch ohne Beitragsbild). Bereits vorhandene Anzeigen und manuelle Shortcodes werden respektiert, kein zweiter Banner darüber.
- Neu: Startseite `start_after_topics` erhält im Rückfall einen allgemeinen, klar als Ausrüstung bezeichneten Suchbanner. Keine neuen oder verlegten Mietwerbeplätze.
- Bestehende Dimensionen: Quadrat 1:1, Querformat **4,2:1**. Alle vorher abgenommenen Verlauf-/Buttonregeln bleiben bestehen.
- **Produktplätze:** Keine erfundenen Einzelprodukte oder Preise. Solche Plätze bleiben bis zu verifizierten ASINs/idealo/eBay-Identitäten leer. DataForSEO, Partnerimporte, AWIN/ADCELL-Zuordnung und die native Bannerpriorität wurden nicht verändert.
- **Tests:** Original 0.1.23 SHA geprüft; 33/33 ZIP-Dateien CRC PASS, 24/24 PHP-Syntax PASS, sechs ausführbare PHP-Fälle mit Originalmethoden PASS (Bild/kein Bild/Kategorieterm/Artikel/Vorrang/Hauptseite). Browser-Simulation mit tatsächlichen Seitenlayouts der Homepage/Kategorien/Beiträge/Register bei 1440/900/390/360 PASS, inklusive nur einem thematischen Werbefoto je Registerprofil. Actions 42394892545 und 42395022776.
- **Grenze:** Das installierte Live-WordPress ist noch 0.1.23. Die neue 0.1.24 wurde lokal/hart geprüft, aber noch nicht produktiv installiert oder live abgenommen. Es wird nicht behauptet, dass alle ca. 485 Sitemapseiten nach dem Update schon live geprüft wurden.
