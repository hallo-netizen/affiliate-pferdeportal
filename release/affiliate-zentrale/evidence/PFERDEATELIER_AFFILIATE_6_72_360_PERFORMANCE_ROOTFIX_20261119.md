# Pferdeatelier – Affiliate 6.72.360 – FREIGABE WIDERRUFEN

Stand: 2026-11-19

**6.72.360 darf nicht installiert werden.**

Die nachträgliche Vollprüfung hat bewiesen, dass die erste Cross-Slot-Wiederverwendung nicht alle zustandsabhängigen Eingaben abbildete. Reproduzierte Abweichungen zwischen `category_product_1..3`:
- wechselnde idealo-Linkstrategie;
- wechselnde Otto/Awin-Freigabe;
- wechselnde GTIN-/Produktidentität;
- wechselnde eBay-Seller-Metadaten.

Damit war die frühere lokale Semantikprüfung für 6.72.360 nicht vollständig genug. Die frühere Freigabeaussage ist hiermit ausdrücklich widerrufen.

Ersatz: **6.72.361**, die diese Zustände in der Cache-Identität abbildet bzw. bei dynamischen WordPress-Erweiterungspunkten auf das exakte 6.72.359-Slotverhalten zurückfällt.

Der formale `release/affiliate-zentrale/current`-Stand wird durch diese Korrektur nicht automatisch geändert.
