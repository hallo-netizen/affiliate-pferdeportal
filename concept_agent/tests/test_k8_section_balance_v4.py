from __future__ import annotations
import unittest

from concept_agent.konzept8_verbot.engine import k8_section_balance


def p(words:int)->str:
    return "<p>" + " ".join(["wort"] * words) + "</p>"


def sec(block:str, words:int, paras:int=2)->str:
    chunks=[]
    base=words//paras
    rest=words%paras
    for i in range(paras):
        chunks.append(p(base+(1 if i<rest else 0)))
    return f'<section data-block="{block}"><h2>{block} Überschrift</h2>' + "".join(chunks) + "</section>"


def article(normal_counts, table_words=80, conclusion_words=90, further_words=25, intro_words=70):
    return (
        '<article>'
        f'<section data-block="intro">{p(intro_words)}</section>'
        + "".join(sec(f"body{i}", w) for i,w in enumerate(normal_counts))
        + sec("table", table_words, 1)
        + sec("conclusion", conclusion_words, 2)
        + sec("further_information", further_words, 1)
        + '</article>'
    )


class K8SectionBalanceTest(unittest.TestCase):
    def test_balanced_two_section_article_passes(self):
        html=article([220,220],table_words=100,conclusion_words=100,further_words=30,intro_words=90)
        result=k8_section_balance.validate(html)
        self.assertEqual(result["status"],"PASS")
        self.assertGreaterEqual(result["main_ratio"],0.50)

    def test_huge_conclusion_is_blocked(self):
        html=article([220,220],table_words=60,conclusion_words=180,further_words=20,intro_words=60)
        with self.assertRaisesRegex(k8_section_balance.SectionBalanceError,"K8_CONCLUSION_RATIO_TOO_HIGH"):
            k8_section_balance.validate(html)

    def test_table_padding_cannot_rescue_short_main_text(self):
        html=article([110,110],table_words=350,conclusion_words=80,further_words=20,intro_words=60)
        with self.assertRaisesRegex(k8_section_balance.SectionBalanceError,"K8_MAIN_TEXT_RATIO_TOO_LOW"):
            k8_section_balance.validate(html)

    def test_uneven_main_sections_are_blocked(self):
        html=article([100,200],table_words=300,conclusion_words=80,further_words=20,intro_words=60)
        with self.assertRaisesRegex(k8_section_balance.SectionBalanceError,"K8_H2_SECTION_IMBALANCE"):
            k8_section_balance.validate(html)

    def test_article_too_long_is_blocked(self):
        html=article([220,220,220],table_words=90,conclusion_words=100,further_words=20,intro_words=90)
        with self.assertRaisesRegex(k8_section_balance.SectionBalanceError,"K8_TOTAL_WORD_RANGE"):
            k8_section_balance.validate(html)


if __name__ == "__main__":
    unittest.main()
