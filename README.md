# Burgenkampf

Ballerburg-artiges Spiel fuer RetroDesk 2 (BURGEN.EXE): Computer (3 Staerken), zwei Spieler am selben Rechner,
Netz ueber TCP 2626 mit Pruefsumme. Flugbahn ganzzahlig, 8087 optional fuers Zielen des Computers (KIFPU.C).
Alle Grafikarten von RD2, laeuft ab 8086.

Stand 1.2 (01.11.2026): Musik und Geraeusche, ungetestet. 1.1 (31.10.2026): an API 2.0 angepasst. In Arbeit, nicht Teil des RD2-Diskettensatzes. Bekannter Fehler: Haenger nach drei Zuegen
(test/burgen.sh: "kein Sieger", Fenster schliesst nicht).

Herkunft: bis 30.10.2026 in Karre-ops/retrodesk2 unter apps/burgen (Commit c02e85a).

## Fertiges Programm

bin/BURGEN.EXE und bin/BURGEN.IMF (Musik) (RD2 2.1, API 2.0) zusammen nach A:\RD2 bzw. C:\RD2 kopieren und in RD2 starten. Pruefsumme in bin/SHA256.TXT.
Wird bei jeder Aenderung neu gebaut und mit eingecheckt.

## Bauen

Fuer RetroDesk 2.1 (SDK API 2.0). Braucht eine gebaute Arbeitskopie von Karre-ops/retrodesk2
(sdk/, out/RD2.LIB, tools/rdrc.py, tools/rd2link.py) und Open Watcom:

    RD2=<pfad zu retrodesk2> ./build.sh        # -> out/BURGEN.EXE

Eine mit API 1.0 (RD2 2.0) gebaute BURGEN.EXE laeuft unter RD2 2.1 nicht mehr (Funktionsnummern neu).
Groesse 1.1: Datei 27.146 Bytes, Speicher etwa 29 KB (Stapel 6 KB).

## Grafik

1 Bit (CGA, Hercules, VGA/EGA mono): Muster. 4 Farben (CGA4, EGA4, VGA4): Himmel tuerkis, Mauern
rosa (CGA4) bzw. hellgrau (EGA4/VGA4), sonst Muster. 16/256 Farben: Farben. Unter 480 Punkten
Fensterbreite (CGA4, EGA320, MCGA) kurze Statuszeilen.

## Test

test/burgen.sh (QEMU, HGC und VGA) aus der retrodesk2-Arbeitskopie heraus starten.

## Klang

- Musik: BURGEN.IMF laeuft mit AdLib/Sound Blaster (OPL-Stimmen 0-5) das ganze Spiel in Schleife.
  Quelle src/MUSIK.TXT (Notentext), umgewandelt mit tools/mkmusik.py. Vorlaeufig ein eigener
  "Burgmarsch" als Platzhalter; "Preussens Gloria" folgt, sobald eine Notenvorlage da ist.
- Geraeusche (Schuss, Pfeifen der fallenden Kugel, Einschlag Boden/Burg, Pulverlager, Kauf) ueber
  SndNote: bei OPL auf Stimme 7 neben der Musik, beim PC-Lautsprecher auf Stimme 0. Dort statt
  Hintergrundmusik nur Melodien zum Start, Sieg und Niederlage.
- Menue Spiel: Musik / Geraeusche an und aus, gespeichert in RD2.INI [Burgen] Musik=, Klang=.
