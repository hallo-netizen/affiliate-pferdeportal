# STARTMASTER0069 – Release-Checkpoint

Basis: STARTMASTER0068 / d1befd2c23bdb1c10a0ee11ef41805bb8d8fc95e.

Scope ausschließlich: PSTE 0.56.9 upstream Titel-Hardlock und read-only Alttitel-Revalidierung; PSERC 0.28.4 finaler Titel-Hardlock, Beratung Batch-/Published-Phrasenprüfung und vollständige Compilerstatussichtbarkeit. Textmaschine/PPM 6.7.9, Link Policy 1.0.1, Design, Inhalte und Publish unverändert.

Root Cause: PSTE 0.56.8 enthielt im produktiven Beratung-Fallback bereits verbotene Formeln. PSERC 0.28.3 zeigte zusätzlich nur ausgewählte nachgelagerte Statuszähler, obwohl `seo_eligible` nur ein upstream Zulassungszähler ist.

Boxenmatten deterministisch: `Boxenmatten für Pferde – worauf es bei der Auswahl ankommt`.

QA: PSTE Source/Fresh PHP 72/72 und JSON 52/52; PSERC Source/Fresh PHP 40/40 und JSON 16/16; Source/Fresh byteidentisch; Package-Integrity positiv und negativ PASS; systemweiter PSERC→Supervisor→PPM→Draft→Readback Source + Fresh PASS; PPM 137/137; Link 19/19; Publish false.

Installer: PSTE SHA-256 `7711c50ad76f5658334c1b29739f6039da833520c38fa5b24d953bfb349277c5`; PSERC SHA-256 `9c156169c26c98ea13f1281566476d3e36b7e45be221b2f5923a4fd24631e303`.

Offen bleibt ausschließlich der dynamische Live-Beleg: beide Installer installieren und PSERC-Redaktionsplan exakt einmal neu aufbauen. Kein künstlicher Live-PASS.