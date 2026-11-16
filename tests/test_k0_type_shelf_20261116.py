"""K0 type shelf: fresh, isolated acceptance without old run artifacts.

No WordPress access, publish, stale run reuse, new worker, or metadata redecision.
"""
import copy
import hashlib
import json
import tempfile
import zipfile
import unittest
from pathlib import Path
from unittest.mock import patch

from engine import core, checkers, k0_full_rules, k0_writer_station
from engine.k0_portal_resolver import validate_intake, stable


def valid_article():
    blocks=["intro","preparation","steps","risks","verification","conclusion","further_information"]
    items=[]
    for block in blocks:
        text=("Vorbereitung und Umsetzung erfolgen Schritt für Schritt. "+
              "Jede Voraussetzung und Gefahr wird dabei verständlich erläutert. ")
        inner="<p>"+text*3+"</p>"
        if block=="steps":
            inner += '<ol data-list="steps"><li>Ersten Schritt ausführen</li><li>Zweiten Schritt ausführen</li></ol>'
        if block=="risks":
            inner += '<ul data-list="mistakes"><li>Falsche Befestigung vermeiden</li><li>Unzureichende Kontrolle vermeiden</li></ul>'
        heading="" if block=="intro" else "<h2>"+block.title()+" beachten</h2>"
        items.append('<section data-block="'+block+'">'+heading+inner+"</section>")
    return {
      "article_id":"test-only-article",
      "article_type":"Anleitung",
      "title":"Einen sicheren Wassertrog für Pferde selber bauen",
      "html":"".join(items),
      "wordpress_category":{"id":100,"slug":"wassertroege-fuer-weiden-installation","taxonomy":"category"},
      "type_meta":{
        "procedure_goal":"Einen sicheren Trog selbst aufbauen",
        "preparation_items":["Material bereitlegen"],
        "procedure_steps":["Untergrund prüfen","Trog aufstellen"],
        "safety_controls":["Standsicherheit beachten"],
        "common_errors":["Kippende Konstruktion"],
        "result_checks":["Standfestigkeit kontrollieren"]
      }
    }


def receipt_status(article, rule_id):
    rows=checkers.structural_receipts(article)
    relevant=[x for x in rows if x["rule_id"]==rule_id]
    assert len(relevant)==1
    return relevant[0]["status"],relevant[0]["evidence"]


