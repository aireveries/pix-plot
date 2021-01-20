import csv
import sys
import glob
import xml.etree.ElementTree as ET

path = sys.argv[1]
with open('test.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=",",
                        quotechar="|", quoting=csv.QUOTE_MINIMAL)
    # write the header
    writer.writerow(['filename', 'tags', 'description', 'permalink'])
    for filename in glob.glob(path):
        if filename[-8:] != "mask.png":
            dataFile = filename[:-4] + ".xml"
            tree = ET.parse(dataFile)
            root = tree.getroot()
