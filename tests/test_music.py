import importlib.util, pathlib, tempfile, unittest, struct, json
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('music',ROOT/'skills/music-tools/scripts/music.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class MusicTests(unittest.TestCase):
    def test_flat_chord(self): self.assertEqual(m.chord('Bb')['notes'],['Bb','D','F'])
    def test_sharp_spelling(self): self.assertEqual(m.chord('F#')['notes'],['F#','A#','C#'])
    def test_inversion(self): self.assertEqual(m.chord('C','major',1)['midi'],[64,67,72])
    def test_seventh(self): self.assertEqual(m.chord('Eb','maj7')['notes'],['Eb','G','Bb','D'])
    def test_scale(self): self.assertEqual(m.scale('F','major')['notes'],['F','G','A','Bb','C','D','E'])
    def test_harmonic_minor(self): self.assertEqual(m.scale('A','harmonic-minor')['notes'][-1],'G#')
    def test_all_roots_qualities(self):
        for root in m.SHARP+m.FLAT:
            for quality,(ints,_) in m.CHORDS.items():
                for inv in range(len(ints)):
                    c=m.chord(root,quality,inv); self.assertEqual({m.parse_note(n)[1] for n in c['notes']},{(m.parse_note(root)[1]+i)%12 for i in ints}); self.assertEqual(c['midi'],sorted(c['midi']))
    def test_all_scales(self):
        for root in m.SHARP+m.FLAT:
            for kind,(ints,_) in m.SCALES.items(): self.assertEqual([ (m.parse_note(n)[1]-m.parse_note(root)[1])%12 for n in m.scale(root,kind)['notes']],ints)
    def test_shapes(self):
        for name in m.SHAPES:
            quality='7' if name.endswith('7') else 'minor' if name.endswith('m') else 'major'; root=name[0]
            self.assertEqual({p%12 for p in m.guitar_shape(name)['sounding_midi']},{m.parse_note(n)[1] for n in m.chord(root,quality)['notes']})
    def test_fretboard(self):
        b=m.fretboard('bass','A','minor-pentatonic',12); self.assertEqual([s['open'] for s in b['strings']],['E1','A1','D2','G2']); self.assertTrue(b['strings'][1]['positions'][0]['root'])
        for instrument in m.TUNINGS:
            for s,p in zip(m.fretboard(instrument,'Eb','major',24)['strings'],m.TUNINGS[instrument]):
                for f in s['positions']: self.assertEqual(f['midi'],p+f['fret']); self.assertEqual(m.parse_note(f['note'])[1],f['midi']%12)
    def test_bad_inputs(self):
        for fn,args in [(m.chord,('H',)),(m.chord,('C','major',3)),(m.fretboard,('piano','C')),(m.guitar_shape,('H',)),(m.scale,('C','unknown'))]:
            with self.assertRaises(ValueError): fn(*args)
    def test_midi(self):
        # Parse each event, verify lengths, timing, note pairing, and prohibited message absence.
        with tempfile.TemporaryDirectory() as d:
            for instrument in ('piano','guitar','bass'):
                for difficulty in ('beginner','intermediate'):
                    path=pathlib.Path(d)/'x.mid'; result=m.exercise(instrument,'A',75,8,path,'minor',difficulty); data=path.read_bytes(); self.assertEqual(data[:4],b'MThd'); self.assertEqual(struct.unpack('>IHHH',data[4:14]),(6,1,4,480)); offset=14; names=[]
                    def readvlq(raw,i):
                        n=0
                        while True:
                            v=raw[i]; i+=1; n=(n<<7)|(v&127)
                            if not v&128:return n,i
                    for _ in range(4):
                        self.assertEqual(data[offset:offset+4],b'MTrk'); size=int.from_bytes(data[offset+4:offset+8],'big'); raw=data[offset+8:offset+8+size]; offset+=8+size; i=t=0; active=set(); ended=False
                        while i<len(raw):
                            delta,i=readvlq(raw,i); t+=delta; status=raw[i]; i+=1
                            if status==255:
                                typ=raw[i]; i+=1; n,i=readvlq(raw,i); payload=raw[i:i+n]; i+=n
                                if typ==3:names.append(payload.decode())
                                if typ==47: ended=True; self.assertEqual(i,len(raw)); self.assertEqual(t,8*1920)
                            else:
                                self.assertIn(status&240,(128,144)); p,v=raw[i:i+2]; i+=2; key=(status&15,p)
                                if status&240==144 and v: self.assertNotIn(key,active); active.add(key)
                                else: self.assertIn(key,active); active.remove(key)
                        self.assertTrue(ended); self.assertFalse(active)
                    self.assertEqual(offset,len(data)); self.assertEqual(len(set(names)),4); self.assertEqual(len(result['score']),8)
    def test_manifest(self):
        manifest=json.loads((ROOT/'plugin.json').read_text()); self.assertEqual(manifest['version'],'1.8.0'); self.assertEqual(manifest['name'],'practice-room'); self.assertEqual(len(list((ROOT/'skills').glob('*/SKILL.md'))),2)
if __name__=='__main__': unittest.main()