class TypeShelfVirginTests(unittest.TestCase):
    def make_temp(self, name, package):
        tmp=tempfile.TemporaryDirectory()
        (Path(tmp.name)/(name+".json")).write_text(json.dumps(package,ensure_ascii=False),encoding="utf-8")
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def extension(self, name):
        d=json.loads((core.TYPE_SHELF/"Anleitung.json").read_text(encoding="utf-8"))
        d["article_type"]=name
        return d

    def test_01_original_rule_data_unmodified(self):
        legacy=json.loads(core.VALUES_PATH.read_text(encoding="utf-8"))
        self.assertEqual(set(legacy["types"]),{"Beratung","Vergleich","FAQ","Pflege"})
        self.assertEqual(core.load_values(),legacy)
        for name in legacy["types"]:
            self.assertEqual(core.load_values(name),legacy)
            self.assertEqual(core.values_hash(name),core.values_hash())
            self.assertEqual(k0_full_rules.writer_rule_bundle(name)["rule_values"],legacy)

    def test_02_anleitung_full_package_and_separate_hash(self):
        ext=core.load_values("Anleitung")
        self.assertEqual(set(ext["types"])-set(core.load_values()["types"]),{"Anleitung"})
        self.assertEqual(ext["types"]["Anleitung"]["required_lists"],["steps","mistakes"])
        self.assertEqual(ext["table"]["presence_policy"]["Anleitung"],"REQUIRED_UNLESS_EXCEPTION")
        self.assertNotEqual(core.values_hash("Anleitung"),core.values_hash())
        job=k0_full_rules.writer_rule_bundle("Anleitung")
        self.assertEqual(job["rule_values_sha256"],core.values_hash("Anleitung"))
        self.assertIs(job["publish_allowed"],False)

    def test_03_category_does_not_define_article_type(self):
        ident={"article_type":"Anleitung","category":"wassertroege-fuer-weiden-installation",
               "title":"Einen sicheren Wassertrog für Pferde selber bauen",
               "target_keyword":"wassertröge selber bauen",
               "plan_slot":"1b60069d26ce9f6a70de15852e683a57262282acdead981d9b73742185ef5aeb"}
        batch={"contract":"PSERC_TEXTMACHINE_METADATA_BATCH_V2",
               "status":"READY_FOR_TEXTMACHINE_METADATA_INTAKE",
               "item_count":1,"publish_allowed":False,"content_or_format_payload_present":False,
               "items":[ident]}
        batch["batch_sha256"]=hashlib.sha256(stable(batch).encode("utf-8")).hexdigest()
        self.assertEqual(validate_intake(batch),[ident])
        self.assertEqual(ident["article_type"],"Anleitung")
        self.assertNotEqual(ident["category"],ident["article_type"])

    def test_04_legacy_category_label_not_silent_article_alias(self):
        with self.assertRaisesRegex(ValueError,"K0_TYPE_NOT_DEFINED:Installation"):
            core.load_values("Installation")
        with self.assertRaisesRegex(ValueError,"K0_TYPE_NOT_DEFINED:Kosten"):
            core.load_values("Kosten")

    def test_05_planned_type_is_held(self):
        name="Erfahrungsbericht"
        d=self.extension(name);d["status"]="PLANNED"
        with patch.object(core,"TYPE_SHELF",self.make_temp(name,d)):
            with self.assertRaisesRegex(ValueError,"K0_TYPE_NOT_READY:Erfahrungsbericht"):
                core.load_values(name)

    def test_06_missing_rules_are_diagnosed_directly(self):
        name="Erfahrungsbericht";d=self.extension(name)
        del d["rules"]["type_meta_schema"]
        with patch.object(core,"TYPE_SHELF",self.make_temp(name,d)):
            with self.assertRaisesRegex(ValueError,"K0_TYPE_RULES_INCOMPLETE:Erfahrungsbericht"):
                core.load_values(name)

    def test_07_empty_safety_rules_cannot_be_called_ready(self):
        name="Erfahrungsbericht";d=self.extension(name)
        d["rules"]["required_lists"]=[]
        with patch.object(core,"TYPE_SHELF",self.make_temp(name,d)):
            with self.assertRaisesRegex(ValueError,"K0_TYPE_RULE_LISTS_INVALID:Erfahrungsbericht"):
                core.load_values(name)

    def test_08_name_identity_mismatch_is_rejected(self):
        name="Erfahrungsbericht";d=self.extension(name)
        d["article_type"]="Kosten"
        with patch.object(core,"TYPE_SHELF",self.make_temp(name,d)):
            with self.assertRaisesRegex(ValueError,"K0_TYPE_PACKAGE_IDENTITY_INVALID:Erfahrungsbericht"):
                core.load_values(name)

    def test_09_new_type_works_without_another_worker_or_historic_run(self):
        name="Erfahrungsbericht";d=self.extension(name)
        d["intent_boundary"]["primary_goal_code"]="REPORT_OWN_EXPERIENCE"
        d["intent_boundary"]["primary_goal"]="Erfahrungen aus erster Hand nachvollziehbar schildern"
        before_legacy=core.values_hash()
        before_anleitung=core.values_hash("Anleitung")
        with patch.object(core,"TYPE_SHELF",self.make_temp(name,d)):
            new=core.load_values(name)
            self.assertIn(name,new["types"])
            self.assertEqual(core.values_hash(),before_legacy)
        self.assertEqual(core.values_hash("Anleitung"),before_anleitung)

    def test_10_required_steps_and_mistakes_pass(self):
        a=valid_article()
        self.assertEqual(receipt_status(a,"structure.required_blocks")[0],"PASS")
        self.assertEqual(receipt_status(a,"structure.required_lists")[0],"PASS")
        self.assertEqual(receipt_status(a,"type.metadata_schema")[0],"PASS")

    def test_11_missing_mistakes_list_fails_same_existing_gate(self):
        a=valid_article()
        a["html"]=a["html"].replace('data-list="mistakes"','data-list="tips"')
        self.assertEqual(receipt_status(a,"structure.required_lists")[0],"FAIL")

    def test_12_missing_result_verification_fails_same_existing_gate(self):
        a=valid_article()
        a["html"]=a["html"].replace('data-block="verification"','data-block="tips"')
        self.assertEqual(receipt_status(a,"structure.required_blocks")[0],"FAIL")

    def test_13_missing_safety_metadata_fails_same_existing_gate(self):
        a=valid_article()
        del a["type_meta"]["safety_controls"]
        self.assertEqual(receipt_status(a,"type.metadata_schema")[0],"FAIL")

    def test_14_single_type_scope_distinct_from_pflege(self):
        kind=core.load_values("Anleitung")["types"]["Anleitung"]
        pflege=core.load_values("Pflege")["types"]["Pflege"]
        self.assertIn("verification",kind["required_blocks"])
        self.assertIn("preparation",kind["required_blocks"])
        self.assertNotIn("verification",pflege["required_blocks"])
        self.assertNotIn("preparation",pflege["required_blocks"])
        self.assertIn("steps",pflege["required_blocks"])
        self.assertIn("steps",kind["required_blocks"])
        boundary=json.loads((core.TYPE_SHELF/"Anleitung.json").read_text(encoding="utf-8"))["intent_boundary"]
        self.assertIn("Pflege",boundary["outside_scope"])
        self.assertIn("reparieren",boundary["primary_goal"])

    def test_15_type_receipt_uses_exact_type_rule_hash(self):
        a=valid_article()
        rows=checkers.structural_receipts(a)
        self.assertGreater(len(rows),10)
        for row in rows:
            self.assertEqual(row["rule_values_sha256"],core.values_hash("Anleitung"))
        self.assertEqual(core.values_hash("Pflege"),core.values_hash())

    def test_17_no_change_to_ppm_104_baseline_or_existing_types(self):
        # K0's PPM gate verifies the pinned global 104-rule baseline. The
        # Anleitung-specific blocks are enforced by K0's existing type checks.
        # System 4 itself also has no fixed article-type whitelist.
        from engine.ppm_parity_guard import verify
        package=core.ROOT/"k0_canonical_assets"/"PPM_6.7.9.zip"
        self.assertTrue(package.is_file(),"PPM_6_7_9_ARCHIVE_MISSING")
        with zipfile.ZipFile(package) as z:
            root="portal-production-machine/contracts/"
            templates=json.loads(z.read(root+"article-type-templates.json").decode("utf-8"))
            manifest=json.loads(z.read(root+"article-type-extension-manifest-v1.json").decode("utf-8"))
        standard=templates.get("types") if isinstance(templates,dict) else {}
        extensions=manifest.get("extensions") if isinstance(manifest,dict) else {}
        self.assertEqual(set(standard),{"Beratung","Vergleich","FAQ","Pflege"})
        self.assertTrue("Journal" in [x for e in extensions.values() if isinstance(e,dict) for x in e.get("aliases",[])])
        result=verify()
        self.assertEqual(result["status"],"PASS",result)
        self.assertEqual(result["legacy_rule_count"],104)
        self.assertIn("Anleitung",core.load_values("Anleitung")["types"])
        self.assertNotEqual(core.values_hash("Anleitung"),core.values_hash())

    def synthetic_job(self):
        identity={
          "title":"Einen sicheren Wassertrog für Pferde selber bauen",
          "target_keyword":"wassertröge selber bauen",
          "category":"wassertroege-fuer-weiden-installation",
          "article_type":"Anleitung",
          "plan_slot":"1b60069d26ce9f6a70de15852e683a57262282acdead981d9b73742185ef5aeb"
        }
        intake={
          "contract":"PSERC_TEXTMACHINE_METADATA_BATCH_V2",
          "status":"READY_FOR_TEXTMACHINE_METADATA_INTAKE",
          "item_count":1,
          "publish_allowed":False,
          "content_or_format_payload_present":False,
          "items":[identity]
        }
        intake["batch_sha256"]=hashlib.sha256(stable(intake).encode("utf-8")).hexdigest()
        portal={
          "contract":"K0_PORTAL_ASSIGNMENT_V1",
          "status":"PASS",
          "items":[{"status":"AUTO_DETECTED","portal_id":"pferdeatelier","job_identity":identity}]
        }
        claims={}
        for i in range(1,4):
            claims["F"+str(i)]={
              "source_title":"Fiktive Testquelle "+str(i),
              "source_url":"https://example.org/test/"+str(i),
              "evidence_text_sha256":str(i)*64,
              "statement":"Eine fachliche Testaussage zur schrittweisen Anleitung.",
              "evidence_text":"Eine fachliche Testaussage zur schrittweisen Anleitung.",
              "claim_status":"FULLY_SUPPORTED",
              "article_types":["Anleitung"]
            }
        links=[
          {"role":"parent_category","href":"/category/wassertroege-fuer-weiden-installation/",
           "anchor":"Wassertröge sicher aufstellen","block":"preparation"},
          {"role":"semantic_related","href":"/category/wassertroege-fuer-weiden-beratung/",
           "anchor":"Material und Größe passend wählen","block":"steps"},
          {"role":"further_information","href":"/category/wassertroege-fuer-weiden-faq/",
           "anchor":"Antworten zu Pferdetränken","block":"further_information"}
        ]
        rules={
          "contract":"K0_AUTHORING_RULE_CONTEXT_V1",
          "type_meta":valid_article()["type_meta"],
          "research_claims":claims,
          "required_fact_ids":["F1","F2","F3"],
          "allowed_fact_ids":["F1","F2","F3"],
          "bound_links":links,
          "link_registry":[{"href":x["href"],"active":True} for x in links],
          "runtime_link_roles":[x["role"] for x in links],
          "wordpress_category":{"slug":identity["category"],"taxonomy":"category"},
          "heading_intent_terms":["Wassertrog","Sicherheit","Montage"],
          "comparison_source_bindings":[],
          "table_decision":{
             "decision":"OMIT_NO_ADDED_VALUE",
             "exception_code":"LINEAR_SEQUENCE",
             "rationale":"Eine lineare Schrittfolge ist hier besser als eine Vergleichstabelle."
          },
          "semantic_rule_results":{}
        }
        context={
          "contract":"K0_AUTHORING_CONTEXT_V1",
          "publish_allowed":False,
          "run_instance_id":"run:"+"0"*24,
          "identity":identity,
          "content_profile":{"search_intent":"Anleitung – Pferdetränke"},
          "production_context":{
            "fact_pack":{"contract":"canonical_fact_pack_v1","status":"SOURCE_VERIFIED_PRODUCTION_READY"},
            "production_plan_item":{"article_type":"Anleitung"}
          },
          "rule_context":rules
        }
        return intake,portal,context

    def test_18_fresh_authoring_intake_builds_bound_writer_job(self):
        intake,portal,context=self.synthetic_job()
        job=k0_writer_station.prepare(intake,portal,context)
        self.assertEqual(job["status"],"OPEN")
        self.assertEqual(job["identity"],intake["items"][0])
        self.assertEqual(job["writer_rule_binding"]["rule_values_sha256"],
                         core.values_hash("Anleitung"))
        self.assertEqual(job["writer_rule_bundle"]["article_type"],"Anleitung")
        self.assertFalse(job["publish_allowed"])
        self.assertNotIn("html",job)

    def test_19_missing_mandatory_anleitung_input_stops_before_worker(self):
        intake,portal,context=self.synthetic_job()
        del context["rule_context"]["type_meta"]["common_errors"]
        with self.assertRaisesRegex(k0_writer_station.Blocked,
                                   "K0_RULE_CONTEXT_TYPE_META_REQUIRED:common_errors"):
            k0_writer_station.prepare(intake,portal,context)

    def test_20_unapproved_unknown_article_type_cannot_be_auto_corrected(self):
        intake,portal,context=self.synthetic_job()
        for row in (intake["items"][0],portal["items"][0]["job_identity"],context["identity"]):
            row["article_type"]="Installation"
        intake["batch_sha256"]=hashlib.sha256(stable({k:v for k,v in intake.items() if k!="batch_sha256"}).encode("utf-8")).hexdigest()
        with self.assertRaisesRegex(k0_writer_station.Blocked,"K0_TYPE_NOT_DEFINED:Installation"):
            k0_writer_station.prepare(intake,portal,context)

    def test_21_new_type_goal_codes_must_be_unique_at_registration(self):
        # One structural registration check in QA, never an article decision.
        packages=[]
        for path in sorted(core.TYPE_SHELF.glob("*.json")):
            value=json.loads(path.read_text(encoding="utf-8"))
            if value.get("contract")!=core.TYPE_PACKAGE_CONTRACT:
                continue
            if value.get("status")!="READY":
                continue
            code=value.get("intent_boundary",{}).get("primary_goal_code")
            self.assertTrue(code,"K0_TYPE_GOAL_CODE_MISSING:"+path.stem)
            packages.append((code,path.stem))
        self.assertTrue(packages)
        seen={}
        for code,name in packages:
            self.assertNotIn(code,seen,"K0_TYPE_INTENT_CODE_DUPLICATE:"+code)
            seen[code]=name

    def test_22_anleitung_explicitly_excludes_other_core_types(self):
        data=json.loads((core.TYPE_SHELF/"Anleitung.json").read_text(encoding="utf-8"))
        exclusion=data["intent_boundary"]["outside_scope"]
        for other in ("Pflege","Beratung","Vergleich","FAQ"):
            self.assertIn(other,exclusion,"K0_TYPE_BOUNDARY_INCOMPLETE:"+other)
        self.assertIn("reparieren",data["intent_boundary"]["primary_goal"])
        self.assertIn("aufbauen",data["intent_boundary"]["primary_goal"])

    def test_16_no_old_run_files_are_used_by_any_acceptance_test(self):
        self.assertTrue((core.TYPE_SHELF/"Anleitung.json").is_file())
        self.assertNotIn("real_runs",str(core.TYPE_SHELF))
        self.assertTrue(core.load_values("Pflege"))


if __name__=="__main__":
    unittest.main(verbosity=2)
