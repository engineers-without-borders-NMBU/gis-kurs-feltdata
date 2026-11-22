# GIS-kurs – fra feltarbeid til ferdig kart

Skript og veiledning til GIS-kurset i **Ingeniører uten grenser NMBU**.
Deltakerne samler inn egne observasjoner på campus med mobilappen SW Maps,
og bearbeider og analyserer dataene i QGIS.

Kurset bruker QGIS, som er gratis: <https://qgis.org>

## Innhold

| Fil | Hva den gjør |
|---|---|
| `skript/Eksporter_bilder_SWmaps.py` | Gjør bildene fra SW Maps om til vanlige bildefiler, slik at de kan vises i QGIS på alle maskiner |

---

## Vise feltbilder fra SW Maps i QGIS

### Hvor ligger bildene?

SW Maps lagrer ikke bildene som egne filer. Hvert bilde ligger **inni**
GeoPackage-fila (`.gpkg`), i kolonnen `bilde`, som binærdata (en «BLOB»).
Derfor blir filene store. QGIS kan ikke vise en BLOB som bilde uten hjelp.

### Hvorfor ikke bare bruke en HTML-widget?

En vanlig løsning er en HTML-widget i attributtskjemaet, med JavaScript som gjør
BLOB-en om til et bilde. Det krever at QGIS har en innebygd nettleser, og det
har ikke alle installasjoner. Blant annet mangler den i QGIS på Mac, i en del
Linux-utgaver og i QGIS 4. Der blir feltet bare tomt, uten noen feilmelding.

### Løsningen: vanlige bildefiler og Vedlegg-widgeten

Skriptet `Eksporter_bilder_SWmaps.py` gjør dette for hvert punkt som har bilde:

1. **Skriver bildet ut som en `.jpg`-fil** i mappen `bilder` ved siden av prosjektfila
2. **Snur bildet riktig vei.** Telefoner lagrer ofte bildet liggende, med en
   merknad (EXIF) om hvordan det skal snus, og ulike telefoner gjør det ulikt.
   Skriptet leser merknaden i hvert bilde i stedet for å snu alle likt.
3. **Lagrer stien til fila** (for eksempel `bilder/lyktestolper_12.jpg`) i et
   nytt felt, `bilde_fil`

Stien er **relativ**, altså regnet fra prosjektmappen. Derfor virker den uansett
hvor mappen pakkes ut, og på alle operativsystemer.

Bildet vises deretter med widgeten **Vedlegg** (Attachment). Den viser bilder
direkte i QGIS og trenger verken nettleser eller JavaScript.

### Slik gjør du det

1. **Lagre prosjektet**, så QGIS vet hvor mappen `bilder` skal ligge.
2. **Marker laget** med bilder i lagpanelet.
3. Åpne **Programtillegg → Python-konsoll** og klikk **Vis editor**
   (ikonet med ark og blyant).
4. Klikk mappeikonet i editoren, åpne `Eksporter_bilder_SWmaps.py` og trykk **Kjør (▶)**.
   I konsollen skal det stå for eksempel `Ferdig: 84 bilder lagret fra ...`.
5. Gjenta steg 2–4 for hvert lag med bilder.
6. Gå til **Lagegenskaper → Attributtskjema** og velg feltet `bilde_fil`:
   - Widgettype: **Vedlegg** (Attachment)
   - Sti: **Relativ til prosjektsti**
   - Innebygd dokumentvisning: **Bilde**
7. Klikk på et punkt med **Identifiser objekter**. Bildet vises i skjemaet.

> **Tips:** Kjør skriptet fra *editoren*, ikke ved å lime koden rett inn i
> konsollen. Konsollen krever en tom linje etter hver blokk med innrykk og gir
> ellers `SyntaxError`.

### Hvis noe ikke virker

| Problem | Løsning |
|---|---|
| `Lagre prosjektet først …` | Lagre prosjektet (`.qgz`) og kjør skriptet på nytt |
| `KeyError: 'bilde'` | Kolonnen heter noe annet i laget ditt. Endre `BILDEKOLONNE` øverst i skriptet |
| Bildet vises ikke i skjemaet | Sjekk at mappen `bilder` ligger ved siden av prosjektfila, og at stien står som *relativ* |

### Deling av prosjektet

Del **prosjektfila (`.qgz`), GeoPackage-filene og mappen `bilder`** samlet i én
zip-fil, med samme mappestruktur. Da vises bildene hos alle.

Feltdataene ligger ikke i dette repoet, fordi filene er for store og bildene
kan vise personer.

---

Laget av Ingeniører uten grenser NMBU.
