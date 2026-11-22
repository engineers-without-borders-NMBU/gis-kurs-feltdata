# =====================================================================
#  Eksporter bilder fra SW Maps til vanlige bildefiler
# ---------------------------------------------------------------------
#  SW Maps lagrer hvert bilde INNE i GeoPackage-fila, i kolonnen "bilde",
#  som binærdata (BLOB). QGIS kan ikke vise en BLOB som bilde uten hjelp.
#
#  Skriptet gjør tre ting for hvert punkt som har bilde:
#    1. Skriver bildet ut som en .jpg-fil i mappen "bilder" ved prosjektfila
#    2. Snur bildet riktig (telefonen lagrer retningen som EXIF-info)
#    3. Skriver den relative stien (f.eks. "bilder/lyktestolper_12.jpg")
#       i et nytt felt "bilde_fil"
#
#  Etterpå settes feltet "bilde_fil" opp med widgeten "Vedlegg"
#  (Attachment), som viser bildet i skjemaet på alle QGIS-versjoner.
#
#  Bruk: lagre prosjektet først. Marker laget i lagpanelet. Åpne
#  Python-konsollen -> Vis editor, åpne denne fila og trykk Kjør (▶).
#  Gjenta for hvert lag med bilder.
# =====================================================================

import os
from qgis.core import QgsProject, QgsField
from qgis.PyQt.QtGui import QImageReader

# Felttypen "tekst" skrives ulikt i eldre og nyere QGIS – dette virker i begge
try:
    from qgis.PyQt.QtCore import QMetaType
    TEKST = QMetaType.Type.QString      # QGIS 3.38 og nyere, QGIS 4
except AttributeError:
    from qgis.PyQt.QtCore import QVariant
    TEKST = QVariant.String             # eldre QGIS 3.x

BILDEKOLONNE = "bilde"      # kolonnen SW Maps lagrer bildet i
STIFELT = "bilde_fil"       # nytt felt som får stien til bildefila

lag = iface.activeLayer()

# 1) Lag mappen "bilder" ved siden av prosjektfila
prosjektmappe = QgsProject.instance().homePath()
if not prosjektmappe:
    raise Exception("Lagre prosjektet først, så QGIS vet hvor bildene skal ligge.")
mappe = os.path.join(prosjektmappe, "bilder")
os.makedirs(mappe, exist_ok=True)

# 2) Legg til feltet "bilde_fil" hvis det ikke finnes fra før
if lag.fields().indexOf(STIFELT) == -1:
    lag.dataProvider().addAttributes([QgsField(STIFELT, TEKST)])
    lag.updateFields()
idx = lag.fields().indexOf(STIFELT)

# 3) Gå gjennom alle punktene
antall = 0
lag.startEditing()
for f in lag.getFeatures():
    data = f[BILDEKOLONNE]
    if not data:
        continue                                   # punktet har ikke bilde

    navn = f"{lag.name()}_{f.id()}.jpg"
    sti = os.path.join(mappe, navn)

    # a) Skriv rådataene rett til fil (originalbildet, med EXIF-info)
    with open(sti, "wb") as fil:
        fil.write(bytes(data))

    # b) Les fila igjen og snu bildet etter EXIF-retningen, lagre over
    leser = QImageReader(sti)
    leser.setAutoTransform(True)
    bilde = leser.read()
    del leser                                      # slipp fila før vi skriver
    if not bilde.isNull():
        bilde.save(sti, "JPG")

    # c) Lagre relativ sti i attributtabellen
    lag.changeAttributeValue(f.id(), idx, "bilder/" + navn)
    antall += 1

lag.commitChanges()
print(f"Ferdig: {antall} bilder lagret fra {lag.name()} i {mappe}")
