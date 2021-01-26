from pycocotools.coco import COCO

if __name__ == '__main__':
    ann_file = './aireverie-datasets/clients/epri/annotations/instances.json'
    coco = COCO(ann_file)

    import pdb; pdb.set_trace()
    print('hey')