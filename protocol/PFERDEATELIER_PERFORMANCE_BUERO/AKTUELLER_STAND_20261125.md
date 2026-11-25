# Pferdeatelier Performance – aktueller Stand am 25.11.2026

**Arbeitszweck:** Fortschritt protokollieren, keine Änderung am Live-Plugin.

## Wo stehen wir?
- Aktuelle LIVE-Version der Affiliate-Zentrale: **6.72.379** (bestehender GitHub-Livenachweis und passiver Messlauf vom 25.11.2026).
- Nutzer berichtet am 25.11.2026: **„bis jetzt gibt es noch keine Probleme“**.
- Das ist eine positive Betriebsbeobachtung, noch keine belegte Langzeitstabilität und keine neue Messung.
- Keine Plugin-, WordPress-, K0- oder Funktionsänderung in diesem Protokollschritt.

## Geschwindigkeit und Funktionsschutz – vorhandene Belege
- Letzte gespeicherte PASSIV-Gesamtmessung: `pferdeatelier-performance-gesamtanalyse-20261125-091933.json`.
- Pferdesättel 6.72.379: Wall 2.435,59 ms, CPU 1.127,46 ms, 316 Queries.
- Verglichen mit einzelnem 6.72.378-Lauf: Wall +9,61 %, CPU +3,21 %, sechs Queries mehr. **Kein Live-Speedup aus diesem Lauf bewiesen.**
- Keine kausale Verschlechterung durch die beiden Änderungen von 6.72.379 bewiesen.
- Vorhandene lokale Vergleichstests im Prüfnachweis 6.72.379: 2.721/2.721 Kampagnennormalisierungen, 25/25 Seiten-/Providerkombinationen und 75/75 Produktkarten inklusive HTML identisch.
- Diese Zahlen sind historisch belegte Tests, **nicht** neue Livetests vom Zeitpunkt dieser Rückmeldung.

## Plugin-Archiv
- Dateiname: `PFERDEATELIER_AFFILIATE_6.72.379_GEBUENDELT_EXACT_TARGET_ROOTFIX.zip`.
- SHA-256: `264b872aae3238027b38304282ddc6fcca868cb8a0b46629ad85f67b813ecc67`.
- Das vorhandene ZIP aus der Pferdeatelier-Bibliothek wurde erneut eingelesen: 66 Dateien, 23 PHP-Dateien, ZIP-Integritätsprüfung PASS und SHA-256 gleich Freigabeprotokoll.
- Library-Original: `/pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.379_GEBUENDELT_EXACT_TARGET_ROOTFIX.zip`.
- Zusätzlich Library-Kopie: `/pferdeatelier/PLUGINS/PERFORMANCE/PFERDEATELIER_AFFILIATE_6.72.379_GEBUENDELT_EXACT_TARGET_ROOTFIX.zip`.
- GitHub-Nachweis/Archivverweis: `protocol/PFERDEATELIER_PERFORMANCE_BUERO/ARCHIV_6.72.379_ZIP_VERWEIS.md`.
- **Abgrenzung:** Das ZIP liegt in der Benutzerdateibibliothek, nicht als binäre ZIP-Datei im GitHub-Repository. GitHub enthält das Protokoll und den verifizierten Archivverweis.

## Entscheidung
**6.72.379 unverändert beibehalten.** Kein neues Plugin wegen eines positiven Zwischenstands. Weitere Änderungen nur bei isoliertem kausalem Nachweis und inhaltlichem Funktionsschutz, gesammelt statt einzeln.
