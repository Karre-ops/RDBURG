#!/bin/bash
# Burgenkampf bauen: braucht eine gebaute Arbeitskopie von Karre-ops/retrodesk2 (SDK API 2.0, out/RD2.LIB,
# obj/rd2start.obj, tools/rdrc.py, tools/rd2link.py) und Open Watcom. Aufruf: RD2=<pfad zu retrodesk2> ./build.sh
# Ergebnis: out/BURGEN.EXE und out/BURGEN.IMF
set -e
cd "$(dirname "$0")"
RD2=${RD2:-../retrodesk2}
export WATCOM=${WATCOM:-/opt/ow} PATH=/opt/ow/binl64:/opt/ow/binl:$PATH INCLUDE=/opt/ow/h
mkdir -p obj out
wcc -0 -mm -fpi87 -os -s -zq -w4 -bt=dos -zl -fo=obj/kifpu.obj src/KIFPU.C          # 8087-Befehle, nur mit Koprozessor aufgerufen
wcc -0 -mm -os -s -zq -w4 -bt=dos -zl -i=$RD2/sdk -fo=obj/burgen.obj src/BURGEN.C
wasm -q -0 -dSTK=6144 -fo=obj/rd2start.obj $RD2/sdk/RD2START.ASM                    # Startcode mit 6 KB Stapel
wlink option quiet format dos name out/BURGEN.EXE file obj/rd2start.obj,obj/burgen.obj,obj/kifpu.obj \
  library $RD2/out/RD2.LIB,$WATCOM/lib286/dos/clibm.lib option nodefaultlibs,map=obj/burgen.map >/dev/null
python3 $RD2/tools/rdrc.py src/BURGEN.RC obj/burgen.res >/dev/null
python3 $RD2/tools/rd2link.py out/BURGEN.EXE "Burgenkampf" --stack 6144 --res obj/burgen.res
python3 tools/mkmusik.py src/MUSIK.TXT out/BURGEN.IMF          # Hintergrundmusik (AdLib/SB), gehoert neben BURGEN.EXE
ls -l out/BURGEN.EXE out/BURGEN.IMF | awk '{print $9, $5, "Bytes"}'
