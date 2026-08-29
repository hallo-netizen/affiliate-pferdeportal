# HARDLOCK-BASE negative selftest and path fix

Purpose: before `hardlock-base` becomes a required Ruleset check, prove that the trusted base workflow rejects a PR which changes an immutable entrance-security path, while the currently required deterministic `hardlock` remains PASS.

Expected negative result: `hardlock-base` FAIL with `IMMUTABLE_ENTRANCE_SECURITY_PATH_CHANGE_BLOCKED`.

This PR also fixes the discovered continuity-test filename in the immutable base workflow and broadens the ordinary hardlock trigger to all workflow changes. No domain/content/quality/design logic changes.
