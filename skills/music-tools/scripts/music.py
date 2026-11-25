"""Practice Room deterministic music tools. Python 3.10+, standard library only."""
import argparse, json, re, struct, sys
from pathlib import Path

LETTERS = 'CDEFGAB'
NAT = dict(zip(LETTERS, [0,2,4,5,7,9,11]))
SHARP = 'C C# D D# E F F# G G# A A# B'.split()
FLAT = 'C Db D Eb E F Gb G Ab A Bb B'.split()
CHORDS = {'major':([0,4,7],[0,2,4]), 'minor':([0,3,7],[0,2,4]), 'dim':([0,3,6],[0,2,4]), 'aug':([0,4,8],[0,2,4]), 'sus2':([0,2,7],[0,1,4]), 'sus4':([0,5,7],[0,3,4]), '7':([0,4,7,10],[0,2,4,6]), 'maj7':([0,4,7,11],[0,2,4,6]), 'm7':([0,3,7,10],[0,2,4,6]), 'm7b5':([0,3,6,10],[0,2,4,6])}
SCALES = {'major':([0,2,4,5,7,9,11],list(range(7))), 'minor':([0,2,3,5,7,8,10],list(range(7))), 'dorian':([0,2,3,5,7,9,10],list(range(7))), 'mixolydian':([0,2,4,5,7,9,10],list(range(7))), 'major-pentatonic':([0,2,4,7,9],[0,1,2,4,5]), 'minor-pentatonic':([0,3,5,7,10],[0,2,3,4,6]), 'harmonic-minor':([0,2,3,5,7,8,11],list(range(7)))}
TUNINGS = {'guitar':[40,45,50,55,59,64], 'bass':[28,33,38,43]}
SHAPES = {'C':[None,3,2,0,1,0], 'G':[3,2,0,0,0,3], 'D':[None,None,0,2,3,2], 'A':[None,0,2,2,2,0], 'E':[0,2,2,1,0,0], 'F':[None,None,3,2,1,1], 'Am':[None,0,2,2,1,0], 'Em':[0,2,2,0,0,0], 'Dm':[None,None,0,2,3,1], 'A7':[None,0,2,0,2,0], 'E7':[0,2,0,1,0,0], 'D7':[None,None,0,2,1,2]}

def parse_note(note):
    m=re.fullmatch(r'([A-Ga-g])([#b]{0,2})',note.replace('♯','#').replace('♭','b'))
    if not m or ('#' in m[2] and 'b' in m[2]): raise ValueError('Use a note such as C, F# or Bb.')
    letter=m[1].upper(); return letter,(NAT[letter]+m[2].count('#')-m[2].count('b'))%12

def spell(root, intervals, degrees):
    letter,pc=parse_note(root); result=[]
    for interval,degree in zip(intervals,degrees):
        l=LETTERS[(LETTERS.index(letter)+degree)%7]; delta=(pc+interval-NAT[l]+6)%12-6
        result.append(l+('#'*delta if delta>=0 else 'b'*(-delta)))
    return result

def chord(root, quality='major', inversion=0):
    if quality not in CHORDS: raise ValueError('Unsupported chord quality: '+quality)
    ints,deg=CHORDS[quality]; notes=spell(root,ints,deg)
    if not 0<=inversion<len(ints): raise ValueError('Invalid inversion.')
    base=60+parse_note(root)[1]; pitches=[base+x for x in ints]
    pitches=pitches[inversion:]+[n+12 for n in pitches[:inversion]]
    return {'root':root,'quality':quality,'inversion':inversion,'notes':notes[inversion:]+notes[:inversion], 'midi':pitches,'span_semitones':pitches[-1]-pitches[0]}

def scale(root,kind='major'):
    if kind not in SCALES: raise ValueError('Unsupported scale: '+kind)
    ints,deg=SCALES[kind]; return {'root':root,'scale':kind,'notes':spell(root,ints,deg),'intervals':ints}

