# Burgenkampf

Ballerburg-artiges Spiel fuer RetroDesk 2 (BURGEN.EXE): Computer (3 Staerken), zwei Spieler am selben Rechner,
Netz ueber TCP 2626 mit Pruefsumme. Flugbahn ganzzahlig, 8087 optional fuers Zielen des Computers (KIFPU.C).
Alle Grafikarten von RD2, laeuft ab 8086.

Stand: in Arbeit, nicht Teil des RD2-Diskettensatzes. Bekannter Fehler: Haenger nach drei Zuegen
(test/burgen.sh: "kein Sieger", Fenster schliesst nicht).

Herkunft: bis 30.10.2026 in Karre-ops/retrodesk2 unter apps/burgen (Commit c02e85a).

## Bauen

Braucht eine Arbeitskopie von Karre-ops/retrodesk2 (SDK, build.sh-Funktion `app`, Open Watcom):

    cp src/* <retrodesk2>/apps/burgen/
    cd <retrodesk2>
    wcc -0 -mm -fpi87 -os -s -zq -w4 -bt=dos -zl -fo=obj/kifpu.obj apps/burgen/KIFPU.C
    APPOBJ=,obj/kifpu.obj APPSTACK=6144 app apps/burgen/BURGEN.C BURGEN.EXE "Burgenkampf"

Speichergrenze bisher: Datei 32 KB, Speicher 48 KB.

## Test

test/burgen.sh (QEMU, HGC und VGA) aus der retrodesk2-Arbeitskopie heraus starten.
