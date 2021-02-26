from pycocotools.coco import COCO
from PIL import Image
from pathlib import Path
from tqdm import tqdm
import argparse
import csv

parser = argparse.ArgumentParser(description='extract objects from coco dataset')
parser.add_argument('s3_path', type=str)

if __name__ == '__main__':
    args = parser.parse_args()
    root = Path(args.s3_path[5:])
    ann_file = root / 'annotations/instances.json'
    coco = COCO(ann_file)

    # display COCO categories and supercategories
    catIds = coco.getCatIds()
    cats = coco.loadCats(catIds)
    nms=[cat['name'] for cat in cats]
    print('COCO categories: \n{}\n'.format(' '.join(nms)))

    def extract_objects(root, img_id, writer):
        annIds = coco.getAnnIds(imgIds=img_id, catIds=catIds, iscrowd=None)
        anns = coco.loadAnns(annIds)
        imgInfo = coco.loadImgs(img_id)[0]
    #     print(imgInfo)
        img_path = root / 'images' / imgInfo['file_name']
        img = Image.open(img_path)
        max_width, max_height = img.size
        Path(root / 'objects').mkdir(parents=True, exist_ok=True)
        for ann in anns:
            out_path = root / 'objects' / imgInfo['file_name']
            out_path = out_path.with_name(out_path.stem + f"_{ann['id']}").with_suffix(out_path.suffix)
            bbox = ann['bbox']
            x, y, w, h = bbox
            
            crop_rect = (x, y, min(x+w+1, max_width), min(y+h+1, max_height))
    #         print(bbox, crop_rect, img.size)
            crop_img = img.crop(crop_rect)
    #         crop_img = img.crop([10, 10, 100, 100])
            crop_img.save(out_path)
            cat = coco.loadCats(ann['category_id'])[0]
            writer.writerow([out_path, cat['name']])

    with open('metadata.csv', 'w', newline='') as outcsv:
        writer = csv.writer(outcsv, quoting=csv.QUOTE_ALL)
        writer.writerow(["filename", "category"])

        for ix, img in tqdm(coco.imgs.items()):
            try:
                extract_objects(root, img['id'], writer)
            except Exception as e:
                print(img, e)