"""Hobbydepot: regression tests for ORIGINAL WordPress type -> ONE hobby editorial book.

Test-only. Does not invoke K0, K-Multi, WordPress, a writer or any network.
The resolver below is a test assertion of the prepared editorial manifest,
NOT an alternate productive router or a second editorial decision.
"""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TYPES = ("Beratung", "FAQ", "Pflege", "Vergleich", "Anleitung")
FILES = ("10_BERATUNG.json", "20_FAQ.json", "30_PFLEGE.json",
         "40_VERGLEICH.json", "50_ANLEITUNG.json")
FIVE = ("title", "target_keyword", "category", "article_type", "plan_slot")


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def select_for_test(original_wordpress_type, manifest, books):
    """Verify the ONE manifest-owned lookup, never infer a type from keyword."""
    if not isinstance(original_wordpress_type, str):
        raise ValueError("NO_ORIGINAL_WORDPRESS_TYPE")
    entries = [b for b in manifest["books"]
               if b["wordpress_article_type"] == original_wordpress_type]
    if len(entries) != 1:
        raise ValueError("TYPE_MISSING_OR_DUPLICATE_NO_FALLBACK")
    reference = entries[0]
    candidate = books.get(reference["file"])
    if (not isinstance(candidate, dict)
            or candidate.get("wordpress_article_type") != original_wordpress_type
            or candidate.get("hobby_rulebook_id") != reference["own_hobby_rulebook_id"]
            or candidate.get("shared_hobby_policy_ref")
                  != manifest["shared_rulebook_filename"]):
        raise ValueError("HOBBY_BOOK_TYPE_ID_OR_COMMON_OWNER_MISMATCH")
    return candidate


class HobbydepotOriginalFiveTypeContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load("00_MANIFEST.json")
        cls.shared = load("05_GEMEINSAME_REGELN.json")
        cls.books = {name: load(name) for name in FILES}
        cls.formal = load("100_HOBBY_FACHREGELN_FORMALE_FREIGABEVORLAGE_20261121.json")

    def test_01_exact_original_wordpress_types(self):
        self.assertEqual(self.manifest["original_wp_types"], list(TYPES))

    def test_02_exact_one_original_input_contract(self):
        h = self.manifest["handoff_contract"]
        self.assertEqual(h["input"]["package_contract"], "WP_K0_UPLOAD_PACKAGE_V1")
        self.assertTrue(h["input"]["same_original_wordpress_json_only"])

    def test_03_five_original_fields_unchanged(self):
        self.assertEqual(self.manifest["handoff_contract"]["input"]["exact_existing_five_fields"], list(FIVE))
        self.assertTrue(self.manifest["handoff_contract"]["input"]["original_five_fields_and_article_identity_immutable"])

    def test_04_portal_identity_from_original_receipt_only(self):
        i = self.manifest["handoff_contract"]["input"]
        self.assertEqual(i["site_host_location"], "word_press_order_receipt.site_host")
        self.assertEqual(i["recognized_portal"], "hobby_depot")
        self.assertEqual(i["accepted_hobby_hosts"], ["hobby-depot.de", "www.hobby-depot.de"])

    def test_05_original_mini_only_authority(self):
        self.assertEqual(self.manifest["handoff_contract"]["editor_source"]["article_type_is_only_decided_by"],
                         "ORIGINAL_WORDPRESS_MINI")

    def test_06_single_selection_reference_only(self):
        x = self.manifest["handoff_contract"]["editor_source"]
        self.assertEqual(x["selection_table_authority"], "THIS_MANIFEST.books")
        self.assertEqual(x["own_rulebook_path_from"], "THIS_MANIFEST.books[*].file")
        self.assertTrue(x["no_fallback_on_missing_or_conflicting_book"])

    def test_07_no_additional_wp_field_or_sidecar(self):
        x = self.manifest["handoff_contract"]["input"]
        self.assertTrue(x["no_added_portal_field"])
        self.assertTrue(x["no_sidecar"])
        self.assertTrue(x["no_user_second_upload"])

    def test_08_five_distinct_original_type_entries(self):
        entries = self.manifest["books"]
        self.assertEqual(len(entries), 5)
        self.assertEqual([b["wordpress_article_type"] for b in entries], list(TYPES))
        self.assertEqual(len({b["own_hobby_rulebook_id"] for b in entries}), 5)
        self.assertEqual([b["file"] for b in entries], list(FILES))

    def test_09_no_new_magazine_type(self):
        self.assertFalse(self.manifest["extra_portal_types_created"])
        self.assertNotIn("Porträt & Bericht", self.manifest["original_wp_types"])
        self.assertNotIn("Inspiration", self.manifest["original_wp_types"])

    def test_10_single_shared_twelve_rule_owner(self):
        self.assertTrue(self.manifest["single_shared_rule_owner"])
        self.assertEqual(self.manifest["shared_rulebook_filename"], "05_GEMEINSAME_REGELN.json")
        self.assertEqual(len(self.shared["shared_rules"]), 12)
        self.assertEqual(self.shared["status"], "EDITORIAL_DRAFT_ONLY_NOT_RUNTIME_APPROVED")

    def test_11_shared_rule_ids_unique_and_single_owner(self):
        rules = self.shared["shared_rules"]
        self.assertEqual(len({r["id"] for r in rules}), 12)
        self.assertTrue(all(r.get("owner") and r.get("rule") for r in rules))

    def test_12_no_shared_rule_copies_in_typebooks(self):
        for b in self.books.values():
            self.assertNotIn("common_editorial_rules", b)
            self.assertEqual(b["shared_hobby_policy_ref"], "05_GEMEINSAME_REGELN.json")

    def test_13_original_type_id_and_book_match(self):
        for t in TYPES:
            with self.subTest(type=t):
                selected = select_for_test(t, self.manifest, self.books)
                self.assertEqual(selected["wordpress_article_type"], t)

    def test_14_own_rules_exactly_31_with_distinct_ids(self):
        rules = [r for b in self.books.values() for r in b["additional_type_rules"]]
        self.assertEqual([len(self.books[n]["additional_type_rules"]) for n in FILES],
                         [6, 5, 6, 7, 7])
        self.assertEqual(len(rules), 31)
        self.assertEqual(len({r["id"] for r in rules}), 31)

    def test_15_every_specific_rule_has_one_owner(self):
        for b in self.books.values():
            for r in b["additional_type_rules"]:
                self.assertTrue(r.get("owner") and r.get("rule"))

    def test_16_all_five_books_are_hobby_drafts(self):
        for b in self.books.values():
            self.assertEqual(b["portal_id"], "hobby_depot")
            self.assertTrue(b["original_wordpress_type_is_authority"])
            self.assertEqual(b["status"], "HOBBY_EDITORIAL_DRAFT_COMPLETE_NOT_ACTIVATED")

    def test_17_no_fake_active_writer_or_publishing(self):
        self.assertFalse(self.manifest["authoring_active"])
        self.assertFalse(self.manifest["publish_allowed"])
        self.assertTrue(self.manifest["no_automatic_runtime_injection"])
        self.assertFalse(self.formal["known_not_active"]["production_enabled"])
        self.assertFalse(self.formal["known_not_active"]["wordpress_import_allowed"])

    def test_18_valid_editorial_targets_not_hard_gates(self):
        for b in self.books.values():
            f = b["format_guidance"]
            self.assertEqual(f["values_are"],
              "HOBBY_EDITORIAL_TARGETS_NOT_AUTOMATIC_RUNTIME_HARD_LIMITS")
            self.assertEqual(len(f["words"]), 2)
            self.assertLess(f["words"][0], f["words"][1])
            self.assertEqual(len(f["h2"]), 2)
            self.assertLess(f["h2"][0], f["h2"][1])

    def test_19_faq_no_mandatory_table(self):
        self.assertIn("Keine Pflichttabelle", self.books["20_FAQ.json"]["format_guidance"]["tables"])

    def test_20_pflege_and_anleitung_have_separate_content_books(self):
        p, a = self.books["30_PFLEGE.json"], self.books["50_ANLEITUNG.json"]
        self.assertEqual((p["hobby_rulebook_id"], a["hobby_rulebook_id"]),
                         ("HOBBY_PFLEGE", "HOBBY_ANLEITUNG"))
        self.assertNotEqual(p["additional_type_rules"], a["additional_type_rules"])

    def test_21_all_five_kmulti_types_now_attached_separately(self):
        expected = {
            "Beratung": "HOBBY_RATGEBER_WISSEN", "FAQ": "HOBBY_FAQ",
            "Pflege": "HOBBY_PFLEGE", "Vergleich": "HOBBY_VERGLEICH",
            "Anleitung": "HOBBY_ANLEITUNG",
        }
        self.assertEqual(
            {r["wordpress_article_type"]: r["existing_kmulti_transport_reference"]
             for r in self.manifest["books"]}, expected)
        self.assertTrue(all(r["existing_transport_matches_new_own_book"]
                            for r in self.manifest["books"]))
        self.assertEqual(len(set(expected.values())), 5)
        self.assertTrue(self.manifest["handoff_contract"]
                        ["current_integration"]["all_five_types_attached_to_unique_books"])

    def test_22_unknown_type_must_fail_without_guessing(self):
        for t in ("Porträt & Bericht", "Inspiration", "Münzen", "", "faq", None):
            with self.subTest(type=t):
                with self.assertRaises(ValueError):
                    select_for_test(t, self.manifest, self.books)

    def test_23_missing_book_must_fail(self):
        altered = dict(self.books)
        altered.pop("20_FAQ.json")
        with self.assertRaises(ValueError):
            select_for_test("FAQ", self.manifest, altered)

    def test_24_duplicate_type_definition_must_fail(self):
        altered = copy.deepcopy(self.manifest)
        altered["books"].append(copy.deepcopy(altered["books"][1]))
        with self.assertRaises(ValueError):
            select_for_test("FAQ", altered, self.books)

    def test_25_mismatched_type_book_must_fail(self):
        altered = copy.deepcopy(self.books)
        altered["20_FAQ.json"]["wordpress_article_type"] = "Pflege"
        with self.assertRaises(ValueError):
            select_for_test("FAQ", self.manifest, altered)

    def test_26_mismatched_rulebook_id_must_fail(self):
        altered = copy.deepcopy(self.books)
        altered["30_PFLEGE.json"]["hobby_rulebook_id"] = "HOBBY_ANLEITUNG"
        with self.assertRaises(ValueError):
            select_for_test("Pflege", self.manifest, altered)

    def test_27_missing_common_rulebook_reference_must_fail(self):
        altered = copy.deepcopy(self.books)
        altered["50_ANLEITUNG.json"]["shared_hobby_policy_ref"] = None
        with self.assertRaises(ValueError):
            select_for_test("Anleitung", self.manifest, altered)

    def test_28_foreign_old_750_word_rule_not_automatically_inherited(self):
        self.assertTrue(self.formal["never_import_foreign_formal_values"]
                        ["collision_for_all_three_real_Hobby_FAQs"])
        self.assertEqual(self.books["20_FAQ.json"]["format_guidance"]["words"], [500, 800])

    def test_29_no_preemptive_kmulti_binding_activation(self):
        integration = self.manifest["handoff_contract"]["current_integration"]
        self.assertEqual(integration["inactive_rule_state"], "NO_VALUES_BLOCKED")
        self.assertFalse(integration["current_production_enabled"])
        self.assertFalse(integration["automatic_article_writing_allowed"])

    def test_30_no_extra_owner_or_legacy_k0_dependency(self):
        self.assertTrue(self.manifest["no_second_editorial_owner"])
        self.assertTrue(self.manifest["k0_only_read_as_general_guidance"])
        self.assertFalse(self.manifest["copy_of_k0_rule_values"])



    def test_31_design_muster_meta_not_invented_as_fully_verified_body(self):
        m=self.manifest["editorial_design_reference_20261122"]
        self.assertEqual(m["new_specific_rule_counts"],
                         dict(zip(TYPES,[6,5,6,7,7])))
        self.assertIn("reported by user",m["evidence"])
        self.assertTrue(m["not_a_product_release"])

    def test_32_merksatz_is_optional_and_one_content_and_design_owner(self):
        x=self.shared["single_owner_nonrule_context"]["optional_reader_elements"]
        self.assertIn("Optional",x["merksatz"])
        self.assertIn("HD003_DESIGN",x["authority"])
        self.assertTrue(x["same_single_editorial_owner"])
        self.assertEqual(len(self.shared["shared_rules"]),12)

    def test_33_for_whom_which_only_advice_and_comparison(self):
        b=self.books["10_BERATUNG.json"]["additional_type_rules"]
        v=self.books["40_VERGLEICH.json"]["additional_type_rules"]
        self.assertIn("Für wen",next(x for x in b if x["id"]=="B02_EIGNUNG")["rule"])
        self.assertIn("Für wen",next(x for x in v if x["id"]=="V04_FAIRE_EINORDNUNG")["rule"])
        self.assertNotIn("B02_EIGNUNG",
                         [x["id"] for x in self.books["20_FAQ.json"]["additional_type_rules"]])

    def test_34_checklist_applies_only_for_real_preparation(self):
        expected={"Beratung":"B05_STARTCHECK_NACH_WAHL",
                  "Vergleich":"V06_KURZER_PRAXISCHECK"}
        for name,rule_id in expected.items():
            b=next(x for x in self.books.values() if x["wordpress_article_type"]==name)
            self.assertIn(rule_id,[r["id"] for r in b["additional_type_rules"]])
        faq=self.books["20_FAQ.json"]
        self.assertIn("keine künstliche Liste",
                      next(x for x in faq["additional_type_rules"]
                           if x["id"]=="F05_KURZE_HANDLUNG")["rule"])

    def test_35_safety_is_existing_shared_rule_not_5_duplicate_rules(self):
        ids=[r["id"] for r in self.shared["shared_rules"]]
        self.assertEqual(ids.count("H06_SICHERHEIT"),1)
        self.assertTrue(all("shared_hobby_policy_ref" in b for b in self.books.values()))

    def test_36_FAQ_type_still_one_question_no_second_FAQ_block(self):
        f=self.books["20_FAQ.json"]
        self.assertIn("Keine zusätzlichen",next(x for x in
                          f["additional_type_rules"] if x["id"]=="F02_EINE_FRAGE")["rule"])
        self.assertIn("kein",f["article_structure"][-2].lower())
        self.assertEqual(len(f["additional_type_rules"]),5)

    def test_37_optional_short_followup_questions_not_double_content(self):
        for name in ("10_BERATUNG.json","30_PFLEGE.json",
                     "40_VERGLEICH.json","50_ANLEITUNG.json"):
            own=self.books[name]["additional_type_rules"]
            last=own[-1]
            self.assertTrue(any(x in last["rule"].lower() for x in
                                ("nicht", "keine")))
        self.assertTrue(self.shared["single_owner_nonrule_context"]
                        ["optional_reader_elements"]["old_design_plugin_not_modified"])

    def test_38_same_five_types_and_writer_remain_blocked(self):
        self.assertEqual(self.manifest["original_wp_types"],list(TYPES))
        self.assertFalse(self.manifest["authoring_active"])
        self.assertFalse(self.manifest["publish_allowed"])
        self.assertEqual(self.manifest["editorial_design_reference_20261122"]["total_type_rules"],31)

if __name__ == "__main__":
    unittest.main(verbosity=2)
