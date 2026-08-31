# Output-Quarantine Negativtest-Matrix

1. veralteter Worker-HEAD -> BLOCK
2. falscher/alter Step -> BLOCK
3. ungebundene Chat-ZIP -> QUARANTINE / keine Freigabe
4. Output-SHA weicht vom Manifest ab -> BLOCK
5. Receipt-SHA weicht ab -> BLOCK
6. Receipt != PASS -> BLOCK
7. anderer Step/Sequence -> BLOCK
8. workflow_pass != true -> BLOCK
9. created_by != BOUND_WORKER -> BLOCK
10. publish_allowed != false -> BLOCK
11. Gate beansprucht Inhalts-/Qualitätsautorität -> BLOCK
12. identischer gebundener Output mit gültigem PASS -> RELEASE

Diese Matrix bewertet keinerlei Artikelinhalt oder Qualität. Sie prüft ausschließlich Herkunft, Identität, Status, Hashes und Autorität.
