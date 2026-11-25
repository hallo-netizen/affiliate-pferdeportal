# Aktuelles Performance-Plugin

Stand: 25.11.2026

LIVE:
- Affiliate-Zentrale 6.72.379.

FREIGEGEBENER TESTKANDIDAT:
- Affiliate-Zentrale 6.72.380 – gebündelter Performance-Rootfix
- Paket: PFERDEATELIER_AFFILIATE_6.72.380_GEBUENDELT_PERFORMANCE_ROOTFIX.zip
- SHA-256: 00da8aa7bf6ff560563433abeb643eb0352b72ef5a97c1314a6a40c365223348
- Büro: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.380_GEBUENDELT_PERFORMANCE_ROOTFIX.zip
- Prüfnachweis: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_6.72.380_PRUEFNACHWEIS.md

VERBINDLICHER FREIGABEBEWEIS VOR PLUGIN-AUSGABE:
- finales ZIP neu entpackt und exakt dieser Quellstand geprüft.
- kompletter lokaler Drei-Slot-Seitenpfad, 20 alternierende Alt/Neu-Läufe:
  6.72.379 Median 465,55 ms -> 6.72.380 Median 248,58 ms = -46,61 %.
- fünf zusätzliche komplette Seitenpfade alle schneller: -41,80 %, -46,51 %, -31,04 %, -17,37 %, -11,10 %.
- 2.721/2.721 reale Kampagnennormalisierungen Alt=Neu.
- 25/25 Seiten-/Provider-/Strategiekonfigurationen Alt=Neu.
- 75/75 gerenderte Produktkarten inkl. vollständigem HTML Alt=Neu.
- 2.955/2.955 Inhalts-/Sperrlogikfälle Alt=Neu.
- Notabschaltung, eBay-/idealo-Pause, sanitize_key-, Metadata-, pre_option-Filter, externer Objektcache, Locale-Wechsel, REST und Cron Alt=Neu.
- Meta-/Options-/Home-Aufrufzahlen im kompletten Haupttest exakt Alt=Neu: 3138 / 42 / 5.
- kein bestehender Funktionsname entfernt; Funktionen 1603 -> 1605, nur zwei interne Wiederverwendungshelfer neu.
- Produktions-Schreibprimitive exakt gleiche Vorkommenszahlen.
- ZIP 66/66 Dateien, PHP 23/23 PASS, Re-Extract 0 Abweichungen, PHP erneut 23/23 PASS.

GEBÜNDELTE MASSNAHMEN:
1. exakte eBay-Textnormalisierung request-lokal wiederverwenden.
2. exakte eBay-Tokenisierung request-lokal wiederverwenden.
3. unveränderliche Inhaltsrichtlinien-Marker einmal vorbereiten; keine Sperrregel entfällt.
4. identische Titel-Token/Wortstämme in der Produktform-Sperrprüfung wiederverwenden; alle 30 Sperrbegriffe bleiben geprüft.
5. Creative-Type-/Placement-Normalisierung innerhalb desselben Indexlaufs wiederverwenden; bei sanitize_key-Filter historischer Weg.

NÄCHSTER SCHRITT:
- ausschließlich 6.72.380 installieren.
- danach genau ein PASSIV-Live-Lauf als Bestätigung des bereits lokal bewiesenen Gesamtgewinns.
