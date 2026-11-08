# PSTE + PSERC – unveränderte Testpakete im Plugin-Büro (Stand 08.11.2026, 16 Uhr Berlin)

**Art:** Inventar der vom Nutzer bereits installierten und im Chat verwendeten Testpakete. **Keine neue Pluginversion, kein Release, keine neue Installation, keine K0-Änderung.**

## Binärdateien – tatsächlich gesichert und danach erneut gelistet

| Paket | Physischer Speicherort | Größe (Byte) | SHA-256 |
|---|---|---:|---|
| PSTE 0.57.144.22 TEST | Privat-Library `/pferdeatelier/PLUGINS/PSTE-0.57.144.22-TEST.zip` | 634339 | `384203f4971fc6d98eaa7613835c75f2b1ff976471659afa8dae60ac09a08ad1` |
| PSERC 0.28.55 TEST | Privat-Library `/pferdeatelier/PLUGINS/PSERC-0.28.55-TEST.zip` | 266498 | `501959a0ac73a1b81070ed23623935999ed1058385b3ba587e0f8bef9c9816d0` |
| Beide zusammen, äußeres Paket | Privat-Library `/pferdeatelier/PLUGINS/PFERDEATELIER-BEIDE-TEST-PLUGINS.zip` | 901105 | `1085ba60a704a24b0688c19afc724ea25feb68ee8def786688ce7fa69164e45c` |

**Speicherungsbeleg:** Library-List Readback: exakt die drei obigen Pfade und Größen. PSTE und PSERC local ZIP `testzip()=None` (CRC vollständig), 121 bzw. 63 Pfade; aus den echten PHP-Plugin-Headern Versionen 0.57.144.22 / 0.28.55. Das äußere Paket enthält exakt diese beiden ZIPs unverändert (SHA256 der inneren Dateien stimmt überein).

**Wichtig:** Die Binärdateien liegen in der **privaten Plugin-Dateiablage**, **nicht als ZIP-Dateien im GitHub-Git-Baum**. GitHub hält dieses Register, Prüfsummen, QA-Quellen und Protokolle. Kein nicht existentes GitHub-ZIP behaupten; der im GitHub-Git-Baum vorhandene ältere `INSTALLATIONS_PAKETE/PSTE-0.57.144.22-NUR-TEST.zip` ist **nicht** mit dem obigen 634339-Byte-Testzip gleichzusetzen (abweichende Dateigröße 624952 Byte). PSERC-0.28.55-Testzip ist die aus Original-0.28.53 isoliert reproduzierte QA-Kopie; **nicht** die historisch mit .55 benannte alte Release-ZIP. Diese Abweichung schützt vor vertauschten Originalen.

**Installationsbeleg:** Anwender gibt Installation beider Plugins an; WordPress-Screenshots zeigen PSERC `0.28.55-one-owner-no-fallback`, SEO-Themenengine `0.57.144.22` und dessen `METADATEN-VORSCHAU PASS`. Kein Dateibytevergleich der *auf dem Server* installierten Plugins, daher nur Versionen belegt, keine serverseitigen ZIP-Hashes.

**Keine Freigabe für produktive Verwendung**, kein Merge, kein stillschweigendes Überschreiben der aktuell autoritativen `/Campus-Plugins/.../CURRENT.zip`-Pfade. Originale und K0 unverändert.