def fretboard(instrument,root,kind='major',frets=12):
    if instrument not in TUNINGS or not 0<=frets<=24: raise ValueError('Use guitar or bass; 0–24 frets.')
    data=scale(root,kind); names={parse_note(n)[1]:n for n in data['notes']}; pc=parse_note(root)[1]
    return {'instrument':instrument,'scale':data,'order':'low to high strings','strings':[{'string':len(TUNINGS[instrument])-i,'open':SHARP[p%12]+str(p//12-1),'positions':[{'fret':f,'note':names[(p+f)%12],'midi':p+f,'root':(p+f)%12==pc} for f in range(frets+1) if (p+f)%12 in names]} for i,p in enumerate(TUNINGS[instrument])]}

def guitar_shape(name):
    if name not in SHAPES: raise ValueError('No vetted open shape for this chord; use fretboard or request another voicing.')
    frets=SHAPES[name]; pitches=[p+f for p,f in zip(TUNINGS['guitar'],frets) if f is not None]
    return {'chord':name,'order':'low E A D G B high e','frets':['x' if f is None else f for f in frets],'sounding_midi':pitches}

def vlq(n):
    if not 0<=n<=0x0fffffff: raise ValueError('Invalid MIDI delta')
    b=[n&127]; n>>=7
    while n: b.insert(0,(n&127)|128); n>>=7
    return bytes(b)

def track(name,events,end):
    raw=bytes([0,255,3,len(name)])+name.encode('ascii'); last=0
    for t,priority,msg in sorted(events,key=lambda e:(e[0],e[1])):
        raw+=vlq(t-last)+msg; last=t
    raw+=vlq(end-last)+b'\xff\x2f\x00'
    return b'MTrk'+struct.pack('>I',len(raw))+raw

def exercise(instrument,root,bpm,bars,path,kind='minor',difficulty='beginner'):
    if instrument not in ('piano','guitar','bass') or not 40<=bpm<=200 or not 4<=bars<=32: raise ValueError('Use piano/guitar/bass, 40–200 BPM, 4–32 bars.')
    if kind not in ('major','minor') or difficulty not in ('beginner','intermediate'): raise ValueError('Use major/minor and beginner/intermediate.')
    pc=parse_note(root)[1]; base=48+pc if instrument=='piano' else 52+pc if instrument=='guitar' else 36+pc
    degrees=[0,5,7,0] if kind=='major' else [0,8,7,0]
    qualities=['major','major','major','major'] if kind=='major' else ['minor','major','minor','minor']
    lead=[]; backing=[]; drum=[]; score=[]; ppq=480; bar=ppq*4
    def add(events,t,d,p,ch,v):
        events.extend([(t,1,bytes([0x90|ch,p,v])),(t+d,0,bytes([0x80|ch,p,0]))])
    for i in range(bars):
        idx=i%4; r=base+degrees[idx]; ints=CHORDS[qualities[idx]][0]; t=i*bar
        step=480 if difficulty=='beginner' else 240
        motif=[0,0,2,1] if instrument=='bass' else [0,1,2,1]
        pattern=motif if step==480 else [0,1,2,1,0,2,1,0]
        notes=[]
        for j,k in enumerate(pattern):
            pitch=r+ints[k]; start=t+j*step; duration=int(step*.82)
            add(lead,start,duration,pitch,0,80+(j%4==0)*8); notes.append({'beat':1+j*step/ppq,'midi':pitch,'note':SHARP[pitch%12]+str(pitch//12-1),'duration_beats':duration/ppq})
        for p in ints: add(backing,t,bar-60,60+pc+degrees[idx]+p,1,55)
        for j in range(4): add(drum,t+j*ppq,60,37,9,90 if j==0 else 60)
        score.append({'bar':i+1,'chord':SHARP[(pc+degrees[idx])%12]+' '+qualities[idx], 'notes':notes})
    end=bars*bar; tempo=round(60_000_000/bpm).to_bytes(3,'big'); conductor=track('Tempo',[(0,0,b'\xff\x51\x03'+tempo),(0,1,b'\xff\x58\x04\x04\x02\x18\x08')],end)
    blob=b'MThd'+struct.pack('>IHHH',6,1,4,ppq)+conductor+track('Practice - '+instrument,lead,end)+track('Harmony backing',backing,end)+track('Click',drum,end)
    Path(path).write_bytes(blob)
    return {'file':str(path),'bpm':bpm,'bars':bars,'time_signature':'4/4','tracks':4,'ppq':ppq,'difficulty':difficulty,'score':score}

def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='cmd',required=True)
    c=sub.add_parser('chord'); c.add_argument('root'); c.add_argument('quality',choices=CHORDS); c.add_argument('--inversion',type=int,default=0)
    s=sub.add_parser('scale'); s.add_argument('root'); s.add_argument('kind',choices=SCALES)
    f=sub.add_parser('fretboard'); f.add_argument('instrument',choices=TUNINGS); f.add_argument('root'); f.add_argument('kind',choices=SCALES); f.add_argument('--frets',type=int,default=12)
    g=sub.add_parser('shape'); g.add_argument('name')
    e=sub.add_parser('exercise'); e.add_argument('instrument',choices=['piano','guitar','bass']); e.add_argument('root'); e.add_argument('--bpm',type=int,default=75); e.add_argument('--bars',type=int,default=8); e.add_argument('--kind',choices=['major','minor'],default='minor'); e.add_argument('--difficulty',choices=['beginner','intermediate'],default='beginner'); e.add_argument('--out',required=True)
    a=vars(p.parse_args()); cmd=a.pop('cmd')
    try:
        if cmd=='exercise': a['path']=a.pop('out')
        result={'chord':chord,'scale':scale,'fretboard':fretboard,'shape':guitar_shape,'exercise':exercise}[cmd](**a)
        print(json.dumps(result,indent=2))
    except (ValueError,OSError) as exc: p.error(str(exc))
if __name__=='__main__': main()
