# Fra feltdata til kart: Hvor er det for mørkt på NMBU-campus?

**Steg-for-steg-veiledning til videotutorialen · Ingeniører uten grenser NMBU · GIS-kurs høsten 2026**

Denne veiledningen viser hvert klikk og hver innstilling i videotutorialen. Du kan følge den med eller uten videoen. Den er laget i **QGIS 3.44** på Windows. Navn på menyer og knapper står på engelsk, slik de vises i QGIS.

**Det du lager:** et kart som viser hvilke gangveier og stier på campus som er godt belyst, svakt belyst eller mørke, og en tabell med hvor mange meter vei som faller i hver klasse.

**Du trenger:**

- QGIS 3.x (gratis fra <https://qgis.org>)
- Feltdataene fra SW Maps: én GeoPackage per gruppe (`Belysning_Campus_gruppe_X.gpkg`), pluss `lyktestolper_ekstradata.gpkg` og `andre_lyspunkt_ekstradata.gpkg`
- Skriptet `Eksporter_bilder_SWmaps.py` fra <https://github.com/engineers-without-borders-NMBU/gis-kurs-feltdata>
- Internett (for bakgrunnskart og OpenStreetMap-data)

**Slik leser du veiledningen:** `Meny → Undermeny` betyr at du klikker deg gjennom menyene. Tekst i `kodeskrift` skriver du inn nøyaktig slik den står. Verktøy i **Processing Toolbox** finner du ved å skrive navnet i søkefeltet øverst i panelet. Åpne panelet med tannhjulikonet eller `Ctrl+Alt+T`.

> **Om midlertidige lag:** Mange verktøy lager et *midlertidig lag* (Create temporary layer), merket med et lite ikon i lagpanelet. Midlertidige lag forsvinner når QGIS lukkes. Lagre resultatene som GeoPackage der veiledningen sier det, og lagre prosjektet ofte (`Ctrl+S`).

---

## Del A – Oppsett og feltdata

### Steg 1 – Nytt prosjekt, koordinatsystem og feltdata

1. Start QGIS og velg **New Empty Project**.
2. **Project → Save As…** Velg kursmappen (for eksempel `C:\IUG GIS Kurs`) og gi prosjektet et navn, for eksempel `GIS_tutorial.qgz`. Prosjektet lagres tidlig, slik at alle filer senere kan lagres med relative stier.
3. **View → Panels**: slå på **Browser**, **Layers** og **Processing Toolbox**.
4. **Project → Properties… → CRS**. Skriv `25832` i filterfeltet, velg **EPSG:25832 – ETRS89 / UTM zone 32N**, trykk **Apply** og **OK**. Nederst til høyre i statuslinjen skal det nå stå `EPSG:25832`.
   *Hvorfor:* UTM 32N måler i meter. Det trenger vi for avstander og buffere.
5. **Plugins → Manage and Install Plugins…** Søk etter `QuickOSM`, velg det og trykk **Install Plugin**, og deretter **Close**.
6. I Browser-panelet: utvid **XYZ Tiles** og dobbeltklikk **OpenStreetMap**. Zoom inn til NMBU-campus i Ås.

   > **Sjekk statuslinjen:** Når OpenStreetMap legges inn først, kan prosjektet bytte til `EPSG:3857`. Står det ikke lenger `EPSG:25832`, gjentar du punkt 4.
7. I Browser-panelet: gå til mappen med feltdataene. Utvid hver `Belysning_Campus_gruppe_X.gpkg` og dra lagene **lyktestolper_grX** og **andre_lyspunkt_grX** inn i kartet. Hopp over `android_metadata`. Dra også inn `lyktestolper_ekstradata` og `andre_lyspunkt_ekstradata`.
8. Marker alle andre_lyspunkt-lagene (`Ctrl`+klikk), høyreklikk og velg **Group Selected**. Kall gruppen `andre lyspunkt`. Gjør det samme for lyktestolpene, med gruppenavnet `lyktestolper`.

### Steg 2 – Fjern FID-kolonnen

SW Maps lagrer `FID` som tekst. QGIS krever at FID er et heltall, og vil derfor ikke lagre lagene. Vi fjerner kolonnen fra alle lagene samtidig.

1. **Processing Toolbox** → søk `drop field`. Høyreklikk **Drop field(s)** og velg **Execute as Batch Process…**
2. Kolonnen **Input layer**: legg inn ett lyktestolpe-lag per rad. Bruk **+** for nye rader og **–** for å fjerne rader du ikke trenger.
3. Rad 1, kolonnen **Fields to drop**: klikk **…**, huk av `FID` og trykk **OK**.
4. Klikk overskriften **Autofill** i samme kolonne og velg **Fill Down**. Nå står FID på alle radene.
5. Kolonnen **Remaining fields**: skriv et navn per rad, for eksempel `utenFID_lyktestolper_gr1`. Det blir midlertidige lag.
6. Trykk **Run**. Når loggen viser at alle radene er ferdige, trykker du **Close**.
7. Marker de nye lagene, høyreklikk og velg **Group Selected**. Kall gruppen `lyktestolper uten FID kolonne`.
8. Gjenta punkt 1–7 for alle andre_lyspunkt-lagene, med gruppenavnet `andre lyspunkt uten FID kolonne`.
9. Kontroller: høyreklikk et nytt lag og velg **Open Attribute Table**. Kolonnen FID skal være borte.

### Steg 3 – Slå sammen gruppene (Merge)

1. Fjern de opprinnelige gruppene `andre lyspunkt` og `lyktestolper`: marker dem, høyreklikk og velg **Remove**.
2. **Processing Toolbox** → søk `merge` og velg **Merge vector layers** (Vector general).
3. **Input layers**: klikk **…**, huk av alle `utenFID_andre_lyspunkt_*` og trykk **OK**.
4. La **Add source layer information** være huket av. Da får hvert punkt et felt som viser hvilken gruppe det kom fra. **Merged**: midlertidig lag. Trykk **Run**, og deretter **Close**.
5. Høyreklikk det nye laget **Merged**, velg **Rename Layer** og skriv `andre_lyspunkt_merged`.
6. Gjenta punkt 2–5 for alle `utenFID_lyktestolper_*`, med navnet `lyktestolper_merged`.

---

## Del B – Bakgrunnsdata og avgrensning

### Steg 4 – Last ned bygninger og veier (QuickOSM)

1. Slå av punktlagene. **Vector → QuickOSM → QuickOSM…** og velg **Quick query** i menyen til venstre.
2. **Key:** `building`. La **Value** stå tomt, så hentes alle bygninger.
3. Endre nedtrekkslisten **In** til **Canvas Extent**. Bare området som vises i kartet lastes ned, så zoom ut til hele campus vises.
4. Trykk **Run query** og vent på «Successful query».
5. QuickOSM gir tre lag som alle heter `building` (punkt, linje og polygon). Behold **polygonlaget**. Fjern de to andre: høyreklikk og velg **Remove Layer**.
6. Kjør QuickOSM på nytt med **Key:** `highway` og **Canvas Extent**, og trykk **Run query**.

   > Får du feilen **«Bad Gateway»**, er OpenStreetMap-tjenesten opptatt. Trykk **Run query** på nytt.
7. Behold **linjelaget** `highway`, og fjern punkt- og polygonlaget.

### Steg 5 – Reprojiser alt til UTM 32N

Lagene fra SW Maps og QuickOSM ligger i **EPSG:4326** og måles i grader. En buffer på 0,5 ville da bli en halv *grad*, ikke en halv meter.

1. Kontroller: høyreklikk et lag og velg **Layer CRS**. Det står EPSG:4326.
2. **Processing Toolbox** → søk `reproject`. Høyreklikk **Reproject layer** og velg **Execute as Batch Process…**
3. **Input layer**, én rad per lag: `highway`, `building`, `andre_lyspunkt_merged` og `lyktestolper_merged`.
4. **Target CRS**, rad 1: velg **Project CRS: EPSG:25832 – ETRS89 / UTM zone 32N**. Klikk så **Autofill → Fill Down**.
5. **Convert curved geometries**: No.
6. **Reprojected**: klikk **…** på hver rad, velg **Save to File…** og lagre i kursmappen som `veier_UTM32.gpkg`, `bygninger_UTM32.gpkg`, `andre_lyspunkt_UTM32.gpkg` og `lyktestolper_UTM32.gpkg`.
7. Trykk **Run** og deretter **Close**.
8. Kontroller at `veier_UTM32` nå står på EPSG:25832. Fjern de gamle lagene (`highway`, `building`, `*_merged`).

### Steg 6 – Tegn campusavgrensningen

1. **Layer → Create Layer → New Shapefile Layer…** (eller **New GeoPackage Layer…**).
2. **File name:** `NMBU_polygon` i kursmappen. **Geometry type:** Polygon.
3. **CRS:** velg **Project CRS: EPSG:25832**. Standardvalget er EPSG:4326, så pass på å endre det. Trykk **OK**.
4. Marker `NMBU_polygon` og trykk **Toggle Editing** (blyanten), og deretter **Add Polygon Feature** (`Ctrl+.`).
5. Venstreklikk punkt for punkt rundt campusområdet. Avslutt med **høyreklikk**. Trykk **OK** i vinduet *Feature Attributes*. Feltet id kan stå tomt.
6. Trykk **Save Layer Edits** og slå av **Toggle Editing**.

### Steg 7 – Klipp bygninger og veier til campus

1. **Processing Toolbox** → søk `clip` og velg **Clip** (Vector overlay).
2. **Input layer:** `bygninger_UTM32`. **Overlay layer:** `NMBU_polygon`. Trykk **Run** og deretter **Close**.
3. Høyreklikk det nye laget **Clipped**, velg **Rename Layer** og skriv `bygninger_clipped`.
4. Gjenta med **Input layer:** `veier_UTM32`, og gi resultatet navnet `veier_clipped`.
5. Lagre begge til fil: høyreklikk laget og velg **Export → Save Features As…**. Velg **Format: GeoPackage**, sett **File name** til kursmappen og `veier_clipped` (eller `bygninger_clipped`), og trykk **OK**.
6. Fjern de midlertidige lagene og `*_UTM32`-utgavene av bygninger og veier fra prosjektet.

---

## Del C – Feltbildene

### Steg 8 – Vis feltbildene fra SW Maps

SW Maps lagrer hvert bilde **inni** datafila, som binærdata (BLOB) i kolonnen `bilde`. QGIS kan ikke vise det som bilde direkte. Skriptet lagrer bildene som vanlige `.jpg`-filer. Da kan QGIS vise dem på alle maskiner, også på Mac og i QGIS 4.

1. Last ned `Eksporter_bilder_SWmaps.py` fra GitHub-repoet: åpne fila og trykk **Download raw file**.
2. Lagre prosjektet (`Ctrl+S`). Skriptet lagrer bildene i mappen `bilder` ved siden av prosjektfila.
3. **Plugins → Python Console** (`Ctrl+Alt+P`) → **Show Editor** (ikonet med ark og blyant) → **Open Script…** (mappeikonet). Åpne skriptet.
4. Marker `andre_lyspunkt_UTM32` i lagpanelet og trykk **Run Script** (grønn trekant). Konsollen skriver for eksempel «Ferdig: 61 bilder lagret fra andre_lyspunkt_UTM32».
5. Marker `lyktestolper_UTM32` og trykk **Run Script** igjen.

   > Kjør skriptet fra *editoren*. Limer du koden rett inn i konsollen, får du lett `SyntaxError`.
6. Høyreklikk `lyktestolper_UTM32` og velg **Properties → Attributes Form**.
7. Endre **Autogenerate** til **Drag and Drop Designer**. Fjern alle felt fra *Form Layout* med minusknappen, og dra inn `ID`, `h_yde_m`, `skjerming`, `lux_under` og `bilde_fil`.
8. Velg `bilde_fil`:
   - **Widget Type:** Attachment
   - **Store path as:** Relative to Project Path
   - **Integrated Document Viewer → Type:** Image
9. Trykk **OK**. Velg **Identify Features** (i-ikonet) og klikk en lyktestolpe. Bildet vises i skjemaet.
10. Gjenta punkt 6–9 for `andre_lyspunkt_UTM32`, med feltene `ID`, `radius`, `lux_under`, `beskrivelse` og `bilde_fil`.

---

## Del D – Lysmodellen

### Steg 9 – Lux ved veggen på bygningene

1. Høyreklikk `bygninger_clipped` og velg **Open Attribute Table** (`F6`).
2. **Organize Columns** (ikon i tabellen) → **Hide All** → huk av `name` → **OK**.
3. **Toggle Editing** (blyanten i tabellen) → **New Field** (`Ctrl+W`): **Name** `lux_vegg`, **Type** *Decimal number (real)*. Trykk **OK**.
4. Klikk på en rad for å se hvilken bygning den gjelder. Bygningen markeres i kartet.
5. Skriv inn målt lux ved veggen for bygningene dere har data for:

   | Bygning | lux_vegg |
   |---|---|
   | Bikuben | 317 |
   | Økonomibygningen | 79 |
   | Cirkus | 63 |
   | Tivoli | 50 |
   | Urbygningen | 21 |
   | Bioteknologibygningen | 15 |
   | Sørhellinga | 12 |
   | TF fløy 6 Studentenes hus | 10 |
   | Kassa nova | 8 |
   | Meieribygningen, Tårnbygningen, TF, Vitenparken | 1,5 |

   Bygninger uten måling blir stående tomme (NULL).
6. **Save Edits**, slå av **Toggle Editing** og lukk tabellen.

*Lysmodell for bygninger:* lux = lux_vegg / (1 + 2 · avstand). Lyset faller raskt nær veggen, men har en lang hale.

### Steg 10 – Buffer og lux rundt bygningene

1. **Processing Toolbox** → **Retain fields**. **Input layer:** `bygninger_clipped`. **Fields to retain:** `building`, `name`, `lux_vegg`. Trykk **Run**. Gi det nye laget navnet `bygninger_clipped_utvalgte_kolonner`.
   *Hvorfor:* Ellers blir alle OSM-feltene kopiert inn i hver ring.
2. **Processing Toolbox** → **Multi-ring buffer (constant distance)**:
   - **Input layer:** `bygninger_clipped_utvalgte_kolonner`
   - **Number of rings:** `30`
   - **Distance between rings:** `0,5` meters

   Trykk **Run**. Gi laget navnet `buffer_bygninger`. Hver ring har feltet `distance`, som er avstanden fra bygningen.
3. Åpne attributtabellen og **Field Calculator** (kalkulatorikonet):
   - Huk av **Create a new field**
   - **Output field name:** `lux`
   - **Output field type:** Decimal number (real)
   - **Expression:** `"lux_vegg" / (1 + 2 * "distance")`

   Trykk **OK**, deretter **Save Edits** og **Toggle Editing** av.
4. **Processing Toolbox** → **Extract by expression**. **Input layer:** `buffer_bygninger`. **Expression:** `"lux" >= 1`. Trykk **Run**.
5. Gi resultatet navnet `buffer_bygninger_luxover1`. Lagre det med **Export → Save Features As… → GeoPackage**, som `buffer_bygninger_luxover1.gpkg` i kursmappen.
6. Fjern de midlertidige lagene.

### Steg 11 – Rens feltdataene

Før analysen sjekker vi punktene for feilregistreringer.

1. Høyreklikk `lyktestolper_UTM32` og velg **Open Attribute Table**.
2. **Organize Columns** → **Hide All** → huk av `lux_under`, `skjerming`, `h_yde_m` og `p_retilstand` → **OK**.
3. Klikk kolonneoverskriften `h_yde_m` for å sortere. Punkter med høyde 0 eller tom høyde kommer øverst. De kan ikke brukes i lysformelen, fordi den deler på høyden.
4. Høyreklikk en rad og velg **Zoom to Feature**. Vurder punktet i kartet og på bildet. Er det en tydelig feilregistrering eller en dobbeltregistrering?
5. **Toggle Editing** → marker raden → **Delete Selected Features** (søppelkassen).
6. Gjenta for alle tvilsomme punkter. Sorter også på `lux_under`.
7. **Save Edits**, slå av **Toggle Editing** og lagre prosjektet.

> Gjør det samme med `andre_lyspunkt_UTM32`: se etter punkter med `radius` = 0.

### Steg 12 – Behold bare kolonnene du trenger

1. **Retain fields** på `lyktestolper_UTM32`: `ID`, `lux_under`, `skjerming`, `h_yde_m`. Trykk **Run**. Gi laget navnet `lyktestolper_utvalgte_kolonner`.
   *Hvorfor:* Bildene fjernes. Ellers blir de kopiert inn i hver eneste ring, og filene blir flere gigabyte.
2. **Retain fields** på `andre_lyspunkt_UTM32`: `ID`, `lux_under`, `radius` (og gjerne `beskrivelse`). Gi laget navnet `andre_lyspunkt_utvalgte_kolonner`.

### Steg 13 – Buffer rundt lyspunktene

1. **Multi-ring buffer (constant distance)** på `lyktestolper_utvalgte_kolonner`: **Number of rings** `30`, **Distance between rings** `0,5`. Trykk **Run** og gi laget navnet `lyktestolper_buffer`.
2. Det samme for `andre_lyspunkt_utvalgte_kolonner`. Gi laget navnet `andre_lyspunkt_buffer`.

### Steg 14 – Lux i ringene rundt lyktestolpene

*Lysmodell for lyktestolper:* lux = lux_under · e^(−(2 / høyde) · avstand). Høye stolper lyser lenger ut enn lave.

1. Åpne attributtabellen til `lyktestolper_buffer` og velg **Field Calculator**:
   - **Create a new field**, **Output field name:** `lux`, **Output field type:** Decimal number (real)
   - **Expression:**

     ```
     "lux_under" * exp( - (2 / "h_yde_m") * "distance")
     ```
2. Trykk **OK**, deretter **Save Edits** og **Toggle Editing** av.
3. **Extract by expression** på `lyktestolper_buffer` med `"lux" > 1`. Trykk **Run**.
4. Gi resultatet navnet `lyktestolper_buffer_luxover1`.

### Steg 15 – Lux rundt andre lyspunkt, og lagring

*Lysmodell for andre lyspunkt (spotter, lykter):* lyset faller jevnt fra `lux_under` til null ved målt radius: lux = lux_under · (1 − avstand / radius).

1. Åpne attributtabellen til `andre_lyspunkt_buffer` og velg **Toggle Editing** → **Field Calculator**:
   - **Create a new field**, **Output field name:** `lux`, **Output field type:** Decimal number (real)
   - **Expression:** `"lux_under" * (1 - "distance" / "radius")`
2. Trykk **OK** og deretter **Save Edits**. Utenfor radiusen blir lux negativ. Det gjør ikke noe, fordi de ringene fjernes i neste punkt.
   *Alternativ:* `"lux_under" * max(0, 1 - "distance" / "radius")` gir 0 i stedet for negative verdier.
3. **Extract by expression** med `"lux" > 1`. Gi resultatet navnet `andre_lyspunkt_buffer_luxover1`.
4. Lagre begge bufferlagene: høyreklikk og velg **Export → Save Features As… → GeoPackage**, som `andre_lyspunkt_buffer_luxover1.gpkg` og `lyktestolper_buffer_luxover1.gpkg`.
5. Fjern de midlertidige lagene. Samle gjerne lagene i lagpanelet i to grupper: **BUFFER** og **DATA**.

---

## Del E – Resultat

### Steg 16 – Slå sammen alle lysbufferne

1. **Merge vector layers** → **Input layers**: `andre_lyspunkt_buffer_luxover1`, `buffer_bygninger_luxover1`, `lyktestolper_buffer_luxover1`. Trykk **Run**.
2. Høyreklikk **Merged** og velg **Export → Save Features As… → GeoPackage**. Sett **File name** til `Alle_lys_buffer` og **Layer name** til `Alle_lys_buffer`, og trykk **OK**.
3. Fjern det midlertidige laget **Merged**.

### Steg 17 – Del veiene i biter på 5 meter

1. **Retain fields** på `veier_clipped`: `highway`, `surface`. Trykk **Run**.
2. Attributtabellen → **Field Calculator**: **Create a new field** `lengde_m`, *Decimal number (real)*, **Expression:** `length($geometry)`. Trykk **OK** og lagre. Gi laget navnet `veier_lengde`.
3. **Processing Toolbox** → **Split lines by maximum length**:
   - **Input layer:** `veier_lengde`
   - **Maximum line length:** `5` meters

   Trykk **Run**. Gi laget navnet `veier_5m`. Du får nå rundt 2000 veibiter.

   > Merk: `lengde_m` viser fortsatt lengden på **hele** veien. Vil du ha lengden per bit, regner du ut `length($geometry)` på nytt *etter* oppdelingen.

### Steg 18 – Lux per veibit

1. **Processing Toolbox** → **Join attributes by location (summary)**:
   - **Join to features in:** `veier_5m`
   - **Where the features:** `intersect`
   - **By comparing to:** `Alle_lys_buffer`
   - **Fields to summarise:** `lux`
   - **Summaries to calculate:** bare `max`
   - **Joined layer:** **Save to GeoPackage…** → `veibiter_med_lux.gpkg`
2. Trykk **Run**. Veibitene får feltet `lux_max`. Veibiter som ingen lysring treffer, får NULL.

### Steg 19 – Del veibitene i lysklasser

1. Attributtabellen til `veibiter_med_lux` → **Field Calculator**:
   - **Create a new field**, **Output field name:** `klasse`, **Output field type:** Text (string)
   - **Expression:**

     ```
     CASE
       WHEN "lux_max" IS NULL OR "lux_max" < 1 THEN 'mork'
       WHEN "lux_max" < 5 THEN 'svakt'
       ELSE 'godt'
     END
     ```
2. Trykk **OK** og lagre. QGIS sjekker linjene ovenfra og ned og velger den første som stemmer.

### Steg 20 – Symbologi og statistikk

1. Høyreklikk `veibiter_med_lux` og velg **Properties → Symbology**. Endre **Single Symbol** til **Categorized**, sett **Value** til `klasse` og trykk **Classify**.
2. Dobbeltklikk hver klasse og velg farge: **mork** = rød, **svakt** = oransje, **godt** = grønn. Gi linjene en passe bredde under **Symbol → Width**. Trykk **Apply** og **OK**.
3. **Processing Toolbox** → **Statistics by categories**. **Input vector layer:** `veibiter_med_lux`. **Field(s) with categories:** `klasse`. Trykk **Run**.

   > Får du feilen «Wrong or missing parameter value: Field(s) with categories», velger du `klasse` på nytt i lista.
4. Åpne tabellen *Statistics by category* → **Toggle Editing** → **Delete Field**. Slett alt unntatt `klasse` og `count`. Gi `count` nytt navn: `antall_veibiter`.
5. **Field Calculator**: **Create a new field** `tot_meter_vei` med uttrykket `"antall_veibiter" * 5`. Hver bit er omtrent 5 m. Lagre.
6. Høyreklikk tabellen og velg **Export → Save Features As…**. **Format:** *MS Office Open XML spreadsheet (XLSX)*, **File name:** `Statistikk_lysforhold_vei.xlsx`. Trykk **OK**.

Resultat i tutorialen: godt 326 biter (ca. 1 630 m), svakt 382 biter (ca. 1 910 m), mørk 1 276 biter (ca. 6 380 m).

### Steg 21 – Lag ferdig kart

1. **Project → New Print Layout…** Gi layouten et navn og trykk **OK**.
2. **Add Map** (verktøylinjen til venstre): dra et rektangel over arket. Juster utsnittet med **Move Item Content**, og målestokken under **Item Properties → Scale**.
3. **Add North Arrow**: plasser pilen øverst til høyre.
4. **Add Scale Bar**: plasser målestokken nederst til venstre (meter).
5. **Add Legend**: plasser tegnforklaringen øverst til venstre. Under **Legend Items**: ta bort haken ved **Auto update**, og fjern alle lag unntatt `veibiter_med_lux` med minusknappen.
6. Dobbeltklikk elementene i tegnforklaringen og gi dem nye navn:
   - `veibiter_med_lux` → **Belysning på veier og stier (lux)**
   - `godt` → **Godt belyst (≥ 5 lux)**
   - `svakt` → **Svakt belyst (1–5 lux)**
   - `mork` → **Mørkt (< 1 lux)**
7. **Add Item → Add Label**: dra en boks øverst og skriv tittelen *Belysningsnivå ved gangveier på NMBU Campus*. Sett skriftstørrelsen til rundt 20 pt og sentrer teksten.
8. **Layout → Export as Image…** Lagre som `kart_lysforhold.jpg`, med 300 dpi, og trykk **Save**.
9. Lagre prosjektet.

---

## Hva kan vi – og hva kan vi ikke – konkludere med?

- Resultatet gjelder bare lys fra de bygningene, lyktestolpene og andre lyspunktene vi målte. Steder uten målinger får 0 lux, selv om det kan være lys der.
- Lux-verdiene mellom målepunktene er *modellerte*. Ulike formler for bygninger, lyktestolper og andre lyspunkt gir ulike antakelser.
- Grensene 1 og 5 lux er valgt for enkelhets skyld. Prøv andre grenser i steg 19 og se hvor mye kartet endrer seg.
- Mørke strekninger bør kontrolleres på stedet før man trekker konklusjoner.

## Filer som lages underveis

| Fil | Steg |
|---|---|
| `GIS_tutorial.qgz` | 1 |
| `veier_UTM32.gpkg`, `bygninger_UTM32.gpkg`, `andre_lyspunkt_UTM32.gpkg`, `lyktestolper_UTM32.gpkg` | 5 |
| `NMBU_polygon.shp` | 6 |
| `veier_clipped.gpkg`, `bygninger_clipped.gpkg` | 7 |
| mappen `bilder` med feltbilder | 8 |
| `buffer_bygninger_luxover1.gpkg` | 10 |
| `lyktestolper_buffer_luxover1.gpkg`, `andre_lyspunkt_buffer_luxover1.gpkg` | 15 |
| `Alle_lys_buffer.gpkg` | 16 |
| `veibiter_med_lux.gpkg` | 18 |
| `Statistikk_lysforhold_vei.xlsx` | 20 |
| `kart_lysforhold.jpg` | 21 |
