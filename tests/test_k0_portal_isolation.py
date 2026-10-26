import json
import unittest
from pathlib import Path

from engine.k0_portal_resolver import Blocked, wordpress_site_for_portal

ROOT=Path(__file__).resolve().parents[1]


class PortalIsolationPreparationTests(unittest.TestCase):
    def registry(self):
        return json.loads((ROOT/'K0_PORTAL_REGISTRY.json').read_text(encoding='utf-8'))

    def test_pferdeatelier_uses_only_its_documented_wordpress_site(self):
        self.assertEqual(wordpress_site_for_portal(self.registry(),'pferdeatelier'),'https://pferde-atelier.de')

    def test_hobby_depot_not_silently_redirected_to_pferdeatelier(self):
        with self.assertRaisesRegex(Blocked,'PORTAL_WORDPRESS_SITE_NOT_CONFIGURED:hobby'):
            wordpress_site_for_portal(self.registry(),'hobby')

    def test_unknown_portal_is_rejected(self):
        with self.assertRaisesRegex(Blocked,'PORTAL_WORDPRESS_PROFILE_NOT_UNIQUE'):
            wordpress_site_for_portal(self.registry(),'not-a-portal')

    def test_depot_will_have_own_site_after_real_configuration(self):
        reg=self.registry()
        next(p for p in reg['profiles'] if p['portal_id']=='hobby')['wordpress_base_url']='https://example-hobby.test'
        self.assertEqual(wordpress_site_for_portal(reg,'hobby'),'https://example-hobby.test')
        self.assertEqual(wordpress_site_for_portal(reg,'pferdeatelier'),'https://pferde-atelier.de')

    def test_no_cross_portal_shared_site(self):
        reg=self.registry()
        next(p for p in reg['profiles'] if p['portal_id']=='hobby')['wordpress_base_url']='https://pferde-atelier.de'
        with self.assertRaisesRegex(Blocked,'PORTAL_WORDPRESS_SITE_SHARED'):
            wordpress_site_for_portal(reg,'hobby')

    def test_no_insecure_or_embedded_credentials(self):
        for site in ('http://example-hobby.test','https://user:pw@example-hobby.test','https://example-hobby.test/category/test'):
            with self.subTest(site=site):
                reg=self.registry()
                next(p for p in reg['profiles'] if p['portal_id']=='hobby')['wordpress_base_url']=site
                with self.assertRaisesRegex(Blocked,'PORTAL_WORDPRESS_SITE_INVALID'):
                    wordpress_site_for_portal(reg,'hobby')

    def test_workflows_consult_portal_registry_instead_of_horse_fallback(self):
        author=(ROOT/'.github/workflows/k0-authoring-context.yml').read_text()
        writer=(ROOT/'.github/workflows/k0-writer-accept.yml').read_text()
        self.assertIn('wordpress_site_for_portal',author)
        self.assertIn('wordpress_site_for_portal',writer)
        self.assertNotIn('https://pferde-atelier.de/wp-json',writer)

    def test_unverified_canonical_id_registry_cannot_bind_hobby(self):
        writer=(ROOT/'.github/workflows/k0-writer-accept.yml').read_text()
        self.assertIn('K0_CANONICAL_ARTICLE_REGISTRY_UNVERIFIED_FOR_PORTAL',writer)


if __name__=='__main__':
    unittest.main()
