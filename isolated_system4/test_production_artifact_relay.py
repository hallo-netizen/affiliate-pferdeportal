import hashlib,tempfile,unittest
from pathlib import Path

import handoff_transport as ht
import production_artifact_relay as relay
from test_handoff_transport import HandoffTransportTests

class ProductionArtifactRelayTests(unittest.TestCase):
    def _completion(self,root:Path,token=None):
        helper=HandoffTransportTests(); payload=helper.payload(1)
        src=root/'source.json'; helper.write(src,payload)
        canonical=root/ht.HANDOFF_FILENAME; raw=ht.canonicalize_handoff(src,canonical)
        inline=root/ht.INLINE_FILENAME; env=ht.inline_pack(canonical,inline)
        text=((token or relay.READY_TOKEN)+'\n'+relay.SHA_LABEL+':'+hashlib.sha256(raw).hexdigest()+'\n'+relay.BYTES_LABEL+':'+str(len(raw))+'\n'+relay.PARTS_LABEL+':'+str(env['part_count'])+'\n'+inline.read_text(encoding='utf-8'))
        return text,raw

    def test_positive_ready_reconstruct_and_verify_after_runtime_separation(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); text,raw=self._completion(root)
            artifact,receipt,value=relay.reconstruct_from_comment(text,root/'persisted','12345')
            self.assertEqual(artifact.read_bytes(),raw); self.assertEqual(value['sha256'],hashlib.sha256(raw).hexdigest())
            copied=root/'downloaded'; copied.mkdir(); da=copied/artifact.name; dr=copied/receipt.name
            da.write_bytes(artifact.read_bytes()); dr.write_bytes(receipt.read_bytes())
            self.assertEqual(relay.verify_persisted(da,dr)['source_comment_id'],'12345')

    def test_positive_existing_batch_pass_token_is_persisted_before_overall_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); text,raw=self._completion(root,relay.PASS_TOKEN)
            artifact,_,_=relay.reconstruct_from_comment(text,root/'out','77')
            self.assertEqual(artifact.read_bytes(),raw)

    def test_negative_missing_completion_token(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); text,_=self._completion(root)
            with self.assertRaisesRegex(relay.ArtifactRelayError,'RELAY_COMPLETION_TOKEN_MISSING'):
                relay.reconstruct_from_comment(text.replace(relay.READY_TOKEN,'BROKEN',1),root/'out','1')

    def test_negative_sha_metadata_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); text,_=self._completion(root)
            text=text.replace(relay.SHA_LABEL+':',relay.SHA_LABEL+':'+'0'*64+'\nIGNORED:',1)
            with self.assertRaises(relay.ArtifactRelayError): relay.reconstruct_from_comment(text,root/'out','1')

    def test_negative_inline_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); text,_=self._completion(root); begin=text.index(ht.INLINE_BEGIN); payload_pos=text.index('payload_base64',begin); quote=text.index('"',text.index(':',payload_pos)+1)+1
            bad=text[:quote]+('A' if text[quote]!='A' else 'B')+text[quote+1:]
            with self.assertRaises((relay.ArtifactRelayError,ht.HandoffError)): relay.reconstruct_from_comment(bad,root/'out','1')

    def test_negative_downloaded_artifact_missing(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); text,_=self._completion(root); artifact,receipt,_=relay.reconstruct_from_comment(text,root/'out','1'); artifact.unlink()
            with self.assertRaisesRegex(relay.ArtifactRelayError,'RELAY_PERSISTED_ARTIFACT_MISSING'): relay.verify_persisted(artifact,receipt)

if __name__=='__main__': unittest.main(verbosity=2)
