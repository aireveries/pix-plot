import sys
import os
import csv
import glob
from PIL import Image
import xml.etree.ElementTree as ET
import numpy as np
from pathlib import Path
from tqdm import tqdm

# Just try to open image and parse it using the xml
path = sys.argv[1]
csvfile = open('metadata.csv', 'w', newline='')
writer = csv.writer(csvfile, delimiter=",", quotechar="|",
                    quoting=csv.QUOTE_MINIMAL)
writer.writerow(['filename', 'tags', 'description', 'permalink'])

Path('./extracted_objects').mkdir(exist_ok=True)

for fileName in tqdm(glob.glob(path), 'extracting objects'):
    if fileName[-8:] != "mask.png":
        imFile = fileName
        im = Image.open(imFile)
        pix = np.asarray(im)
        # Have to parse the proper mask
        dataFile = Path(imFile[:-4] + ".xml")
        if not dataFile.exists():
            dataFile = Path(imFile[:-4].replace('image', 'annotation') + '.xml')
        tree = ET.parse(dataFile)
        root = tree.getroot()

        for obj in root.iter('object'):
            boundingBox = obj.find('bndbox2D')
            tag = obj.find('category0').text
            xmin = int(boundingBox.find('xmin').text)
            xmax = int(boundingBox.find('xmax').text)
            ymin = int(boundingBox.find('ymin').text)
            ymax = int(boundingBox.find('ymax').text)
            subImageArray = pix[ymin:ymax, xmin:xmax]
            outfile = obj.attrib['id'] + ".png"

            catCounter = 0
            tag = ""
            while not obj.find("category"+str(catCounter)) is None:
                tag = obj.find('category'+str(catCounter)).text
                catCounter += 1
            persistentID = obj.attrib['persistent_id']

            # some images can be outside of screen, in which case, drop em:
            if subImageArray.shape[0] > 0 and subImageArray.shape[1] > 0:
                newim = Image.fromarray(subImageArray)
                newim.save("extracted_objects/" + outfile, "png")
                writer.writerow([outfile, tag, persistentID, "n/a"])
                # might also want to potentially write metadata file. Will do this later
