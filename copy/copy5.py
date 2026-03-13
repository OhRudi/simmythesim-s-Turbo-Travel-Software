from shutil import copy
from glob import iglob
import os
black = open("deformer map example/DB43E069!00000000!52C39ADC3D3D6A65!23106!51.xml", "rb").read()
for filename in iglob('deformer maps/*.xml'):
    deleted = os.path.getsize(filename) == 0 and int(filename.split("!")[-1].replace(".xml", "")) == 0
    if deleted:
        suffix = "0.xml"
    else:
        suffix = "51.xml"
    with open(filename.replace("deformer maps", "deformer maps 2").replace(filename.split("!")[-1], suffix), "wb") as file:
        if deleted:
            file.write(b"")
        else:
            file.write(black)
    print("test")