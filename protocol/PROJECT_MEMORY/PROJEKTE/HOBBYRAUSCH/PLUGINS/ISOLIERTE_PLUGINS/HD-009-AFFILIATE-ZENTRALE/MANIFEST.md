# Hobby Depot HD009 – aktuelle Affiliate-Zentrale

**07.11.2026 – Version 0.1.23**

- Einziges Current: `CURRENT.zip` = `HOBBY_DEPOT_AFFILIATE_HD009_0.1.23.zip` (byteidentisch)
- 1.067.588 Bytes; SHA-256 `9e533d1f47b03c41078baf9260887e4945591244c75fd386a759ab1f9fb11ff1`
- Bestehendes Pluginroot `affiliate-portal-router/`; nur zwei Layout-/Versions-Anpassungen: Querbanner von 3:1 auf **4,2:1** (deutlich flacher) und Browsercache auf 0.1.23, WordPress-Header-Version auf 0.1.23. Quadratbanner und Platz-/Providerlogik bleiben unverändert.
- Quellversion 0.1.22 exakt auf Hash geprüft; ZIP 33/33 CRC PASS, PHP 24/24 PASS, Browser-Test Desktop 1440/960 und Mobil 390/360 auf echten Hobby-Depot-Seiten PASS.
- **Bekannte, nachweislich noch offene Ausspiellücke:** Bei fehlendem genehmigtem Foto entsteht derzeit kein Amazon-Fallback-Banner (z.B. `/hobbyregister/muenzen/`). Normale `post`-Artikel werden von der vorhandenen Auto-Template-Belegung nicht erfasst (s. tatsächliche 4 Kettenhemd-Beiträge). Bitte keine vollständige Abdeckung behaupten. Vorschlag in `../../../../AFFILIATE/BANNER_ZIELREGELN_20261107.md`.
- Auf Website noch nicht live installiert/abgenommen.
