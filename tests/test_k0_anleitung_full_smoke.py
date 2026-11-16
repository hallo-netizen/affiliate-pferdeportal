"""Full K0 article-rule smoke for Anleitung with a NEW synthetic text fixture.

This runs actual unchanged hard-rule checks (no WordPress, no old run files,
no additional worker, no LT bypass in production).
"""
import copy
import unittest

from engine.checkers import run_article_content_checks, article_hash
from engine.final_integrity import verify_article_pre_lt68
from engine.k0_full_rules import verify_pre_lt68, verify_final, Blocked
from tests.test_k10 import make_base, words, trace
from tests.test_k0_full_rule_chain import package_from_article


def fresh_anleitung():
    a=make_base()
    a["article_type"]="Anleitung"
    a["title"]="Longierpeitsche sicher montieren und prüfen"
    a["target_keyword"]="Longierpeitsche montieren"
    a["type_meta"]={
      "procedure_goal":"Eine Longierpeitsche sicher für ihren Einsatz vorbereiten",
      "preparation_items":["Hilfsmittel bereitlegen"],
      "procedure_steps":["Bauteile prüfen","Teile verbinden","Ergebnis kontrollieren"],
      "safety_controls":["Mangelhafte Bauteile nicht verwenden"],
      "common_errors":["Verbindungen unzureichend prüfen"],
      "result_checks":["Sicheren Halt kontrollieren"],
    }
    for c in a["research_claims"].values():
        c["article_types"].append("Anleitung")
    # The test must be a coherent article with a genuine fact-to-paragraph
    # binding, not a mismatched FAQ topic with invented numeric claims.
    import hashlib
    source_statements={
      "F2":"Teile vorbereiten und Beschädigungen erkennen. Benötigte Teile vor der Montage prüfen und sichere Bauteile kontrollieren.",
      "F3":"Montage, Verbindung und Bauteile schrittweise prüfen. Schritte und Reihenfolge müssen die sichere Funktion unterstützen.",
      "F4":"Montagefehler, beschädigte Teile, ungeeignete Hilfsmittel und Sicherheitsabstand beachten. Verbindung nach dem Aufbau kontrollieren, Ergebnis, Standfestigkeit und Funktion prüfen.",
    }
    for fid,statement in source_statements.items():
        claim=a["research_claims"][fid]
        claim["statement"]=statement
        claim["evidence_text"]=statement
        claim["evidence_text_sha256"]=hashlib.sha256(statement.encode("utf-8")).hexdigest()
    a["heading_intent_terms"]=["Montage","Teile","Montagefehler","Verbindung","Aufbau","Standfestigkeit","Kontrolle"]
    a["bound_links"][0]["block"]="preparation"
    a["bound_links"][1]["block"]="steps"
    intro=a["html"].split('<section data-block="intro">',1)[1].split("</section>",1)[0]
    conclusion=a["html"].split('<section data-block="conclusion">',1)[1].split("</section>",1)[0]
    further=a["html"].split('<section data-block="further_information">',1)[1].split("</section>",1)[0]
    hashes={fid:c["evidence_text_sha256"] for fid,c in a["research_claims"].items()}
    def para(fid,subject,number,n,link=""):
        marker=trace(fid,"Fachquelle "+fid,hashes[fid]) if number==1 else ""
        return '<p data-fact-ids="'+fid+'">'+marker+' '+words(subject+" "+("eins","zwei","drei","vier")[number-1],n)+' '+link+'</p>'
    def block(name,title,fid,subject,role="",href="",anchor="",lists=""):
        text="<section data-block='"+name+"'><h2>"+title+"</h2>"
        for i in range(1,5):
            link=('<a data-link-role="'+role+'" href="'+href+'">'+anchor+'</a>') if i==1 and role else ""
            text+=para(fid,subject,i,32,link)
        text+=lists+"</section>"
        return text
    preparation=block("preparation","Benötigte Teile vor der Montage prüfen","F2","Teile vorbereiten und Beschädigungen erkennen",
                      "parent_category","/training/","Training")
    steps_list='<ol data-list="steps"><li data-fact-ids="F3">Bauteile auf Mängel prüfen</li><li data-fact-ids="F3">Teile gemäß Anleitung verbinden</li><li data-fact-ids="F3">Verbindung vorsichtig belasten</li><li data-fact-ids="F3">Sicheren Halt erneut kontrollieren</li></ol>'
    steps=block("steps","Montage in sinnvoller Reihenfolge","F3","Montage Verbindung Bauteile Schrittfolge prüfen",
                "semantic_related","/training/longieren/","Longieren",steps_list)
    risk_list='<ul data-list="mistakes"><li data-fact-ids="F4">Beschädigte Teile weiterverwenden</li><li data-fact-ids="F4">Verbindung nicht ausreichend prüfen</li><li data-fact-ids="F4">Ungeeignete Hilfsmittel einsetzen</li><li data-fact-ids="F4">Sicherheitsabstand unterschätzen</li></ul>'
    risks=block("risks","Typische Montagefehler vermeiden","F4","Montagefehler Sicherheit Abstände Bauteile beachten",lists=risk_list)
    verification=block("verification","Verbindung nach dem Aufbau kontrollieren","F4","Verbindung Aufbau Ergebnis Kontrolle Standfestigkeit Funktion prüfen")
    a["html"]="<article><section data-block=\"intro\">"+intro+"</section>"+preparation+steps+risks+verification+'<section data-block="conclusion">'+conclusion+'</section><section data-block="further_information">'+further+"</section></article>"
    a["table_decision"]={
      "decision":"OMIT_NO_ADDED_VALUE",
      "exception_code":"LINEAR_SEQUENCE",
      "rationale":"Eine lineare Montageanleitung ist als Schrittfolge klarer als eine Vergleichstabelle."
    }
    return a


class AnleitungSmoke(unittest.TestCase):
    def test_positive_all_pre_language_tool_rules(self):
        a=fresh_anleitung()
        pkg,cat=package_from_article(a)
        failed={x["rule_id"]:x["evidence"] for x in run_article_content_checks(a) if x["status"]=="FAIL"}
        self.assertFalse(failed,failed)
        result=verify_pre_lt68(pkg,cat)
        self.assertEqual(result["status"],"READY_FOR_LT68",result)
        self.assertGreaterEqual(result["required_receipt_count"],75)
        final=verify_final(pkg,cat,{"status":"PASS","finding_count":0})
        self.assertEqual(final["status"],"PASS",final)

    def test_missing_steps_is_rejected_by_existing_gate(self):
        a=fresh_anleitung()
        a["html"]=a["html"].replace('data-list="steps"','data-list="hints"')
        pkg,cat=package_from_article(a)
        with self.assertRaisesRegex(Blocked,"structure.required_lists"):
            verify_pre_lt68(pkg,cat)

    def test_wrong_writer_type_does_not_pass_anleitung(self):
        a=fresh_anleitung()
        a["article_type"]="Pflege"
        pkg,cat=package_from_article(a)
        with self.assertRaisesRegex(Blocked,"K0_RULE_CONTEXT_TYPE_META_REQUIRED:risk_controls"):
            verify_pre_lt68(pkg,cat)


if __name__=="__main__":
    unittest.main()
