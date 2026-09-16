# STARTMASTER0107 – Closeout-Synchronisationskorrektur 2026-09-11

**HISTORISCHER WAS/WARUM-NACHWEIS. KEINE CURRENT-AUTORITÄT.** Current ausschließlich `control/startmaster0107/CURRENT_STATE.json`.

Bei der finalen Negativprüfung wurde erkannt, dass ein exakt gespeicherter `hobbyroom_head_sha` in CURRENT_STATE nach jeder reinen Status-/Protokoll-Merge sofort wieder veralten würde. Das wäre erneut eine konkurrierende/veraltete Standwahrheit.

KISS-Korrektur: Der dynamische Hobbyraum-SHA wurde aus CURRENT_STATE entfernt. Stattdessen gilt dauerhaft: Vor jeder funktionalen Arbeit muss `hobbyroom/ppm-inner-reason-visibility-20260911` zuerst auf den dann aktuellen kanonischen `main` fast-forward synchronisiert werden. Während des Freeze darf der Branch keine funktionale Abweichung enthalten.

Geändert wurden ausschließlich CURRENT_STATE, dessen START_HERE-Hash und dieser historische Nachweis. Keine Fach-, Inhalts-, PPM-, PSERC-, PSTE-, LanguageTool-, SEO-, Design-, Publish- oder Workflowcode-Änderung.
