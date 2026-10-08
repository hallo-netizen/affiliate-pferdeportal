# AFF-ERR-058 – KISS Banner Single Target Local Simulation

Date: 2026-10-08

Source:
- branch: affiliate-release-current
- plugin: 6.72.203
- source manifest SHA-256: 4e215f50ac0bb4482dc296768d2f53bb154cdf4880945ff21bce0747053e69a0

Contract:
`banner -> one stored topic/portal target -> existing format/slot path -> output`

Local/source simulation:

Positive:
- automatic mapped topic is read from topic_targets: PASS
- manual topic assignment replaces the portal record in the same topic_targets truth: PASS
- matching stored target remains deliverable: PASS

Negative:
- wrong topic: PASS fail-closed
- missing topic: PASS fail-closed
- invalid target key: PASS fail-closed
- mapping for another portal: PASS fail-closed
- legacy state=general: PASS fail-closed
- assignment_mode=fallback cannot bypass a missing stored target for output_object_v4 banners: PASS
- horse-breed neutral fallback cannot bypass a missing stored target for output_object_v4 banners: PASS

Independent local PHP harness:
- php -l: PASS
- 10/10 scenario assertions PASS
- 0 failures

Performance/database hardlock:
- campaign_match_rank changed path adds 0 direct $wpdb accesses
- adds 0 get_posts()
- adds 0 get_post_meta()
- adds 0 get_option()
- adds 0 wp_remote_*/wp_safe_remote* calls
- frontend target classification remains stored-map-only
- manual assignment adds one backend Creative-Library update for the selected banner; no new table

Important root-cause follow-up:
During the simulation, the first failure was found in the later campaign ranking path: output_object_v4 banners could still fall into general fallback mode and a horse-breed neutral fallback before the stored-target hard gate. Commit 02799c180da3b95ad34341fbfa939db599891eb2 removes that bypass for automatic Creative-Library banners. The simulation was rerun after this fix and passed.

Status:
LOCAL_POSITIVE_NEGATIVE_SIM_PASS / PERFORMANCE_DB_HARDLOCK_PASS / WORDPRESS_MARIADB_RELEASE_GATES_STILL_REQUIRED / NO_RELEASE_PASS


## Correction after authoritative contract re-check

The prior hard statement "no matching stored topic = no banner" was too broad and contradicted section 9.4 of the authoritative banner contract.

Correct fixed order:
1. specific stored mapped banner for the current target/path wins;
2. a specific banner that does not match stays out;
3. if no specific banner is available for the target, an explicitly general active banner may be selected from the existing technically/format-valid fallback pool;
4. existing stable deterministic distribution remains;
5. no frontend reclassification, provider HTTP, new frontend DB query or new table.

The too-hard source change was corrected:
- restore stored state `general` as an explicit fallback state;
- for `output_object_v4` banners: matching `automation_target_keys` win; otherwise only `assignment_mode=fallback` may enter the general pool; a nonmatching specific banner remains blocked;
- horse-breed special handling cannot turn a nonmatching specific Creative-Library banner into a fallback candidate.

Corrected local rule matrix: 13/13 PASS.
