# V6.60 final error catalog

E1 API redirect 403: automatic redirect could lose POST semantics on legacy host. Fixed with allowlisted HTTPS manual redirect chain preserving POST and x-api-key.

E2 stale staging: products removed from a new full feed could otherwise survive in historical staging. Fixed by binding materialization to the current successfully parsed import snapshot.

E3 false provider matching: similar products must never be merged. Fixed by exact normalized GTIN intersection only; no fuzzy/title/image/category/AI matching.

E4 separate-mode cross-provider dedupe: the same product at two providers must be allowed as separate cards. Dedupe is provider-bound in separate mode; exact identity collapse is only combined/automatic.

E5 eBay regression risk: upgrade default remains ebay_only; 1,000 randomized selection and 1,000 cohort decisions are exactly V6.58-parity; single-provider markup is byte-identical.

E6 stale idealo output: public idealo use requires valid source/provider/GTIN/targets/placements, explicit activation and import freshness <=48h. Failure is provider-isolated/fail-closed.

E7 full-feed URL: the official platform-generated download URL is an external configuration value. It is not derived or guessed. Manual CSV/GZ import remains supported until this value is supplied.