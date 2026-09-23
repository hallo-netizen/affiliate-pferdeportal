# Kategorieintegration – Fallback-Matrix

| System | Gebundener sicherer Ausgangs-/Fallbackstand | Status |
|---|---|---|
| Zentrales Kategorie-Plugin | V1.6.1, `QUELLCODE_KATEGORIE_WORKFLOW_V1.6.1_WORKFLOW_HARDLOCK.zip`, SHA256 `c0572951a5672e04fbad87f27ff6bb4990072db55500c6ad865c4d8193719c55` | exakt gebunden |
| Affiliate-Zentrale | 6.72.142 GOLDMASTER | bestehender sicherer Fallback; 6.72.145 bleibt Arbeitsbasis für Strukturdelta |
| PPM | PPM 6.7.9 Paket SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1` | exakt gebunden |
| PSERC | `PSERC-FIX.zip` SHA256 `77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314` | exakt gebunden |
| PPA-013 | letzter exakt hashgebundener Source-Apply 1.50.558 / SHA256 `840130139597c6152a385475c05b2786c96d08bd137785e127280d9aabe979f1`; aktueller Live-Vollstand nach 30-Text-Lauf noch neu zu binden | KEINE Änderung bis aktueller Vollstand gesichert |
| PSTE | dynamischer WordPress-Strukturpfad; keine neue statische Kategoriequelle belegt | Codeänderung nur bei nachgewiesenem Bedarf |
| pa-affiliate-design-performance | ausdrücklich außerhalb Kategorien-Scope | nicht anfassen |

## Regel
Kein bestehender Produktivstand wird überschrieben, bevor der jeweilige Kandidat lokal/CI positiv, negativ und regressiv PASS ist. Bei PPA-013 ist vor jeder Änderung zwingend zuerst der aktuelle echte Vollstand als neuer Fallback zu sichern.
