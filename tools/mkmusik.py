#!/usr/bin/env python3
"""mkmusik.py MUSIK.TXT BURGEN.IMF - Notentext nach IMF Typ 1 (560 Hz) fuer RDMUS (AdLib/Sound Blaster).
Nur OPL-Stimmen 0..5, damit BURGEN.EXE auf Stimme 7 Geraeusche neben der Musik spielen kann.
Notentext: 'TEMPO n' (Viertel je Minute), 'STIMME k INSTRUMENT' (k 0..5; MELODIE, BLECH, BASS, TROMMEL),
danach Zeilen mit Noten der aktuellen Stimme: C4:2 = c' ein Achtel (Laenge in Sechzehnteln), Fis/Es: C#4 Eb4, R:4 = Pause.
'|' Taktstriche und ';' Kommentare werden ignoriert. Alle Stimmen beginnen gleichzeitig."""
import sys, re
INSTR = {   # 20h,40h,60h,80h,E0h je Operator (Modulator, Traeger), C0h
    'MELODIE': ((0x21, 0x1A, 0xF2, 0x24, 0x00), (0x21, 0x06, 0xF2, 0x26, 0x00), 0x0A),
    'BLECH':   ((0x21, 0x1C, 0xA3, 0x45, 0x00), (0x21, 0x0E, 0xB3, 0x46, 0x00), 0x08),
    'BASS':    ((0x01, 0x15, 0xF5, 0x37, 0x00), (0x01, 0x0A, 0xF4, 0x38, 0x00), 0x0C),
    'TROMMEL': ((0x0F, 0x00, 0xF8, 0x0F, 0x00), (0x00, 0x08, 0xF8, 0x0F, 0x00), 0x0E),
}
OP = [0, 1, 2, 8, 9, 10]
NAMEN = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11, 'H': 11}
def midi(t):
    m = re.fullmatch(r'([A-H])([#b]?)(\d)', t)
    if not m: raise SystemExit('Note? ' + t)
    return 12 * (int(m.group(3)) + 1) + NAMEN[m.group(1)] + (1 if m.group(2) == '#' else -1 if m.group(2) == 'b' else 0)
def fnum(n):
    f = 440.0 * 2 ** ((n - 69) / 12.0)
    for blk in range(8):
        fn = int(round(f * (1 << (20 - blk)) / 49716.0))
        if fn < 1024: return fn, blk
    return 1023, 7
tempo = 112; stimmen = {}; akt = None
for z in open(sys.argv[1], encoding='utf-8'):
    z = z.split(';')[0].replace('|', ' ').strip()
    if not z: continue
    w = z.split()
    if w[0] == 'TEMPO': tempo = int(w[1]); continue
    if w[0] == 'STIMME': akt = int(w[1]); assert 0 <= akt <= 5; stimmen[akt] = (w[2], []); continue
    for t in w:
        n, l = t.split(':'); stimmen[akt][1].append((None if n == 'R' else midi(n), int(l)))
tick = 560 * 60.0 / tempo / 4                       # IMF-Takte je Sechzehntel
ev = []                                              # (zeit in 1/16, reihenfolge, reg, wert)
for k, (ins, noten) in stimmen.items():
    m, c, fb = INSTR[ins]; o = OP[k]
    for i, r in enumerate((0x20, 0x40, 0x60, 0x80, 0xE0)): ev.append((0, 0, r + o, m[i])); ev.append((0, 0, r + o + 3, c[i]))
    ev.append((0, 0, 0xC0 + k, fb))
    t = 0
    for n, l in noten:
        if n is not None:
            fn, blk = fnum(n); kurz = 1 if ins == 'TROMMEL' else max(1, l) - 0.25
            ev.append((t, 2, 0xA0 + k, fn & 255)); ev.append((t, 3, 0xB0 + k, 0x20 | (blk << 2) | (fn >> 8)))
            ev.append((t + kurz, 1, 0xB0 + k, (blk << 2) | (fn >> 8)))
        t += l
ende = max(sum(l for _, l in v[1]) for v in stimmen.values())
ev.append((0, 0, 0x01, 0x20)); ev.sort(key=lambda e: (e[0], e[1]))
out = bytearray(); last = 0.0
for i, (t, _, r, v) in enumerate(ev):
    nxt = ev[i + 1][0] if i + 1 < len(ev) else ende
    d = int(round(nxt * tick)) - int(round(t * tick))
    out += bytes((r, v)) + max(0, d).to_bytes(2, 'little')
open(sys.argv[2], 'wb').write(len(out).to_bytes(2, 'little') + out)
print(sys.argv[2], len(out) + 2, 'Bytes,', len(stimmen), 'Stimmen,', round(ende * tick / 560, 1), 's')
