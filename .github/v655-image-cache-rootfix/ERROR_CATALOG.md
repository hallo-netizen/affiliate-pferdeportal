# FEHLERKATALOG – Produktbild Cache-Rootfix ONLY

## IMG-655-002 – geänderte Bild-CSS kommt live nicht zuverlässig an

**Symptom:** Trotz installiertem Installer mit fester 150×150-Produktbildregel zeigt das reale Frontend weiterhin die vorherige Bildgeometrie. Im Screenshot vom 23.08.2026 22:13 ist insbesondere ein Hochformatbild weiterhin hochformatig statt quadratisch gefüllt.

**Live-Gegenbeweis:** Der zuvor automatisch grüne CSS-Vertrag reicht nicht für Live-PASS; er bewies nur, dass die Regel im ZIP vorhanden war.

**Verifizierte Ursache:** `frontend.css` wird im produktiven Plugin mit `self::VERSION` als Asset-Version enqueued. Da die Plugin-Version 6.55.0 bei den CSS-only Versuchen unverändert blieb, blieb die Cache-Kennung gleich. Eine alte CSS-Datei kann deshalb nach Installation weiter ausgeliefert werden.

**Rootfix:** CSS-Regel beibehalten und zusätzlich ausschließlich den CSS-Enqueue cache-sicher machen: Version = `self::VERSION` + SHA-256-Kurzfingerabdruck der realen `frontend.css`. Dadurch ändert sich die Asset-URL bei jeder CSS-Inhaltsänderung deterministisch.

**Scope:** Produktionsdelta exakt zwei Dateien: `assets/frontend.css` und `pferdeportal-affiliate-router.php`. Im PHP ausschließlich der CSS-Enqueue; JS, eBay, Scheduler, Provider, Auswahl und sonstige Renderer unverändert. Designplugin unverändert.

**Negativschutz:** Release blockiert bei zusätzlicher Produktionsdatei, Position-1-Sonderregel, Banner-Scope, unverändertem statischen CSS-Cache-Key, verändertem JS-Enqueue oder fehlendem Real-WordPress-Nachweis der tatsächlichen CSS-Version.
