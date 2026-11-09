# ROBOTIK – Footer-Umzug Release-Protokoll
Stand 09.11.2026. **Dieses Protokoll und die ZIP bei jeder neuen Version gemeinsam aktualisieren.**

| Version | Wo | Inhalt/Änderung | Prüfung | Nutzerinstallation |
|---|---|---|---|---|
| 1.1.1 (Original) | Nur **Hobbydepot** `TOOL-FOOTER-UMZUG/CURRENT.zip` | Footer-Seiten+Menüs+Widgets, alte Pferde↔Hobby-Textersetzungen, kann vorhandene Seiten ändern | PHP aus Original-ZIP binär geprüft | **Nicht für Robotik freigegeben** |
| **1.2.1 Robotik TEST** | **`CURRENT.zip` = `VERSIONEN/1.2.1.zip`** | Seiten samt Inhalt+Menüs; **KEIN Design/WIDGET**, echte 1.1.1-JSON-Importkompatibilität, Vorschau, ausdrückliche Freigabe, neue Seiten immer Entwurf, vorhandene Seiten/Menüs geschützt | **Datei 6.395 Byte, SHA256 `125bb9f4889e6bf8d23e6b2ffee00fae6322a378fd37348e4ede20ef2d28c428`, Git-Blob `6158877b77b5444b3f0ce31bd9ac6fdfc3ed2f88`; ZIP-CRC PASS, PHP-Lint PASS, künstlicher Legacy-JSON Test 2 Seiten/1 Footer-Menü PASS, negatives Format PASS** | **Noch nicht gemeldet, Live-Test offen** |

## Übernahme ins nächste Chatfenster
- Robotik-Kategorieplugin **0.3.0** bleibt anderes Plugin, unverändert.
- Footer-Umzug auf der Quellseite **1.1.1 belassen**; nur auf Robotik **1.2.1 Test** installieren, wenn Footer-Seiten übertragen werden sollen.
- Erst einen JSON-Export der Quellseite erstellen (keine einzelnen Seitendateien), in Robotik 1.2.1 importieren **nach Vorschau**. Rechtstexte nur als Entwürfe.
- Nach WordPress-Live-Test Ergebnis und Risiken hier ergänzen. Bei neuer ZIP `VERSIONEN/` + `CURRENT.zip` + dieses Protokoll + `KATEGORIE/CURRENT_STATE.md` gemeinsam aktualisieren.
