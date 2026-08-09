## Affiliate-Zentrale V6.4.0 – Atomic Last-Known-Good Recovery

V6.4.0 stellt den zuletzt funktionierenden öffentlichen eBay-Auslieferungsvertrag wieder her und härtet die nach V6.0–V6.3 aufgetretenen Regressionen als zusammenhängenden Workflow. Es wird kein zusätzliches Plugin eingeführt; der Pluginpfad bleibt `affiliate-portal-router/`.

### Verbindliche Workflow-Invarianten

- PRIVATE = eBay-Privatanzeigen in HivePress. BUSINESS = eBay-Produkte in Content-Produktslots. Beide Pipelines bleiben getrennt.
- Frontend-HivePress-AJAX gilt als öffentliche Anfrage. `admin-ajax.php` darf PRIVATE-Policy, Nachfülllogik und Sichtbarkeitsregeln nicht über `is_admin()` umgehen.
- `Private Anzeigen` wird erst nach aktueller zentraler Policy gefiltert und danach auf maximal 9 gültige Teaser begrenzt; Unterkategorien erben diesen Parent-Deckel nicht.
- Die zentrale eBay-Content-Policy wird am finalen öffentlichen Rand erneut ausgewertet; Spielzeug bleibt auch bei alten gespeicherten `allowed`-Zuständen gesperrt.
- BUSINESS verwendet nur den verifizierten eBay-Produktvertrag. Fachlich unklare Neuware fällt auf Review und nicht auf ein ähnliches Nachbarprodukt.
- Ein bereits veröffentlichtes BUSINESS-Produkt ist Last-Known-Good. Soft-Review, Vertragsmigration, Refresh-Fälligkeit oder ein fehlgeschlagener Ersatz dürfen es nicht vor erfolgreichem Ersatz aus dem Content entfernen.
- Harte Endsignale, zentrale Policy/Veto und abgelaufenes eBay-Enddatum bleiben sofort fail-closed.
- Ein bestehendes Ausgabeobjekt wird bei Titel-/Preis-/Bild-/Linkänderung nicht vorab deaktiviert. Supersede erfolgt erst nach erfolgreicher Materialisierung des Ersatzes.
- Eine BUSINESS-Quelle wird erst `route_state=ready`, wenn mindestens eine aktive Produktkampagne tatsächlich materialisiert wurde.
- `Bestand jetzt abgleichen` ist der deterministische Reparatur-/Reconcile-Pfad: lokaler Policy-/Klassifikationsabgleich einschließlich BUSINESS-Ausgabereparatur, Assetphase und danach nur fälliger Source-Refresh. Discovery wird dadurch nicht gestartet.
- Der manuelle Bestandsabgleich kann auch bereits versionsaktuelle BUSINESS-Zeilen erneut durch den Delivery-Pfad führen, damit ein durch frühere Versionen beschädigter Ausgabezustand repariert wird.
- `fresh_until` ist Refresh-Fälligkeit, kein Sichtbarkeits-/Löschsignal.
- BUSINESS-Diagnose bleibt read-only.
- Pluginpfad bleibt exakt `affiliate-portal-router/`.

### Installation / erster Lauf

Nach Update genau einmal:
Affiliate-Zentrale → eBay → „Bestand jetzt abgleichen“.

Bis dieser Reconcile-Lauf abgeschlossen ist keinen vollständigen Discovery-Abruf starten.

Stable tag: 6.4.0
